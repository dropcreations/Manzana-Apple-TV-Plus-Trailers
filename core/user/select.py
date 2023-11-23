from rich import box
from rich.table import Table
from rich.console import Console
from rich.columns import Columns

from utils import logger

cons = Console()

def get_select(data):
    if len(data) == 1:
        return data
    
    ids = []
    table = Table(box=box.ROUNDED)

    table.add_column("ID", justify="center")
    table.add_column("Content", justify="left")
    table.add_column("Name", justify="left")

    logger.info("Fetching background videos...")

    for i, c in enumerate(data):
        ids.append(i)
        table.add_row(
            str(i),
            c["title"],
            c["videoTitle"]
        )

    print()
    columns = Columns(["       ", table])
    cons.print(columns)
    id = input("\n\t Enter ID: ")
    print()

    if id == "":
        logger.error("Please enter an ID to continue...")
        get_select(data)
    elif id in ["all", "a"]:
        return data
    else:
        try:
            return [data[int(i)] for i in id.split(' ')]
        except (ValueError, IndexError):
            logger.error("Unable to process ID(s)...")
            get_select(data)