import re
import pyttsx3
import speech_to_text
import random
import time

speed = 225

def set_up_tts():
	engine = pyttsx3.init()
	engine.setProperty('rate', speed)
	#voices = engine.getProperty('voices')
	return engine

def main():
	engine = set_up_tts()

	raw_scene = open('scene.txt').read()
	character = input('Enter your character: ').upper()
	
	scene = re.sub(r'\([^()]*\)', '', raw_scene) # Removes stage directions
	scene = re.sub(r'Scene.+', '', scene).strip() # Removes any "Scene x" headings
	lines = re.findall(r'([A-Z][A-Z\' /]+): (.+)', scene) # Extracts all lines and characters

	# Add each line of the user's character to the character_lines list of tuples
	character_lines = []

	for line in lines:
		if line[0] == character:
			character_lines.append((lines.index(line), line[1].strip()))

	chosen_line = character_lines[random.randint(0, len(character_lines) - 1)]

	print(chosen_line)

	if chosen_line[0] == 0:
		engine.say('...' + 'Scene start.' + '...')
	else:
		engine.say('...' + lines[chosen_line[0] - 1][1] + '...')
	
	engine.runAndWait()

	#speech_to_text()

if __name__ == '__main__':
	main()