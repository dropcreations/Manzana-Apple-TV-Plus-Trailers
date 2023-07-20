import os
import requests

from rich import box
from rich.table import Table
from rich.console import Console
from rich.columns import Columns

from utils import logger

console = Console()

def __getUrls(uri):
    __data = requests.get(uri).text
    __baseUri = os.path.dirname(uri)

    urls = []

    for line in __data.split('\n'):
        if line != "":
            if line.startswith("#EXT-X-MAP:URI"):
                urls.append(
                    line.replace(
                        "#EXT-X-MAP:URI=\"", ""
                    ).replace(
                        "\"", ""
                    )
                )
            if not line.startswith("#"):
                urls.append(line)

    return [__baseUri + f"/{url}" for url in urls]

def __codecs(audios: list):
    ids = []
    codecs = []

    table = Table(box=box.ROUNDED)
    table.add_column("ID", justify="center")
    table.add_column("Codec", justify="center")

    for audio in audios:
        codec = audio["codec"]
        if not codec in codecs:
            codecs.append(codec)

    for i, item in enumerate(codecs):
        ids.append(i)
        table.add_row(str(i), item)

    print()

    columns = Columns(["       ", table])
    console.print(columns)
    id = input("\n\t Enter ID: ")

    print()
    
    if id == "": logger.error("Please enter an ID to continue!", 1)
    else:
        __id = id.split(",")
        __id = [int(id.strip()) for id in __id]

    userWant = []

    for id in __id:
        if id in ids: userWant.append(codecs[id])
        else: logger.warning(f"ID: {id} is not found in the list!")
    
    if userWant: return userWant
    else: logger.error("No ID has selected to proceed!", 1)

def __streams(data, codecId):
    ids = []
    sorts = []

    for id in codecId:
        if id == "AAC":
            for stream in data["audios"]:
                if stream["codec"] == "AAC":
                    sorts.append(stream)
        elif id == "HE-AAC":
            for stream in data["audios"]:
                if stream["codec"] == "HE-AAC":
                    sorts.append(stream)
        elif id == "AC-3":
            for stream in data["audios"]:
                if stream["codec"] == "AC-3":
                    sorts.append(stream)
        elif id == "Atmos":
            for stream in data["audios"]:
                if stream["codec"] == "Atmos":
                    sorts.append(stream)
    
    table = Table(box=box.ROUNDED)

    table.add_column("ID", justify="center")
    table.add_column("Codec", justify="center")
    table.add_column("Bitrate", justify="center")
    table.add_column("Channels", justify="center")
    table.add_column("Language", justify="center")
    table.add_column("Original", justify="center")
    table.add_column("AD", justify="center")

    for i, stream in enumerate(sorts):
        ids.append(i)
        table.add_row(
            str(i),
            stream["codec"],
            stream["bitrate"],
            stream["channels"],
            stream["language"],
            "✅" if stream["isOriginal"] else "❌",
            "✅" if stream["isAD"] else "❌"
        )

    print()

    columns = Columns(["       ", table])
    console.print(columns)
    id = input("\n\t Enter ID: ")

    print()
    
    if id == "": logger.error("Please enter an ID to continue!", 1)
    elif id.lower() == "all":
        logger.info("Fetching audio uris...")

        for i, _ in enumerate(sorts):
            sorts[i]["uri"] = __getUrls(sorts[i]["uri"])
            sorts[i]["file"] = "audio{}{}{}.mp4".format(
                "_" + sorts[i]["language"],
                "_ad" if sorts[i]["isAD"] else "",
                "_" + sorts[i]["codec"].lower()
            )

        return sorts
    else:
        logger.info("Fetching audio uris...")
        
        __id = id.split(",")
        __id = [int(id.strip()) for id in __id]

    userWant = []

    for id in __id:
        if id in ids:
            sorts[id]["uri"] = __getUrls(sorts[id]["uri"])
            sorts[id]["file"] = "audio{}{}{}.mp4".format(
                "_" + sorts[id]["language"],
                "_ad" if sorts[id]["isAD"] else "",
                "_" + sorts[id]["codec"].lower()
            )
            userWant.append(sorts[id])
        else: logger.warning(f"ID \"{id}\" is not found in the list!")

    if userWant: return userWant
    else: logger.error("No IDs are selected to proceed!", 1)

def audio(data):
    logger.info("Getting accessible audio codecs...")
    codecId = __codecs(data["audios"])

    logger.info("Getting relavant streams for selected codec...")
    return __streams(data, codecId)