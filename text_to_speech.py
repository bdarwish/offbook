from RealtimeTTS import TextToAudioStream, KokoroEngine, PiperEngine, PiperVoice, KokoroVoice

def set_up_tts():
	male_voice = 'am_echo'
	female_voice = 'af_bella'

	engine = KokoroEngine(voice='af_bella')
	stream = TextToAudioStream(engine)
	return stream