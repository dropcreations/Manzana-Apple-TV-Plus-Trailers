import m3u8
from urllib.parse import urlparse

from utils import logger

def get_hls(url):
    try:
        logger.info("Loading HLS url...")
        data = m3u8.load(url)
    except:
        logger.warning("SSL failed! Trying without SSL...")
        data = m3u8.load(url, verify_ssl=False)

    dataListVideo = []
    dataListAudio = []
    dataListSubs = []

    for v in data.playlists:
        if len(dataListVideo) > 0:
            previousUri = dataListVideo[-1]['uri']
            previousUriPath = urlparse(previousUri).path
            currentUri = v.uri
            currentUriPath = urlparse(currentUri).path

            if previousUriPath == currentUriPath:
                continue

        Codec = v.stream_info.codecs
        VideoRange = v.stream_info.video_range

        if 'PQ' in VideoRange:
            VideoRange = 'HDR'
        if 'avc' in Codec:
            Codec = 'AVC'
        if 'hvc' in Codec:
            Codec = 'HEVC'
        if 'dvh' in Codec:
            Codec = 'HEVC'
            VideoRange = 'DoVi'

        dataListVideo.append(
            {
                'type': 'video',
                'range': VideoRange,
                'fps': v.stream_info.frame_rate,
                'codec': Codec,
                'resolution': v.stream_info.resolution,
                'bitrate': f'{round((v.stream_info.average_bandwidth)/1000000, 2)} Mb/s',
                'uri': v.uri
            }
        )

    for m in data.media:
        if m.type == "AUDIO":
            if len(dataListAudio) > 0:
                previousUri = dataListAudio[-1]['uri']
                previousUriPath = urlparse(previousUri).path
                currentUri = m.uri
                currentUriPath = urlparse(currentUri).path

                if previousUriPath == currentUriPath:
                    continue
                
            isAD = False
            isOriginal = False
            
            c = m.characteristics
            if c:
                if "original-content" in c:
                    isOriginal = True
                if "accessibility" in c:
                    isAD = True

            g = m.group_id
            
            if "atmos" in g:
                Codec = "Atmos"
            elif "ac3" in g:
                Codec = "DD5.1"
            elif "stereo" in g:
                if "HE" in g:
                    Codec = "HE-AAC"
                else: Codec = "AAC"

            b = "Null"

            if "gr32" in m.uri:
                b = '32 Kb/s'
            elif "gr64" in m.uri:
                b = '64 Kb/s'
            elif "gr160" in m.uri:
                b = '160 Kb/s'
            elif "gr384" in m.uri:
                b = '384 Kb/s'
            elif "gr2448" in m.uri:
                b = '488 Kb/s'

            dataListAudio.append(
                {
                    'type': 'audio',
                    'name': m.name,
                    'language': m.language,
                    'isAD': isAD,
                    'isOriginal': isOriginal,
                    'channels': m.channels,
                    'codec': Codec,
                    'bitrate': b,
                    'uri': m.uri
                }
            )

        elif m.type == "SUBTITLES":
            if len(dataListSubs) > 0:
                previousUri = dataListSubs[-1]['uri']
                previousUriPath = urlparse(previousUri).path
                currentUri = m.uri
                currentUriPath = urlparse(currentUri).path

                if previousUriPath == currentUriPath:
                    continue

            isSDH = False

            c = m.characteristics
            if c:
                if "accessibility" in c:
                    isSDH = True

            dataListSubs.append(
                {
                    'type': 'subtitle',
                    'name': m.name,
                    'language': m.language,
                    'isForced': True if m.forced == "YES" else False,
                    'isSDH': isSDH,
                    'uri': m.uri
                }
            )

    return {
        "video": dataListVideo,
        "audio": dataListAudio,
        "subtitle": dataListSubs
    }