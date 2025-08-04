import customtkinter as ctk
import practice_gui
import text_to_speech
import speech_recognition as sr

silence_time = 3

class ScriptFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.grid_columnconfigure(0, weight=1)

        self.title_label = ctk.CTkLabel(self, text='Enter scene:', font=ctk.CTkFont('Roboto', 16))
        self.title_label.grid(row=0, column=0, pady=(10, 0), sticky='ns')

        self.script_box = ctk.CTkTextbox(self, wrap='word', font=ctk.CTkFont('Roboto', 14))
        self.script_box.grid(row=1, column=0, padx=10, pady=10, sticky='nesw')
    
    def get(self):
        return self.script_box.get('0.0', 'end')

class CharacterFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.grid_columnconfigure(0, weight=1)

        self.title_label = ctk.CTkLabel(self, text='Enter your character:', font=ctk.CTkFont('Roboto', 16))
        self.title_label.grid(row=0, column=0, padx=10, pady=(10, 0), sticky='ns')

        self.character_box = ctk.CTkTextbox(self, height=18)
        self.character_box.grid(row=1, column=0, padx=10, pady=10, sticky='nesw')
    
    def get(self):
        return self.character_box.get('0.0', 'end')

class HomeWindow(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.stream = text_to_speech.set_up_tts()

        self.recognizer = sr.Recognizer()
        self.recognizer.pause_threshold = silence_time
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source)

        self.title('OffBook')
        self.geometry('850x550')
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((0, 1, 2, 3, 4), weight=1)

        self.title_label = ctk.CTkLabel(self, text='OffBook', font=ctk.CTkFont('Roboto', 32))
        self.title_label.grid(row=0, column=0, pady=(20, 0), sticky='ns')

        self.error_label = ctk.CTkLabel(self, text='You must enter your character and the scene!', font=ctk.CTkFont('Roboto', 16), text_color='#bb3434', height=16)
        self.error_label.grid(row=1, column=0, pady=(20,0), sticky='ns')
        self.error_label.grid_remove()

        self.character_frame = CharacterFrame(self)
        self.character_frame.grid(row=2, column=0, padx=20, pady=(20, 0), sticky='nesw')

        self.script_frame = ScriptFrame(self)
        self.script_frame.grid(row=3, column=0, padx=20, pady=(20, 0), sticky='nesw')

        self.start_button = ctk.CTkButton(self, text='Start', font=ctk.CTkFont('Roboto', 16), fg_color="#459d2a", hover_color="#54bb34", command=self.start_practice)
        self.start_button.grid(row=4, column=0, padx=20, pady=20, sticky='nesw')
        
        self.practice_window = None

    def start_practice(self):
        if self.character_frame.get().strip() != '' and self.script_frame.get().strip() != '':
            if self.practice_window is None or not self.practice_window.winfo_exists():
                self.error_label.grid_remove()
                self.practice_window = practice_gui.PracticeWindow(self, [
                    self.character_frame.get().strip().upper(),
                    self.script_frame.get().strip(),
                ], self.stream, self.recognizer)
            else:
                self.error_label.grid_remove()
                self.practice_window.focus()
        else:
            self.error_label.grid()

home = HomeWindow()
home.resizable(False, False)
home.mainloop()