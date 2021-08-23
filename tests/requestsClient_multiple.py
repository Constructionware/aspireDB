import requests
import time, sys

start_time = time.time()
url = 'http://localhost:8080/pokemon/'
for number in range(1, 151):    
    resp = requests.get(f'{url}{number}')
    pokemon = resp.json()
    sys.stdout.write(f"{pokemon['name']}-")

print("--- %s seconds ---" % (time.time() - start_time))