import dotenv
import base64
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
import threading
import queue

response_queue = queue.Queue()

def get_feedback(wav_path: str, character: str, scene: str):
	dotenv.load_dotenv()

	audio_data = open(wav_path, 'rb').read()

	encoded_audio = base64.b64encode(audio_data).decode()

	message = HumanMessage(
		content=[
			{'type': 'text', 'text': f'Provide a short paragraph of feedback (no styling) on the delivery of this line from a play/musical, include improvements. Before the paragraph, add the percentage of their accuracy (how well they memorized it) and a short sentence about the memorization. Make sure the percentage is honest. Give feedback on clarity, tone, and energy. All feedback should be in second person. This is the scene for context, the character is {character}: {scene}'},
			{'type': 'media', 'data': encoded_audio, 'mime_type': 'audio/wav'}
		]
	)

	os.remove(wav_path)

	threading.Thread(target=generate_response, args=(message, ), daemon=True).start()

	while True:
		try:
			feedback = response_queue.get_nowait()
			return feedback.content
		except queue.Empty:
			continue


def generate_response(message: HumanMessage):
	llm = ChatGoogleGenerativeAI(model='gemini-2.5-flash', temperature=0)

	feedback = llm.invoke([message])
	response_queue.put(feedback)