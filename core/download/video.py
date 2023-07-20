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

def video(data):
    logger.info("Getting video streams...")

    ids = []
    table = Table(box=box.ROUNDED)

    table.add_column("ID", justify="center")
    table.add_column("Codec", justify="left")
    table.add_column("Bitrate", justify="left")
    table.add_column("Resolution", justify="left")
    table.add_column("FPS", justify="center")
    table.add_column("Range", justify="center")

    for i, stream in enumerate(data["videos"]):
        ids.append(i)
        table.add_row(
            str(i),
            stream["codec"],
            stream["bitrate"],
            stream["resolution"],
            str(stream["fps"]),
            stream["range"]
        )

    print()

    columns = Columns(["       ", table])
    console.print(columns)
    id = input("\n\t Enter ID: ")

    print()
    
    if id == "": logger.error("Please enter an ID to continue!", 1)
    else:
        try: id = int(id)
        except ValueError: logger.error("Unable to use multiple IDs!", 1)

    if id in ids:
        logger.info("Fetching video uri...")

        videorange = data["videos"][id]["range"]
        if videorange == "Dolby Vision": videorange = "dolby_vision"
        
        data["videos"][id]["uri"] = __getUrls(data["videos"][id]["uri"])
        data["videos"][id]["file"] = "video{}{}{}.mp4".format(
            "_" + data["videos"][id]["codec"].lower(),
            "_" + videorange.lower(),
            "_" + data["videos"][id]["resolution"]
        )

        return [data["videos"][id]]
    else: logger.error("ID not found in the list!", 1)