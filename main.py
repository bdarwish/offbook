import re
import speech_to_text
import text_to_speech
import random

def main():
	stream = text_to_speech.set_up_tts()

	raw_scene = open('scene.txt').read()
	character = input('Enter your character: ').upper()
	
	scene = re.sub(r'\([^()]*\)', '', raw_scene) # Removes stage directions
	scene = re.sub(r'Scene.+', '', scene).strip() # Removes any "Scene x" headings
	lines = re.findall(r'([A-Z][A-Z\' /]+): (.+)', scene) # Extracts all lines and characters

	# Add each line of the user's character to the character_lines list of tuples
	# (<index of lines in lines>, <line>)
	character_lines = []

	for line in lines:
		if line[0] == character:
			character_lines.append((lines.index(line), line[1].strip()))

	chosen_line = character_lines[random.randint(0, len(character_lines) - 1)]

	print(chosen_line)

	# If the chosen line is first (i.e. no line before it)
	if chosen_line[0] == 0:
		stream.feed('Scene start.' + '....................')
	else:
		stream.feed(lines[chosen_line[0] - 1][1] + '....................') # The lines are to prevent it from cutting off the last word.
	
	stream.play()

	#speech_to_text()

if __name__ == '__main__':
	main()