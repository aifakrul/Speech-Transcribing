# -*- coding: utf-8 -*-

import uvicorn
from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
import pickle
from fastapi_utils.tasks import repeat_every
from fastapi import FastAPI
import os

app = FastAPI()

StorageMap = {}
Storage= {}
ServiceMap = []

AUDIO_PROCESSED_PATH = '/home/fakrul/flask_session_server/audio_processed/'

class Items(BaseModel):
    RequestId:str
    FilePath:str
    SequenceId:str
    UserType:str


#@app.on_event("startup")
#@repeat_every(seconds=5)  # 5 seconds
#def remove_expired_tokens_task() -> None:
#    print('Hello in 5 seconds')

@app.on_event("startup")
async def startup_event():
    with open('StorageMap.pickle', 'rb') as fstp:
        StorageMap = pickle.load(fstp)
        print('Type:',type(StorageMap))
        print('Total Items in Storage:',len(StorageMap))
        print('Storage MAP Loaded: ', StorageMap)
        
    with open('ServiceMapList.pickle', 'rb') as fsrp:
        ServiceMap = pickle.load(fsrp)    
        print('Type:',type(ServiceMap))
        print('Total Items in Served:',len(ServiceMap))
        print('Service MAP Loaded: ', ServiceMap)


@app.on_event("shutdown")
def shutdown_event():
    pickle_storageMap_out = open("StorageMap.pickle","wb")
    pickle.dump(StorageMap, pickle_storageMap_out)
    pickle_storageMap_out.close()

    pickle_ServiceMap_out = open("ServiceMapList.pickle","wb")
    pickle.dump(ServiceMap, pickle_ServiceMap_out)
    pickle_ServiceMap_out.close()
    
    with open("log.txt", mode="a") as log:
        log.write("Application shutdown")

@app.get("/")
def read_root():
    return {"Hello": "World"}

#Called BY AIOHTTP
@app.get("/fetch/{RequestId}")
async def read_memory(RequestId):
    
    print('Route /fetch/ read memory')
    
    requested_storage = StorageMap[RequestId]
    
    print('requested_storage: ',requested_storage)
    print('FilePath: ', requested_storage['FilePath'])
    print('SequenceId: ', requested_storage['SequenceId'])
    print('UserType: ', requested_storage['UserType'])
    
    #ServiceMap.append(RequestId)
    
    #return {"RequestId": RequestId}
    return requested_storage


#Called by Websocket
@app.get("/process_finish/{RequestId}")
async def clean_memory(RequestId):
    print('Route /process_finish/')        
    ServiceMap.append(RequestId)    
    print('Service MAP: ', ServiceMap)
    return 'Success'

#Called by FLASK_SCHEDULER
@app.get("/process_finish_all/")
async def clean_memory_space():
    
    print('Route /process_finish_all/')
    print('Current Service MAP: ', ServiceMap)
    print('Current Storage MAP: ', StorageMap)
    
    try:
        item = ServiceMap.pop()
        print('Item: ', item)
        print('Type: ', type(item))
        item = str(item)
        #ServiceMap.remove(item)
        print('Storage: ',StorageMap)
        requested_storage = StorageMap[item]
        print('requested_storage: ',requested_storage)
        print('FilePath: ', requested_storage['FilePath'])
        print('SequenceId: ', requested_storage['SequenceId'])
        print('UserType: ', requested_storage['UserType'])
        file_path = requested_storage['FilePath']
        del StorageMap[item]
        print('New Storage Map: ',StorageMap )
        print('New Service Map: ',ServiceMap )
        COMMAND = "mv "+ str(file_path)+ " "+ str(AUDIO_PROCESSED_PATH)
        print('Command :', COMMAND)
        returned_value = os.system(COMMAND) 
        print('command return value: ',returned_value)
        
    except Exception as e:
        print("Oops!", e.__class__, "occurred.")
    
    return 'Success'
        
@app.post("/items/")
async def save_data_memory(item: Items):
    print('Route /items/ Saved in Memory')
    
    print('RequestId: ', item.RequestId)
    print('FilePath: ', item.FilePath)
    print('SequenceId: ', item.SequenceId)
    print('UserType: ', item.UserType)
    
    Storage['FilePath']=item.FilePath
    Storage['SequenceId']=item.SequenceId
    Storage['UserType']=item.UserType
    
    StorageMap[item.RequestId]=Storage
    
    print(StorageMap)
    
    return item
    #return {"Hello": "World"}


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)