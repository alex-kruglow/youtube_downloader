# Youtube downloader

This script can help you to download YouTube video.
It is saving the video in video file or audio
file on your computer.

## How to install

Prepare some Linux system with python 3.10
```bash
git clone https://github.com/alex-kruglow/youtube_downloader.git
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

## How to use

To get help how to use the script
```bash
./youtube_downloader.py -h
```
To download YouTube content as video file:
```bash
./youtube_downloader.py -v <YOUTUBE VIDEO URL ADDRESS>
```
To download YouTube content as audio file:
```bash
./youtube_downloader.py -a <YOUTUBE VIDEO URL ADDRESS>
```
