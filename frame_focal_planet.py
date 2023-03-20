import json
from tkinter import *
from tkinter import ttk
from pathlib import Path

from calculator import Calculator
# from astronomie import CHAR_DIGITS, ASTRES


astres_file = Path("data/astres.json")
with open(astres_file, "r") as f:
    ASTRES = json.load(f)

# Valid Characters for digits.
CHAR_DIGITS = ".,-;" + "".join([str(i) for i in range(0, 10)])


class FrameByPlanet(LabelFrame):

    def __init__(self, container, *args, **kwargs):
        """Docstring"""
        super().__init__(container, *args, **kwargs)
        self.container = container
        self.create_widgets()
        self.place_widgets()

    def create_widgets(self):
        """Docstring"""
        self._create_combobox()
        self._create_labels()
        self._create_entrys()
        self._create_buttons()
    
    def _create_combobox(self):
        """Docstring"""
        # Combobox camera.
        astres_list = [i.capitalize() for i in ASTRES.keys()]
        self.combo_astre = ttk.Combobox(self, values=astres_list)
        self.combo_astre.config(state=NORMAL)
        self.combo_astre.bind("<<ComboboxSelected>>", self.set_astre)
        self.combo_astre.current(0)

    def _create_labels(self):
        """Docstring"""
        self.label_astre = Label(self, text="Selectionner un astre:")
        self.label_astreSize = Label(self, text="Diamètre de l'astre:")
        self.label_pixelNumber = Label(self, text="Taille de l'astre (pixels):")
        self.label_distanceKm = Label(self, text="Distance de la planète (Km):")

    def _create_entrys(self):
        """Docstring"""
        validation = self.register(self.only_numbers)
        # planet Diameter.
        self.entry_astreSize = Entry(self)
        self.entry_astreSize.config(validate="key", validatecommand=(validation, '%S'))
        self.entry_astreSize.bind('<KeyPress-Return>', self.container.trigger)
        # planet size in pixels.
        self.entry_pixelNumber = Entry(self)
        self.entry_pixelNumber.config(validate="key", validatecommand=(validation, '%S'))
        self.entry_pixelNumber.bind('<KeyPress-Return>', self.container.trigger)
        # result.
        self.entry_distanceKm = Entry(self)
        self.entry_distanceKm.config(validate="key", validatecommand=(validation, '%S'))
        self.entry_distanceKm.bind('<KeyPress-Return>', self.container.trigger)

    def _create_buttons(self):
        """Docstring"""
        self.button_openImage = Button(self, text="Ouvrir image...", command=lambda :self.container.open_image(self))
    
    def place_widgets(self):
        """Docstring"""
        self.label_astre.grid(row=1, column=0)
        self.combo_astre.grid(row=1, column=1)
        self.label_astreSize.grid(row=2, column=0)
        self.entry_astreSize.grid(row=2, column=1)
        self.label_distanceKm.grid(row=3, column=0)
        self.entry_distanceKm.grid(row=3, column=1)
        self.button_openImage.grid(row=5, column=0, columnspan=2)
        self.label_pixelNumber.grid(row=6, column=0)
        self.entry_pixelNumber.grid(row=6, column=1)
        for widget in self.winfo_children():
            widget.grid_configure(pady=10, padx=10)

    def set_astre(self, event):
        """Docstring"""
        selected = self.combo_astre.get().lower()
        if selected != "--":
            _max = ASTRES[selected]['dist_min']
            _min = ASTRES[selected]['dist_max'] 
            distanceKm = int(Calculator.average_dist(_min, _max))
            self.entry_astreSize.config(state=NORMAL)
            self.entry_astreSize.delete(0, END)
            self.entry_distanceKm.delete(0, END)
            self.entry_astreSize.insert(0, ASTRES[selected]['size'])
            self.entry_distanceKm.insert(0, distanceKm)
            self.entry_astreSize.config(state=DISABLED)
        self.container.trigger()

    def only_numbers(self, string_):
        """Docstring"""
        return all([(char in CHAR_DIGITS) for char in string_])