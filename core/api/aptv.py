import json
import requests
import datetime
import warnings

from bs4 import BeautifulSoup
from urllib.parse import unquote
from urllib.parse import urlparse

from utils import logger

warnings.filterwarnings("ignore")

HEADERS = {
    "content-type": "application/json",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "en-US,en;q=0.9",
    "origin": "https://tv.apple.com",
    "referer": "https://tv.apple.com/",
    "user-agent": "AppleTV6,2/11.1"
}

class AppleTVPlus:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers = HEADERS
        self.__get_access_token()

    def __get_access_token(self):
        logger.info("Fetching access-token from web...")
        
        try:
            r = requests.get("https://tv.apple.com/us")
        except:
            logger.warning("SSL failed! Trying without SSL...")
            r = requests.get("https://tv.apple.com/us", verify=False)

        if r.status_code != 200:
            logger.error("Failed to get https://tv.apple.com/. Try-again...", 1)

        c = BeautifulSoup(r.text, "html.parser")
        m = c.find(
            "meta",
            attrs={
                'name': 'web-tv-app/config/environment',
                'content': True
            }
        )

        accessToken = json.loads(unquote(m.get("content")))
        accessToken = accessToken["MEDIA_API"]["token"]
        self.session.headers.update(
            {'authorization': f'Bearer {accessToken}'}
        )

    def __get_url(self, url):
        logger.info("Checking and parsing url...")

        def check(url):
            try:
                try:
                    r = requests.get(url)
                except:
                    logger.warning("SSL failed! Trying without SSL...")
                    r = requests.get(url, verify=False)
                
                if r.status_code == 200:
                    return True
            except:
                return False
            
        u = urlparse(url)
        
        if not u.scheme:
            url = f"https://{url}"
        
        if u.netloc == "tv.apple.com":
            if check(url):
                s = u.path.split('/')

                self.id = s[-1]
                self.kind = s[2]

                if self.kind in ["episode", "season"]:
                    self.kind = "show"

                    if "showId" in u.query:
                        self.id = u.query.replace('showId=', '')
                    else:
                        logger.error("Unable to parse showId from URL!", 1)
            else: logger.error("URL is invalid! Please check the URL!", 1)
        else: logger.error("URL is invalid! Host should be tv.apple.com!", 1)

    def __get_json(self):
        logger.info("Fetching API response...")

        apiUrl = f"https://tv.apple.com/api/uts/v3/{self.kind}s/{self.id}"
        params = {
            "caller": "web",
            "locale": "en-US",
            "pfm": "appletv",
            "sf": "143441",
            "utscf": "OjAAAAAAAAA~",
            "utsk": "6e3013c6d6fae3c2::::::235656c069bb0efb",
            "v": "68"
        }
        
        try:
            r = requests.get(url=apiUrl, params=params)
        except:
            logger.warning("SSL failed! Trying without SSL...")
            r = requests.get(url=apiUrl, params=params, verify=False)

        return json.loads(r.text)
    
    def __get_default(self):
        def genres(genre):
            if not isinstance(genre, list): genre = [genre]
            return [g["name"] for g in genre]
        
        def fixdate(date):
            return datetime.datetime.utcfromtimestamp(date/1000.0).strftime('%Y-%m-%d')

        data = self.__get_json()

        try:
            coverImage = data["data"]["content"]["backgroundVideo"]["images"]["contentImage"]["url"].format(
                w=data["data"]["content"]["backgroundVideo"]["images"]["contentImage"]["width"],
                h=data["data"]["content"]["backgroundVideo"]["images"]["contentImage"]["height"],
                f="jpg"
            )
        except:
            coverImage = None

        return {
            "hlsUrl": data["data"]["content"]["backgroundVideo"]["assets"]["hlsUrl"],
            "cover": coverImage,
            "videoTitle": data["data"]["content"]["backgroundVideo"]["title"],
            "title": data["data"]["content"]["title"],
            "releaseDate": fixdate(data["data"]["content"]["releaseDate"]),
            "description": data["data"]["content"]["description"],
            "genres": genres(data["data"]["content"]["genres"])
        }
    
    def __get_trailers(self):
        def genres(genre):
            if not isinstance(genre, list): genre = [genre]
            return [g["name"] for g in genre]
        
        def fixdate(date):
            return datetime.datetime.utcfromtimestamp(date/1000.0).strftime('%Y-%m-%d')
        
        data = self.__get_json()

        backgroundVideos = next(
            (shelve["items"] for shelve in data["data"]["canvas"]["shelves"] if shelve.get("title") == "Trailers"), None)
        
        dataList = []

        if backgroundVideos:
            for item in backgroundVideos:
                try:
                    coverImage = item["playables"][0]["canonicalMetadata"]["images"]["contentImage"]["url"].format(
                        w=item["playables"][0]["canonicalMetadata"]["images"]["contentImage"]["width"],
                        h=item["playables"][0]["canonicalMetadata"]["images"]["contentImage"]["height"],
                        f="jpg"
                    )
                except:
                    coverImage = None

                dataList.append(
                    {
                        "hlsUrl": item["playables"][0]["assets"]["hlsUrl"],
                        "cover": coverImage,
                        "videoTitle": item["playables"][0]["title"],
                        "title": data["data"]["content"]["title"],
                        "releaseDate": fixdate(data["data"]["content"]["releaseDate"]),
                        "description": data["data"]["content"]["description"],
                        "genres": genres(data["data"]["content"]["genres"])
                    }
                )
            
            return dataList
        else:
            return [self.__get_default()]
    
    def get_info(self, url, default):
        self.__get_url(url)

        if default:
            return [self.__get_default()]
        else:
            return self.__get_trailers()