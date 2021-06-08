#pip install fastapi-utils
#pip install uvicorn
#Run the server as 
#uvicorn main:app --reload
#python3 main.py

import requests

pload = {'RequestId':'123456789',
         'FilePath':'/home/fakrul/LeadDesk/audios/7185838650087181924__test.wav', 
         'SequenceId':'1234', 
         'UserType':'Agent'}

r = requests.post('http://127.0.0.1:8000/items', json = pload)
#print(r.text)
print(r.json())



