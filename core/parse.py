import os
import sys
import m3u8
import aiohttp
import asyncio

def __get_path():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    else:
        return os.path.dirname(
            os.path.dirname(
                os.path.abspath(__file__)
            )
        )

TEMPDIR = os.path.join(__get_path(),'temp')
if not os.path.exists(TEMPDIR):
    os.makedirs(TEMPDIR)

def parse_uri(data: list, ssl=True):
    def get_size(urls: list, ssl):
        async def contentLength(url, ssl):
            async with aiohttp.ClientSession() as session:
                async with session.head(url, ssl=ssl) as response:
                    current.append(asyncio.current_task().get_name())
                    sys.stdout.write(f"\r\t Fetching segments...[{len(current)}/{count}]")
                    sys.stdout.flush()
                    return response.content_length

        loop = asyncio.get_event_loop()
        tasks = [contentLength(url, ssl) for url in urls]
        tot = loop.run_until_complete(asyncio.gather(*tasks))
        return sum(tot)
    
    async def parse(item, ssl):
        async with aiohttp.ClientSession() as session:
            async with session.get(item["uri"], ssl=ssl) as response:
                tempname = os.path.join(TEMPDIR, os.path.basename(item["uri"]))
                with open(tempname, 'wb') as fp:
                    fp.write(await response.content.read())

                content = []

                with open(tempname, 'r+') as fp:
                    data = m3u8.loads(fp.read())
                    baseUri = os.path.dirname(item["uri"])
                    
                    initSeg = ""
                    if data.segment_map:
                        initSeg = data.segment_map[0].uri
                        content.append(baseUri + '/' + initSeg)
                    for seg in data.segments:
                        if seg.uri != initSeg:
                            content.append(baseUri + '/' + seg.uri)

                item["uri"] = content

    loop = asyncio.get_event_loop()
    tasks = [parse(item, ssl) for item in data]
    loop.run_until_complete(asyncio.gather(*tasks))

    count = 0
    current = []
    
    for item in data:
        count += len(item['uri'])

    print()
    for item in data:
        item["size"] = get_size(item["uri"], ssl)
    print('\n')