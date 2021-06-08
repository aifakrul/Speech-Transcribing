# -*- coding: utf-8 -*-

import requests

pload = {'RequestId':'123456789','FilePath':'/home/fakrul/LeadDesk/audios/7185838650087181924__test.wav'}
r = requests.post('http://0.0.0.0:9001/',data = pload)
print(r.text)