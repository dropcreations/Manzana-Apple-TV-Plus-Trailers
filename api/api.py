import re
import json
import requests

from urllib.parse import unquote
from urllib.parse import urlparse
from urllib.request import urlopen
from urllib.error import URLError, HTTPError

from utils import logger
from api.movie import movie

HEADERS = {
    "content-type": "application/json",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "en-US,en;q=0.9",
    "origin": "https://tv.apple.com",
    "referer": "https://tv.apple.com/",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
}

class AppleTVPlus(object):
    def __init__(self):
        self.session = requests.Session()
        self.session.headers = HEADERS
        self.__accessToken()

    def __checkUrl(self, url):
        try:
            urlopen(url)
            return True
        except (URLError, HTTPError):
            return False

    def __getUrl(self, url):
        __url = urlparse(url)

        if not __url.scheme:
            url = f"https://{url}"

        if __url.netloc == "tv.apple.com":
            if self.__checkUrl(url):
                splits = __url.path.split('/')

                self.id = splits[-1]
                self.kind = splits[2]

            else: logger.error("URL is invalid!", 1)
        else: logger.error("URL is invalid!", 1)
        
    def __accessToken(self):
        logger.info("Fetching access token from web...")

        response = requests.get("https://tv.apple.com/us/")
        if response.status_code != 200:
            logger.error("Failed to get tv.apple.com! Please re-try...", 1)

        response = response.text.replace('\r\n', '')
        response = response.replace('\n', '')
        response = response.replace('\r', '')
        response = response.replace('\t', '')
        response = response.replace('  ', '')

        configJson = re.search('(<meta name="web-tv-app/config/environment" content=")(.*)("><!-- EMBER_CLI_FASTBOOT_TITLE --)', response).group(2)
        accessToken = json.loads(unquote(configJson))["MEDIA_API"]["token"]
        
        self.session.headers.update(
            {
                'authorization': f'Bearer {accessToken}'
            }
        )

    def __get_json(self):
        apiUrl = f"https://tv.apple.com/api/uts/v3/{self.kind}s/{self.id}"

        if self.kind == "movie":
            params = {
                "caller": "web",
                "locale": "en-US",
                "pfm": "web",
                "sf": "143441",
                "utscf": "OjAAAAAAAAA~",
                "utsk": "6e3013c6d6fae3c2::::::235656c069bb0efb",
                "v": "68"
            }
        
        response = requests.get(
            url=apiUrl,
            params=params
        )

        return json.loads(response.text)

    def getInfo(self, url):
        self.__getUrl(url)
        
        if self.kind == "movie":
            return movie(self.__get_json())