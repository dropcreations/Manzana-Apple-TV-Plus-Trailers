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

def __types(subs: list):
    if subs:
        ids = []
        types = ["Normal"]

        table = Table(box=box.ROUNDED)
        
        table.add_column("ID", justify="center")
        table.add_column("Type", justify="center")

        for sub in subs:
            if sub["isSDH"]:
                if not "SDH" in types:
                    types.append("SDH")
            if sub["isForced"]:
                if not "Forced" in types:
                    types.append("Forced")

        for i, item in enumerate(types):
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
            if id in ids: userWant.append(types[id])
            else: logger.warning(f"ID: {id} is not found in the list!")
        
        if userWant: return userWant
        else: logger.error("No ID has selected to proceed!", 1)
    else:
        logger.warning("No subtitles available!")
        return None

def __streams(data, typeId):
    ids = []
    sorts = []

    for id in typeId:
        if id == "Normal":
            for stream in data["subtitles"]:
                if not stream["isSDH"]:
                    if not stream["isForced"]:
                        sorts.append(stream)
        elif id == "SDH":
            for stream in data["subtitles"]:
                if stream["isSDH"]:
                    if not stream["isForced"]:
                        sorts.append(stream)
        elif id == "Forced":
            for stream in data["subtitles"]:
                if stream["isForced"]:
                    sorts.append(stream)

    table = Table(box=box.ROUNDED)

    table.add_column("ID", justify="center")
    table.add_column("Language", justify="center")
    table.add_column("Forced", justify="center")
    table.add_column("SDH", justify="center")

    for i, stream in enumerate(sorts):
        ids.append(i)
        table.add_row(
            str(i),
            stream["language"],
            "✅" if stream["isForced"] else "❌",
            "✅" if stream["isSDH"] else "❌"
        )

    print()
    columns = Columns(["       ", table])
    console.print(columns)
    id = input("\n\t Enter ID: ")
    print()
    
    if id == "": logger.error("Please enter an ID to continue!", 1)
    elif id.lower() == "all":
        logger.info("Fetching subtitle uris...")

        for i, _ in enumerate(sorts):
            sorts[i]["uri"] = __getUrls(sorts[i]["uri"])
            sorts[i]["file"] = "sub_{}{}{}.srt".format(
                sorts[i]["language"],
                "_sdh" if sorts[i]["isSDH"] else "",
                "_forced" if sorts[i]["isForced"] else ""
            )

        return sorts
    else:
        logger.info("Fetching subtitle uris...")

        __id = id.split(",")
        __id = [int(id.strip()) for id in __id]

    userWant = []

    for id in __id:
        if id in ids:
            sorts[id]["uri"] = __getUrls(sorts[id]["uri"])
            sorts[id]["file"] = "sub_{}{}{}.srt".format(
                sorts[id]["language"],
                "_sdh" if sorts[id]["isSDH"] else "",
                "_forced" if sorts[id]["isForced"] else ""
            )
            userWant.append(sorts[id])
        else: logger.warning(f"ID \"{id}\" is not found in the list!")

    if userWant: return userWant
    else: logger.error("No IDs are selected to proceed!", 1)
    
def subtitle(data):
    logger.info("Getting accessible subtitle types...")
    typeId = __types(data["subtitles"])

    if typeId:
        logger.info("Getting relavant streams for selected type...")
        return __streams(data, typeId)
    else:
        return []