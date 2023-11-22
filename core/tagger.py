import requests
from mutagen.mp4 import MP4, MP4Cover

def tagFile(data: dict, file):
    tags = MP4(file)
    tags.delete()

    __tags = {
        "\xa9alb": data.get("title"),
        "\xa9nam": data.get("videoTitle"),
        "\xa9gen": data.get("genres"),
        "\xa9day": data.get("releaseDate"),
        "desc": data.get("description")
    }

    for key, value in __tags.items():
        if value:
            if not isinstance(value, list):
                value = [value]
            tags[key] = value

    if data.get("cover"):
        try: cover = requests.get(data.get("cover"), stream=True).content
        except: cover = requests.get(data.get("cover"), stream=True, verify=False).content
        tags["covr"] = [MP4Cover(cover, MP4Cover.FORMAT_JPEG)]
    
    tags.save()