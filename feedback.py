import base64
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai.chat_models import ChatGoogleGenerativeAIError
from langchain_core.messages import HumanMessage
from typing import Callable

def check_api_key():
	llm = ChatGoogleGenerativeAI(model='gemini-2.5-flash-lite', temperature=0)

	try:
		llm.invoke('Hello, Gemini!')
	except ChatGoogleGenerativeAIError as e:
		if 'API_KEY_INVALID' in str(e):
			return False
	
	return True

def get_feedback(wav_path: str, character: str, scene: str, after_feedback: Callable[[str], None]):
	llm = ChatGoogleGenerativeAI(model='gemini-2.5-flash', temperature=0)

	try:
		audio_data = open(wav_path, 'rb').read()
	except FileNotFoundError as e:
		print(f'An error occured while getting feedback: {e}')

	encoded_audio = base64.b64encode(audio_data).decode()

	message = HumanMessage(
		content=[
			{'type': 'text', 'text': f'''
			You are a theater coach evaluating a performance of lines from a play or musical. Listen carefully to the audio provided and base your evaluation strictly on the lines performed in this recording (though you can use the other lines only for context).

			1. Start with the memorization accuracy as a percentage (e.g., 82%) and one short, honest sentence describing how well the lines were remembered.

			2. Then, give a brief paragraph (no extra formatting) of feedback in second person on the delivery, addressing clarity, tone, and energy. Consider the genre and mood of the scene when assessing tone and energy.

			3. Do not be overly strict about minor deviations from the script if they are clearly artistic choices that work in the context of the performance.

			4. Recognize that different actors may interpret a role in different but valid ways—offer suggestions for improvement without insisting on a single “correct” delivery style.

			5. Do not mention the scene title or describe the scene itself. Focus only on evaluating the actor's performance.

			6. Be specific, constructive, and encouraging, with actionable suggestions for improvement. Keep the feedback concise but insightful.

			Context for your evaluation: The character is {character}. Scene: {scene}
			'''},
			{'type': 'media', 'data': encoded_audio, 'mime_type': 'audio/wav'}
		]
	)

	if os.path.exists(wav_path):
		os.remove(wav_path)
	feedback = llm.invoke([message])

	after_feedback(feedback.content)

	return feedback