from rich import box
from rich.table import Table
from rich.console import Console
from rich.columns import Columns

from utils import logger

cons = Console()

def user_video(data):
    def get_codec(data):
        codecs = list(set([c["range"] for c in data]))

        ids = []
        table = Table(box=box.ROUNDED)

        table.add_column("ID", justify="center")
        table.add_column("Codec", justify="left")

        logger.info("Fetching video ranges...")

        for i, c in enumerate(codecs):
            ids.append(i)
            table.add_row(str(i), c)

        print()
        columns = Columns(["       ", table])
        cons.print(columns)
        id = input("\n\t Enter ID: ")
        print()

        if id == "":
            logger.error("Please enter an ID to continue...", 1)
        elif id in ["all", "a"]:
            return codecs
        else:
            try:
                return [codecs[int(i)] for i in id.split(' ')]
            except (ValueError, IndexError):
                logger.error("Unable to process ID(s)...", 1)

    userWant = []
    userWantCodec = get_codec(data)

    for c in data:
        if c["range"] in userWantCodec:
            userWant.append(c)

    ids = []
    table = Table(box=box.ROUNDED)

    table.add_column("ID", justify="center")
    table.add_column("Codec", justify="left")
    table.add_column("Bitrate", justify="left")
    table.add_column("Resolution", justify="left")
    table.add_column("FPS", justify="center")
    table.add_column("Range", justify="left")

    logger.info("Fetching video streams...")

    for i, c in enumerate(userWant):
        ids.append(i)
        table.add_row(
            str(i),
            c["codec"],
            c["bitrate"],
            f'{c["resolution"][0]}x{c["resolution"][1]}',
            str(c["fps"]),
            c["range"]
        )

    print()
    columns = Columns(["       ", table])
    cons.print(columns)
    id = input("\n\t Enter ID: ")
    print()

    if id == "":
        logger.error("Please enter an ID to continue...", 1)
    else:
        try:
            return [userWant[int(id)]]
        except (ValueError, IndexError):
            logger.error("Unable to process ID(s)...", 1)

def user_audio(data):
    def get_codec(data):
        codecs = list(set([c["codec"] for c in data]))

        ids = []
        table = Table(box=box.ROUNDED)

        table.add_column("ID", justify="center")
        table.add_column("Codec", justify="left")

        logger.info("Fetching audio codecs...")

        for i, c in enumerate(codecs):
            ids.append(i)
            table.add_row(str(i), c)

        print()
        columns = Columns(["       ", table])
        cons.print(columns)
        id = input("\n\t Enter ID: ")
        print()

        if id == "":
            logger.error("Please enter an ID to continue...", 1)
        elif id in ["all", "a"]:
            return codecs
        else:
            try:
                return [codecs[int(i)] for i in id.split(' ')]
            except (ValueError, IndexError):
                logger.error("Unable to process ID(s)...", 1)

    userWant = []
    userWantCodec = get_codec(data)

    for c in data:
        if c["codec"] in userWantCodec:
            userWant.append(c)

    ids = []
    table = Table(box=box.ROUNDED)

    table.add_column("ID", justify="center")
    table.add_column("Codec", justify="left")
    table.add_column("Bitrate", justify="center")
    table.add_column("Channels", justify="center")
    table.add_column("Language", justify="center")
    table.add_column("OG", justify="left")
    table.add_column("AD", justify="left")

    logger.info("Fetching audio streams...")

    for i, c in enumerate(userWant):
        ids.append(i)
        table.add_row(
            str(i),
            c["codec"],
            c["bitrate"],
            c["channels"],
            c["language"],
            "[green bold]YES[/]" if c["isOriginal"] else "[red bold]NO[/]",
            "[green bold]YES[/]" if c["isAD"] else "[red bold]NO[/]"
        )

    print()
    columns = Columns(["       ", table])
    cons.print(columns)
    id = input("\n\t Enter ID: ")
    print()

    if id == "":
        logger.error("Please enter an ID to continue...", 1)
    elif id in ["all", "a"]:
        return userWant
    else:
        try:
            return [userWant[int(i)] for i in id.split(' ')]
        except (ValueError, IndexError):
            logger.error("Unable to process ID(s)...", 1)

def user_subs(data):
    def get_codec(data):
        normalSubs = []
        forcedSubs = []
        sdhSubs = []
        subs = []

        for c in data:
            if c["isForced"]: forcedSubs.append(c)
            if c["isSDH"]: sdhSubs.append(c)
            if not c["isForced"]:
                if not c["isSDH"]:
                    normalSubs.append(c)

        ids = []
        table = Table(box=box.ROUNDED)

        table.add_column("ID", justify="center")
        table.add_column("Type", justify="left")

        logger.info("Fetching subtitle types...")

        if len(normalSubs) > 0: subs.append("Normal")
        if len(forcedSubs) > 0: subs.append("Forced")
        if len(sdhSubs) > 0: subs.append("SDH")

        for i, c in enumerate(subs):
            ids.append(i)
            table.add_row(str(i), c)

        print()
        columns = Columns(["       ", table])
        cons.print(columns)
        id = input("\n\t Enter ID: ")
        print()

        if id == "":
            logger.error("Please enter an ID to continue...", 1)
        elif id in ["all", "a"]:
            return subs
        else:
            try:
                return [subs[int(i)] for i in id.split(' ')]
            except (ValueError, IndexError):
                logger.error("Unable to process ID(s)...", 1)

    if len(data) > 0:
        userWant = []
        userWantCodec = get_codec(data)

        for c in data:
            if "Normal" in userWantCodec:
                if not c["isForced"]:
                    if not c["isSDH"]:
                        userWant.append(c)
            if "Forced" in userWantCodec:
                if c["isForced"]:
                    userWant.append(c)
            if "SDH" in userWantCodec:
                if c["isSDH"]:
                    userWant.append(c)

        ids = []
        table = Table(box=box.ROUNDED)

        table.add_column("ID", justify="center")
        table.add_column("Language", justify="center")
        table.add_column("Forced", justify="center")
        table.add_column("SDH", justify="center")

        logger.info("Fetching subtitle streams...")

        for i, c in enumerate(userWant):
            ids.append(i)
            table.add_row(
                str(i),
                c["language"],
                "[green bold]YES[/]" if c["isForced"] else "[red bold]NO[/]",
                "[green bold]YES[/]" if c["isSDH"] else "[red bold]NO[/]"
            )

        print()
        columns = Columns(["       ", table])
        cons.print(columns)
        id = input("\n\t Enter ID: ")
        print()

        if id == "":
            logger.error("Please enter an ID to continue...", 1)
        elif id in ["all", "a"]:
            return userWant
        else:
            try:
                return [userWant[int(i)] for i in id.split(' ')]
            except (ValueError, IndexError):
                logger.error("Unable to process ID(s)...", 1)
    else:
        logger.info("No subtitles available!")
        return []