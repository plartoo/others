
import os
from azure.storage.blob import BlobService, BlockBlobService, PublicAccess
import time
import urllib.request
import ssl


def copy_azure_files(self):
    # https://stackoverflow.com/questions/32500935/python-how-to-move-or-copy-azure-blob-from-one-container-to-another
    blob_service = BlockBlobService(account_name='wmdatarfcolgate',account_key='ww2KsXz/Jz29XztHWshmgg1o+Cd8PffTzNcKAumCjiO/VG7j2EhFGk5iezEkpizvY1NHgCTp06CHtcDcd1bh3A==')

    blob_name = 'test_1534532726.json'
    copy_from_container = 'colgate-palmolive'
    copy_to_container = 'colgate-palmolive/Test'

    blob_url = blob_service.make_blob_url(copy_from_container, blob_name)
    # blob_url:https://demostorage.blob.core.windows.net/image-container/pretty.jpg

    blob_service.copy_blob(copy_to_container, blob_name, blob_url)

    # for move the file use this line
    blob_service.delete_blob(copy_from_container, blob_name)
    print("Finished copying blob")



if (not os.environ.get('PYTHONHTTPSVERIFY', '') and
    getattr(ssl, '_create_unverified_context', None)):
    # Turn off the Python certificate verification
    ssl._create_default_https_context = ssl._create_unverified_context

 # Create the BlockBlobService that is used to call the Blob service for the storage account
block_blob_service = BlockBlobService(account_name='wmdatarfcolgate',
                                      account_key='ww2KsXz/Jz29XztHWshmgg1o+Cd8PffTzNcKAumCjiO/VG7j2EhFGk5iezEkpizvY1NHgCTp06CHtcDcd1bh3A==')

print("\nList blobs in the container")
generator = block_blob_service.list_blobs('colgate-palmolive')
for blob in generator:
   print("\t Blob name: " + blob.name)

copy_azure_files()

#
#
# url='http://data.groupm.com/api/SavedQuery/a9c450ab-9bb1-4368-9035-c746cba52363?applicationtype=DataMarketplace_API&useremail=phyo.thiha%40groupm.com&applicationtoken=ea55447a-bd17-404c-8539-87ecba7e72d1'
# req = urllib.request.Request(url)
# result=urllib.request.urlopen(req)
# #result_bytes = result.read()
# #result_str = result_bytes.decode('utf8')
# #result_json = json.loads(result_str)
# #def __init__(self):
#
# postfix = str(int(time.time()))
# fname = ''.join(['','test_', postfix, '.json'])
#
# block_blob_service.create_blob_from_bytes(
#     container_name='colgate-palmolive',
#     blob_name=fname,
#     blob=result.read()
# )