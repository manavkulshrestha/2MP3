import spotipy
import os
import json
import spotipy.util as util
import pprint
import time

# PATH = os.path.dirname(__file__)
spotify_token = None
pp = pprint.PrettyPrinter(indent=4)


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

def get_spotify_playlist_songs(username, playlist_id):
	songs = []
	results = sp.user_playlist_tracks(username, playlist_id=playlist_id)
	if 'external_urls' in results:
		results = results['tracks']
	while True:
		for item in results['items']:
			song = {
				'artists': [artist['name'] for artist in item['track']['artists']],
				'duration_ms': item['track']['duration_ms'],
				'explicit': item['track']['explicit'],
				'name': item['track']['name'],
			}
			songs.append(song)

		if results['next']:
			results = sp.next(results)
		else:
			break
	return songs


info = open_json_file('info.txt')
spotify_token = get_spotify_token(info)

if spotify_token:
	sp = spotipy.Spotify(auth=spotify_token)
else:
	sp = spotipy.Spotify()

url = 'https://open.spotify.com/user/kieron/playlist/5Rrf7mqN8uus2AaQQQNdc1'

playlist = parse_spotify_playlist_url(url)
playlist = get_spotify_playlist_songs(playlist[0], playlist[1])

pp.pprint(playlist)
print(len(playlist))

