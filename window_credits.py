from tkinter import *


class WindowCredits(Tk):

    def __init__(self, *args, **kwargs):
        """Docstrings"""
        super().__init__(*args, **kwargs)
        width_of_window = 400
        height_of_window = 300
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x_coordinate = (screen_width//2)-(width_of_window//2)
        y_coordinate = (screen_height//2)-(height_of_window//2)
        self.geometry(f"{width_of_window}x{height_of_window}+{x_coordinate}+{y_coordinate}")    
        self.overrideredirect(0)
        self.create_frames()
        self.create_widgets()
        self.place_widgets()
    
    def create_frames(self):
        """Docstrings"""
        self.frame_main = Frame(self)
        self.frame_buttons= Frame(self)
        self.frame_autors = Frame(self.frame_main)

    def create_widgets(self):
        """Docstrings"""
        self._create_labels()
        self._create_buttons()

    def _create_labels(self):
        """Docstrings"""
        # frame_autors
        self.label_autor1 = Label(self.frame_autors, text="Goyard Maxime")
        self.label_autor2 = Label(self.frame_autors, text="D'Eurveilher Thibault")
        # frame_mail
        self.label_mail = Label(self.frame_main, text="astroas@laposte.fr")
    
    def _create_buttons(self):
        """Docstrings"""
        self.button_github = Button(self.frame_buttons, text="Git-Hub")
        self.button_donation = Button(self.frame_buttons, text="Payez un café")

    def place_widgets(self):
        """Docstrings"""
        self.frame_main.pack(pady=10, padx=10)
        self.frame_buttons.pack()
        self.frame_autors.pack()
        # frame_mail
        self.label_mail.pack()
        # frame_autors
        self.label_autor1.pack()
        self.label_autor2.pack()
        # frame_buttons.
        self.button_github.pack()
        self.button_donation.pack()

    def call_back(self, event):
        """Docstrings"""
        # Click to close window
        pass


if __name__ == '__main__':
    APP = WindowCredits()
    APP.mainloop()