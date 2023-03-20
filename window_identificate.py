from tkinter import *
from pathlib import PurePath

from calculator import Calculator
# from astronomie import CURRENT_DIR


# Set current Path.
CURRENT_DIR = PurePath.parent


class WindowIdentificate(Toplevel):

    def __init__(self, crater_size="", longitude="", latitude="", *args, **kwargs):
        """Docstring"""
        super().__init__(*args, **kwargs)
        self.crater_size = crater_size
        self.longitude = longitude
        self.latitude = latitude
        self.geometry("285x380")
        self.title("Identifier le cratere.")
        self.create_widgets()
        self.place_widgets()
        self.write_listbox()
    
    def create_widgets(self):
        """Docstring"""
        # Frames.
        self.frame_info = Frame(self)
        self.frame_result = Frame(self)
        self.button = Button(self, text="quit", command=self.quit)
        # Inside frame_infos.
        self.label_diameter = Label(self.frame_info, text=f"Diamètre: {self.crater_size} ; ")
        self.label_longitude = Label(self.frame_info, text=f"Longitude: {self.longitude} ; ")
        self.label_latitude = Label(self.frame_info, text=f"Latitude: {self.latitude}")
        # Inside frame_result.
        self.label_listBox = Label(self.frame_result, text="Liste des cratères correspondant.")  
        self.listbox = Listbox(self.frame_result, width=40, height=19)
    
    def place_widgets(self):
        """Docstring"""
        # Frames.
        self.frame_info.grid(row=0, column=0, columnspan=2)
        self.frame_result.grid(row=2, column=0, columnspan=2, padx=0, pady=5)
        self.button.grid(row=3)
        # Inside frame_infos.
        self.label_diameter.grid(row=0, column=0)
        self.label_longitude.grid(row=0, column=1)
        self.label_latitude.grid(row=0, column=2)
        # Inside frame_result.
        self.label_listBox.grid(row=0, column=0, columnspan=2, padx=20, pady=10)
        self.listbox.grid(row=1, column=0, padx=20)
    
    def search_match(self):
        """Docstring"""
        if all((self.isfloat(self.crater_size), self.isfloat(self.longitude), self.isfloat(self.latitude))):
            return Calculator.identificat_crater(
                            float(self.crater_size),
                            float(self.longitude),
                            float(self.latitude)
                        )

    def isfloat(self, _string):
        """Docstring"""
        try:
            float(_string)
            return True
        except ValueError:
            return False
    
    def show_result(self, matchs:dict):
        """Docstring"""
        result = sorted(matchs.items(), key=lambda x: x[1], reverse=True)
        pivot = int(len(result)/2)
        i = 0
        for k, v in result[:pivot]:
            self.listbox.insert(i,f"{k} a {v}%")
            i+=1
    
    def write_listbox(self):
        """Docstring"""
        self.show_result(self.search_match())


if __name__ == '__main__':
    APP = WindowIdentificate(94, longitude=-20, latitude=10)
    APP.mainloop()