from youtube_downloader import check_url
import pytest
import pathlib
import subprocess
import os


@pytest.mark.parametrize(
    'test, result',
    (
        ('test', False),
        ('1', False),
        ('http://youtube.com', True),
    )
)
def test_check_url(test: str, result: bool):
    assert check_url(test) == result


def test_run_script():
    curDir: str = pathlib.Path(__file__).parent.resolve()
    p: subprocess.Popen = subprocess.Popen(
        f'python3 {curDir}/youtube_downloader.py -h',
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
    )
    res = p.communicate()
    print("retcode =", p.returncode)
    print("res =", res)
    print("stderr =", res[1])
    assert p.returncode == 0
    assert res


def test_save_video():
    curDir: str = pathlib.Path(__file__).parent.resolve()
    p: subprocess.Popen = subprocess.Popen(
        (
            f'python3 {curDir}/youtube_downloader.py -v '
            'https://www.youtube.com/watch?v=NTa6Xbzfq1U'
        ),
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
    )
    res = p.communicate()
    print("retcode =", p.returncode)
    print("res =", res)
    print("stderr =", res[1])
    assert p.returncode == 0
    assert res
    assert os.path.isfile(f'{curDir}/Super_Mario_Bros._Theme_Song.mp4')


def test_save_audio():

    curDir: str = pathlib.Path(__file__).parent.resolve()
    p: subprocess.Popen = subprocess.Popen(
        (
            f'python3 {curDir}/youtube_downloader.py -a '
            'https://www.youtube.com/watch?v=NTa6Xbzfq1U'
        ),
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
    )
    res = p.communicate()
    print("retcode =", p.returncode)
    print("res =", res)
    print("stderr =", res[1])
    assert p.returncode == 0
    assert res
    assert os.path.isfile(f'{curDir}/Super_Mario_Bros._Theme_Song.mp3')
