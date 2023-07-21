# __Manzana Apple TV Plus Trailers__

A python program to download Apple TV Plus movie and tv-show trailers. Video streams upto 4K with Dolby Vision, HDR10+ and SDR. Audio streams with HE-AAC, AAC, AC-3 and Dolby Atmos (EAC-3 JOC). Audio descriptions are also available. SDH and forced subtitle streams are also available. You can choose what streams you want to download.

<picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/dropcreations/Manzana-Apple-TV-Plus-Trailers/main/assets/manzana__darkmode.png">
    <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/dropcreations/Manzana-Apple-TV-Plus-Trailers/main/assets/manzana__lightmode.png">
    <img alt="Apple TV Plus" src="https://raw.githubusercontent.com/dropcreations/Manzana-Apple-TV-Plus-Trailers/main/assets/manzana__lightmode.png">
</picture>

## __TODO__

- [x] Add non-original movie trailers.
- [ ] Add tv-show trailers support.
- [ ] Add tags to the output video.

## __Required__

- [ffmpeg](https://ffmpeg.org/download.html)

## Demo

![demo](https://raw.githubusercontent.com/dropcreations/Manzana-Apple-TV-Plus-Trailers/main/assets/demo.gif)

## __How to use?__

First of all clone this project or download the project as a zip file and extract it to your pc. (or you can see [Releases](https://github.com/dropcreations/Manzana-Apple-TV-Plus-Trailers/releases))

```
git clone https://github.com/dropcreations/Manzana-Apple-TV-Plus-Trailers.git && cd Manzana-Apple-TV-Plus-Trailers
```

Install required modules for python (use `pip3` if `pip` doesn't work for you)

```
pip install -r requirements.txt
```

Now open terminal and run below command (Use `py` or `python3` if `python` doesn't work for you)

```
python manzana.py [url]
```

While downloading streams you will ask what stream you want. When it asked for stream's `ID`, you can use multiple options as mentioned below.

__Video stream__

- You can only select one stream for the ouput, give it's `ID`.

__Audio stream__

- You can select multiple streams, give `ID`s as a comma seperated list. Remember the firs `ID` you give in the list will mark as the default stream in output. __(ex: 5, 2, 16, 20...)__

__Subtitle stream__

- You can also select multiple streams or all streams if you want. Give `ID`s as a list or simply type `all` to get all tracks. Remember when you using `all` the first stream in the list will mark as the default stream in output.

If you don't need audio. just use `--no-audio` or `-an` argument with command

```
python manzana.py --no-audio [url]
```

If you don't need subtitles. just use `--no-subs` or `-sn` argument with command

```
python manzana.py --no-subs [url]
```

Get help using `-h` or `--help` command

```
usage: manzana.py [-h] [-v] [-an] [-sn] url

Manzana: Apple TV Plus Trailers Downloader

positional arguments:
  url              Apple TV Plus URL for a movie

optional arguments:
  -h, --help       show this help message and exit
  -v, --version    show program's version number and exit
  -an, --no-audio  Don't download audio streams. (default: False)
  -sn, --no-subs   Don't download subtitle streams. (default: False)
```

## About me

Hi, You might recognize me as GitHub's [dropcreations](https://github.com/dropcreations).

__Other useful python scripts done by me__

| Project        | Github location                                |
|----------------|------------------------------------------------|
| MKVExtractor   | https://github.com/dropcreations/MKVExtractor  |
| FLAC-Tagger    | https://github.com/dropcreations/flactagger    |
| MP4/M4A-Tagger | https://github.com/dropcreations/mp4tagger     |
| MKV-Tagger     | https://github.com/dropcreations/mkvtagger     |

<br>

- __NOTE: If you found any issue using this program, mention in issues section__
