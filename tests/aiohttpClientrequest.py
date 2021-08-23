import aiohttp
import asyncio
import time, sys

start_time = time.time()
semaphore = asyncio.Semaphore(2000)

async def main():
    async with aiohttp.ClientSession() as session:
        await semaphore.acquire()
        try:
            for number in range(1, 2):
                pokemon_url = f'http://localhost:8080/user/{number}'
                async with session.get(pokemon_url) as resp:
                    pokemon = await resp.json()
                    sys.stdout.write(f"{pokemon['name']}-")
                    #print(pokemon['name'])
        finally:
            semaphore.release()

asyncio.run(main())
print("Task Completed in--- %s seconds ---" % (time.time() - start_time))