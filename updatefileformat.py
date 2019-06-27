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
domain = "https://evolve.diksha.gov.in/api/"

account_name = os.environ.get('AZURE_ACCOUNT_NAME')
account_key = os.environ.get('AZURE_ACCOUNT_KEY')

AZURE_BLOB_URL = "https://evolveprodall.blob.core.windows.net"
sastoken = (requests.get(domain +'/content/getsas')).json()
block_blob_service = BlockBlobService(account_name=account_name, account_key=account_key,sas_token=sastoken['token'])
container_name = 'evolve'


dictionary={}
final_data= []
r = requests.get( domain + 'othercontents/urlupdate')
for i in r.json()['data']:
    if i['file_url'] is not None:
        path = i['file_url'].replace("https://evolveprodall.blob.core.windows.net/evolve/","").replace("%20","")
        _path,filename  = os.path.split(path)
        if os.path.isdir(_path)== False:
            os.makedirs(_path)
        name,ext =  os.path.splitext(i['file_url'])
#         filename = (os.path.basename(i['file_url']))
        
        if (ext != '.mp4') and (ext != '.pdf') and (ext !='.pptx') :
            dictionary["content_id"]=(i['id'])
            dictionary["file_path_from_database"]=(i['file_url'])
            
            _database_url = str(str(i['file_url']) + "?"+ str(i['sas_token'])) 
            print(_database_url)
            file_path = str(_path)+"/"+str(filename)
            urllib.request.urlretrieve(_database_url , file_path )
            mime = magic.Magic(mime=True)
            content_type= mime.from_file(_path+"/"+filename)
            if content_type == 'application/pdf':
                filename_change_ext= (os.path.splitext(filename)[0]) + ".pdf"
                os.rename(os.path.join(_path, filename), os.path.join(_path,filename_change_ext))
                full_path_to_file = os.path.join(_path+"/"+filename_change_ext)

                dictionary["final_url"]=(AZURE_BLOB_URL +"/"+ container_name +"/"+ full_path_to_file)
                final_data.append(dictionary)
                resp = block_blob_service.create_blob_from_path(container_name,full_path_to_file,full_path_to_file)

            elif content_type == "video/mp4" or content_type == "video/x-m4v":
                filename_change_ext= (os.path.splitext(filename)[0]) + ".mp4"
                os.rename(os.path.join(_path, filename), os.path.join(_path,filename_change_ext))
                full_path_to_file = os.path.join(_path+"/"+filename_change_ext)

                dictionary["final_url"]=(AZURE_BLOB_URL +"/"+ container_name +"/"+ full_path_to_file)
                final_data.append(dictionary)
                resp = block_blob_service.create_blob_from_path(container_name,full_path_to_file,full_path_to_file)
            dictionary = {}
payload = final_data
print("finallist:--"+ str(payload))

url = domain + "othercontents/urlputrequest"


headers = {
    'content-type': "application/json",
    'cache-control': "no-cache",
    'postman-token': "15f793b9-2ea3-41cd-a04d-2badd12a3395"
    }

response = requests.request("POST", url, data=json.dumps(payload), headers=headers)

print(response.text)

