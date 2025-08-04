import customtkinter as ctk
import main
import speech_recognition as sr
from RealtimeTTS import TextToAudioStream
import threading
import os
import feedback

wav_path = 'output/line.wav'

class PracticeWindow(ctk.CTkToplevel):
    def __init__(self, master, user_input, stream: TextToAudioStream, recognizer):
        super().__init__(master)

        self.user_input = user_input
        self.stream = stream
        self.recognizer = recognizer

        self.title('Practice')
        self.geometry('638x413')
        self.resizable(False, False)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((0,1), weight=1)

        self.text = ctk.CTkLabel(self, text=main.gui_run(self.user_input[0], self.user_input[1], self.stream), fg_color='#54bb34', text_color='black', font=ctk.CTkFont('Roboto', 30), wraplength=598, height=363)
        self.text.grid(row=0, column=0, sticky='nesw')

        self.cancel_button = ctk.CTkButton(self, text='Cancel', command=lambda: self.cancel(master=master), fg_color='#bb3434', corner_radius=0, border_width=1, border_color='black', font=ctk.CTkFont('Roboto', 14))
        self.cancel_button.grid(row=1, column=0, sticky='nesw')

        self.trigger_recording()

    def trigger_recording(self):
        if not self.stream.is_playing():
            threading.Thread(target=self.record_and_save_audio, daemon=True).start()
        else:
            self.after(100, lambda: self.trigger_recording())
    
    def record_and_save_audio(self):
        if self.winfo_exists():
            self.after(0, lambda: self.text.configure(text='Say your line'))

        with sr.Microphone() as source:
            audio = self.recognizer.listen(source)

        if self.winfo_exists():
            self.after(0, lambda: self.text.configure(text='Recording over', fg_color='#bb3434'))

        open(wav_path, 'wb').write(audio.get_wav_data())

        if self.winfo_exists():
            self.after(0, lambda: self.text.configure(text='Please wait', fg_color='#919191'))

        self.after(100, self.get_feedback)
    
    def get_feedback(self):
        if self.winfo_exists():
            # TODO: change fg_color depending on accuracy -> green: good (>50%), red: bad (<50%)
            self.text.configure(text=feedback.get_feedback(wav_path, self.user_input[0], self.user_input[1]), font=ctk.CTkFont('Roboto', 16))
        
        if self.winfo_exists():
            self.cancel_button.configure(text='Return to home')

    # Also the return to home function
    def cancel(self, master):
        # Save old values and make them extreme to instantly stop recording
        old_energy_threshold = self.recognizer.energy_threshold
        old_pause_threshold = self.recognizer.pause_threshold
        self.recognizer.energy_threshold = 1000000
        self.recognizer.pause_threshold = 0

        # Stop any current TTS
        self.stream.stop()

        # Destroy current window and focus on main window
        self.destroy()
        master.focus()

        # Delete any recorded audio files
        try:
            os.remove(wav_path)
        except FileNotFoundError as e:
            pass

        # Restore old values
        self.after(100, lambda: self.restore_threshold(old_energy_threshold, old_pause_threshold))
    
    def restore_threshold(self, old_energy_threshold, old_pause_threshold):
        self.recognizer.energy_threshold = old_energy_threshold
        self.recognizer.pause_threshold = old_pause_threshold