import spotipy
import os
import json
import spotipy.util as util
import pprint

pp = pprint.PrettyPrinter(indent=4)

with open(os.path.join(os.path.dirname(__file__), 'info.txt'), 'r') as file:
	info = json.load(file)

def get_spotify_token():
	try:
		return util.prompt_for_user_token(info['username'], client_id=info['client_id'], client_secret=info['client_secret'], redirect_uri=info['redirect_uri'])
	except:
		os.remove(f'.cache-{info["username"]}')
		return get_spotify_token()

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

token = get_spotify_token()

if token:
	sp = spotipy.Spotify(auth=token)

url = 'https://open.spotify.com/user/manavkoolz/playlist/38emfFLnZtfyOocIXX7AYG';
url = 'https://open.spotify.com/user/kieron/playlist/5Rrf7mqN8uus2AaQQQNdc1';
url = 'https://open.spotify.com/user/manavkoolz/playlist/38emfFLnZtfyOocIXX7AYG?si=DBMzLn7xTymkxe-sAeKqZg'

playlist = parse_spotify_playlist_url(url);
playlist = get_spotify_playlist_songs(playlist[0], playlist[1])

pp.pprint(playlist);
print(len(playlist))

