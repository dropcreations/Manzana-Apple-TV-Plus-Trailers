import os
import json
import m3u8

from utils import logger

def hls(url):
    data = m3u8.load(url)
    data = json.loads(
        json.dumps(
            data.data
        )
    )

    __video = []
    __audio = []
    __subtitle = []

    logger.info("Getting hls streams list...")

    for video in data["playlists"]:
        codec = video["stream_info"]["codecs"]
        videorange = video["stream_info"]["video_range"]

        if "PQ" in videorange: videorange = "HDR"
        if "avc" in codec: codec = "AVC"
        elif "hvc" in codec: codec = "HEVC"
        elif "dvh" in codec:
            codec = "HEVC"
            videorange = "Dolby Vision"

        __info = {
            "type": "video",
            "range": videorange,
            "fps": video["stream_info"]["frame_rate"],
            "codec": codec,
            "resolution": video["stream_info"]["resolution"],
            "bitrate": f'{round((video["stream_info"]["average_bandwidth"])/1000000, 2)} Mb/s'
        }

        if len(__video) > 0:
            __check = __video[-1]

            if __check["codec"] == __info["codec"]:
                if __check["resolution"] == __info["resolution"]:
                    if __check["range"] == __info["range"]:
                        if __check["bitrate"] == __info["bitrate"]:
                            del __video[-1]
    
        __info["uri"] = video["uri"]
        __video.append(__info)

    for stream in data["media"]:
        if stream["type"] == "AUDIO":
            if "characteristics" in stream:
                if "original-content" in stream["characteristics"]: isOriginal = True
                else: isOriginal = False
                if "accessibility" in stream["characteristics"]: isAD = True
                else: isAD = False
            else:
                isOriginal = False
                isAD = False

            __uri = stream["uri"]

            groupId = stream["group_id"]
            groupId = groupId.split("_")[0]

            if "atmos" in groupId: codec = "Atmos"
            elif "ac3" in groupId: codec = "AC-3"
            elif "stereo" in groupId:
                if "HE" in groupId: codec = "HE-AAC"
                else: codec = "AAC"

            __info = {
                "type": "audio",
                "name": stream["name"],
                "language": stream["language"],
                "isAD": isAD,
                "isOriginal": isOriginal,
                "channels": stream["channels"],
                "codec": codec
            }

            __assetname = os.path.splitext(
                os.path.basename(
                    __uri
                )
            )[0].split("_")

            bitrate = "None"

            for _ in __assetname:
                if _ == "gr32":
                    bitrate = "32kb/s"
                    break
                if _ == "gr64":
                    bitrate = "64kb/s"
                    break
                if _ == "gr160":
                    bitrate = "160kb/s"
                    break
                if _ == "gr384":
                    bitrate = "384kb/s"
                    break
                if _ == "gr2448":
                    bitrate = "488kb/s"
                    break

            __info["bitrate"] = bitrate

            if len(__audio) > 0:
                __check = __audio[-1]

                if __check["codec"] == __info["codec"]:
                    if __check["channels"] == __info["channels"]:
                        if __check["language"] == __info["language"]:
                            if __check["bitrate"] == __info["bitrate"]:
                                del __audio[-1]
        
            __info["uri"] = __uri
            __audio.append(__info)

        elif stream["type"] == "SUBTITLES":

            isSDH = False

            if "characteristics" in stream:
                if "accessibility" in stream["characteristics"]:
                    isSDH = True

            __info = {
                "type": "subtitle",
                "name": stream["name"],
                "language": stream["language"],
                "isForced": True if stream["forced"] == "YES" else False,
                "isSDH": isSDH
            }

            if len(__subtitle) > 0:
                __check = __subtitle[-1]

                if __check["language"] == __info["language"]:
                    if __check["isForced"] == __info["isForced"]:
                        del __subtitle[-1]

            __info["uri"] = stream["uri"]
            __subtitle.append(__info)

    return {
        "videos": __video,
        "audios": __audio,
        "subtitles": __subtitle
    }