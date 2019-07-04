import json
import uuid
import os
import requests
import time
from azure.storage.blob import BlockBlobService, PublicAccess
from azure.storage.blob.models import Blob
import requests
import urllib.request
import magic
domain = "http://52.172.196.135/api/"

account_name = os.environ.get('AZURE_ACCOUNT_NAME')
account_key = os.environ.get('AZURE_ACCOUNT_KEY')
AZURE_BLOB_URL = "https://evolvestoragesunbird.blob.core.windows.net"
sastoken = (requests.get(domain +'content/getsas')).json()
block_blob_service = BlockBlobService(account_name=account_name, account_key=account_key,sas_token=sastoken['token'])
container_name = 'evolve'


dictionary={}
final_data= []
r = requests.get( domain + 'content/urlupdate')
for i in r.json()['data']:
    if i['video'] is not None:        
        path = i['video'].replace("https://evolvestoragesunbird.blob.core.windows.net/evolve/","").replace("%20","")
        _path,filename  = os.path.split(path)
        if os.path.isdir(_path)== False:
            os.makedirs(_path)
        name,ext =  os.path.splitext(i['video'])
#         filename = (os.path.basename(i['file_url']))
        if (ext != '.mp4'):
            print("withoutext:-" +str(i))
            dictionary["content_id"]=(i['id'])
            dictionary["file_path_from_database"]=(i['video'])
            urllib.request.urlretrieve(i['video'] + "?"+ i['sas_token']  , _path+"/"+filename) 
            mime = magic.Magic(mime=True)
            content_type= mime.from_file(_path+"/"+filename)
            if content_type == "video/mp4":
                filename_change_ext= (os.path.splitext(filename)[0]) + ".mp4"
                os.rename(os.path.join(_path, filename), os.path.join(_path,filename_change_ext))
                full_path_to_file = os.path.join(_path+"/"+filename_change_ext)
                print("filename : - "+full_path_to_file)
                print("file :- "+_path+"/"+ filename )
                dictionary["video"]=(AZURE_BLOB_URL +"/"+ container_name +"/"+ full_path_to_file)
                final_data.append(dictionary)
#                 resp = block_blob_service.create_blob_from_path(container_name,full_path_to_file,full_path_to_file)
            dictionary = {}
print(final_data)
payload = final_data
url = domain + "content/urlputrequest"

headers = {
    'content-type': "application/json",
    
    }

response = requests.request("POST", url, data=json.dumps(payload), headers=headers)

print(response.text)
