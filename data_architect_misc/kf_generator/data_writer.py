import csv
import os.path
import sys
import datetime

class DataWriter(object):
    BYTES_IN_MEGABYTES = 1000000

    def __init__(self):
        self.encoding = 'utf-8'
        self.newline = ''
        self.lineterminator = "\n" # to return 'LF' only. REF: https://stackoverflow.com/a/17725590
        self.delimiter = ','
        self.quotechar = '"'
        self.quoting = csv.QUOTE_ALL
        self.row_count_limit = 1000000
        self.file_size_limit = 10 * DataWriter.BYTES_IN_MEGABYTES # 10MB as default file size limit

        # default output directory in 'current_directory/YYYY-MM-DD-HHMMSS' format
        cur_dir_path = os.path.dirname(os.path.realpath(__file__))
        self.output_dir = os.path.join(cur_dir_path, datetime.datetime.now().strftime('%Y-%m-%d-%H%M%S'))
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def get_size_in_bytes(self, row):
        # Note: this will only return the best size approximation for each row
        qc = self.quotechar # workaround for REF: https://stackoverflow.com/a/28130950
        row_str = self.delimiter.join((qc+str(r)+qc) for r in row) #+ self.lineterminator
        # REF1: https://stackoverflow.com/a/4013418
        # REF2: https://stackoverflow.com/q/5290182
        return len(row_str.encode(self.encoding))

    def write_to_file(self, data, output_file, configs):
        self.encoding = configs['encoding'] if 'encoding' in configs else self.encoding
        self.newline = configs['newline'] if 'newline_char' in configs else self.newline
        self.lineterminator = configs['lineterminator'] if 'lineterminator' in configs else self.lineterminator
        self.delimiter = configs['delimiter'] if 'delimiter' in configs else self.delimiter
        self.quotechar = configs['quotechar'] if 'quotechar' in configs else self.quotechar
        self.quoting = configs['quoting'] if 'quoting' in configs else self.quoting

        file_extension = '.tsv' if self.delimiter == '\t' else '.csv'
        output_file = ''.join([output_file, file_extension])
        with open(output_file, 'w', newline=self.newline, encoding=self.encoding) as fo:
            try:
                writer = csv.writer(fo, delimiter=self.delimiter, lineterminator=self.lineterminator,
                                    quotechar=self.quotechar, quoting=self.quoting)
                writer.writerows(data)
                print('Wrote file: ', output_file)
            except csv.Error as e:
                print('\n\n***!!! Error in writing CSV (output) file: ', output_file, '\n\n')
                sys.exit()

    def prepare_output_file_path_and_name(self, file_num, file_basename):
        return file_basename + str(file_num) + datetime.datetime.now().strftime('_%m_%Y')

    def write_data_all_at_once(self, data, configs):
        include_header = configs['include_header'] if 'include_header' in configs else True
        split = configs['split_file'] if 'split_file' in configs else False
        split_by = configs['split_by'] if 'split_by' in configs else 'row'
        split_limit = configs['split_limit'] if 'split_limit' in configs else self.row_count_limit

        if not split:
            self.write_to_file(data, os.path.join(self.output_dir, configs['output_file_basename']), configs)
            print('<===\n')
        else:
            # I can split data using list comprehension like below and write it. The code would be much shorter/cleaner!
            # REF: https://stackoverflow.com/a/312464
            # [data[i:i+n] for i in range(0,len(data),n)]
            # But that may create space inefficiencies for gigantic lists.
            # That's why I opted instead to write chunk by chunk (looks a bit naive to say the least)
            cur_row_num = 0
            file_count = 1
            header = data[0]
            header_size = self.get_size_in_bytes(header) # this gives approximate size
            cur_doc = [header]
            cur_doc_size = header_size
            for i, row in enumerate(data[1:]):
                cur_row_num = i
                cur_row_size = self.get_size_in_bytes(row)
                if (split_by == 'row' and ((i+1)%split_limit != 0)) \
                        or (split_by == 'size' and (cur_doc_size+cur_row_size <= split_limit)):
                    cur_doc.append(row)
                    cur_doc_size += cur_row_size
                else:
                    output_file_name = self.prepare_output_file_path_and_name(str(file_count),
                                                                              configs['output_file_basename'])
                    self.write_to_file(cur_doc, os.path.join(self.output_dir, output_file_name), configs)
                    print('at row number:', str(i+1), '\t\twith approx. file size (in MB):',
                          cur_doc_size/DataWriter.BYTES_IN_MEGABYTES)
                    file_count += 1

                    # reset tracking variable and current document container
                    cur_doc = [header] if include_header else []
                    cur_doc_size = header_size if include_header else 0

            output_file_name = self.prepare_output_file_path_and_name(str(file_count),
                                                                      configs['output_file_basename'])
            self.write_to_file(cur_doc, os.path.join(self.output_dir, output_file_name), configs)
            print('at row number:', str(cur_row_num+1), '\t\twith approx. file size (in MB):',
                  cur_doc_size/DataWriter.BYTES_IN_MEGABYTES, '\n<===\n')

    def get_size_of_first_row(self, db_connection, query):
        cursor = db_connection.cursor()
        cursor.execute(query)
        row = [i for i in cursor.fetchone()]
        cursor.close()
        return self.get_size_in_bytes(row)

    def get_approximate_rows_per_doc(self, row_size, size_limit):
        return int(size_limit/row_size)

    def get_row_per_doc(self, db_connection, configs):
        # since we are going to pull and write data incrementally, we need two parameters below
        if ('split_by' not in configs) or ('split_limit' not in configs):
            sys.exit("\n\n***!!! You must define how to ('split_by') and when to ('split_limit') "
                     "split the data if you are to incrementally write data."
                     "\nTerminating the program until these parameters are included in configuration.\n")

        if configs['split_by'] == 'row':
            return configs['split_limit']
        elif configs['split_by'] == 'size':
            row_size = self.get_size_of_first_row(db_connection, configs['query'])
            row_limit = self.get_approximate_rows_per_doc(row_size, configs['split_limit'])
            return self.get_approximate_rows_per_doc(row_size, configs['split_limit'])
        else:
            return self.row_count_limit

    def write_data_incrementally(self, db_connection, configs):
        include_header = configs['include_header'] if 'include_header' in configs else True
        row_per_doc = self.get_row_per_doc(db_connection, configs)

        cursor = db_connection.cursor()
        cursor.execute(configs['query'])

        file_count = 1
        total_row_count = 0
        header = [header[0] for header in cursor.description]
        print("\nMax. row(s) per doc:", str(row_per_doc))
        while True:
            # Here, I decided to use 'fetchmany' instead of 'fetchone' (see footnote for detail)
            # REF: https://github.com/mkleehammer/pyodbc/wiki/Cursor
            rows = [list(row) for row in cursor.fetchmany(row_per_doc)]
            if not rows:
                break

            cur_doc = ([header] + rows) if include_header else rows
            total_row_count += len(rows)
            output_file_name = self.prepare_output_file_path_and_name(str(file_count),
                                                                      configs['output_file_basename'])
            self.write_to_file(cur_doc, os.path.join(self.output_dir, output_file_name), configs)
            print('at row number:', str(total_row_count))
            del cur_doc # hoping to invoke Python garbage collector REF: https://stackoverflow.com/q/1316767
            del rows
            file_count += 1

        cursor.close()


    ## Footnote
    # The incremental write method (write_data_incrementally) came about because some of our tables
    # have tens of millions of rows. That pretty much ensured getting MemoryError from Python if
    # we use 'write_data_all_at_once' because that approach loads ALL of the data in the table
    # into Python's working memory.
    #
    # In incremental approach, we can go like this: fetch ONE row, then write that row to CSV,
    # keep doing the previous two steps until no more rows to fetch. BUT that, in my opinion,
    # is a waste because we can reduce the network IO (back and forth 'talking' between DB server
    # and current Python instance) by fetching many rows per cursor's move forward. That's why
    # I've decided to use 'fetchmany' method to fetch and write X (where X > 1) number of rows
    # at every iteration/increment.
    #
    # Now, there comes the question of how to decide the optimal number of rows per fetch.
    # Well...we have client's delivery requirement of 1.5 million rows per doc.
    # And we also know that sometimes our FTPs aren't good enough to transfer files that are
    # of in 100s of MB range. Using that as baseline, I've decide to roughly calculate the number
    # of rows, which can be configured, to write per document using 'get_row_per_doc' method, which
    # uses a simple formula (max_file_size_allowed/size_of_each_row) to estimate the number of
    # rows per file (if row limit is not provided).
    #
    # Below is another way to calculate the number of rows per file if file size limit is given:
    # 1. Pass table name and change the way we connect to DB (APAC vs. other)
    # 2. Run cursor.columns(table=<table_name>) and get max possible size of each column like below:
    # [i[6] for i in [r for r in cursor.columns(table='CP_DIM_COUNTRY')]]
    # 3. Calculate number of rows that will fit in a split_limit based on info from #2 above
    # This approach will tend to over-estimate the actual size of the rows under split_limit,
    # so we may undershoot the number of rows in each file delivered.
    #
    # For now, let's stick to the naive approach of calculating row limit for each file. We can try
    # the more robust approach later.
