import youtube_dl
from urllib import parse, request
from re import findall
import eyed3
import pprint
import os
import pprint

pp = pprint.PrettyPrinter(indent=4)
PATH = os.path.dirname(os.path.abspath(__file__))
SONGS_PATH = f'{PATH}/songs/'

def download_image(image_url, file_name):
	request.urlretrieve(image_url, file_name)
	return file_name

def add_meta_data(songname, song):
	image_types = [0x00,0x01,0x02,0x03,0x04,0x05,0x06,0x07,0x08,0x09,0x0A,0x0B,0x0C,0x0D,0x0E,0x0F,0x10,0x11,0x12,0x13,0x14]
	print(f'PATH: "{PATH}"')
	os.rename(songname, song)
	audiofile = eyed3.load(song)
	print('ATTRIBUTES:')
	pp.pprint(audiofile.tag.__dict__)
	audiofile.tag.artist = 'Boyce Avenue'
	# audiofile.tag.album = ""
	# audiofile.tag.album_artist = "TIntegrity"
	audiofile.tag.title = "Let Her Go"
	# for type in image_types:
		#eyed3.id3.frames.ImageFrame.ARTIST
		# audiofile.tag.images.set(type, request.urlopen('https://i.scdn.co/image/93b671372b0b256ff878c9f78d5dcd7f68fe7a20').read(), 'image/jpeg')
	file_path = download_image('https://i.scdn.co/image/93b671372b0b256ff878c9f78d5dcd7f68fe7a20', f'{SONGS_PATH}temp_art.jpeg')
	with open(file_path, 'r') as file:
		audiofile.tag.images.set(eyed3.id3.frames.ImageFrame.ARTIST, file, 'image/jpeg')
	os.remove(file_path)

	# audiofile.tag.track_num = 2
	# audiofile.tag.addImage(0x08, f'{SONGS_PATH}album_art.jpg')
	audiofile.tag.save()

def youtube_search(q):
	query = parse.urlencode({'search_query' : str.strip(q)})
	req = request.urlopen(f'https://www.youtube.com/results?{query}')
	sr = findall(r'href=\"\/watch\?v=(.{11})', req.read().decode())
	return [f'http://www.youtube.com/watch?v={x}' for x in sr]

song = {
	'title': 'Here Comes Your Man'
}

mp3 = {
		'verbose':			True,
		'fixup': 			'detect_or_warn',
		'format': 			'bestaudio/best',
		'postprocessors': [{
							'key': 'FFmpegExtractAudio',
							'preferredcodec': 'mp3',
							'preferredquality': '320',
		 }],
		'extractaudio': 	True,
		'outtmpl': 			f'{SONGS_PATH}%(title)s.%(ext)s',
		'noplaylist': 		True,
	}

# download_image('https://i.scdn.co/image/93b671372b0b256ff878c9f78d5dcd7f68fe7a20', f'{SONGS_PATH}album_art.jpg')
add_meta_data(f'{SONGS_PATH}Boyce Avenue - Let Her Go.mp3', f'{SONGS_PATH}Boyce Avenue - Let Her Go.mp3')
# set_image('https://i.scdn.co/image/93b671372b0b256ff878c9f78d5dcd7f68fe7a20')
# os.remove(f'{SONGS_PATH}album_art.jpg')

# add_meta_data(f'{SONGS_PATH}test.mp3', f'{SONGS_PATH}Boyce Avenue - Let Her Go.mp3')

# search_results = youtube_search("let you down nf hq")[:1]
# search_results += youtube_search("house of cards season 5 theme")[:1]

# with youtube_dl.YoutubeDL(mp3) as ytdl:
# 	search_results = [ytdl.extract_info(song) for song in search_results]
# os.execute(f'mv {SONG_PATH}/{search_results['title']}.mp3 {SONG_PATH}/{song['title']}.mp3')
#set artist name, album artist name, title, thumbnail, track number

# pp.pprint(search_results)