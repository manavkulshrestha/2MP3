import youtube_dl
from urllib import parse, request
from re import findall
import pprint
import os

SONG_PATH = '/songs'
pp = pprint.PrettyPrinter(indent=2)

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
		'outtmpl': 			f'{SONG_PATH[1:]}%(title)s.%(ext)s',
		'noplaylist': 		True,
	}

search_results = youtube_search('Here Comes Your Man Pixies HQ')[:1]

with youtube_dl.YoutubeDL(mp3) as ytdl:
	search_results = [ytdl.extract_info(song) for song in search_results]
os.execute(f'mv {SONG_PATH}/{search_results['title']}.mp3 {SONG_PATH}/{song['title']}.mp3')
#set artist name, album artist name, title, thumbnail, track number

pp.pprint(search_results)