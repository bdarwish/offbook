import edge_tts
import os
from playsound3 import playsound
import asyncio
import threading

class TTS:
    def __init__(self, voice: str = 'en-US-AndrewNeural'):
        # en-GB-SoniaNeural F
        # en-GB-RyanNeural M
        # en-US-AvaNeural F
        # en-US-AndrewNeural M
        self.voice = voice
        self.rate = 100
        self.sound = None
        self.is_processing = False
        self.is_playing = False

        self.on_processing_start = None
        self.on_processing_end = None
        self.on_playing_start = None
        self.on_playing_end = None
        
        self._text = ''
        self._output_file = 'output/tts-output-file.mp3'
    
    def feed(self, text: str):
        self._text = self._text + ' ' + text
    
    def synthesize(self, play: bool = True):
        async def synthesize_text():
            self.is_processing = True

            if callable(self.on_processing_start):
                self.on_processing_start()

            communicate = edge_tts.Communicate(self._text or 'Something went wrong, so a default audio is playing.', self.voice, rate=f'{'+' if self.rate >= 100 else ''}{self.rate - 100}%')
            await communicate.save(self._output_file)

            self.is_processing = False
        
        asyncio.run(synthesize_text())
        
        if callable(self.on_processing_end):
            self.on_processing_end()

        if play:
            self.play_async()
    
    def play(self):
        self.is_playing = True

        if callable(self.on_playing_start):
            self.on_playing_start()

        self.sound = playsound(self._output_file, False)
        while self.sound.is_alive():
            continue
        self.is_playing = False

        if callable(self.on_playing_end):
            self.on_playing_end()

        if (os.path.exists(self._output_file)):
            os.remove(self._output_file)
        self._text = ''
    
    def play_async(self, daemon: bool = False):
        t = threading.Thread(target=self.play, daemon=daemon)
        t.start()
        return t
    
    def stop(self):
        if self.sound:
            self.is_playing = False
            self.sound.stop()

        if (os.path.exists(self._output_file)):
            os.remove(self._output_file)