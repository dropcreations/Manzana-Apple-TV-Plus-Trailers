import os
import subprocess

def ffmpeg(data: list, output):
    cmd_args = ['ffmpeg', '-y']

    subs = []
    videos = []
    audios = []

    mapArgs = []
    copyArgs = []
    inputArgs = []

    for i, item in enumerate(data):
        inputArgs += ['-i', os.path.join("temp", item["file"])]

        if item["type"] == "video":
            mapArgs += ['-map', f'{i}:v']
        elif item["type"] == "audio":
            mapArgs += ['-map', f'{i}:a']
        elif item["type"] == "subtitle":
            mapArgs += ['-map', f'{i}:s']

    for item in data:
        if item["type"] == "video":
            videos.append(item)
        if item["type"] == "audio":
            audios.append(item)
        elif item["type"] == "subtitle":
            subs.append(item)

    for i, item in enumerate(videos):
        copyArgs += [
            f'-c:v:{i}', 'copy',
            f'-metadata:s:v:{i}', 'title=',
            f'-metadata:s:v:{i}', 'language=und'
        ]
    for i, item in enumerate(audios):
        name = item["name"].strip()
        if item["isAD"]:
            name += " (Audio Description)"

        copyArgs += [
            f'-c:a:{i}', 'copy',
            f'-metadata:s:a:{i}', 'title={}'.format(name),
            f'-metadata:s:a:{i}', 'language={}'.format(item["language"])
        ]
    for i, item in enumerate(subs):
        name = item["name"].strip()
        if item["isSDH"]:
            name += " (SDH)"

        copyArgs += [
            f'-c:s:{i}', 'copy',
            f'-metadata:s:s:{i}', 'title={}'.format(name),
            f'-metadata:s:s:{i}', 'language={}'.format(item["language"])
        ]
        if item["isForced"]:
            copyArgs += [f'-disposition:s:{i}', 'forced']

    cmd = cmd_args + inputArgs + ['-map_metadata', '-1'] + mapArgs + copyArgs + [output]

    try:
        retCode = subprocess.Popen(
            cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.STDOUT
        ).wait()
    except Exception:
        retCode = 1
    
    return retCode