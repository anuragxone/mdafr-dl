import asyncio
import aiohttp

# Function to download a single file asynchronously
async def download_file(session, url, filename):
    try:
        async with session.get(url) as response:
            if response.status == 200:
                with open(filename, 'wb') as f:
                    while True:
                        chunk = await response.content.read(1024)
                        if not chunk:
                            break
                        f.write(chunk)
                print(f"Downloaded: {filename}")
    except Exception as e:
        print(f"Failed to download {url}: {e}")

# Function to download files concurrently
async def download_concurrently(links, num_concurrent_downloads):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for i, link in enumerate(links, start=1):
            filename = f"file_{i}.zip"  # Adjust filename generation if needed
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
num_concurrent_downloads = 5

# Start the download process
loop = asyncio.get_event_loop()
loop.run_until_complete(download_concurrently(direct_links, num_concurrent_downloads))
