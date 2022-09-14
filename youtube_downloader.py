#!/usr/bin/env python3

import argparse
import os
import pytube
import sys
import tempfile
from urllib import request


# VAR
VERBOSE = False


def parse_args() -> argparse.ArgumentParser:
    '''Parse command line arguments.'''
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-a',
        help='Save as audio MP3 file',
        default=False,
        action='store_true'
    )
    parser.add_argument(
        '-v',
        help='Save as video MP4 file',
        default=False,
        action='store_true'
    )
    parser.add_argument(
        '-dir',
        help='Directory to store.',
        default='./',
        required=False
    )
    parser.add_argument(
        'url',
        help='URL to youtube video',
    )
    parser.add_argument(
        '-vv',
        help='Verbose mode',
        default=False,
        action='store_true'
    )
    return parser.parse_args()


def log(message: str):
    '''Print message logs if VERBOSE variable is True.'''
    if VERBOSE:
        print(message)


def check_url(url: str) -> bool:
    '''Return True is URL can be requested.'''
    log(f'Checking URL is starting. URL: {url}')
    try:
        status_code: request.response = request.urlopen(url).getcode()
    except ValueError:
        log(f'Request to {url} returned ValueError.')
        return False
    return status_code == 200


def check_is_playlist(url: str) -> bool:
    '''Return True is URL leads to a YouTube playlist.'''
    log(f'Checking if URL {url} is playlist.')
    p: pytube.Playlist = pytube.Playlist(url)
    try:
        p.title
    except KeyError:
        log(f'URL: {url} is NOT playlist.')
        return False
    log(f'URL: {url} is playlist')
    return True


def check_is_channel(url: str):
    '''Return True if URL leads to a YouTube channel.'''
    log(f'Checking if URL {url} is channel.')
    try:
        pytube.Channel(url)
    except pytube.exceptions.RegexMatchError:
        log(f'URL: {url} is NOT channel.')
        return False
    log(f'URL: {url} is channel.')
    return True


def normalyze_title(title: str) -> str:
    '''Return normalyzed title.
    It returns title without special symbols and backspaces.
    param title - string
    '''
    for c in '\'"!@#$%^&*+/?\\`~':
        title = title.replace(c, '')
    title = title.replace(' - ', '-')
    title = title.replace(' ', '_')
    return title


def download_video(url: str, directory: str) -> str:
    '''Return filename that was downloaded.'''
    log(f'Downloading video is starting. URL: {url}; DIR: {directory}')
    yt: pytube.YouTube = pytube.YouTube(url)
    title: str = normalyze_title(yt.title)
    # title = translate(title)
    log(f'title: {title}')
    filename: str = f'{directory}/{title}.mp4'
    log(f'filename: {filename}')
    streams: list = yt.streams.filter(progressive=True, file_extension='mp4')
    if streams.filter(file_extension='mp4'):
        streams = streams.filter(file_extension='mp4')
    else:
        streams = streams.filter(file_extension='webm')
    stream: pytube.Stream = streams.order_by('resolution').desc().first()
    log(f'Chosen stream: {str(stream)}')
    log('Start of stream downloading.')
    stream.download(filename=filename)
    log('Stream downloading is completed.')
    log(f'Video filename: {filename}.')
    return filename


def convert_video_to_audio(
        video_filename: str, audio_filename: str, directory: str
) -> None:
    '''Convert video MP4 file to audio MP3 file via using ffmpeg.
    param video_filename - name of source video file.
    param audio_filename - name of destination audio file.
    param directory - directory path to save audio file.
    '''
    log('Starting converting MP4 to MP3.')
    log(f'Convert {video_filename} to {directory}/{audio_filename}.')
    cmd: str = (
        '/bin/ffmpeg '
        '-y '
        '-i '
        f'\'{video_filename}\' '
        f'\'{directory}/{audio_filename}\' '
        '-hide_banner '
        '-loglevel error'
    )
    log(f'Command to run: {cmd}')
    os.system(cmd)


def download_audio(url: str, directory: str) -> str:
    '''Return filename that was downloaded from YouTube and
    converted it by ffmpeg to MP3.'''
    log(f'Downloading audio is starting. URL: {url}; DIR: {directory};')
    tmp_dir: str = tempfile.gettempdir()
    video_filename: str = download_video(url, tmp_dir)
    log(f'video file name: {video_filename}')
    audio_filename: str = '.'.join(
        video_filename.split('/')[-1].split('.')[:-1]
    ) + '.mp3'
    log(f'audio file name: {audio_filename}')
    convert_video_to_audio(video_filename, audio_filename, directory)
    log(f'Starting of deleting video file in tmp: {video_filename}')
    os.remove(video_filename)
    log(f'Audio filename: {audio_filename}.')
    return audio_filename


def check_dir(directory: str):
    pass


def get_video_urls(url: str, is_playlist: bool, is_channel: bool) -> tuple:
    '''Return URLs of videos if URL is playlist or channel.'''
    log('Getting of video urls is started.')
    if is_playlist or is_channel:
        if is_channel:
            c: pytube.Channel = pytube.Channel(url)
            urls: tuple = tuple(c.video_urls)
        if is_playlist:
            p: pytube.Playlist = pytube.Playlist(url)
            urls: tuple = tuple(p.video_urls)
    log('List of URLs: {}'.format(', '.join(urls)))
    return urls


def progressbar(it, prefix="", size=60, out=sys.stdout):  # Python3.6+
    count = len(it)

    def show(j):
        x = int(size*j/count)
        print(
            f"{prefix}[{u'█'*x}{('.'*(size-x))}] {j}/{count}",
            end='\r',
            file=out,
            flush=True
        )
    show(0)
    for i, item in enumerate(it):
        yield item
        show(i+1)
    print("\n", flush=True, file=out)


def main():
    args: argparse.ArgumentParser = parse_args()
    if not check_url(args.url):
        print('Invalid URL')
        return
    if not args.a and not args.v:
        print('You have to set -a or -v')
        return
    if args.vv:
        global VERBOSE
        VERBOSE = True
    # Create tuple with video URLs.
    is_playlist: bool = check_is_playlist(args.url)
    is_channel: bool = check_is_channel(args.url)
    if is_channel or is_playlist:
        video_urls: tuple = get_video_urls(args.url, is_playlist, is_channel)
    else:
        video_urls = (args.url, )

    # Download video or audio by video_urls.
    if args.a:
        for url in progressbar(video_urls, 'Download: '):
            download_audio(url, args.dir)
    elif args.v:
        for url in progressbar(video_urls, 'Download: '):
            download_video(url, args.dir)


if __name__ == '__main__':
    main()
