import spotipy
import os
import json
import spotipy.util as util
import time
import youtube_dl
from urllib import parse, request
from re import findall
import eyed3
import pprint

pp = pprint.PrettyPrinter(indent=2)

spotipy_token = None
PATH = os.path.dirname(os.path.abspath(__file__))
SONGS_PATH = f'{PATH}/songs/'
PLACEHOLDER_FILE_NAME = 'song'
PLACEHOLDER_ART_NAME = 'album_art'

with open(f'{PATH}/in.txt', 'r') as file:
    urls = file.read().splitlines()

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
		'outtmpl': 			f'{SONGS_PATH}{PLACEHOLDER_FILE_NAME}.%(ext)s',#f'{SONGS_PATH}%(title)s.%(ext)s'
		'noplaylist': 		True,
	}

def youtube_search(q):
	query = parse.urlencode({'search_query' : str.strip(q)})
	req = request.urlopen(f'https://www.youtube.com/results?{query}')
	sr = findall(r'href=\"\/watch\?v=(.{11})', req.read().decode())
	return [f'http://www.youtube.com/watch?v={x}' for x in sr]

def download_image(image_url, file_name):
    request.urlretrieve(image_url, file_name)
    return file_name

def add_meta_data(name, song):
	audiofile = eyed3.load(f'{SONGS_PATH}{name}')
	audiofile.tag.artist = song['artists'][0]
	audiofile.tag.album = song['album']
	audiofile.tag.album_artist = ', '.join(song['artists'])
	audiofile.tag.title = song['title']
	audiofile.tag.track_num = song['track_number']
	audiofile.tag.play_count = 0
	audiofile.tag.save()

	file_path = download_image(song['image'], f'{SONGS_PATH}image.jpeg')
	os.system(f'eyeD3 --add-image="{file_path}":FRONT_COVER "{SONGS_PATH}{name}"')
	os.remove(file_path)

	os.rename(f'{SONGS_PATH}{name}', f'{SONGS_PATH}{song["artists"][0].replace("/", ":")} - {song["title"].replace("/", ":")}{" (Explicit)" if song["explicit"] else ""}.mp3')

def open_json_file(file_name):
	with open(file_name, 'r') as file:
		return json.load(file)

def get_spotify_token(info):
	try:
		cache_file = f'.cache-{info["username"]}'
		cache = open_json_file(cache_file)
		if cache['expires_at'] < int(time.time()):
			os.remove(cache_file)
			get_spotify_token(info)
		else:
			return cache['access_token']
	except:
		return util.prompt_for_user_token(info['username'], client_id=info['client_id'], client_secret=info['client_secret'], redirect_uri=info['redirect_uri'])

def parse_spotify_playlist_url(url):
	user_start = url.find('/user/')+6
	user_end = url.find('/', user_start)
	return (url[user_start:user_end], url[url.rfind('/')+1:])

def get_spotify_image_url(images, priority_height, priority_width):
	for image in images:
		if image['height'] == priority_height and image['width'] == priority_width:
			return image['url']
	return images[0]['url']

def get_spotify_playlist_songs(username, playlist_id):
	songs = []
	results = sp.user_playlist_tracks(username, playlist_id=playlist_id)
	if 'external_urls' in results:
		results = results['tracks']
	while True:
		pp.pprint(results)
		for item in results['items']:
			song = {
				'album': item['track']['album']['name'],
				'image': get_spotify_image_url(item['track']['album']['images'], 640, 640),
				'artists': [artist['name'] for artist in item['track']['artists']],
				# 'duration_ms': item['track']['duration_ms'],
				'explicit': item['track']['explicit'],
				'title': item['track']['name'],
				'track_number': item['track']['track_number'],
			}
			songs.append(song)
			
		if results['next']:
			results = sp.next(results)
		else:
			break
	return songs


info = open_json_file('info.txt')
spotipy_token = get_spotify_token(info)

if spotipy_token:
	sp = spotipy.Spotify(auth=spotipy_token)
else:
	print(f'No token: {spotipy_token}')

for url in urls:
	playlist = parse_spotify_playlist_url(url)
	playlist = get_spotify_playlist_songs(playlist[0], playlist[1])

	i=1

	for song in playlist:
		with youtube_dl.YoutubeDL(mp3) as ytdl:
			query = f'{" ".join(song["artists"])} {song["title"]}{" Dirty" if song["explicit"] else ""} HQ'
			ytdl.download(youtube_search(query)[:1])
		add_meta_data(f'{PLACEHOLDER_FILE_NAME}.mp3', song)
		print(f'{i}. Download complete: {song["title"]}')
		i += 1

	pp.pprint(playlist)
	print(len(playlist))

