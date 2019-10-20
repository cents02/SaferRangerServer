import random
import requests
import time

ids = []
xs = []
ys = []
date = '19-10-2019'
status = []

URL = "http://0.0.0.0:5005/balladd"
for i in range(10):
    ids.append(str(i) + 'A')
    ys.append(random.randint(0,500))
    xs.append(random.randint(0,500))
    temp = random.choice(['dead', 'idle'])
    PARAMS = { 'ID':ids[i],'X':xs[i],'Y':ys[i],'DATE':date,'STATUS':temp}
    r = requests.post(url = URL, data = PARAMS)
    print(r)
    time.sleep(1)
