from RealtimeTTS import TextToAudioStream, KokoroEngine

def set_up_tts():
	male_voice = 'am_echo'
	female_voice = 'af_bella'

	engine = KokoroEngine(voice=male_voice)
	stream = TextToAudioStream(engine)
	
	return stream