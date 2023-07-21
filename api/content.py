import datetime
from sanitize_filename import sanitize

def __date(date: int):
    return datetime.datetime.utcfromtimestamp(
        date / 1000.0
    ).strftime('%Y-%m-%d')

def content(info):
    __info = {}
    
    content = info["data"]["content"]

    if "backgroundVideo" in content:
        __info["hlsUrl"] = content["backgroundVideo"]["assets"]["hlsUrl"]

        if "images" in content["backgroundVideo"]:
            if "contentImage" in content["backgroundVideo"]["images"]:
                __info["coverUrl"] = content["backgroundVideo"]["images"]["contentImage"]["url"].format(
                    w=content["backgroundVideo"]["images"]["contentImage"]["width"],
                    h=content["backgroundVideo"]["images"]["contentImage"]["height"],
                    f="jpg"
                )

    if "countriesOfOrigin" in content:
        originCountry = content["countriesOfOrigin"]

        if not isinstance(originCountry, list):
            originCountry = [originCountry]

        __country = []

        for country in originCountry:
            __country.append(country["displayName"])

        __info["originCountry"] = __country

    if "description" in content:
        __info["description"] = content["description"]

    if "genres" in content:
        __genre = []

        for genre in content["genres"]:
            __genre.append(genre["name"])

        __info["genre"] = __genre

    if "originalSpokenLanguages" in content:
        __lang = []

        for lang in content["originalSpokenLanguages"]:
            __lang.append(lang["displayName"])

        __info["language"] = __lang

    if "rating" in content:
        __info["rating"] = content["rating"]["displayName"]

    if "releaseDate" in content:
        __info["releaseDate"] = __date(content["releaseDate"])

    if "rolesSummary" in content:
        if "cast" in content["rolesSummary"]:
            __info["cast"] = content["rolesSummary"]["cast"]
        if "directors" in content["rolesSummary"]:
            __info["director"] = content["rolesSummary"]["directors"]

    __info["name"] = content["title"]

    contentType = content["type"]
    if contentType.lower() == "movie":
        __info["file"] = sanitize(
            "{0} ({1}) [Movie] [AppleTVPlus] [Trailer].mkv".format(
                __info["name"],
                __info["releaseDate"][0:4]
            )
        )
    elif contentType.lower() == "show":
        __info["file"] = sanitize(
            "{0} ({1}) [TVShow] [AppleTVPlus] [Trailer].mkv".format(
                __info["name"],
                __info["releaseDate"][0:4]
            )
        )

    return __info

