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
        qc = self.quotechar # workaround for REF: https://stackoverflow.com/a/28130950
        row_str = self.delimiter.join((qc+str(r)+qc) for r in row) #+ self.lineterminator
        # REF1: https://stackoverflow.com/a/4013418
        # REF2: https://stackoverflow.com/q/5290182
        return len(row_str.encode(self.encoding))

    def write_to_file(self, data, configs):
        self.encoding = configs['encoding'] if 'encoding' in configs else self.encoding
        self.newline = configs['newline'] if 'newline_char' in configs else self.newline
        self.lineterminator = configs['lineterminator'] if 'lineterminator' in configs else self.lineterminator
        self.delimiter = configs['delimiter'] if 'delimiter' in configs else self.delimiter
        self.quotechar = configs['quotechar'] if 'quotechar' in configs else self.quotechar
        self.quoting = configs['quoting'] if 'quoting' in configs else self.quoting

        output_file = configs['output_file']
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

    def write_data(self, data, configs):
        include_header = configs['include_header'] if 'include_header' in configs else True
        split = configs['split_file'] if 'split_file' in configs else False
        split_by = configs['split_by'] if 'split_by' in configs else 'row'
        split_limit = configs['split_limit'] if 'split_limit' in configs else self.row_count_limit

        if not split:
            configs['output_file'] = os.path.join(self.output_dir, configs['output_file_basename'])
            self.write_to_file(data, configs)
            print('<===\n')
        else:
            # I can split data using list comprehension like below and write it. The code would be much shorter/cleaner!
            # REF: https://stackoverflow.com/a/312464
            # [data[i:i+n] for i in range(0,len(data),n)]
            # But that may create space inefficiencies for gigantic lists. TODO: verify space inefficiencies
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
                    output_file_name = configs['output_file_basename'] + str(file_count)\
                                             + datetime.datetime.now().strftime('_%m_%Y')
                    configs['output_file'] =  os.path.join(self.output_dir, output_file_name)
                    self.write_to_file(cur_doc, configs)
                    print('at row number:', str(i+1), '\t\twith approx. file size (in MB):',
                          cur_doc_size/DataWriter.BYTES_IN_MEGABYTES)
                    file_count += 1

                    # reset tracking variable and current document container
                    cur_doc = [header] if include_header else []
                    cur_doc_size = header_size if include_header else 0

            output_file_name = configs['output_file_basename'] + str(file_count) \
                               + datetime.datetime.now().strftime('_%m_%Y')
            configs['output_file'] = os.path.join(self.output_dir, output_file_name)
            self.write_to_file(cur_doc, configs)
            print('at row number:', str(cur_row_num+1), '\t\twith approx. file size (in MB):',
                  cur_doc_size/DataWriter.BYTES_IN_MEGABYTES, '\n<===\n')
