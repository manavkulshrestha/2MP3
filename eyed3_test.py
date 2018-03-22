import eyed3

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

