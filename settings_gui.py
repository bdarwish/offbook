import customtkinter as ctk
from configparser import ConfigParser
import os

class GeneralFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        
        self.grid_columnconfigure(0, weight=1)
        
        self.title_label = ctk.CTkLabel(self, text='General', font=ctk.CTkFont('Roboto', 20))
        self.title_label.grid(row=0, column=0, pady=(10, 0), sticky='ns')

        self.feedback_mode_label = ctk.CTkLabel(self, text='Feedback Mode', font=ctk.CTkFont('Roboto', 14))
        self.feedback_mode_label.grid(row=1, column=0, padx=10, pady=0, sticky='ns')

        self.options_frame = ctk.CTkFrame(self, fg_color='transparent')
        self.options_frame.grid(row=2, column=0, padx=10, pady=(0,10), sticky='nesw')
        self.options_frame.grid_columnconfigure((0, 1), weight=1)

        self.line_mode = ctk.CTkRadioButton(self.options_frame, text='Random line', value='line', variable=self.master.settings['general']['feedback_mode'])
        self.line_mode.grid(row=2, column=0, padx=(10,0), pady=0)

        self.scene_mode = ctk.CTkRadioButton(self.options_frame, text='Entire scene', value='scene', variable=self.master.settings['general']['feedback_mode'])
        self.scene_mode.grid(row=2, column=1, padx=(10,0), pady=0)


class VoiceFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.grid_columnconfigure((0, 1, 2, 3), weight=1)

        self.title_label = ctk.CTkLabel(self, text='Voice', font=ctk.CTkFont('Roboto', 20))
        self.title_label.grid(row=0, column=0, pady=(10, 0), sticky='ns', columnspan=4)

        self.us_male = ctk.CTkRadioButton(self, text='Male (US)', value='en-US-AndrewNeural', variable=self.master.settings['voice']['voice'], font=ctk.CTkFont('Roboto', 14))
        self.us_male.grid(row=1, column=0, padx=(10,0), pady=(10,0), sticky='ew')

        self.us_female = ctk.CTkRadioButton(self, text='Female (US)', value='en-US-AvaNeural', variable=self.master.settings['voice']['voice'], font=ctk.CTkFont('Roboto', 14))
        self.us_female.grid(row=1, column=1, padx=(10,0), pady=(10,0), sticky='ew')

        self.gb_male = ctk.CTkRadioButton(self, text='Male (GB)', value='en-GB-RyanNeural', variable=self.master.settings['voice']['voice'], font=ctk.CTkFont('Roboto', 14))
        self.gb_male.grid(row=1, column=2, padx=(10,0), pady=(10,0), sticky='ew')

        self.gb_female = ctk.CTkRadioButton(self, text='Female (GB)', value='en-GB-SoniaNeural', variable=self.master.settings['voice']['voice'], font=ctk.CTkFont('Roboto', 14))
        self.gb_female.grid(row=1, column=3, padx=10, pady=(10,0), sticky='ew')

        self.speed_label = ctk.CTkLabel(self, text='Speed Percent', font=ctk.CTkFont('Roboto', 14))
        self.speed_label.grid(row=2, column=0, padx=10, pady=(10,0), sticky='ns', columnspan=4)

        self.speed_number = ctk.CTkLabel(self, textvariable=self.master.settings['voice']['speed'], font=ctk.CTkFont('Roboto', 14))
        self.speed_number.grid(row=3, column=0, padx=10, pady=0, sticky='ns', columnspan=4)

        self.speed_slider = ctk.CTkSlider(self, from_=0, to=200, variable=self.master.settings['voice']['speed'], number_of_steps=40)
        self.speed_slider.grid(row=4, column=0, padx=10, pady=(0,10), sticky='nesw', columnspan=4)

class SilenceFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.grid_columnconfigure(0, weight=1)

        self.title_label = ctk.CTkLabel(self, text='Silence', font=ctk.CTkFont('Roboto', 20))
        self.title_label.grid(row=0, column=0, padx=10, pady=(10,0), sticky='ns')

        self.toggle_checkbox = ctk.CTkCheckBox(self, text='Stop recording on silence', variable=self.master.settings['silence']['toggle_silence_stop'], font=ctk.CTkFont('Roboto', 14))
        self.toggle_checkbox.grid(row=1, column=0, padx=10, pady=0, sticky='nesw')

        self.silence_seconds_label = ctk.CTkLabel(self, text='Seconds of Silence', font=ctk.CTkFont('Roboto', 14))
        self.silence_seconds_label.grid(row=2, column=0, padx=10, pady=(5,0), sticky='ns', columnspan=4)
        
        self.silence_number = ctk.CTkLabel(self, textvariable=self.master.settings['silence']['seconds_of_silence'], font=ctk.CTkFont('Roboto', 14))
        self.silence_number.grid(row=3, column=0, padx=10, pady=0, sticky='ns', columnspan=4)
        
        self.silence_slider = ctk.CTkSlider(self, from_=1, to=10, number_of_steps=10, variable=self.master.settings['silence']['seconds_of_silence'])
        self.silence_slider.grid(row=4, column=0, padx=10, pady=0, sticky='nesw')

        self.adjust_button = ctk.CTkButton(self, text='Adjust Silence Threshold for Background Noise', anchor='center', command=master.master.recorder.adjust_to_background_noise)
        self.adjust_button.grid(row=5, column=0, padx=10, pady=10, sticky='nesw')

class DurationFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.title_label = ctk.CTkLabel(self, text='Duration', font=ctk.CTkFont('Roboto', 20))
        self.title_label.grid(row=0, column=0, padx=10, pady=(10,0), sticky='ns')

        self.toggle_checkbox = ctk.CTkCheckBox(self, text='Cap the duration of the recording', variable=self.master.settings['duration']['toggle_max_duration'], font=ctk.CTkFont('Roboto', 14))
        self.toggle_checkbox.grid(row=1, column=0, padx=10, pady=(10,0), sticky='nesw')

        self.duration_label = ctk.CTkLabel(self, text='Max Duration (seconds)', font=ctk.CTkFont('Roboto', 14))
        self.duration_label.grid(row=2, column=0, padx=10, pady=(10,0), sticky='ns', columnspan=4)
        
        self.duration_number = ctk.CTkLabel(self, textvariable=self.master.settings['duration']['max_duration'], font=ctk.CTkFont('Roboto', 14))
        self.duration_number.grid(row=3, column=0, padx=10, pady=0, sticky='ns', columnspan=4)
        
        self.duration_slider = ctk.CTkSlider(self, from_=0, to=120, variable=self.master.settings['duration']['max_duration'], number_of_steps=60)
        self.duration_slider.grid(row=4, column=0, padx=10, pady=(0,10), sticky='nesw')

class OtherFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.grid_columnconfigure(0, weight=1)

        self.title_label = ctk.CTkLabel(self, text='Other', font=ctk.CTkFont('Roboto', 20))
        self.title_label.grid(row=0, column=0, pady=(10, 0), sticky='ns')

        self.api_key_button = ctk.CTkButton(self, text='Set API Key', font=ctk.CTkFont('Roboto', 14), command=self.set_api_key)
        self.api_key_button.grid(row=1,column=0, padx=10, pady=10, sticky='ns')
    
    def set_api_key(self):
        dialog = ctk.CTkInputDialog(text='Enter your API key:', title='API Key', font=ctk.CTkFont('Roboto', 14))
        self.master.settings['other']['api_key'].set(dialog.get_input())


class SettingsWindow(ctk.CTkToplevel):
    def __init__(self, master, config: ConfigParser, config_path: str):
        super().__init__(master)

        self.config = config
        self.config_path = config_path

        self.load_values()
        
        self.title('Settings')
        self.protocol('WM_DELETE_WINDOW', self.close_window)
        self.geometry('638x650')
        self.resizable(False, False)

        self.grid_columnconfigure((0, 1), weight=1)
        self.grid_rowconfigure((0, 1, 2, 3), weight=1)

        self.general_frame = GeneralFrame(self)
        self.general_frame.grid(row=0, column=0, padx=20, pady=(20,0), sticky='nesw', columnspan=2)

        self.voice_frame = VoiceFrame(self)
        self.voice_frame.grid(row=1, column=0, padx=20, pady=(20,0), sticky='nesw', columnspan=2)

        self.silence_frame = SilenceFrame(self)
        self.silence_frame.grid(row=2, column=0, padx=(20,0), pady=(20, 0), sticky='nesw')

        self.duration_frame = DurationFrame(self)
        self.duration_frame.grid(row=2, column=1, padx=20, pady=(20, 0), sticky='nesw')

        self.other_frame = OtherFrame(self)
        self.other_frame.grid(row=3, column=0, padx=20, pady=20, sticky='nesw', columnspan=2)
    
    def load_values(self):
        self.settings = {
            'general': {
                'feedback_mode': ctk.StringVar(value=self.config.get('general', 'feedback_mode'))
            },

            'voice': {
                'voice': ctk.StringVar(value=self.config.get('voice', 'voice')),
                'speed': ctk.IntVar(value=self.config.getint('voice', 'speed'))
            },
            'silence': {
                'toggle_silence_stop': ctk.BooleanVar(value=self.config.getboolean('silence', 'toggle_silence_stop')),
                'seconds_of_silence': ctk.IntVar(value=self.config.getint('silence', 'seconds_of_silence'))
            },
            'duration': {
                'toggle_max_duration': ctk.BooleanVar(value=self.config.getboolean('duration', 'toggle_max_duration')),
                'max_duration': ctk.IntVar(value=self.config.getint('duration', 'max_duration'))
            },

            'other': {
                'api_key': ctk.StringVar(value=self.config.get('other', 'api_key'))
            }
        }
    
    def save_values(self):
        for section in self.settings:
            for setting in self.settings[section]:
                self.config[section][setting] = str(self.settings[section][setting].get())

        os.environ['GOOGLE_API_KEY'] = self.settings['other']['api_key'].get()
        
        with open(self.config_path, 'w') as file:
            self.config.write(file)

    def close_window(self):
        # Save values
        self.save_values()

        # Destroy current window and focus on main window
        self.destroy()
        self.master.focus()

