import speech_recognition as sr

def identify_line(wav_path, silence_time=3):
	r = sr.Recognizer()
	r.pause_threshold = silence_time

	with sr.Microphone() as source:
		r.adjust_for_ambient_noise(source)
		print('Say your line.')
		audio = r.listen(source)
		print('Recording over.')

	open(wav_path, 'wb').write(audio.get_wav_data())

	transcript = r.recognize_whisper(audio, language='english')

	try:
		print("The line you said was:\n" + transcript)
	except sr.UnknownValueError:
		print('Could not understand audio.')
	except sr.RequestError as e:
		print(f'Could not request results from Whisper; {e}')
		
	return transcript

