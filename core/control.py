import os
import sys
import shutil
from rich.console import Console

from core.api import AppleTVPlus
from core.api import get_hls
from core.user import get_select
from core.user import user_video
from core.user import user_audio
from core.user import user_subs
from core.parse import parse_uri
from core.process import download
from core.process import appendFiles
from core.tagger import tagFile

from utils import logger, sanitize

cons = Console()

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
OUTPUTDIR = os.path.join(__get_path(),'output')

if not os.path.exists(TEMPDIR):
    os.makedirs(TEMPDIR)

if not os.path.exists(OUTPUTDIR):
    os.makedirs(OUTPUTDIR)

def run(args):
    if not shutil.which("ffmpeg"):
        logger.warning("Unable to find \"FFmpeg\" in PATH!", 1)
        
    if not shutil.which("MP4Box"):
        logger.warning("Unable to find \"MP4Box\" in PATH!", 1)

    try:
        atvp = AppleTVPlus()
        data = atvp.get_info(args.url, args.default)
        data = get_select(data)

        for item in data:
            op = os.path.join(OUTPUTDIR, '{} - {} ({}) Trailer [WEB-DL] [ATVP].mp4'.format(
                sanitize(item['title']),
                sanitize(item['videoTitle']),
                item['releaseDate'][0:4]
            ))

            if not os.path.exists(op):
                dataHLS = get_hls(item["hlsUrl"])

                print()
                cons.print(f'\tContent: [i bold purple]{item["videoTitle"]}[/]')
                print()

                userVideo = user_video(dataHLS["video"])
                if not args.noAudio:
                    userAudio = user_audio(dataHLS["audio"])
                else: userAudio = []
                if not args.noSubs:
                    userSubs = user_subs(dataHLS["subtitle"])
                else: userSubs = []

                logger.info("Fetching m3u8...")

                userReq = userVideo + userAudio + userSubs
                try: parse_uri(userReq)
                except: parse_uri(userReq, ssl=False)

                logger.info("Downloading segments...")
                
                print()
                try: download(userReq)
                except: download(userReq, ssl=False)
                print()

                logger.info("Appending segments...")

                appendFiles(userReq)

                logger.info("Saving output...")
                shutil.move(os.path.join(TEMPDIR, 'output.mp4'), op)

                logger.info("Tagging...")
                tagFile(item, op)
            else:
                logger.info(f'"{item["videoTitle"]}" is already exists! Skipping...')

            print('-' * 30)

        logger.info("Cleaning temp...")
        for temp in os.listdir(TEMPDIR):
            try:
                os.remove(os.path.join(TEMPDIR, temp))
            except PermissionError:
                logger.error(f"Unable to remove '{temp}' temp! Remove it manually...")
        try:
            os.removedirs(TEMPDIR)
        except OSError:
            logger.error("Unable to remove 'temp' dir! Remove it manually...")

        logger.info("Done.")
    except KeyboardInterrupt:
        print()
        logger.error("Interrupted by user.")