import youtube_dl
from urllib import parse, request
from re import findall
import eyed3
import pprint
import os

PATH = os.path.dirname(os.path.abspath(__file__))
SONGS_PATH = f'{PATH}/songs/'



def download_image(image_url, file_name):
    request.urlretrieve(image_url, file_name)

download_image('https://i.scdn.co/image/93b671372b0b256ff878c9f78d5dcd7f68fe7a20', f'{SONGS_PATH}album_art.jpg')

def add_meta_data(songname, song):
	print(f'PATH: "{PATH}"')
	os.rename(songname, song)
	audiofile = eyed3.load(song)
	audiofile.tag.artist = 'Boyce Avenue'
	# audiofile.tag.album = ""
	# audiofile.tag.album_artist = "TIntegrity"
	audiofile.tag.title = "Let Her Go"
	audiofile.tag.addImage()
	# audiofile.tag.track_num = 2
	audiofile.tag.addImage(0x08, f'{SONGS_PATH}album_art.jpg')
	audiofile.tag.save()

add_meta_data(f'{SONGS_PATH}Boyce Avenue - Let Her Go.mp3', f'{SONGS_PATH}Boyce Avenue - Let Her Go.mp3')
os.remove(f'{SONGS_PATH}album_art.jpg')

# add_meta_data(f'{SONG_PATH}test.mp3', f'{SONG_PATH}Boyce Avenue - Let Her Go.mp3')

# pp = pprint.PrettyPrinter(indent=2)

# def youtube_search(q):
# 	query = parse.urlencode({'search_query' : str.strip(q)})
# 	req = request.urlopen(f'https://www.youtube.com/results?{query}')
# 	sr = findall(r'href=\"\/watch\?v=(.{11})', req.read().decode())
# 	return [f'http://www.youtube.com/watch?v={x}' for x in sr]

# song = {
# 	'title': 'Here Comes Your Man'
# }

# mp3 = {
# 		'verbose':			True,
# 		'fixup': 			'detect_or_warn',
# 		'format': 			'bestaudio/best',
# 		'postprocessors': [{
# 							'key': 'FFmpegExtractAudio',
# 							'preferredcodec': 'mp3',
# 							'preferredquality': '320',
# 		 }],
# 		'extractaudio': 	True,
# 		'outtmpl': 			f'{SONG_PATH}%(title)s.%(ext)s',
# 		'noplaylist': 		True,
# 	}

# search_results = youtube_search('Legend Has It Run The Jewels HQ')[:1]

# with youtube_dl.YoutubeDL(mp3) as ytdl:
# 	search_results = [ytdl.extract_info(song) for song in search_results]
# # os.execute(f'mv {SONG_PATH}/{search_results['title']}.mp3 {SONG_PATH}/{song['title']}.mp3')
# #set artist name, album artist name, title, thumbnail, track number

# pp.pprint(search_results)