
import os
from azure.storage.blob import BlockBlobService, PublicAccess
import time
import urllib.request
import ssl

if (not os.environ.get('PYTHONHTTPSVERIFY', '') and
    getattr(ssl, '_create_unverified_context', None)): 
    ssl._create_default_https_context = ssl._create_unverified_context



 # Create the BlockBlockService that is used to call the Blob service for the storage account
block_blob_service = BlockBlobService(account_name='wmdatarfcolgate', account_key='ww2KsXz/Jz29XztHWshmgg1o+Cd8PffTzNcKAumCjiO/VG7j2EhFGk5iezEkpizvY1NHgCTp06CHtcDcd1bh3A==')

#print("\nList blobs in the container")
#generator = block_blob_service.list_blobs('colgate-palmolive')
#for blob in generator:
#    print("\t Blob name: " + blob.name)


url='http://data.groupm.com/api/SavedQuery/a9c450ab-9bb1-4368-9035-c746cba52363?applicationtype=DataMarketplace_API&useremail=phyo.thiha%40groupm.com&applicationtoken=ea55447a-bd17-404c-8539-87ecba7e72d1'
req = urllib.request.Request(url)
result=urllib.request.urlopen(req)
#result_bytes = result.read()
#result_str = result_bytes.decode('utf8')
#result_json = json.loads(result_str)
#def __init__(self):

postfix = str(int(time.time()))
fname = ''.join(['test_', postfix, '.json'])

block_blob_service.create_blob_from_bytes(
    container_name='colgate-palmolive',
    blob_name=fname,
    blob=result.read()
)