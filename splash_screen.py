import time
from tkinter import *

from PIL import Image, ImageTk
# from tkinter.ttk import Progressbar



class SplashScreen(Tk):

    def __init__(self, *args, **kwargs):
        """Docstrings"""
        super().__init__(*args, **kwargs)
        width_of_window = 790
        height_of_window = 610
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x_coordinate = (screen_width//2)-(width_of_window//2)
        y_coordinate = (screen_height//2)-(height_of_window//2)
        # Configure window.
        self.geometry(f"{width_of_window}x{height_of_window}+{x_coordinate}+{y_coordinate}")
        self.overrideredirect(1)
        # Widgets
        self.image = self.load_image()
        self.create_widgets()
        self.place_widgets()
        # Timer
        self.after(300, self.bar)
    
    def load_image(self):
        """Docstring"""
        image = Image.open("data\\splash.png")
        return image

    def create_widgets(self):
        """Docstring"""
        self._create_canvas()
        # self._create_labels()
        # self._create_progressBar()

    def _create_canvas(self):
        """Docstring"""
        _width, _height = self.image.size
        self.photo = ImageTk.PhotoImage(master=self, image=self.image)
        self.canvas = Canvas(self, width=_width, height=_height)
        self.canvas.create_image(0, 0, anchor=NW, image=self.photo)

    # def _create_labels(self):
    #     """Docstring"""
    #     self.label_astro = Label(self, text='Astro', fg='white', bg='black')
    #     style_labelAstro = ('Calibri (Body)', 18)
    #     self.label_astro.config(font=style_labelAstro)
    #     self.label_az = Label(self, text='Az', fg='white', bg='black')
    #     style_labelAz = ('Calibri (Body)', 18, 'bold')
    #     self.label_az.config(font=style_labelAz)
    #     self.label_credit = Label(self, text=' ', fg='white', bg='black')
    #     style_labelCredit = ('Calibri (Body)', 13)
    #     self.label_credit.config(font=style_labelCredit)

    # def _create_progressBar(self):
    #     """Docstring"""
    #     # s = tkinter.ttk.Style()
    #     # s.theme_use('clam')
    #     # s.configure("red.Horizontal.TProgressbar", foreground='red', background='#4f4f4f')
    #     self.progress = Progressbar(self, style="red.Horizontal.TProgressbar", orient=HORIZONTAL, length=500, mode='determinate')

    def place_widgets(self, loading=False):
        """Docstring"""
        self.canvas.place(x=-10, y=-10)
        # self.label_astro.grid(row=1, column=0)
        # self.label_az.grid(row=1, column=1)
        # self.label_credit.grid(row=2, column=0)
        # if loading:
            # self.label_loading.grid(row=3, column=0, sticky=W)
        # self.progress.grid(row=4, columnspan=3,sticky=S)

    def bar(self):
        """Docstring"""
        # self.label_loading = Label(self, text='Loading...', fg='white', bg='black')
        # style_label =('Calibri (Body)', 10)
        # self.label_loading.config(font=style_label)
        # self.place_widgets(loading=True)
        for i in range(180):
            # self.progress['value'] = i
            self.update_idletasks()
            time.sleep(0.01)
        self.destroy()


if __name__ == '__main__':
    APP = SplashScreen()
    APP.mainloop()