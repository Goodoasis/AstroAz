from tkinter import *
from tkinter import filedialog
from pathlib import PurePath

from PIL import Image, UnidentifiedImageError

from calculator import Calculator
from window_image import WindowImage
from frame_focal_crater import FrameByCrater
from frame_focal_planet import FrameByPlanet


# Set current Path.
CURRENT_DIR = PurePath.parent
# Valid Characters for digits.
CHAR_DIGITS = ".,-;" + "".join([str(i) for i in range(0, 10)])


class WindowFocalReal(Toplevel):

    def __init__(self, pixel_size="", *args, **kwargs):
        """Docstring"""
        super().__init__(*args, **kwargs)
        self.init_pixelSize = pixel_size
        self.geometry("380x500")
        self.resizable(0, 0)
        self.title("Calcul de la focale réelle.")
        self.create_widgets()
        self.place_widgets()

    @property
    def pixel_size(self):
        """Docstring"""
        return self.entry_pixelSize.get() or self.init_pixelSize
    
    def create_widgets(self):
        """Docstring"""
        self._create_labels()
        self._create_entrys()
        self._create_radios()
        self._create_buttons()
        self.frame_crater = FrameByCrater(self, text="D'après un cratère. ", width=350, height=280)
        self.frame_planet = FrameByPlanet(self, text="D'après un astres. ", width=350, height=280)
        self.frame_planet.grid_propagate(False)
    
    def _create_labels(self):
        """Docstring"""
        # Before Subframe.
        self.label_pixelSize = Label(self, text="Taille du pixels (microns):")
        # After Subframe.
        self.label_focalReal = Label(self, text="Focale réelle:  ")

    def _create_entrys(self):
        """Docstring"""
        validation = self.register(self.only_numbers)
        self.entry_pixelSize = Entry(self)
        self.entry_pixelSize.insert(0, self.pixel_size)
        self.entry_pixelSize.config(validate="key", validatecommand=(validation, '%S'))
        self.entry_pixelSize.bind('<KeyPress-Return>', self.trigger)

    def _create_buttons(self):
        """Docstring"""
        self.button_computFocal = Button(self, text="Calcul Focale Réelle", command=self.trigger)

    def _create_radios(self):
        """Docstring"""
        self.radio_var = StringVar(master=self)
        self.radio_var.set("crater")
        self.radio_crater = Radiobutton(self, variable=self.radio_var, value="crater", text="Cratere", command=self.radio_callback)
        self.radio_planet = Radiobutton(self, variable=self.radio_var, value="planet", text="Planète", command=self.radio_callback)

    def radio_callback(self):
        """Docstring"""
        if self.radio_var.get() == "crater":
            self.frame_planet.grid_remove()
            self.frame_crater.grid(row=4, column=0, columnspan=2, ipadx=5, ipady=5, pady=10, padx=10)
        elif self.radio_var.get() == "planet":
            self.frame_crater.grid_remove()
            self.frame_planet.grid(row=4, column=0, columnspan=2, ipadx=5, ipady=5, pady=10, padx=10)
        self.trigger()

    def place_widgets(self):
        """Docstring"""
        self.label_pixelSize.grid(row=2, column=0)
        self.entry_pixelSize.grid(row=2, column=1)
        self.radio_crater.grid(row=3, column=0)
        self.radio_planet.grid(row=3, column=1)
        self.frame_crater.grid(row=4, column=0, columnspan=2, ipadx=5, ipady=5)
        self.frame_crater.grid_propagate(False)
        for widget in self.winfo_children():
            if widget.winfo_name() == "!framebyplanet":
                continue
            widget.grid_configure(pady=10, padx=10)
        # self.frame_planet.grid_forget()
        self.button_computFocal.grid(row=8, column=0, columnspan=2)
        self.label_focalReal.grid(row=10, column=0, columnspan=2)


    def open_image(self, event):
        """Docstring"""
        filetypes = (
            ('jpeg files', '*.jpg'),
            ('png files', '*.png'),
            ('All files', '*.*')
            )
        filename = filedialog.askopenfilename(title='Open a file', initialdir=CURRENT_DIR, filetypes=filetypes)
        try:
            img = Image.open(filename)
        except UnidentifiedImageError:
            print("Fichier non pris en charge")
        else:
            self.window_image = WindowImage(img, parent=event)

    def trigger(self, event=None):
        """Docstring"""
        if self.radio_var.get() == "planet":
            obj_distance = self.frame_planet.entry_distanceKm.get()
            obj_sizeKm = self.frame_planet.entry_astreSize.get()
            obj_sizePx = self.frame_planet.entry_pixelNumber.get()
            latitude = 0
            longitude = 0
        elif self.radio_var.get() == "crater":
            obj_distance = self.frame_crater.entry_moonDistance.get()
            obj_sizeKm = self.frame_crater.entry_craterSize.get()
            obj_sizePx = self.frame_crater.entry_pixelNumber.get()
            latitude = self.frame_crater.entry_latitude.get()
            longitude = self.frame_crater.entry_longitude.get()
            
        if all([self.isfloat(self.pixel_size), self.isfloat(obj_distance), self.isfloat(obj_sizeKm), self.isfloat(obj_sizePx)]):
            focal_real = int(Calculator.comput_focalReal(
                                        float(self.pixel_size),
                                        float(obj_sizeKm),
                                        float(obj_sizePx),
                                        float(obj_distance),
                                        float(latitude),
                                        float(longitude)
                                        ))
        else:
            focal_real = ""

        self.label_focalReal.config(text=f"Focale réelle:  {focal_real}")

    def isfloat(self, _string):
        """Docstring"""
        try:
            float(_string)
            return True
        except ValueError:
            return False

    def only_numbers(self, string_):
        """Docstring"""
        return all([(char in CHAR_DIGITS) for char in string_])

if __name__ == '__main__':
    APP = WindowFocalReal(pixel_size="3.75")
    APP.mainloop()