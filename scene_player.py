import re
import random
from tts import TTS

def process_scene(character_input: str, scene_input: str):
	# r'([A-Z0-9 /]+):?\s+(.+)' / Works for CHARACTER: Line, CHARACTER\nLine, etc.
	# r'([A-Z][A-Z\' /]+): (.+)' / Works for CHARACTER: Line
	scene = re.sub(r'\([^()]*\)', '', scene_input) # Removes stage directions
	scene = re.sub(r'Scene.+', '', scene).strip() # Removes any "Scene x" headings
	lines = re.findall(r'([A-Z0-9 /]+):?\s+(.+)', scene) # Extracts all lines and characters

	# Add each line of the user's character to the character_lines list of tuples
	# (<index of lines in lines>, <line>)
	character_lines = []

	for line in lines:
		if line[0] == character_input:
			character_lines.append((lines.index(line), line[1].strip()))

	return lines, character_lines

def run(scene_input: str, tts_engine: TTS, practice_window):
	tts_text = ''

	line = practice_window.character_lines[0] if practice_window.config.get('general', 'feedback_mode') == 'scene' else practice_window.character_lines[random.randint(0, len(practice_window.character_lines) - 1)]

	if line[0] == 0:
		tts_text = 'Scene start'
	else:
		tts_text = practice_window.lines[line[0] - 1][1]
	
	practice_window.after(100, practice_window.text.configure(text=tts_text))
	tts_engine.feed(tts_text)
	practice_window.character_lines.pop(0)
	tts_engine.synthesize()