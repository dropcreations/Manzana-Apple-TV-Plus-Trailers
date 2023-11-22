import os
import sys
import aiohttp
import asyncio
import subprocess

from rich.progress import (
    BarColumn,
    Progress,
    TextColumn,
    DownloadColumn,
    TransferSpeedColumn,
    TimeRemainingColumn
)

from utils import logger

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
STATFILE = os.path.join(TEMPDIR, "pgrstat.mnst")

if not os.path.exists(TEMPDIR):
    os.makedirs(TEMPDIR)

def download(data: list, ssl=True):
    
    st = []

    async def get_bytes(uri, ty, ssl, overall: Progress, progress: Progress):
        async with aiohttp.ClientSession() as session:
            async with session.get(uri, ssl=ssl) as response:
                tempname = os.path.join(TEMPDIR, os.path.basename(uri))
                if os.path.exists(tempname):
                    os.remove(tempname)

                with open(tempname, 'wb') as fp:
                    async for chunk in response.content.iter_any():
                        fp.write(chunk)
                        if ty != 'subtitle':
                            progress.update(taskId, advance=len(chunk))
                            overall.update(taskOId, advance=len(chunk))

                st.append(uri)
                with open(STATFILE, 'w') as fp:
                    fp.write(str(st))

    if os.path.exists(STATFILE):
        with open(STATFILE, 'r') as fp:
            st = list(fp.read())

    progress = Progress(
        TextColumn("        "),
        TextColumn("[bold blue]Downloading"),
        BarColumn(),
        "[progress.percentage]{task.percentage:>3.2f}%",
        DownloadColumn(),
        TransferSpeedColumn(),
        "eta", TimeRemainingColumn()
    )

    with progress:
        oTotal = 0
        for item in data:
            if item['type'] != 'subtitle':
                oTotal += item["size"]

        taskId = progress.add_task("", start=False)
        taskOId = progress.add_task("", total=oTotal)

        for item in data:
            if item['type'] != 'subtitle':
                progress.update(taskId, total=item["size"])
                progress.reset(taskId)
                progress.start_task(taskId)

            loop = asyncio.get_event_loop()
            tasks = [get_bytes(uri, item['type'], ssl, progress, progress) for uri in item['uri'] if not uri in st]
            loop.run_until_complete(asyncio.gather(*tasks))

def appendFiles(data: list):
    def checkExist(files):
        for file in files:
            file_ = os.path.join(TEMPDIR, file)
            if not os.path.exists(file_):
                logger.warning(f'"{file}" segment is missing!')
                logger.error("Output will be damaged. So, exiting...", 1)

    def append_file(apd, out):
        apd = os.path.join(TEMPDIR, apd)
        with open(apd, 'rb') as afp:
            content = afp.read()
            with open(out, 'ab') as ofp:
                ofp.write(content)

    cmd = ['MP4Box', '-itags', 'tool=']

    for item in data:
        outfile = os.path.basename(item['uri'][0])
        checkExist([outfile])
        outfile = os.path.join(TEMPDIR, outfile)

        if len(item['uri']) > 1:
            apdfile = [os.path.basename(apd) for apd in item['uri'][1:]]
            checkExist(apdfile)

            for apd in apdfile:
                append_file(apd, outfile)

        if item['type'] == 'video':
            cmd += ['-add', f'{outfile}#video:name=:lang=und:group=1']

        elif item['type'] == 'audio':

            nm = item["name"]
            if item['isAD']:
                nm = f'{nm.strip()} [AD]'

            cmd += ['-add', f'{outfile}#audio:name={nm}:lang={item["language"]}:group=2']

        elif item['type'] == 'subtitle':
            __cmd = ['ffmpeg', '-hide_banner', '-i', outfile]

            outfile = os.path.basename(outfile)
            outfile = os.path.splitext(outfile)[0] + '.srt'
            outfile = os.path.join(TEMPDIR, outfile)

            __cmd += [outfile]

            retCode = subprocess.Popen(
                __cmd,
                stdin=subprocess.PIPE,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.STDOUT
            ).wait()
            
            if retCode == 0:
                
                nm = item["name"]
                if item['isSDH']:
                    nm = f'{nm.strip()} [SDH]'

                cmd += ['-add', f'{outfile}:name={nm}:lang={item["language"]}:group=3']

    cmd += ['-new', os.path.join(TEMPDIR, 'output.mp4')]

    logger.info("Muxing streams...")
    returnCode = subprocess.Popen(
        cmd,
        stdin=subprocess.PIPE,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.STDOUT
    ).wait()

    if returnCode != 0:
        logger.error("Unable to handle the muxing!", 1)