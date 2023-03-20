import json
from tkinter import *
from tkinter import ttk
from pathlib import Path, PurePath

from calculator import Calculator
from window_coordinates import WindowCoordinates
# from astronomie import CHAR_DIGITS, CRATERES, MOON_DISTANCE


# Set current Path.
CURRENT_DIR = PurePath.parent

crateres_file = Path("data/craters_visible.json")
with open(crateres_file, "r", encoding='utf-8') as f:
    CRATERES = json.load(f)

astres_file = Path("data/astres.json")
with open(astres_file, "r") as f:
    ASTRES = json.load(f)

# Comput moon distance
_min = ASTRES['moon']['dist_min']
_max = ASTRES['moon']['dist_max']
MOON_DISTANCE = int(Calculator.average_dist(_min, _max))


# Valid Characters for digits.
CHAR_DIGITS = ".,-;" + "".join([str(i) for i in range(0, 10)])


class FrameByCrater(LabelFrame):

    def __init__(self, container, *args, **kwargs):
        """Docstring"""
        super().__init__(container, *args, **kwargs)
        self.container = container
        self.create_widgets()
        self.place_widgets()

    def create_widgets(self):
        """Docstring"""
        self._create_labels()
        self._create_combobox()
        self._create_entrys()
        self._create_buttons()
    
    def _create_combobox(self):
        """Docstring"""
        crateres_list = [i.title() for i in CRATERES.keys()]
        self.combo_selectObj = ttk.Combobox(self, values=crateres_list)
        self.combo_selectObj.bind("<<ComboboxSelected>>", self.set_combo)
        self.combo_selectObj.current(0)
    
    def _create_labels(self):
        """Docstring"""
        self.label_selectObj = Label(self, text="Selectionnez un cratère:")
        self.label_craterSize = Label(self, text="Diamètre du cratère (Km):")
        self.label_moonDistance = Label(self, text="Distance de la lune (Km):")
        self.label_pixelNumber = Label(self, text="Diamètre du cratère (pixels):")
        self.label_latitude = Label(self, text="Latitude (degrés):")
        self.label_longitude = Label(self, text="Longitude (degrés):")

    def _create_entrys(self):
        """Docstring"""
        validation = self.register(self.only_numbers)
        self.entry_craterSize = Entry(self)
        self.entry_craterSize.config(validate="key", validatecommand=(validation, '%S'))
        self.entry_craterSize.bind("<KeyPress-Return>", self.container.trigger)
        self.entry_moonDistance = Entry(self)
        self.entry_moonDistance.config(validate="key", validatecommand=(validation, '%S'))
        self.entry_moonDistance.bind("<KeyPress-Return>", self.container.trigger)
        self.entry_moonDistance.insert(0, MOON_DISTANCE)
        self.entry_pixelNumber = Entry(self)
        self.entry_pixelNumber.config(validate="key", validatecommand=(validation, '%S'))
        self.entry_pixelNumber.bind("<KeyPress-Return>", self.container.trigger)
        # self.entry_pixelNumber.insert(0, "88")  # a suppr
        self.entry_latitude = Entry(self)
        self.entry_latitude.config(validate="key", validatecommand=(validation, '%S'))
        self.entry_latitude.bind("<KeyPress-Return>", self.container.trigger)
        # self.entry_latitude.insert(0, "26")  # a suppr
        self.entry_longitude = Entry(self)
        self.entry_longitude.config(validate="key", validatecommand=(validation, '%S'))
        self.entry_longitude.bind("<KeyPress-Return>", self.container.trigger)
        # self.entry_longitude.insert(0, "11")  # a suppr

    def _create_buttons(self):
        """Docstring"""
        self.button_showCoordinates = Button(self, text="Afficher les coordonées", command=self.show_windowCoordinates)
        self.button_openImage = Button(self, text="Ouvrir image...", command=lambda: self.container.open_image(self))
    
    def place_widgets(self):
        """Docstring"""
        self.label_selectObj.grid(row=0, column=0)
        self.combo_selectObj.grid(row=0, column=1)
        self.label_craterSize.grid(row=1, column=0)
        self.entry_craterSize.grid(row=1, column=1)
        self.label_moonDistance.grid(row=3, column=0)
        self.entry_moonDistance.grid(row=3, column=1)
        self.button_showCoordinates.grid(row=4, column=1)
        self.button_openImage.grid(row=4, column=0)
        self.label_pixelNumber.grid(row=5, column=0)
        self.entry_pixelNumber.grid(row=5, column=1)
        self.label_latitude.grid(row=6, column=0)
        self.entry_latitude.grid(row=6, column=1)
        self.label_longitude.grid(row=7, column=0)
        self.entry_longitude.grid(row=7, column=1)
        for widget in self.winfo_children():
            widget.grid_configure(pady=8, padx=10)

    def show_windowCoordinates(self):
        """Docstring"""
        WindowCoordinates()

    def set_combo(self, event):
        """Docstring"""
        self.entry_craterSize.config(state=NORMAL)
        self.entry_latitude.config(state=NORMAL)
        self.entry_longitude.config(state=NORMAL)
        self.entry_craterSize.delete(0, END)
        self.entry_latitude.delete(0, END)
        self.entry_longitude.delete(0, END)

        selected = self.combo_selectObj.get()
        if selected != "--":
            self.entry_craterSize.config(state=NORMAL)
            self.entry_latitude.config(state=NORMAL)
            self.entry_longitude.config(state=NORMAL)
            self.entry_craterSize.delete(0, END)
            self.entry_latitude.delete(0, END)
            self.entry_longitude.delete(0, END)
            self.entry_craterSize.insert(0, CRATERES[selected]['diameter'])
            self.entry_latitude.insert(0, CRATERES[selected]['latitude'])
            self.entry_longitude.insert(0, CRATERES[selected]['longitude'])
            self.entry_craterSize.config(state=DISABLED)
            self.entry_latitude.config(state=DISABLED)
            self.entry_longitude.config(state=DISABLED)
        self.container.trigger()

    def only_numbers(self, string_):
        """Docstring"""
        return all([(char in CHAR_DIGITS) for char in string_])