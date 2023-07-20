import os
import re
import sys
import shutil
import requests

from api import hls
from core import video
from core import audio
from core import subtitle
from core import download
from core import ffmpeg
from api import AppleTVPlus
from utils import logger

def __getPath():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    else:
        return os.path.dirname(os.path.abspath(__file__))

def __removeTags(quote: str):
    quote = quote.replace("\n", "")
    tags = re.compile('<.*?>')
    return re.sub(tags, '', quote)

def arguments(args):
    if not shutil.which("ffmpeg"):
        logger.error("Unable to find \"ffmpeg\" in PATH!", 1)

    TEMP = os.path.join(
        __getPath(),
        "temp"
    )
    os.makedirs(TEMP, exist_ok=True)

    api_data = AppleTVPlus().getInfo(args.url)
    hls_data = hls(api_data["hlsUrl"])

    userAudio = []
    userSubtitle = []

    userVideo = video(hls_data)

    if not args.no_audio: userAudio = audio(hls_data)
    if not args.no_subs: userSubtitle = subtitle(hls_data)

    userRequest = userVideo + userAudio + userSubtitle

    for item in userRequest:
        if item["type"] == "video":
            download(
                item["uri"],
                TEMP,
                item["file"],
                "Downloading {} ({}) video stream...".format(
                    item["resolution"],
                    item["range"]
                )
            )

        elif item["type"] == "audio":
            download(
                item["uri"],
                TEMP,
                item["file"],
                "Downloading \"{}\" {} audio stream...".format(
                    item["name"].strip(),
                    item["codec"]
                )
            )

        elif item["type"] == "subtitle":
            logger.info(
                'Downloading "{}"{} subtitle stream...'.format(
                    item["name"].strip(),
                    " (SDH)" if item["isSDH"] else ""
                )
            )

            __id = ""
            __sub = []

            for sub in item["uri"]:
                subTemp = os.path.join(
                    TEMP,
                    "sub_temp.txt"
                )

                res = requests.get(sub).content

                with open(subTemp, "wb") as sub_temp: sub_temp.write(res)
                with open(subTemp, "r", encoding="utf-8") as sub_temp: subs = sub_temp.read()

                lines = subs.split("\n\n")

                for subSet in lines:
                    subSet = subSet.split("\n")

                    if subSet[0].isdigit():
                        if subSet[0] != __id:
                            __id = subSet[0]
                            _sub = ""

                            for line in subSet:
                                line = __removeTags(line)
                                lineTs = re.search(
                                    r"\d{2}:\d{2}:\d{2}\.\d{3}\s*-->\s*\d{2}:\d{2}:\d{2}\.\d{3}",
                                    line
                                )

                                if lineTs:
                                    line = lineTs.group(0)

                                _sub += f"{line}\n"
                            __sub.append(_sub)

            subSave = os.path.join(
                TEMP,
                item["file"]
            )

            with open(subSave, "w+", encoding="utf-8") as s:
                s.write('\n'.join(__sub))
            os.remove(subTemp)

    logger.info("Muxing streams...")
    ret = ffmpeg(
        userRequest, 
        os.path.abspath(
            api_data["file"]
        )
    )
    if ret != 0: logger.error("Muxing failed!", 1)

    logger.info("Cleaning temp...")
    for temp in os.listdir(TEMP):
        try:
            os.remove(
                os.path.join(
                    TEMP,
                    temp
                )
            )
        except PermissionError:
            logger.warning(f"Unable to remove '{temp}' temp! Remove it manually...")
    try:
        os.removedirs(TEMP)
    except OSError:
        logger.warning("Unable to remove 'temp' dir! Remove it manually...")

    logger.info("Done.")