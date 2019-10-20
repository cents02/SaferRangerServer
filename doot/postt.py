import requests
URL = "http://192.168.137.13:5010/balladd"
id = 'A6'
x = 120.5
y = 150.12
date = '11-22-3'
status = 'dead'
PARAMS = { 'ID':id,'X':x,'Y':y,'DATE':date,'STATUS':status}
r = requests.post(url = URL, data = PARAMS)
print(r)
