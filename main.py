import json
from tkinter import *
from tkinter import ttk
from pathlib import Path, PurePath

from calculator import Calculator
from window_help import WindowHelp
from splash_screen import SplashScreen
from window_credits import WindowCredits
from window_altitude import WindowAltitude
from window_choix_cam import WindowChoixCam
from window_focal_real import WindowFocalReal
from window_crater_size import WindowCraterSize
from window_planet_distance import WindowPlanetDistance


# Set current Path.
CURRENT_DIR = PurePath.parent

# Load Datas.
cameras_file = Path("data/cameras.json")
with open(cameras_file, "r") as f:
    CAMERAS = json.load(f)

telescopes_file = Path("data/telescopes.json")
with open(telescopes_file, "r") as f:
    TELESCOPES = json.load(f)

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


class Main(Tk):

    def __init__(self):
        """Docstring"""
        super().__init__()
        self.geometry("380x617")
        self.title("AstroAz V0.95")
        self.update_idletasks()
        self.create_frames()
        self.create_widgets()
        self.place_widgets()

    def isfloat(self, _string):
        """Docstring"""
        try:
            float(_string)
            return True
        except ValueError:
            return False

    def only_numbers(self, char):
        """Docstring"""
        return char in CHAR_DIGITS
    
    def create_frames(self):
        """Docstring"""
        self.frame_barlowRDF = LabelFrame(self, text="Barlow ou RDF", labelanchor="nw")
        self.frame_camTele = LabelFrame(self, text="Camera Telescope", labelanchor="nw")
    
    def create_widgets(self):
        """Docstring"""
        self._create_barmenu()
        self._create_labels()
        self._create_entrys()
        self._create_combobox()
        self._create_radios()
        self._create_buttons()
    
    def _create_barmenu(self):
        self.menubar = Menu(self)
        # Cascade Outils.
        menu_tools = Menu(self.menubar, tearoff=0)
        menu_tools.add_command(label="Focale Réele", command=self.show_windowFocalReal)
        menu_tools.add_command(label="Taille de cratère", command=self.show_windowCraterSize)
        menu_tools.add_command(label="Distance d'astre", command=self.show_windowPlanetDistance)
        menu_tools.add_command(label="Aide choix caméra", command=self.show_choixcam)
        menu_tools.add_command(label="Altitude des montagnes", command=self.show_altitude)
        # Cascade Aide.
        menu_help = Menu(self.menubar, tearoff=0)
        menu_help.add_command(label="Aide", command=self.show_help)
        menu_help.add_command(label="A propos", command=self.show_credits)
        # pack
        self.menubar.add_cascade(label="Outils", menu=menu_tools)  
        self.menubar.add_cascade(label="Aide", menu=menu_help)

    def _create_labels(self):
        """Docstring"""
        # Main Frame:
        self.label_cam         = Label(self, text="Please select your camera:\nor write the 'pixel size' (micron) ")
        self.label_lun         = Label(self, text="Please select your telescope:\nor write 'apterure,focal' ")
        # BarlowRDF Frame:
        self.label_factorZoom  = Label(self.frame_barlowRDF, text="Facteur d'agrandissement")
        self.label_barlowFocal = Label(self.frame_barlowRDF, text="Focale Barlow")
        self.label_drawing     = Label(self.frame_barlowRDF, text="Tirage (mm)")
        # camTele Frame:
        self.label_splitP      = Label(self.frame_camTele, text="Pouvoir séparateur :")
        self.label_sampling    = Label(self.frame_camTele, text="Echantillonnage :")
        self.label_ratioFD     = Label(self.frame_camTele, text="Rapport F/D :")
        self.label_ratioFDf    = Label(self.frame_camTele, text="Rapport F/D idéal pour la caméra :")
        # Label Theoric Focal:
        self.Var_theoricFocal  = StringVar()
        self.Var_theoricFocal.set("Focale théorique: ")
        self.label_theoricFocal = Label(self.frame_barlowRDF, textvariable=self.Var_theoricFocal)
    
    def _create_entrys(self):
        """Docstring"""
        self.validation = self.register(self.only_numbers)
        # Barlow RDF frame:
        self.entry_factorZoom   = Entry(self.frame_barlowRDF, state=DISABLED, validate="key", validatecommand=(self.validation, '%S'))
        self.entry_barlowFocal  = Entry(self.frame_barlowRDF, state=DISABLED, validate="key", validatecommand=(self.validation, '%S'))
        self.entry_drawing      = Entry(self.frame_barlowRDF, state=DISABLED, validate="key", validatecommand=(self.validation, '%S'))
        # CamTele Frame:
        self.entry_result_splitP   = Entry(self.frame_camTele, relief="flat")
        self.entry_result_splitP.insert(0, "Select a telescope")
        self.entry_result_splitP.config(state="readonly")
        # Sampling (echantillonnage).
        self.entry_result_sampling = Entry(self.frame_camTele, relief="flat", width=21)
        self.entry_result_sampling.insert(0, "Select camera/telescope")
        self.entry_result_sampling.config(state="readonly")
        # Ratio F/D.
        self.entry_result_ratioFD  = Entry(self.frame_camTele, relief="flat")
        self.entry_result_ratioFD.insert(0, "Select a telescope")
        self.entry_result_ratioFD.config(state="readonly")
        # Ratio F/D foucault.
        self.entry_result_ratioFDf = Entry(self.frame_camTele, relief="flat")
        self.entry_result_ratioFDf.insert(0, "Select a camera")
        self.entry_result_ratioFDf.config(state="readonly")

    def _create_combobox(self):
        """Docstring"""
        # Combobox camera.
        cameras_list = list(CAMERAS.keys())
        self.combo_camera = ttk.Combobox(self, width=30, values=cameras_list)
        self.combo_camera.config(validate="key", validatecommand=(self.validation, '%S'))
        self.combo_camera.bind("<<ComboboxSelected>>", self.set_camera)
        self.combo_camera.bind('<KeyPress>', self.set_camera)
        self.combo_camera.current(0)
        # Combobox telescope.
        telescopes_list = list(TELESCOPES.keys())
        self.combo_telescope = ttk.Combobox(self, width=30, values=telescopes_list)
        self.combo_telescope.config(validate="key", validatecommand=(self.validation, '%S'))
        self.combo_telescope.bind("<<ComboboxSelected>>", self.set_telescope)
        self.combo_telescope.current(0)

    def _create_radios(self):
        """Docstring"""
        # Barlow RDF Frame:
        self.radio_vars = IntVar()
        self.radio_vars.set(0)
        self.radio_none     = Radiobutton(self.frame_barlowRDF, variable=self.radio_vars, value=0, text="None", command=self.radio_callback)
        self.radio_basic    = Radiobutton(self.frame_barlowRDF, variable=self.radio_vars, value=1, text="Basic", command=self.radio_callback)
        self.radio_advanced = Radiobutton(self.frame_barlowRDF, variable=self.radio_vars, value=2, text="Advanced", command=self.radio_callback)

    def _create_buttons(self):
        """Docstring"""
        pass
        self.button_theoricFocal  = Button(self.frame_barlowRDF, text="Calcul de la focale théorique", command=self.trigger)
        self.button_craterSize    = Button(self, text="Calculer la dimension d'un cratère", command=self.show_windowCraterSize)
        self.button_panetDistance = Button(self, text="Calculer la distance d'une planète", command=self.show_windowPlanetDistance)
        self.button_reelFocal     = Button(self, text="Calculer la focale réelle", command=self.show_windowFocalReal)
        self.button_help          = Button(self, text="Aide", command=self.show_help)
    
    def place_widgets(self):
        """Docstring"""
        self.config(menu=self.menubar)
        # Main Frame:
        self.label_cam.pack()
        self.combo_camera.pack(pady=5)
        self.label_lun.pack()
        self.combo_telescope.pack(pady=5)
        # Pack subframes:
        self.frame_barlowRDF.pack(pady=15, padx=30, ipady=5)
        self.frame_camTele.pack(pady=15, ipadx=5)
        # Main frame:
        # self.button_reelFocal.pack(pady=7)
        # self.button_craterSize.pack(pady=7)
        # self.button_panetDistance.pack(pady=7)
        # self.button_help.pack(pady=7)
        # RDFbarlow Frame
        self.radio_none.grid(row=1, column=0)
        self.radio_basic.grid(row=2, column=0)
        self.radio_advanced.grid(row=3, column=0, sticky=E, padx=40)
        self.label_factorZoom.grid(row=4, column=0)
        self.entry_factorZoom.grid(row=5, column=0)
        self.label_barlowFocal.grid(row=6, column=0)
        self.entry_barlowFocal.grid(row=7, column=0)
        self.label_drawing.grid(row=8, column=0)
        self.entry_drawing.grid(row=9, column=0, padx=30)
        self.button_theoricFocal.grid(row=10, column=0, pady=7)
        self.label_theoricFocal.grid(row=11, pady=5)
        # camtele Frame:
        self.label_splitP.grid(row=0, column=0)
        self.label_sampling.grid(row=1, column=0)
        self.label_ratioFD.grid(row=2, column=0)
        self.label_ratioFDf.grid(row=3, column=0)
        self.entry_result_splitP.grid(row=0, column=1, pady=3)
        self.entry_result_sampling.grid(row=1, column=1, pady=3)
        self.entry_result_ratioFD.grid(row=2, column=1, pady=3)
        self.entry_result_ratioFDf.grid(row=3, column=1, pady=3)
        
    def radio_callback(self):
        """Docstring"""
        radio_pos = self.radio_vars.get()
        self.entry_factorZoom.config(state=DISABLED)
        self.entry_barlowFocal.config(state=DISABLED)
        self.entry_drawing.config(state=DISABLED)
        if radio_pos == 1:
            self.entry_factorZoom.config(state=NORMAL)
            self.entry_factorZoom.focus_set()
        elif radio_pos == 2:
            self.entry_barlowFocal.config(state=NORMAL)
            self.entry_barlowFocal.focus_set()
            self.entry_drawing.config(state=NORMAL)
        self.trigger()

    def set_camera(self, event):
        """Docstring"""
        # Ratio FD/f by Camera
        camera = self.get_camera()
        pixel_size = camera.get('pixel_size')
        self.entry_result_ratioFDf.config(state=NORMAL)
        self.entry_result_ratioFDf.delete(0, END)
        if self.isfloat(pixel_size):
            ratio_FDf = round(Calculator.comput_ratioFDf(float(pixel_size)), 2)
            self.entry_result_ratioFDf.insert(0, ratio_FDf)
        else:
            self.entry_result_ratioFDf.insert(0, "Select a camera")
        self.entry_result_ratioFDf.config(state="readonly")
        self.trigger()


    def set_telescope(self, event):
        """Docstring"""
        self.trigger()

    def update_entrys(self, aperture, focal, pixel_size):
        """Docstring"""
        self.entry_result_splitP.config(state=NORMAL)
        self.entry_result_sampling.config(state=NORMAL)
        self.entry_result_ratioFD.config(state=NORMAL)
        self.entry_result_splitP.delete(0, END)
        self.entry_result_sampling.delete(0, END)
        self.entry_result_ratioFD.delete(0, END)
        if aperture:
            self.entry_result_splitP.insert(0, f"{round(Calculator.comput_splitterPower(aperture), 2)}")
            if focal:
                self.entry_result_ratioFD.insert(0, f"{round(Calculator.comput_ratioFD(aperture, focal), 2)}")
        else:
            self.entry_result_ratioFD.insert(0, "Select a telescope")
            self.entry_result_splitP.insert(0, "Select a telescope")
        if pixel_size and focal:
            self.entry_result_sampling.insert(0, f"{round(Calculator.comput_sampling(pixel_size, focal), 2)}")
        else:
            self.entry_result_sampling.insert(0, "Select camera/telescope")
        self.entry_result_splitP.config(state="readonly")
        self.entry_result_sampling.config(state="readonly")
        self.entry_result_ratioFD.config(state="readonly")

    def comput_theoric_focal(self):
        """Docstring"""
        coefficient = 1
        focal, _ = self.get_telescope()
        radio_pos = self.radio_vars.get()
        if radio_pos == 1:
            factorZoom = self.entry_factorZoom.get()
            coefficient = float(factorZoom) if factorZoom else 1
        elif radio_pos == 2:
            drawing_ = self.entry_drawing.get()
            drawing = float(drawing_) if drawing_ else 2  # Si non renseigné.
            focal_barlow_ = self.entry_barlowFocal.get()
            focal_barlow = float(focal_barlow_) if focal_barlow_ else -1  # Si non renseigné.
            coefficient  = abs(Calculator.comput_coefBarlow(drawing, focal_barlow))
        if focal:
            return round((focal * coefficient), 2)
        else:
            return 0
    
    def trigger(self):
        """Docstring"""
        _,aperture = self.get_telescope()
        camera = self.get_camera()
        pixel_size = camera.get('pixel_size')
        focal = self.theoric_focal
        self.update_entrys(self.aperture, focal, pixel_size)
        # self.set_camera(None)
        self.update_label_theoricFocal(focal)
    
    @property
    def theoric_focal(self):
        """Docstring"""
        return self.comput_theoric_focal()
    @property
    def aperture(self):
        """Docstring"""
        _, aperture = self.get_telescope()
        return aperture
    
    def update_label_theoricFocal(self, focal):
        """Docstring"""
        if focal:
            self.Var_theoricFocal.set(f"Focale théorique:  {int(focal)}")
        else:
            self.Var_theoricFocal.set("Focale théorique:  ")

    def get_camera(self):
        """Docstring"""
        selected_cam = self.combo_camera.get()
        if selected_cam not in CAMERAS:
            pixel_size = float(selected_cam)
        else:
            pixel_size = CAMERAS[selected_cam]
        return pixel_size

    def get_telescope(self):
        """Docstring"""
        selected_tele = self.combo_telescope.get()
        if selected_tele not in TELESCOPES:
            aperture, focal = selected_tele.split(",")
            aperture, focal = float(aperture), float(focal)
        else:
            focal = TELESCOPES[selected_tele]['focal']
            aperture = TELESCOPES[selected_tele]['aperture']
        return focal, aperture

    def show_windowCraterSize(self):
        """Docstring"""
        camera = self.get_camera()
        pixel_size = camera.get('pixel_size', "")
        WindowCraterSize(pixel_size, self.theoric_focal)
    
    def show_windowPlanetDistance(self):
        """Docstring"""
        camera = self.get_camera()
        pixel_size = camera.get('pixel_size', "")
        WindowPlanetDistance(pixel_size=pixel_size, focal=int(self.theoric_focal))

    def show_windowFocalReal(self):
        """Docstring"""
        camera = self.get_camera()
        pixel_size = camera.get('pixel_size', "")
        WindowFocalReal(pixel_size=pixel_size)

    def show_help(self):
        """Docstring"""
        WindowHelp()
    
    def show_credits(self):
        """Docstring"""
        WindowCredits()

    def show_choixcam(self):
        """Docstring"""
        WindowChoixCam(self.theoric_focal, self.aperture)

    def show_altitude(self):
        """docstring"""
        camera = self.get_camera()
        pixel_size = camera.get('pixel_size', "")
        WindowAltitude(self.theoric_focal, pixel_size)

splash = SplashScreen()
splash.mainloop()
APP = Main()
APP.mainloop()