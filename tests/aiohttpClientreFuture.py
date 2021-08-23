import aiohttp
import asyncio
import time, sys

start_time = time.time()
semaphore = asyncio.Semaphore(3900)

import aiohttp
import asyncio
import time

start_time = time.time()


async def get_pokemon(session, url):
    await semaphore.acquire()
    try:        
        async with session.get(url) as resp:
            pokemon = await resp.json()
            return pokemon['name']
    finally:
        semaphore.release()


async def main():
    await semaphore.acquire()
    try:

        async with aiohttp.ClientSession() as session:
            tasks = []
            n = 1           
            
            while n <= 1500:
                url = f'http://localhost:9090/user/{n}'
                tasks.append(asyncio.ensure_future(get_pokemon(session, url)))
                n+=1

            original_pokemon = await asyncio.gather(*tasks)
            for pokemon in original_pokemon:
                #print(pokemon)
                sys.stdout.write(f"{pokemon}-")
    finally:
        semaphore.release()

asyncio.run(main())
print("--- %s seconds ---" % (time.time() - start_time))