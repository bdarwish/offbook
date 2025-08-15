import customtkinter as ctk
import scene_player
from tts import TTS
import threading
import os
import feedback
from speechcapture import Recorder
from configparser import ConfigParser

class PracticeWindow(ctk.CTkToplevel):
    def __init__(self, master, user_input, tts_engine: TTS, recorder: Recorder, config: ConfigParser):
        super().__init__(master)

        self.master = master
        self.user_input = user_input
        self.tts_engine = tts_engine
        self.recorder = recorder
        self.config = config
        self.feedback = ''
        self.closed = False

        self.character_lines = []
        self.lines = []
        
        self.tts_engine.on_playing_end = self.start_recording
        self.recorder.on_pause = self.next_line
        self.recorder.on_stop = self.after_recording
        
        self.recorder.max_seconds_of_silence = self.config.getint('silence', 'seconds_of_silence') if self.config.getboolean('silence', 'toggle_silence_stop') else None
        self.recorder.max_duration = self.config.getint('duration', 'max_duration') if self.config.getboolean('duration', 'toggle_max_duration') else None
        self.tts_engine.voice = self.config.get('voice', 'voice')
        self.tts_engine.rate = self.config.getint('voice', 'speed')

        self.title('Practice')
        self.protocol('WM_DELETE_WINDOW', self.close_window)
        self.geometry('638x413')
        self.resizable(False, False)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((0,1), weight=1)

        self.bind('<Key>', self.stop_recording)

        self.text = ctk.CTkLabel(self, fg_color='#54bb34', text='Loading...', text_color='black', font=ctk.CTkFont('Roboto', 30), wraplength=598, height=363)
        self.text.grid(row=0, column=0, sticky='nesw')

        if self.config.get('general', 'feedback_mode') == 'scene':
            self.recorder.pause_on_end = True
        else:
            self.recorder.pause_on_end = False

        self.cancel_button = ctk.CTkButton(self, text='Cancel', command=self.close_window, fg_color='#bb3434', corner_radius=0, border_width=1, border_color='black', font=ctk.CTkFont('Roboto', 14))
        self.cancel_button.grid(row=1, column=0, sticky='nesw')

        self.lines, self.character_lines = scene_player.process_scene(self.user_input[0], self.user_input[1])
        self.practice()

    def practice(self):
        if not self.closed:
            scene_player.run(self.user_input[1], self.tts_engine, self)

    def start_recording(self):
        if not self.closed:
            self.text.configure(text='Say your line\nPress escape to stop')
            self.recorder.resume() if self.config.get('general', 'feedback_mode') == 'scene' and self.recorder.is_recording and self.recorder.is_paused else self.recorder.record_async(True)
    
    def next_line(self):
        if not self.closed:
            if self.character_lines:
                self.practice()
            else:
                self.recorder.stop()
    
    def after_recording(self):
        if not self.closed:
            self.text.configure(text='Recording over, please wait...', fg_color='#bb3434')
            self.get_feedback()

    def get_feedback(self):
        if not self.closed:
            def run():
                feedback.get_feedback(self.recorder.audio_path, self.user_input[0], self.user_input[1], self.after_feedback)

            threading.Thread(target=run, daemon=True).start()
    
    def after_feedback(self, feedback):
        if not self.closed:
            self.text.configure(text=feedback, font=ctk.CTkFont('Roboto', 16), fg_color='#919191')        

    def close_window(self):
        self.closed = True

        # Stop recording
        self.recorder.stop()

        # Stop any current TTS
        self.tts_engine.stop()

        # Destroy current window and focus on main window
        self.destroy()
        self.master.focus()

        # Delete any recorded audio files
        try:
            os.remove(self.recorder.audio_path)
        except FileNotFoundError as e:
            pass
    
    def stop_recording(self, event):
        if (event.keysym == 'Escape' and self.recorder.is_recording):
            self.recorder.stop() if self.config.get('general', 'feedback_mode') == 'line' else self.recorder.pause()