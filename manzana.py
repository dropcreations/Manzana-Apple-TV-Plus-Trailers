import argparse
from rich.traceback import install
from core import run

install()

VERSION = '2.1.0'
LOGO = r"""


    $$$$$$\$$$$\   $$$$$$\  $$$$$$$\  $$$$$$$$\ $$$$$$\  $$$$$$$\   $$$$$$\  
    $$  _$$  _$$\  \____$$\ $$  __$$\ \____$$  |\____$$\ $$  __$$\  \____$$\ 
    $$ / $$ / $$ | $$$$$$$ |$$ |  $$ |  $$$$ _/ $$$$$$$ |$$ |  $$ | $$$$$$$ |
    $$ | $$ | $$ |$$  __$$ |$$ |  $$ | $$  _/  $$  __$$ |$$ |  $$ |$$  __$$ |
    $$ | $$ | $$ |\$$$$$$$ |$$ |  $$ |$$$$$$$$\\$$$$$$$ |$$ |  $$ |\$$$$$$$ |
    \__| \__| \__| \_______|\__|  \__|\________|\_______|\__|  \__| \_______|

                        ──── Apple TV Plus Trailers ────


"""

def main():
    parser = argparse.ArgumentParser(
        description="Manzana: Apple TV Plus Trailers Downloader"
    )
    parser.add_argument(
        '-v',
        '--version',
        version=f"Manzana: Apple TV Plus Trailers {VERSION}",
        action="version"
    )
    parser.add_argument(
        '-d',
        '--default',
        dest="default",
        help="get only the default content trailer. (default: False)",
        action="store_true"
    )
    parser.add_argument(
        '-an',
        '--no-audio',
        dest="noAudio",
        help="don't download audio streams. (default: False)",
        action="store_true"
    )
    parser.add_argument(
        '-sn',
        '--no-subs',
        dest="noSubs",
        help="don't download subtitle streams. (default: False)",
        action="store_true"
    )
    parser.add_argument(
        'url',
        help="AppleTV+ URL for a movie or a tv-show.",
        type=str
    )
    args = parser.parse_args()
    run(args)

if __name__ == "__main__":
    print(LOGO)
    main()
