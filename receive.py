import requests
import urllib.request


URL = 'https://api.nasa.gov/planetary/earth/imagery/'

PARAMS = {'lat':33.4299, 'lon':35.1264, 'api_key':'lKrddrL0IReZgPkY6BeOFZ7tytqOg3MfdG5m5Cq9'}
r = requests.get(url = URL, params = PARAMS)

data = r.json()
print(data['url'])

urllib.request.urlretrieve(data['url'], '000001.png')
