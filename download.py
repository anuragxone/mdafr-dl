import asyncio
import aiohttp
import os
from tqdm import tqdm


# Function to download a single file asynchronously with original filename
async def download_file(session, url, filename):
    try:
        async with session.get(url) as response:
            if response.status == 200:
                file_size = int(response.headers.get('Content-Length', 0))

                with open(filename, 'wb') as f, tqdm(
                        desc=filename,
                        total=file_size,
                        unit='B',
                        unit_scale=True,
                        unit_divisor=1024,
                        miniters=1,
                        ncols=100,
                        position=0,
                        leave=True,
                ) as progress_bar:
                    while True:
                        chunk = await response.content.read(1024)
                        if not chunk:
                            break
                        f.write(chunk)
                        progress_bar.update(len(chunk))
    except Exception as e:
        print(f"Failed to download {url}: {e}")


# Function to download files concurrently
async def download_concurrently(links, num_concurrent_downloads):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for link in links:
            filename = os.path.basename(link)
            task = download_file(session, link, filename)
            tasks.append(task)

            if len(tasks) == num_concurrent_downloads:
                await asyncio.gather(*tasks)
                tasks = []

        if tasks:
            await asyncio.gather(*tasks)


# Read direct links from 'direct_links.txt'
with open('direct_links.txt', 'r') as f:
    direct_links = f.read().splitlines()

# Specify the number of concurrent downloads (e.g., 5)
num_concurrent_downloads = 1

# Start the download process
loop = asyncio.get_event_loop()
loop.run_until_complete(download_concurrently(direct_links, num_concurrent_downloads))
