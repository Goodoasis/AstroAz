from tkinter import *


class WindowChoixCam(Toplevel):

    def __init__(self, focal="", aperture="", *args, **kwargs):
        """Docstring"""
        super().__init__(*args, **kwargs)
        self.focal = focal
        self.aperture = aperture
        self.geometry("340x550")
        self.title("Aide choix caméra")
        self.create_widgets()
        self.place_widgets()
        self.update_entry(self.entry_focalLength, str(self.focal))
        self.update_entry(self.entry_aperture, str(self.aperture))

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
        self._create_radios()
        self._create_slider()
        
    def _create_frames(self):
        """Docstring"""
        # frame telescope
        self.frame_telescope = LabelFrame(self, text="Telescope", labelanchor="nw")
        # frame cible FD
        self.frame_targetFD = LabelFrame(self, labelanchor="nw")
        # frame qualitée du ciel
        self.frame_sky = LabelFrame(self, text="Qualitée du ciel", labelanchor="nw")
        # frame niveau user
        self.frame_levelUser = LabelFrame(self, text="Niveau utilisateur", labelanchor="nw" )
        # frame collimation
        self.frame_collimation = LabelFrame(self, text="Collimation", labelanchor="nw")
        # frame chercher
        self.frame_search = LabelFrame(self)
        # frame resultat
        self.frame_result = LabelFrame(self, text="Résultat", labelanchor="nw")
        # frame warning
        self.frame_warning = LabelFrame(self)
        # frame valider
        self.frame_validate = LabelFrame(self)

    def _create_labels(self):
        """Docstring"""""
         # frame telescope
        self.label_focalLength = Label(self.frame_telescope, text="Focale:")
        self.label_aperture = Label (self.frame_telescope, text="Ouverture:")
        # frame qualitée du ciel
        self.label_sliderMin = Label(self.frame_sky, text="Mauvais", width=10)
        self.label_sliderMax = Label(self.frame_sky, text="Excellent")
        # frame résultat
        self.label_resultat = Label(self.frame_result, text="Taille de pixel recommandé:")
        # frame cible fd
        self.label_targetFD = Label(self.frame_targetFD, text="Rapport F/D:")
        # frame warning
        self.label_warning = Label(self.frame_warning, text="Attention le rapport F/D doit être au minimum de 10", foreground='red')
        #self.label_warning = Label(self.frame_warning, text="Rapport F/D > 10", foreground='green')

    def _create_entrys(self):
        """Creer toutes les entrys de ta fenetre"""
        # frame telescope
        self.entry_focalLength = Entry(self.frame_telescope)
        self.entry_aperture = Entry(self.frame_telescope)
        self.entry_resultat = Entry(self.frame_result)
        # frame cible fd
        self.entry_FD = Entry(self.frame_targetFD, state=DISABLED)

    def _create_buttons(self):
        """Creer touts les buttons de ta fenetre"""
        self.button_search = Button(self.frame_search, text="Recherche",command=self.compute_pixelSize)
        self.button_search.config(state=DISABLED)
        self.button_validate = Button(self.frame_validate, text="Valider", command= self.validate)

    def _create_slider(self):
        """Docstring"""
        # Frame qualitée du ciel
        self.slider = Scale(self.frame_sky, orient=HORIZONTAL)
        self.slider.config(length=180)
        self.slider.config(from_=0, to=10)

    def _create_radios(self):
        """Docstring"""
        # frame niveau utilisateur
        self.radio_value = IntVar()
        self.radio_value.set(0)
        self.radio_beginner = Radiobutton(self.frame_levelUser, value=2, variable= self.radio_value, text="Debutant")
        self.radio_average = Radiobutton(self.frame_levelUser, value=1, variable= self.radio_value, text="Moyen")
        self.radio_expert = Radiobutton(self.frame_levelUser, value=0, variable= self.radio_value, text="Expert")
        # frame collimation
        self.radio_collimation = IntVar()
        self.radio_collimation.set(0)
        self.radio_average = Radiobutton(self.frame_collimation, value=0, variable= self.radio_collimation, text="Moyenne")
        self.radio_perfect = Radiobutton(self.frame_collimation, value=1, variable= self.radio_collimation, text="Parfaite")

    def place_widgets(self):
        """Docstring"""
        # frame
        self.frame_warning.pack(pady=10)
        self.frame_telescope.pack(pady=10)
        self.frame_validate.pack(pady=10)
        self.frame_targetFD.pack(pady=10)
        self.frame_sky.pack(pady=10)
        self.frame_levelUser.pack(pady=10)
        self.frame_collimation.pack(pady=10)
        self.frame_search.pack(pady=10)
        self.frame_result.pack(pady=10)
        # frame telescope
        self.label_focalLength.grid(row=1, column=0)
        self.entry_focalLength.grid(row=1, column=1)
        self.label_aperture.grid(row=3, column=0)
        self.entry_aperture.grid(row=3, column=1)
        # frame cible fd
        self.label_targetFD.grid(row=0, column=0)
        self.entry_FD.grid(row=0, column=1)
        # frame qualitée du ciel
        self.label_sliderMin.grid(row=2, column=0, sticky="s")
        self.slider.grid(row=2, column=1)
        self.label_sliderMax.grid(row=2, column=3, sticky="s")
        # frame niveau utilisateur
        self.radio_beginner.grid(row=1, column=0)
        self.radio_average.grid(row=1, column=1)
        self.radio_expert.grid(row=1, column=2)
        # frame collimation
        self.radio_average.grid(row=1, column=0)
        self.radio_perfect.grid(row=1, column=1)
        # frame chercher
        self.button_search.grid(row=0, column=0)
        # frame résultat
        self.label_resultat.grid(row=0, column=0)
        self.entry_resultat.grid(row=0, column=1)
        # frame warning
        self.label_warning.grid(row= 0, column=0)
        # frame valider
        self.button_validate.grid(row=0, column=0)
        
    def validate(self):
        """Docstring"""
        aperture = float(self.entry_aperture.get())
        focal = float(self.entry_focalLength.get())
        fd =  focal / aperture
        if fd >= 10:
            color = 'green'
            text = "Rapport FD optimal"
        else:
            color = 'red'
            text = 'Attention le rapport FD doit être suppérieur a 10'
        self.update_warning(color, text)            
        self.entry_FD.config(state=NORMAL)
        self.entry_FD.delete(0, END)
        self.entry_FD.insert(0, round(fd, 1))
        self.entry_FD.config(state=DISABLED)    
        self.button_search.config(state=NORMAL)
        # self.label_warning = Label(self.frame_warning, text="Rapport F/D > 10", foreground='green')

    def update_warning(self, color, text):
        """Docstring"""
        self.label_warning.config(text=text, foreground=color)
        
    def compute_pixelSize(self):
        """Docstring"""
        aperture = float(self.entry_aperture.get())
        focal = float(self.entry_focalLength.get())
        fd = focal / aperture
        sky_quality = float(self.slider.get())
        level_user = float(self.radio_value.get()) * 0.8
        collimation = float(self.radio_collimation.get())
        if collimation == 1:
            factor_collimation = 1
        else:
            factor_collimation = 0.8
        factor = (((sky_quality * 0.375) + 3) - level_user) * factor_collimation
        if factor < 2.8:
            factor = 2.8
        if factor > 6:
            factor = 6
        pixel_size = fd / factor
        self.entry_FD.config(state=NORMAL)
        self.entry_FD.delete(0, END)
        self.entry_FD.insert(0, round(fd, 1))
        self.entry_FD.config(state=DISABLED)
        self.entry_resultat.delete(0, END)
        self.entry_resultat.insert(0, round(pixel_size, 2))

        
if __name__ == '__main__':
    APP = WindowChoixCam(1500.0, 127)
    APP.mainloop()