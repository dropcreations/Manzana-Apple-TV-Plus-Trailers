import os
import argparse

from rich.console import Console
from rich.traceback import install

from handler import arguments

install()
console = Console()

LOGO = r"""


        [bright_white bold]$$$$$$\$$$$\   $$$$$$\  $$$$$$$\  $$$$$$$$\ $$$$$$\  $$$$$$$\   $$$$$$\  
        $$  _$$  _$$\  \____$$\ $$  __$$\ \____$$  |\____$$\ $$  __$$\  \____$$\ 
        $$ / $$ / $$ | $$$$$$$ |$$ |  $$ |  $$$$ _/ $$$$$$$ |$$ |  $$ | $$$$$$$ |
        $$ | $$ | $$ |$$  __$$ |$$ |  $$ | $$  _/  $$  __$$ |$$ |  $$ |$$  __$$ |
        $$ | $$ | $$ |\$$$$$$$ |$$ |  $$ |$$$$$$$$\\$$$$$$$ |$$ |  $$ |\$$$$$$$ |
        \__| \__| \__| \_______|\__|  \__|\________|\_______|\__|  \__| \_______|

                            ──── Apple TV Plus Trailers ────[/]


"""

def main():
    parser = argparse.ArgumentParser(
        description="Manzana: Apple TV Plus Trailers Downloader"
    )
    parser.add_argument(
        '-v',
        '--version',
        version="Manzana: Apple TV Plus Trailers v1.0.1",
        action="version"
    )
    parser.add_argument(
        '-an',
        '--no-audio',
        help="Don't download audio streams. (default: False)",
        action="store_true"
    )
    parser.add_argument(
        '-sn',
        '--no-subs',
        help="Don't download subtitle streams. (default: False)",
        action="store_true"
    )
    parser.add_argument(
        'url',
        help="Apple TV Plus URL for a movie",
        type=str
    )
    args = parser.parse_args()
    arguments(args)

if __name__ == "__main__":
    os.system('cls' if os.name == 'nt' else 'clear')
    console.print(LOGO)
    main()
