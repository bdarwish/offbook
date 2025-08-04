import customtkinter as ctk

class CheckboxFrame(ctk.CTkFrame):
    def __init__(self, master, title, values):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)
        self.title = title
        self.values = values
        self.checkboxes = []

        self.title = ctk.CTkLabel(self, text=self.title, fg_color='gray30', corner_radius=6)
        self.title.grid(row=0, column=0, padx=10, pady=(10, 0), sticky='ew')

        for i, value in enumerate(self.values):
            checkbox = ctk.CTkCheckBox(self, text=value)
            checkbox.grid(row=i+1, column=0, padx=10, pady=(10, 0), sticky='w')
            self.checkboxes.append(checkbox)
    
    def get(self):
        checked_checkboxes = []
        for checkbox in self.checkboxes:
            if checkbox.get() == 1:
                checked_checkboxes.append(checkbox.cget('text'))
        return checked_checkboxes
    
class RadiobuttonFrame(ctk.CTkFrame):
    def __init__(self, master, title, values):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)
        self.title = title
        self.values = values
        self.radiobuttons = []
        self.variable = ctk.StringVar(value='')

        self.title = ctk.CTkLabel(self, text=self.title, fg_color='gray30', corner_radius=6)
        self.title.grid(row=0, column=0, padx=10, pady=(10, 0), sticky='ew')

        for i, value in enumerate(self.values):
            radiobutton = ctk.CTkRadioButton(self, text=value, value=value, variable=self.variable)
            radiobutton.grid(row=i+1, column=0, padx=10, pady=(10, 0), sticky='w')
            self.radiobuttons.append(radiobutton)
    
    def get(self):
        return self.variable.get()
    
    def set(self, value):
        self.variable.set(value)

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title('OffBook')
        self.geometry('1200x660')
        self.grid_columnconfigure((0, 1), weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.checkbox_frame = CheckboxFrame(self, 'Values', ['value 1', 'value 2', 'value 3'])
        self.checkbox_frame.grid(row=0, column=0, padx=10, pady=(10, 0), sticky='nesw')
        self.radiobutton_frame = RadiobuttonFrame(self, 'Options', ['option 1', 'option 2'])
        self.radiobutton_frame.grid(row=0, column=1, padx=(0, 10), pady=(10, 0), sticky='nesw')

        self.button = ctk.CTkButton(self, text='Button', command=self.button_callback)
        self.button.grid(row=2, column=0, padx=10, pady=10, sticky='ew', columnspan=2)

    def button_callback(self):
        print('checkbox_frame:', self.checkbox_frame.get())
        print('radiobutton_frame:', self.radiobutton_frame.get())

app = App()
app.mainloop()