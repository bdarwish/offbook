import customtkinter as ctk
from enum import Enum

class ErrorCodes(Enum):
    INVALID_API_KEY: str = 'Your API key is not valid. Please generate one from aistudio.google.com/apikey.'
    NO_CHARACTER_OR_SCENE: str = 'You must input a character and scene.'
    UNKNOWN_ERROR: str = 'An unknown error occured.'

class ErrorWindow(ctk.CTkToplevel):
    def __init__(self, master, error_code: ErrorCodes = ErrorCodes.UNKNOWN_ERROR):
        super().__init__(master)
        
        self.error_code = error_code

        self.title('Error')
        self.geometry('400x125')
        self.resizable(False, False)

        self.columnconfigure(0, weight=1)
        self.rowconfigure((0, 1), weight=1)

        self.title = ctk.CTkLabel(self, text=f'⚠   |   {self.error_code.name.replace('_', ' ')}', font=ctk.CTkFont('Roboto', size=17), justify='left') #⚠   |   {error_title}\n----------------------------------------------------------------------------
        self.title.grid(row=0, column=0, padx=20, pady=(10,0), sticky='nsw')
        
        self.canvas = ctk.CTkCanvas(self, width=400, height=10, bg='#252424', borderwidth=0, highlightthickness=0)
        self.canvas.grid(row=1, column=0, padx=0, pady=0, sticky='nesw')

        self.canvas.create_line(0, 5, 400, 5, fill='white', width=1)

        self.error_label = ctk.CTkLabel(self, text=self.error_code.value, wraplength=360, font=ctk.CTkFont('Roboto', size=15), justify='left')
        self.error_label.grid(row=2, column=0, padx=20, pady=(0,20), sticky='nsw')