import csv
import urllib
import urllib.parse
import requests
import urllib3
import socket
import traceback
import datetime
import zlib

def is_valid(url, qualifying=None):
    """
    Validates if a URL meets standard scheme (e.g., http://blahblah
    """
    # REF: https://stackoverflow.com/a/36283503
    min_attributes = ('scheme', 'netloc')
    qualifying = min_attributes if qualifying is None else qualifying
    token = urllib.parse.urlparse(url)
    return all([getattr(token, qualifying_attr)
                for qualifying_attr in qualifying])

if __name__ == '__main__':
    dt = datetime.datetime.now().strftime('_%Y%m%d_%H%M%S')
    good_urls = []
    bad_urls = []
    i = 0
    try:
        with open('domains.csv') as csvfile:
            csvreader = csv.reader(csvfile)
            for row in csvreader:
                i += 1
                url = 'https://' + row[0] + '/ads.txt'
                try:
                    print(str(i), '.', url)
                    rt = requests.get(url, timeout=10)
                    good_urls.append([url, rt.status_code])
                except Exception as e:
                    url = 'http://' + row[0] + '/ads.txt'
                    try:
                        print(url)
                        rt = requests.get(url, timeout=10)
                        good_urls.append([url, rt.status_code])
                    except (requests.exceptions.ConnectionError, urllib3.exceptions.NewConnectionError, urllib3.exceptions.MaxRetryError, socket.gaierror, socket.timeout, urllib3.exceptions.ReadTimeoutError, zlib.error, urllib3.exceptions.DecodeError, socket.timeout, urllib3.exceptions.ReadTimeoutError) as e:
                        bad_urls.append([url, 'error:', str(e)])
                    except Exception as e: # REF: https://stackoverflow.com/a/45700425
                        print(traceback.print_exc())
                        bad_urls.append([url, 'error:', str(e)])
    except Exception as e:
        fgood = 'good_urls_' + dt + '.csv'
        fbad = 'bad_urls_' + dt + '.csv'
        with open(fgood, 'w') as fo:
                try:
                    writer = csv.writer(fo, delimiter='|', lineterminator='\n')#,quotechar='"', quoting=csv.QUOTE_MINIMAL)
                    writer.writerows(good_urls)
                except csv.Error as e:
                    print('\n\n***!!! Error in writing CSV (output) file\n\n')

        with open(fbad, 'w') as fo:
                try:
                    writer = csv.writer(fo, delimiter='|', lineterminator='\n')#,quotechar='"', quoting=csv.QUOTE_MINIMAL)
                    writer.writerows(bad_urls)
                except csv.Error as e:
                    print('\n\n***!!! Error in writing CSV (output) file\n\n')

    fgood = 'good_urls_' + dt + '.csv'
    fbad = 'bad_urls_' + dt + '.csv'
    with open(fgood, 'w') as fo:
            try:
                writer = csv.writer(fo, delimiter='|', lineterminator='\n')#,quotechar='"', quoting=csv.QUOTE_MINIMAL)
                writer.writerows(good_urls)
            except csv.Error as e:
                print('\n\n***!!! Error in writing CSV (output) file\n\n')

    with open(fbad, 'w') as fo:
            try:
                writer = csv.writer(fo, delimiter='|', lineterminator='\n')#,quotechar='"', quoting=csv.QUOTE_MINIMAL)
                writer.writerows(bad_urls)
            except csv.Error as e:
                print('\n\n***!!! Error in writing CSV (output) file\n\n')

    print('Done')
