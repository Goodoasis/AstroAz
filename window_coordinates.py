from tkinter import *

from PIL import Image, ImageTk


class WindowCoordinates(Toplevel):

    def __init__(self, *args, **kwargs):
        """Docstring"""
        super().__init__(*args, **kwargs)
        self.geometry("637x579")
        self.resizable(0, 0)
        self.title("Coordonées Sélénographique")
        self.image = self.load_image()
        self.create_canvas()
        self.place_canvas()

    def load_image(self):
        """Docstring"""
        image = Image.open("data\\latitude.jpg")
        _width, _height = image.size
        newsize = (int(_width//1.6), int(_height//1.6))
        image = image.resize(newsize)
        return image
    
    def create_canvas(self):
        """Docstring"""
        _width, _height = self.image.size
        self.photo = ImageTk.PhotoImage(master=self, image=self.image)
        self.canvas = Canvas(self, width=_width, height=_height)
        self.canvas.create_image(0, 0, anchor=NW, image=self.photo)
    
    def place_canvas(self):
        """Docstring"""
        self.canvas.pack(expand=True, fill=BOTH)


if __name__ == '__main__':
    APP = WindowCoordinates()
    APP.mainloop()