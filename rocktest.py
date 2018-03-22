import os

PATH = os.path.dirname(os.path.abspath(__file__))
SONGS_PATH = f'{PATH}/songs/'

name = 'Imagine Dragons - Nothing Left To Say : Rocks.mp3'

os.rename(f'{SONGS_PATH}test.mp3', f'{SONGS_PATH}{name}')