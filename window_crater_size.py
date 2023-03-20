import json
from pathlib import PurePath, Path
from tkinter import *
from tkinter import filedialog

from PIL import Image, UnidentifiedImageError

from calculator import Calculator
from window_identificate import WindowIdentificate
from window_image import WindowImage
from window_coordinates import WindowCoordinates
# from astronomie import CURRENT_DIR


# Set current Path.
CURRENT_DIR = PurePath.parent

astres_file = Path("data/astres.json")
with open(astres_file, "r") as f:
    ASTRES = json.load(f)

# Comput moon distance
_min = ASTRES['moon']['dist_min']
_max = ASTRES['moon']['dist_max']
MOON_DISTANCE = int(Calculator.average_dist(_min, _max))


class WindowCraterSize(Toplevel):

    def __init__(self, pixel_size="", focal="", *args, **kwargs):
        """Docstring"""
        super().__init__(*args, **kwargs)
        self.pixel_size = pixel_size
        self.focal = focal
        self.geometry("340x515")
        self.title("Calcul de la dimension d'un cratère")
        self.create_widgets()
        self.place_widgets()
    
    def create_widgets(self):
        """Docstring"""
        self._create_frames()
        self._create_labels()
        self._create_entrys()
        self._create_buttons()
    
    def _create_frames(self):
        """Docstring"""
        # Frames.
        self.frame_equipment = LabelFrame(self, text="Equipement")
        self.frame_info = LabelFrame(self, text="Cratères/Photo")
        self.frame_result = LabelFrame(self, text="Résultat")

    def _create_labels(self):
        """Docstring"""
        # Frame equipment.
        self.label_focalLength = Label(self.frame_equipment, text="Focale:")
        self.label_pixelSize = Label(self.frame_equipment, text="Taille du pixels (microns):")
        # Frame info.
        self.label_moonDistance = Label(self.frame_info, text="Distance de la lune (Km):")
        self.label_pixelNumber = Label(self.frame_info, text="Taille du cratère (pixel):")
        self.label_latitude = Label(self.frame_info, text="Latitude (degrés):")
        self.label_longitude = Label(self.frame_info, text="Longitude (degrés -180/180):")
        # Frame result.
        self.label_craterSize = Label(self.frame_result, text="Taille du cratère (Km):")
        self.label_craterSizePlus = Label(self.frame_result, text="Taille du cratère Corrigé (Km):")

    def _create_entrys(self):
        """Docstring"""
        # Frame equipment.
        self.entry_focalLength = Entry(self.frame_equipment)
        self.entry_focalLength.insert(0, self.focal)
        self.entry_pixelSize = Entry(self.frame_equipment)
        self.entry_pixelSize.insert(0, self.pixel_size)
        # Frame info.
        self.entry_moonDistance = Entry(self.frame_info)
        self.entry_moonDistance.insert(0, MOON_DISTANCE)
        self.entry_pixelNumber = Entry(self.frame_info)
        self.entry_pixelNumber.insert(0, "14.5")  # a suppr
        self.entry_latitude = Entry(self.frame_info)
        self.entry_latitude.insert(0, "38")  # a suppr
        self.entry_longitude = Entry(self.frame_info)
        self.entry_longitude.insert(0, "40.5")  # a suppr
        # Frame result.
        self.entry_craterSize = Entry(self.frame_result, state='readonly')
        self.entry_craterSizePlus = Entry(self.frame_result, state='readonly')

    def _create_buttons(self):
        """Docstring"""
        # Frame info.
        self.button_openImage        = Button(self.frame_info, text="Ouvrir image...", command=self.open_image)
        self.button_Coordinates      = Button(self.frame_info, text="Afficher les coordonées", command=self.show_windowCoordinates)
        # Frame result.
        self.button_computSize       = Button(self.frame_result, text="Calcul", command=self.compute_size)  # A suppri pour Trigger
        self.button_indentification  = Button(self.frame_result, text="Identifier", state=DISABLED, command=self.crater_identify)

    def place_widgets(self):
        """Docstring"""
        # Frame equipment.
        self.label_focalLength.grid(row=1, column=0)
        self.entry_focalLength.grid(row=1, column=1)
        self.label_pixelSize.grid(row=3, column=0)
        self.entry_pixelSize.grid(row=3, column=1)
        # Frame info.
        self.label_moonDistance.grid(row=0, column=0)
        self.entry_moonDistance.grid(row=0, column=1)
        self.button_openImage.grid(row=1, column=0, columnspan=2)
        self.label_pixelNumber.grid(row=2, column=0)
        self.entry_pixelNumber.grid(row=2, column=1)
        self.label_latitude.grid(row=3, column=0)
        self.entry_latitude.grid(row=3, column=1)
        self.label_longitude.grid(row=5, column=0)
        self.entry_longitude.grid(row=5, column=1)
        self.button_Coordinates.grid(row=6, column=0, columnspan=2)
        # Frame result.
        self.button_computSize.grid(row=0, column=0, columnspan=2)  # Supprimer pour trigger
        self.label_craterSize.grid(row=1, column=0)
        self.entry_craterSize.grid(row=1, column=1)
        self.label_craterSizePlus.grid(row=2, column=0)
        self.entry_craterSizePlus.grid(row=2, column=1)  # Mettre en avant
        self.button_indentification.grid(row=3, column=0, columnspan=2)
        
        for frame in self.winfo_children():
            frame.grid(pady=10, padx=15, ipadx=5, ipady=4)
            for wid in frame.children.values():
                wid.grid_configure(padx=2, pady=4)

    
    def show_windowCoordinates(self):
        """Docstring"""
        WindowCoordinates()

    def open_image(self):
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
            self.window_image = WindowImage(img, parent=self)
        
    def compute_size(self):
        """Docstring"""
        data_focal        = float(self.entry_focalLength.get())
        data_pixelSize    = float(self.entry_pixelSize.get())
        data_pixelNumber  = float(self.entry_pixelNumber.get())
        data_moonDistance = float(self.entry_moonDistance.get())
        data_latitude     = float(self.entry_latitude.get())
        data_longitude    = float(self.entry_longitude.get())
        datas = {
            "focal"         : data_focal,
            "pixel_size"    : data_pixelSize,
            "pixel_number"  : data_pixelNumber,
            "moon_distance" : data_moonDistance,
            "latitude"      : data_latitude,
            "longitude"     : data_longitude
        }
        result = Calculator.comput_craterSize(datas)
        self.show_result(result)
    
    def show_result(self, result):
        """Docstring"""
        self.entry_craterSize.config(state=NORMAL)
        self.entry_craterSize.delete(0, END)
        self.entry_craterSize.insert(0, round(result['crater_size'], 2))
        self.entry_craterSize.config(state='readonly')

        self.entry_craterSizePlus.config(state=NORMAL)
        self.entry_craterSizePlus.delete(0, END)
        self.entry_craterSizePlus.insert(0, round(result['crater_sizeP'], 2))
        self.entry_craterSizePlus.config(state='readonly')

        self.button_indentification.config(state=NORMAL)

    def crater_identify(self):
        """Docstring"""
        self.compute_size()
        diameter = float(self.entry_craterSizePlus.get())
        longitude = float(self.entry_longitude.get())
        latitude = float(self.entry_latitude.get())
        WindowIdentificate(diameter, longitude, latitude)


if __name__ == '__main__':
    APP = WindowCraterSize(focal=2000, pixel_size=3.75)
    APP.mainloop()