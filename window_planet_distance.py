import json
from tkinter import *
from tkinter import ttk, filedialog
from pathlib import Path, PurePath

from PIL import Image, UnidentifiedImageError

from calculator import Calculator
from window_image import WindowImage


# Set current Path.
CURRENT_DIR = PurePath.parent

astres_file = Path("data/astres.json")
with open(astres_file, "r") as f:
    ASTRES = json.load(f)

# Valid Characters for digits.
CHAR_DIGITS = ".,-;" + "".join([str(i) for i in range(0, 10)])    


class WindowPlanetDistance(Toplevel):

    def __init__(self, pixel_size="", focal="", *args, **kwargs):
        """Docstring"""
        super().__init__(*args, **kwargs)
        self.pixel_size_init = pixel_size
        self.focal_init = focal
        self.geometry("378x444")
        self.title("Calcul de la distance de l'astre.")
        self.create_widgets()
        self.place_widgets()

    @property
    def focal(self):
        """Docstring"""
        return self.entry_focalLength.get() or self.focal_init

    @property
    def pixel_size(self):
        """Docstring"""
        return self.entry_pixelSize.get() or self.pixel_size_init

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
    
    def create_widgets(self):
        """Docstring"""
        self.requiere_widget = []
        self.Var_slider = IntVar()
        self._create_frames()
        self._create_labels()
        self._create_entrys()
        self._create_buttons()
        self._create_combobox()
        self._create_slider()
    
    def _create_frames(self):
        self.frame_equipment = LabelFrame(self, text="Equipement")
        self.frame_info = LabelFrame(self, text="Infos")
        self.frame_result = LabelFrame(self, text="Résultat", width=338, height=170)
        self.frame_result.grid_propagate(False)
        self.sub_frame = Frame(self.frame_result)

    def _create_labels(self):
        """Docstring"""
        # Frame equipment.
        self.label_focalLength = Label(self.frame_equipment, text="Focale:")
        self.label_pixelSize = Label(self.frame_equipment, text="Taille du pixels (microns):")
        # Frame info.
        self.label_astre = Label(self.frame_info, text="Selectionner un astre: ")
        self.label_pixelNumber = Label(self.frame_info, text="Taille de l'astre (pixels):")
        # Frame result.
        self.label_distanceKm = Label(self.frame_result, text="Distance de la planète (Km):")
        self.label_distanceUa = Label(self.frame_result, text="Distance de la planète (UA):")
        self.label_sliderMin = Label(self.sub_frame, text="Minimum", width=10)
        self.label_sliderMax = Label(self.sub_frame, text="Maximum")

    def _create_entrys(self):
        """Docstring"""
        validation = self.register(self.only_numbers)
        # Frame equipment.
        self.entry_focalLength = Entry(self.frame_equipment)  # other config are after insertion init value.
        self.entry_focalLength.insert(0, self.focal_init)
        self.entry_focalLength.config(validate="key", validatecommand=(validation, '%S'))
        self.entry_focalLength.bind('<KeyPress-Return>', self.trigger)
        self.entry_pixelSize = Entry(self.frame_equipment)  # other config are after insertion init value.
        self.entry_pixelSize.insert(0, self.pixel_size_init)
        self.entry_pixelSize.config(validate="key", validatecommand=(validation, '%S'))
        self.entry_pixelSize.bind('<KeyPress-Return>', self.trigger)
        # Frame info.
        self.entry_pixelNumber = Entry(self.frame_info, validate="key", validatecommand=(validation, '%S'))
        self.entry_pixelNumber.bind('<KeyPress-Return>', self.trigger)
        # Frame result.
        self.entry_distanceKm = Entry(self.frame_result)
        self.entry_distanceUa = Entry(self.frame_result)
        # Add widgets to the requiere for compute.
        self.requiere_widget.append(self.entry_focalLength)
        self.requiere_widget.append(self.entry_pixelSize)
        self.requiere_widget.append(self.entry_pixelNumber)

    def _create_buttons(self):
        """Docstring"""
        # Frame info.
        self.button_openImage      = Button(self.frame_info, text="Ouvrir image", command=self.open_image)
        # Frame Result.
        self.button_computDistance = Button(self.frame_result, text="Calcul", command=self.comput_distance)

    def _create_combobox(self):
        """Docstring"""
        # Frame info.
        astres_list = [i.capitalize() for i in ASTRES.keys()]
        self.combo_astre = ttk.Combobox(self.frame_info, values=astres_list)
        self.combo_astre.config(state=NORMAL)
        self.combo_astre.bind("<<ComboboxSelected>>", self.set_astre)
        self.combo_astre.current(0)
        # Add to requiere widget to comput
        self.requiere_widget.append(self.combo_astre)

    def _create_slider(self):
        """Docstring"""
        # Frame result.
        self.slider = Scale(self.sub_frame, orient=HORIZONTAL, label="Distance Terre/Astre")
        self.slider.config(length=180)
        self.slider.config(from_=0, to=100, variable=self.Var_slider)

    def place_widgets(self):
        """Docstring"""
        # Frame equipment.
        self.label_focalLength.grid(row=0, column=0)
        self.entry_focalLength.grid(row=0, column=1)
        self.label_pixelSize.grid(row=1, column=0)
        self.entry_pixelSize.grid(row=1, column=1)
        # Frame infos.
        self.label_astre.grid(row=0, column=0)
        self.combo_astre.grid(row=0, column=1)
        self.button_openImage.grid(row=1, column=0, columnspan=2)
        self.label_pixelNumber.grid(row=2, column=0)
        self.entry_pixelNumber.grid(row=2, column=1)
        # Frame result.
        self.button_computDistance.grid(row=0, column=0, columnspan=2)
        self.label_distanceKm.grid(row=1, column=0)
        self.entry_distanceKm.grid(row=1, column=1)
        self.label_distanceUa.grid(row=2, column=0)
        self.entry_distanceUa.grid(row=2, column=1)
        self.sub_frame.grid(columnspan=2)
        # subframe
        self.label_sliderMin.grid(row=0, column=0, sticky="s")
        self.slider.grid(row=0, column=1, columnspan=2)
        self.label_sliderMax.grid(row=0, column=3, sticky="s")

        for frame in self.winfo_children():
            frame.grid(pady=10, padx=15, ipadx=5, ipady=4)
            for wid in frame.children.values():
                wid.grid_configure(padx=2, pady=4)

    
    def widget_statut(self, widget):
        """Docstring"""
        # Return False if entry or combox are empty.
        return (widget.get() not in ["", "--"])

    def set_astre(self, event):
        """Docstring"""
        astre = self.combo_astre.get().lower()
        if astre != "--":
            mini = ASTRES[astre]["dist_min"]
            maxi = ASTRES[astre]["dist_max"]
        else:
            astre = "Astre"
            mini = 0
            maxi = 0
        self.slider.config(label=f"Distance Terre/{astre.title()}")
        self.slider.config(from_=mini, to=maxi)
        self.label_sliderMin.config(text=f"Minimum\n{mini}")
        self.label_sliderMax.config(text=f"Maximum\n{maxi}")
        self.trigger()

    def trigger(self, event=None):
        """Docstring"""
        # Check if all required widget are ready.
        if all([self.widget_statut(w) for w in self.requiere_widget]):
            selected = self.combo_astre.get().lower()
            # Get size.
            planet_size = ASTRES[selected]["size"]
            if all((
                self.isfloat(self.focal),
                self.isfloat(self.pixel_size),
                self.isfloat(self.entry_pixelNumber.get())
                )):
                result_km = Calculator.comput_planetDistance(
                                        float(self.focal),
                                        float(self.pixel_size),
                                        float(self.entry_pixelNumber.get()),
                                        float(planet_size)
                                    )
                result_Ua = Calculator.Km_to_Ua(result_km)
                self.entry_distanceKm.delete(0, END)
                self.entry_distanceKm.insert(0, int(result_km))
                self.entry_distanceUa.delete(0, END)
                self.entry_distanceUa.insert(0, round(result_Ua, 3))
                # Set min/max and current on slider.
                self.slider.config(state=NORMAL)
                mini, maxi = ASTRES[selected]["dist_min"], ASTRES[selected]["dist_max"]
                self.slider.config(from_=int(mini), to=int(maxi))
                self.slider.set(int(result_km))
                self.slider.config(state=DISABLED)

    def comput_distance(self):
        """Docstring"""
        self.trigger()

    def open_image(self):
        """Docstring"""
        filetypes = (
            ('jpeg files', '*.jpg'),
            ('png files', '*.png'),
            ('All files', '*.*'))
        filename = filedialog.askopenfilename(title='Open a file', initialdir=CURRENT_DIR, filetypes=filetypes)
        try:
            img = Image.open(filename)
        except UnidentifiedImageError:
            print("Fichier non pris en charge")
        else:
            self.window_image = WindowImage(img, parent=self)


if __name__ == '__main__':
    APP = WindowPlanetDistance(pixel_size=3.75, focal=1500)
    APP.mainloop()