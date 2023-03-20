import math
from tkinter import *
from tkinter import filedialog
from pathlib import PurePath

from PIL import Image, UnidentifiedImageError

# from window_image import WindowImage
from window_image_altitude import WindowImage
from window_coordinates import WindowCoordinates

# Set current Path.
CURRENT_DIR = PurePath.parent


class WindowAltitude(Tk):

    def __init__(self, focal="", pixel_size="", *args, **kwargs):
        """Docstring"""
        super().__init__(*args, **kwargs)
        self.focal = focal
        self.pixel_size = pixel_size
        self.geometry("360x550")
        self.title("Calcul altitude des montagnes")
        self.create_widgets()
        self.place_widgets()
        self.update_entry(self.entry_focalLength, str(self.focal))
        self.update_entry(self.entry_pixelSize, str(self.pixel_size))

    def update_entry(self, entry, text=''):
        """Docstring"""
        entry.delete(0, END)
        entry.insert(0, text)
    
    def create_widgets(self):
        """Docstring"""
        self._create_frames()
        self._create_labels()
        self._create_entrys()
        self._create_buttons()
        
    def _create_frames(self):
        """Docstring"""
        # frame telescope
        self.frame_equipement = LabelFrame(self, text="Equipements", labelanchor="nw")
        # frame terminateur
        self.frame_terminator = LabelFrame(self, text="Terminateur/Mont", labelanchor="nw")
        # frame résultat
        self.frame_result = LabelFrame(self, text= "Résultat", labelanchor= "nw")

    def _create_labels(self):
        """Docstring"""
        # frame equipement
        self.label_focalLength = Label(self.frame_equipement, text="Focale:")
        self.label_pixelSize = Label(self.frame_equipement, text="taille des pixels:")
        # frame terminateur
        self.label_moonDistance = Label(self.frame_terminator, text="Distance de la lune (KM):")
        self.label_mountainLon = Label(self.frame_terminator, text="Longitude du mont (Degrés):")
        self.label_mountainLat = Label(self.frame_terminator, text="Latitude du mont (Degrés):")
        self.label_terminator_distance = Label(self.frame_terminator, text="Distance mont/terminateur (Pixels):")
        self.label_shadowSizePx = Label(self.frame_terminator, text="Taille de l'ombre (Pixels):")
        # frame resultat
        self.label_sunHeight = Label(self.frame_result, text="Hauteur du soleil (degrés):")
        self.label_shadowSizeKm = Label(self.frame_result, text="Taille de l'ombre (KM):")
        self.label_altitude = Label(self.frame_result, text="Altitude (KM):")
    
    def _create_entrys(self):
        """Docstring"""
        # frame equipement
        self.entry_focalLength = Entry(self.frame_equipement)
        self.entry_pixelSize = Entry(self.frame_equipement)
        # frame terminateur
        self.entry_moonDistance = Entry(self.frame_terminator)
        self.entry_moonDistance.insert(0, "400000")
        self.entry_mountainLon = Entry(self.frame_terminator)
        self.entry_montainLat = Entry(self.frame_terminator)
        self.entry_terminator_distance = Entry(self.frame_terminator)
        self.entry_shadowSizePx = Entry(self.frame_terminator)
        # frame resultat
        self.entry_sunHeight = Entry(self.frame_result)
        self.entry_sunHeight.config(state=DISABLED)
        self.entry_shadowSizeKm = Entry(self.frame_result)
        self.entry_shadowSizeKm.config(state=DISABLED)
        self.entry_altitude = Entry(self.frame_result)
        self.entry_altitude.config(state=DISABLED)

    def _create_buttons(self):
        """Creer tout les buttons de la fenetre"""
        # frame terminateur
        self.button_openImage = Button(self.frame_terminator, text="Ouvrir image...",command=self.open_image)
        self.button_showCoordinates = Button(self.frame_terminator, text="Afficher les coordonées", command=self.show_windowCoordinates)
        self.button_calcul = Button(self.frame_result, text="Calcul", command= self.calcul_altitude)

    def place_widgets(self):
        """Pour placer toutes tes frames, labels, entrys, buttons..."""
        # frames
        self.frame_equipement.pack(pady=10)
        self.frame_terminator.pack(pady=10)
        self.frame_result.pack(pady=10)
        # frame equipement
        self.label_focalLength.grid(row=1, column=0, pady=5, padx=5)
        self.entry_focalLength.grid(row=1, column=1, pady=5, padx=5)
        self.label_pixelSize.grid(row=3, column=0, pady=5, padx=5)
        self.entry_pixelSize.grid(row=3, column=1, pady=5, padx=5)
        # frame teminateur
        self.label_moonDistance.grid(row=0, column=0, pady=5, padx=5)
        self.entry_moonDistance.grid(row=0, column=1, pady=5, padx=5)
        self.button_openImage.grid(row=1, column=0, columnspan=2, pady=5, padx=5)
        self.label_mountainLon.grid(row=2, column=0, pady=5, padx=5)
        self.entry_mountainLon.grid(row=2, column=1, pady=5, padx=5)
        self.label_mountainLat.grid(row=3, column=0, pady=5, padx=5)
        self.entry_montainLat.grid(row=3, column=1, pady=5, padx=5)
        self.label_terminator_distance.grid(row=4, column=0, pady=5, padx=5)
        self.entry_terminator_distance.grid(row=4, column=1, pady=5, padx=5)
        self.label_shadowSizePx.grid(row=5, column=0, pady=5, padx=5)
        self.entry_shadowSizePx.grid(row=5, column=1, pady=5, padx=5)
        self.button_showCoordinates.grid(row=6, column=0, columnspan=2, pady=5, padx=5)
        # frame resultat
        self.button_calcul.grid(row=0, column=0, columnspan=2, pady=5, padx=5)
        self.label_sunHeight.grid(row=1, column=0, pady=5, padx=5)
        self.label_shadowSizeKm.grid(row=2, column=0, pady=5, padx=5)
        self.label_altitude.grid(row=3, column=0, pady=5, padx=5)
        self.entry_sunHeight.grid(row=1, column=1, pady=5, padx=5)
        self.entry_shadowSizeKm.grid(row=2, column=1, pady=5, padx=5)
        self.entry_altitude.grid(row=3, column=1, pady=5, padx=5)

    def calcul_altitude(self):
        """Docstring"""
        focal = float(self.entry_focalLength.get())
        pixel_size = float(self.entry_pixelSize.get())
        distance_moon = float(self.entry_moonDistance.get())
        mountainLat = float(self.entry_montainLat.get())
        mountainLon = float(self.entry_mountainLon.get())
        mountainTerminator_distance = float(self.entry_terminator_distance.get())
        shadowSize = float(self.entry_shadowSizePx.get())
        meridian = (mountainLat*mountainLat) + (mountainLon*mountainLon)
        meridian2 = math.sqrt(meridian)
        meridianR = math.radians(meridian2)

        arcs_field = (pixel_size / focal) * 206.265
        degres_field = (arcs_field / 3600) / 2
        radian_field = math.radians(degres_field)  # Conversion degrés en radians.
        tan_field = math.tan(radian_field)
        mountainTerminator_distancekm = tan_field * distance_moon * mountainTerminator_distance * 2
        distance_mont_terminateur_km_cor = mountainTerminator_distancekm / math.cos(meridianR)

        latitude_mont_rad = math.radians(mountainLat)
        rapport_degre_km = (10900 * math.cos(latitude_mont_rad)) / 360
        sun_height = distance_mont_terminateur_km_cor / rapport_degre_km

        shadowSize_km = tan_field * distance_moon * shadowSize * 2
        shadowSize_km_coor = shadowSize_km / math.cos(meridianR)

        altitude = shadowSize_km_coor * math.tan(math.radians(sun_height))

        self.entry_sunHeight.config(state=NORMAL)
        self.entry_sunHeight.delete(0, END)
        self.entry_sunHeight.insert(0, round(sun_height, 2))
        self.entry_sunHeight.config(state=DISABLED)
        self.entry_shadowSizeKm.config(state=NORMAL)
        self.entry_shadowSizeKm.delete(0, END)
        self.entry_shadowSizeKm.insert(0, round(shadowSize_km_coor, 2))
        self.entry_shadowSizeKm.config(state=DISABLED)
        self.entry_altitude.config(state=NORMAL)
        self.entry_altitude.delete(0, END)
        self.entry_altitude.insert(0, round(altitude, 3))
        self.entry_altitude.config(state=DISABLED)

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


if __name__ == '__main__':
    APP = WindowAltitude(1500.0, 3.75)
    APP.mainloop()