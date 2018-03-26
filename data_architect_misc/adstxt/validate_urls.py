import csv
import urllib
import urllib.parse
import requests


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
    valid_urls = []
    invalid_urls = []
    with open('domains.csv') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            url = 'https://' + row[0] + '/ads.txt'
            # checks if the URL text is in valid form
            # if is_valid(url):
            #     valid_urls.append([url])
            # else:
            #     invalid_urls.append([url])

            responses = []
            print(url)
            try:
                r = requests.get(url, timeout=10)
                responses.append([url, r.status_code])
            except:
                url = 'http://' + row[0] + '/ads.txt'
                print(url)
                r = requests.get(url, timeout=10)
                responses.append([url, r.status_code])
                pass

            finally:
                with open('domains-response.csv', 'w') as fo:
                        try:
                            writer = csv.writer(fo, delimiter='|', lineterminator='\n')#,quotechar='"', quoting=csv.QUOTE_MINIMAL)
                            writer.writerows(responses)
                        except csv.Error as e:
                            print('\n\n***!!! Error in writing CSV (output) file\n\n')

    print('Done')