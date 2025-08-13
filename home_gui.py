import customtkinter as ctk
import practice_gui
import settings_gui
import speechcapture as sc
from PIL import Image, ImageTk
import tts
from config import load_config
from error import ErrorCodes, ErrorWindow
from feedback import check_api_key
import os

audio_path = 'output/line.wav'
config_path = 'config/.config.ini'

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
        
        self.config = load_config(config_path)

        os.environ['GOOGLE_API_KEY'] = self.config.get('other', 'api_key')

        self.tts_engine = tts.TTS()

        self.recorder = sc.Recorder(audio_path)
        self.recorder.adjust_to_background_noise()

        self.title('OffBook')
        self.icon_path = ImageTk.PhotoImage(file="assets/offbook-icon.png")
        self.wm_iconbitmap()
        self.iconphoto(True, self.icon_path)
        self.protocol('WM_DELETE_WINDOW', self.close_window)
        self.geometry('850x550')
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((0, 1, 2, 3, 4), weight=1)

        self.title_label = ctk.CTkLabel(self, text='OffBook', font=ctk.CTkFont('Roboto', 32))
        self.title_label.grid(row=0, column=0, pady=(20, 0), sticky='ns', columnspan=2)
        
        self.settings_button = ctk.CTkButton(self, text='', image=ctk.CTkImage(Image.open('assets/settings-icon.png'), size=(25,25)), fg_color='transparent', hover_color='#2e2e2e', width=25, command=self.open_settings)
        self.settings_button.grid(row=0, column=1, padx=(0,20), pady=(30,0), sticky='ne')

        self.character_frame = CharacterFrame(self)
        self.character_frame.grid(row=2, column=0, padx=20, pady=(20, 0), sticky='nesw', columnspan=2)

        self.script_frame = ScriptFrame(self)
        self.script_frame.grid(row=3, column=0, padx=20, pady=(20, 0), sticky='nesw', columnspan=2)

        self.start_button = ctk.CTkButton(self, text='Start', font=ctk.CTkFont('Roboto', 16), fg_color="#459d2a", hover_color="#54bb34", command=self.open_practice)
        self.start_button.grid(row=4, column=0, padx=20, pady=20, sticky='nesw', columnspan=2)
        
        self.practice_window = None
        self.settings_window = None

    def open_practice(self):
        if self.character_frame.get().strip() != '' and self.script_frame.get().strip() != '':
            if (self.practice_window is None or not self.practice_window.winfo_exists()) and (self.settings_window is None or not self.settings_window.winfo_exists()):
                if check_api_key():
                    self.practice_window = practice_gui.PracticeWindow(self, [
                        self.character_frame.get().strip().upper(),
                        self.script_frame.get().strip(),
                    ], self.tts_engine, self.recorder, self.config)
                else:
                    if not any(isinstance(window, ErrorWindow) and window.error_code == ErrorCodes.INVALID_API_KEY for window in self.winfo_children()):
                        ErrorWindow(self, ErrorCodes.INVALID_API_KEY)
            else:
                self.practice_window.focus()
        else:
            if not any(isinstance(window, ErrorWindow) and window.error_code == ErrorCodes.NO_CHARACTER_OR_SCENE for window in self.winfo_children()):
                ErrorWindow(self, ErrorCodes.NO_CHARACTER_OR_SCENE)
    
    def open_settings(self):
        if (self.settings_window is None or not self.settings_window.winfo_exists()) and (self.practice_window is None or not self.practice_window.winfo_exists()):
            self.settings_window = settings_gui.SettingsWindow(self, self.config, config_path)
        else:
            self.settings_window.focus()
    
    def close_window(self):
        self.tts_engine.stop()
        self.recorder.terminate()
        exit()

if __name__ == '__main__':
	home = HomeWindow()
	home.resizable(False, False)
	home.mainloop()