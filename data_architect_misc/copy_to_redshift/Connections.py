'''
Author: Hamza Ahmad
Desc:
'''

import os
import sys
import csv
import warnings
from .FileUtilities import *
import pandas as pd
from pandas.io.sql import DatabaseError
import pyodbc
import psycopg2
import traceback
from boto3 import client, resource
from boto3.s3.transfer import TransferConfig
from botocore.exceptions import ClientError
from .account_info import s3_temp
from FileUtilities import s2hms



class SQLConnection:

    chunk_size = 10000

    def __init__(self, driver, server, database, username, password):
        try:
            self.__connection = pyodbc.connect('DRIVER={};SERVER={};DATABASE={};UID={};PWD={};'
                                               .format(driver, server, database, username, password))
        except pyodbc.Error as err:
            print('Could not connect to database:', err)
            exit()

    def query(self, query, return_chunks=False):
        try:
            chunks = pd.read_sql(sql=query, con=self.__connection, chunksize=self.chunk_size)
            return chunks if return_chunks else pd.concat(chunks, ignore_index=True)
        except DatabaseError as err:
            print('Could not execute query:', err)
            exit()

    def table_exists(self, table):
        cursor = self.__connection.cursor()
        cursor.execute("select count(*) from sys.tables where [Name] = '{0}'"
                       .format(table.replace('\'', '\'\'').replace('[', '', 1).replace(']', '', 1)))
        if cursor.fetchone()[0] == 1:
            cursor.close()
            return True
        cursor.close()
        return False

    def export_query(self, query, output_file, delimiter=','):
        # DEPRECATED ON 7/20/2018 BY HAMZA AHMAD
        # cursor = self.__connection.cursor()
        # cursor.execute(query)
        # with open(output_file, 'w', newline='', encoding='utf-8') as f:
        #     writer = csv.writer(f, delimiter=delimiter)
        #     writer.writerow([x[0] for x in cursor.description])  # Write the column headers
        #     data = cursor.fetchmany(self.chunk_size)
        #     while data:
        #         for row in data:
        #             writer.writerow(row)
        #         data = cursor.fetchmany(self.chunk_size)
        # cursor.close()
        chunks = self.query(query=query, return_chunks=True)
        with open(output_file, 'w', newline='') as f:
            next(chunks).to_csv(f, index=False, sep=delimiter, quoting=csv.QUOTE_ALL)  # First fetch contains headers
            for chunk in chunks:
                chunk.to_csv(f, index=False, header=False, sep=delimiter, quoting=csv.QUOTE_ALL)
        return

    def export_table(self, table, output_file, delimiter=','):
        query = 'select * from {}'.format(table)
        self.export_query(query=query, output_file=output_file, delimiter=delimiter)
        return


class S3Connection:

    def __init__(self, access_key, secret_access_key, session_token=None, region_name=None, bucket=None, prefix=None):
        try:
            self.__access_key = access_key
            self.__secret_access_key = secret_access_key
            self.__session_token = session_token
            self.__region_name = region_name
            self.bucket = bucket if bucket else False
            self.prefix = prefix if prefix else ''
            self.__s3 = resource('s3', aws_access_key_id=self.__access_key,
                                 aws_secret_access_key=self.__secret_access_key,
                                 aws_session_token=self.__session_token,
                                 region_name=self.__region_name)
            self.__s3client = client('s3', aws_access_key_id=self.__access_key,
                                     aws_secret_access_key=self.__secret_access_key,
                                     aws_session_token=self.__session_token,
                                     region_name=self.__region_name)
        except ClientError as err:
            print('Could not connect to S3:', err)
            exit()

    def get_list_of_buckets(self):
        response = self.__s3client.list_buckets()
        return [bucket['Name'] for bucket in response['Buckets']]

    def prefix_exists(self, bucket=None, prefix=None):
        bucket = bucket if bucket else self.bucket
        prefix = prefix if prefix else self.prefix
        if self.__s3client.list_objects(Bucket=bucket, Prefix=prefix):
            return True
        return False

    def get_list_of_objects(self, bucket=None, prefix=None, paginate=False):
        bucket = bucket if bucket else self.bucket
        prefix = prefix if prefix else self.prefix
        if paginate:
            paginator = self.__s3client.get_paginator('list_objects_v2')
            page_response = paginator.paginate(Bucket=bucket, Prefix=prefix)
            objects = []
            for index, page_object in enumerate(page_response):
                objects.extend([obj['Key'] for obj in page_object['Contents']])
                if index > 0 and (index % 5) == 0:
                    warnings.warn('The paginator has counted %s objects.' % '{:,}'.format(index*1000))
            return objects
        else:
            try:
                response = self.__s3client.list_objects_v2(Bucket=bucket, Prefix=prefix)
                if response.get('KeyCount', ''):
                    return [obj['Key'] for obj in response['Contents']]
            except ClientError as e:
                print(e)
                exit()

    def get_object_size(self, key, bucket=None, prefix=None):
        bucket = bucket if bucket else self.bucket
        prefix = prefix if prefix else self.prefix
        key = prefix + key if prefix else key
        response = self.__s3client.list_objects_v2(Bucket=bucket, Prefix=key)
        return [each['Size'] for each in [obj for obj in response['Contents']] if each['Key'] == key][0]

    def upload_file(self, file_path, key, bucket=None, prefix=None):
        bucket = bucket if bucket else self.bucket
        prefix = prefix if prefix else self.prefix
        key = prefix + key if prefix else key
        try:
            config = TransferConfig(multipart_threshold=1024**3, multipart_chunksize=1024**2, max_concurrency=10)
            self.__s3client.upload_file(file_path, bucket, key, Config=config)
        except ClientError as e:
            print('Could not upload file:', e)
        return

    # def write_file(self, df, filename, delimiter=',', index=False, bucket=False, prefix=False):
    #     self.bucket = bucket if bucket else self.bucket
    #     self.prefix = prefix if prefix else self.prefix
    #     # key = prefix + filename
    #     # buffer = StringIO()
    #     # df.to_csv(buffer, index=index, sep=delimiter)
    #     # self.__s3client.put_object(Bucket=bucket, Key=key, Body=buffer.getvalue())
    #     print('BUCKET:', self.bucket)
    #     print('PREFIX:', self.prefix, '\n')

    def download_file(self, key, bucket=None, prefix=None, output_folder=''):
        bucket = bucket if bucket else self.bucket
        prefix = prefix if prefix else self.prefix
        key = prefix + key if prefix else key
        try:
            if not key.endswith("/"):
                output_path = os.path.join(output_folder, os.path.split(key)[1])
                self.__s3client.download_file(bucket, key, output_path)
        except ClientError as err:
            print('Could not download the file object:', err)
        return

    def delete_file(self, key, bucket=False, prefix=False):
        bucket = bucket if bucket else self.bucket
        prefix = prefix if prefix else self.prefix
        key = prefix + key if prefix else key
        self.__s3client.delete_object(Bucket=bucket, Key=key)
        return


class RedshiftConnection:

    slice_count = None

    def __init__(self, host, port, database, username, password, **kwargs):
        try:
            self.database = database
            self.username = username
            self.__connection = psycopg2.connect(dbname=database, host=host, port=port, user=username,
                                                 password=password, **kwargs)
            self.__cursor = self.__connection.cursor()
            self.slice_count = self.get_slice_count()
        except psycopg2.Error as err:
            print('Could not connect to Redshift database:', err)
            exit()

    def get_slice_count(self):
        self.__cursor.execute('select count(distinct slice) from stv_slices')
        return self.__cursor.fetchone()[0]

    def query(self, query):
        self.__cursor.execute(query)
        columns = [desc[0] for desc in self.__cursor.description]
        df = pd.DataFrame(self.__cursor.fetchall(), columns=columns)
        return df

    def exec_commit(self, query, commit=True, return_cursor=False):
        self.__cursor.execute(query)
        if commit:
            self.__connection.commit()
        if return_cursor:
            return self.__cursor

    def close(self):
        self.__cursor.close()
        self.__connection.commit()
        self.__connection.close()

    @staticmethod
    def check_headers_for_reserved_words(headers):
        reserved_words = open(os.path.join(os.path.dirname(__file__), 'redshift_reserved_words.txt'), 'r').readlines()
        reserved_words = [r.strip().lower() for r in reserved_words]
        invalid_words = [r for r in [x.lower() for x in headers] if r in reserved_words]
        if invalid_words:
            raise ValueError('Column header {0} is a reserved word in Amazon Redshift.'.format(invalid_words[0]))
        return True

    def create_table(self, table, columns, drop_if_exists=False, dtype=None):
        dtype = dtype if dtype is not None else ['varchar(256)'] * len(columns)
        columns_and_data_types = ', '.join(['{0} {1}'.format(x, y) for x, y in zip(columns, dtype)])
        query = 'create table {0} ({1})'.format(table, columns_and_data_types)
        if drop_if_exists:
            self.__cursor.execute('drop table if exists {0}'.format(table))
        self.exec_commit(query)
        return

    def copy_to_redshift(self, table, s3_address, s3_credentials, delimiter=',', quote_char='"',
                         date_format='auto', time_format='auto'):
        query = f"""copy {table}
                    from '{s3_address}'
                    delimiter '{delimiter}'
                    ignoreheader 1
                    csv quote as '{quote_char}'
                    dateformat '{date_format}'
                    timeformat '{time_format}'
                    access_key_id '{s3_credentials["access_key"]}'
                    secret_access_key '{s3_credentials["secret_access_key"]}';"""
        try:
            self.exec_commit(query)
        except psycopg2.Error as e:
            print(e)
            traceback.print_exc(file=sys.stdout)
            self.__connection.rollback()
            raise

    def file_to_redshift(self, file_path, table, replace_table, delimiter=',', quote_char='"',
                         date_format='auto', time_format='auto', grant_user_access=None):
        s3 = S3Connection(**s3_temp)
        if replace_table:
            columns, dtypes = get_columns_and_redshift_dtypes(file_path=file_path, delimiter=delimiter)
            self.create_table(table=table, columns=columns, drop_if_exists=True, dtype=dtypes)
        else:
            columns = get_headers(file_path=file_path, delimiter=delimiter)
        if self.check_headers_for_reserved_words(headers=columns):
            file_name = table + os.path.splitext(file_path)[1]
            s3_address = 's3://{0}/{1}'.format(s3_temp['bucket'], s3_temp['prefix'] + file_name)
            s3.upload_file(file_path=file_path, key=file_name)
            self.copy_to_redshift(table=table, s3_address=s3_address, s3_credentials=s3_temp, delimiter=delimiter,
                                  quote_char=quote_char, date_format=date_format, time_format=time_format)
            s3.delete_file(key=file_name)
            if grant_user_access:
                self.exec_commit(f'grant select on public.{table} to {grant_user_access}')
        return


class EC2Connection:

    def __init__(self, aws_access_key_id, aws_secret_access_key, region_name, instance_id=None):
        try:
            self.__ec2 = resource('ec2', aws_access_key_id=aws_access_key_id,
                                  aws_secret_access_key=aws_secret_access_key,
                                  region_name=region_name)
            self.__ec2client = client('ec2', aws_access_key_id=aws_access_key_id,
                                  aws_secret_access_key=aws_secret_access_key,
                                  region_name=region_name)
            # self.instance = self.__ec2.Instance(instance_id)
        except ClientError as err:
            print('Could not connect to EC2:', err)
            exit()

    def overview(self):
        response = self.__ec2client.describe_instances()

        from pprint import pprint
        pprint(response)

        for reservation in response['Reservations']:
            for instance in reservation['Instances']:
                print(instance['KeyName'])
                print(instance['InstanceId'])
                print(instance['State']['Name'])
                print(instance['Tags'])
                # TODO: GET MORE INFORMATION
                print('\n')
        return

    def create_instance(self, ami_image_id, instance_type, min_count, max_count, key_name, security_group_ids, shutdown_behavior, user_data):
        '''
        Launching new instances requires an ImageID and the number of instances
        to launch. It can also take several optional parameters, such as the
        instance type and security group.

        ami-759bc50a = Ubuntu Server 16.04 LTS (HVM), SSD Volume Type
        '''
        instance = self.__ec2client.create_instances(ImageId=ami_image_id, InstanceType=instance_type,
                                                     MinCount=min_count, MaxCount=max_count,
                                                     KeyName=key_name, SecurityGroupIds=security_group_ids,
                                                     InstanceInitiatedShutdownBehavior=shutdown_behavior,
                                                     UserData=user_data)

        # instance_id = instance['Instances'][0]['InstanceID']
        return

    def start_instance(self, instance_id):
        instance_id = instance_id if isinstance(instance_id, list) else [instance_id]
        try:  # Verify permissions using DryRun
            self.__ec2client.start_instances(InstanceIds=instance_id, DryRun=True)
        except ClientError as e:
            if 'DryRunOperation' not in str(e):
                print('You do not have permission to start instances.')
                raise
        try:  # DryRun succeeded. Run start_instances without DryRun
            response = self.__ec2client.start_instances(InstanceIds=instance_id, DryRun=False)
            print(response)
        except ClientError as e:
            print(e)
        return

    def stop_instance(self, instance_id):
        instance_id = instance_id if isinstance(instance_id, list) else [instance_id]
        try:  # Verify permissions using DryRun
            self.__ec2client.stop_instances(InstanceIds=instance_id, DryRun=True)
        except ClientError as e:
            if 'DryRunOperation' not in str(e):
                print('You do not have permission to stop instances.')
                raise
        try:  # DryRun succeeded. Run start_instances without DryRun
            response = self.__ec2client.stop_instances(InstanceIds=instance_id, DryRun=False)
            print(response)
        except ClientError as e:
            print(e)
        return

    def reboot_instance(self, instance_id):
        instance_id = instance_id if isinstance(instance_id, list) else [instance_id]
        try:  # Verify permissions using DryRun
            self.__ec2client.reboot_instances(InstanceIds=instance_id, DryRun=True)
        except ClientError as e:
            if 'DryRunOperation' not in str(e):
                print('You do not have permission to reboot instances.')
                raise
        try:  # DryRun succeeded. Run start_instances without DryRun
            response = self.__ec2client.reboot_instances(InstanceIds=instance_id, DryRun=False)
            print(response)
        except ClientError as e:
            print(e)
        return

    def get_key_pairs(self):
        response = self.__ec2client.describe_key_pairs()
        for each in response['KeyPairs']:
            print('KeyFingerprint: {}\t\tKeyName: {}'.format(each['KeyFingerprint'], each['KeyName']))
