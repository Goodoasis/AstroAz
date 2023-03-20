from tkinter import *
from pathlib import PurePath

from PIL import Image, ImageTk

from calculator import Calculator


class WindowImage(Tk):

    def __init__(self, picture: Image, parent: Tk=None, *args, **kwargs):
        """Docstring"""
        super().__init__(*args, **kwargs)
        self.parent = parent
        self.picture = picture
        self.pic_size = self.picture.size
        pic_name = PurePath(picture.filename).name
        geometry = self._size_position()
        self.geometry(geometry)
        # get screen width and height.
        self.title(f"Image :  {pic_name}")
        # Init variables.
        self.variables()
        self.frame_values = Frame(self)
        self.frame_canvas = Frame(self)
        self.frame_values.pack(expand=YES)
        self.frame_canvas.pack(expand=YES)
        self.create_labels()
        self.create_canvas()

    def variables(self):
        """Docstring"""
        self.leftInterruptor = 0  # J'ai fait un interrupteur pour que l'ordinateur différencie les deux points.
        self.rightInterruptor = 0  # J'ai fait un interrupteur pour que l'ordinateur différencie les deux points.
                              # Quand interuptor est pair c'est le click 1(rouge) si impaire c'est le click 2(bleu).
        self.pos_leftClick = [(0,0), (0,0)] # Pour enregistre la position du click 1 et 2.
        self.pos_rightClick = [(0,0), (0,0)] # Pour enregistre la position du click 1 et 2.

    @property
    def inter_left(self):
        """Docstring"""
        return (self.leftInterruptor % 2) != 1

    @property
    def inter_right(self):
        """Docstring"""
        return (self.rightInterruptor % 2) != 1

    def _size_position(self):
        """Docstring"""
        width_screen = self.winfo_screenwidth() # width of the screen.
        height_screen = self.winfo_screenheight() # height of the screen.
        one_third = width_screen / 3  # 1/3 of with screen.
        if self.pic_size[0] < int(one_third*2):
            width = self.pic_size[0] + 25 # Window take size of img.
        else:
            width = int(one_third *2) - 8  # Window take max of 2/3 of screen.
        if self.pic_size[1] < int(height_screen):
            height = self.pic_size[1] + 25  # Window take size of img.
        else:
            height = int(height_screen) - 75  # Window take full height.
        return f"{width}x{height}+{int(one_third)}+{-3}"

    def create_canvas(self):
        """Docstring"""
        _width, _height = self.pic_size
        self.photo = ImageTk.PhotoImage(master=self, image=self.picture)
        self.canvas = Canvas(self.frame_canvas, width=_width, height=_height, scrollregion=(0,0,_width,_height))
        # Connexion entre le button 1 de la souris et mon canvas.
        self.canvas.bind("<Button-1>", self.mouse_click)
        self.canvas.bind("<Button-3>", self.mouse_click)

        # Scroll bar.
        defilX = Scrollbar(self.frame_canvas, orient='horizontal', command=self.canvas.xview)
        defilY = Scrollbar(self.frame_canvas, orient='vertical', command=self.canvas.yview)
        defilX.pack(side=TOP, fill=X)
        defilY.pack(side=LEFT, fill=Y)
        self.canvas.config(xscrollcommand=defilX.set, yscrollcommand=defilY.set)
        self.canvas.pack(side=BOTTOM, expand=True, fill=BOTH)
        self.canvas.create_image(0, 0, anchor=NW, image=self.photo)

    def create_labels(self):
        """Docstring"""
        # initialisation des 3 labels
        self.label_shadowLenght = Label(self.frame_values, text="Longueur de l'ombre = XXX.XX px", width=40)
        self.label_terminateur = Label(self.frame_values, text="Distance jours/nuit (Terminateur) = XXX.XX px", width=40)
        # Le bouton send:
        self.button_send = Button(self.frame_values, text="Valider", command=self.send_distance)
        # Puis on pack
        self.label_terminateur.grid(row=0, column=0)
        self.label_shadowLenght.grid(row=1, column=0)
        self.button_send.grid(row=0, column=1)

    def send_distance(self):
        """Docstring"""
        if self.parent != None:
            self.parent.entry_terminator_distance.delete(0, END)
            for char in str(round(self.terminateur_lenght, 2))[::-1]:
                self.parent.entry_terminator_distance.insert(0, char)
            self.parent.entry_shadowSizePx.delete(0, END)
            for char in str(round(self.shadow_lenght, 2))[::-1]:
                self.parent.entry_shadowSizePx.insert(0, char)
        try:
            self.parent.trigger()
        except AttributeError:
            pass

    def mouse_click(self, event):
        """Docstring"""
        if event.num == 1:
            tag = 'left'
            inter = self.inter_left
            clicks = self.pos_leftClick
            self.leftInterruptor +=1
        else:
            tag = 'right'
            inter = self.inter_right
            clicks = self.pos_rightClick
            self.rightInterruptor +=1

        x = self.canvas.canvasx(event.x)
        y = self.canvas.canvasy(event.y)
        clicks[inter] = (x, y)
        self.canvas.delete(tag)  # J'efface tout le canvas.
        self.draw_clicks(tag=tag)  # J'appel la fonction qui dessine les clicks.
        self.update_labels()  # Je met a jours les labels.

    def update_labels(self):
        """Fonction qui est appeler a chaque clique pour mettre a jour tout les labels"""
        self.shadow_lenght = Calculator.comput_distanceOrth(self.pos_leftClick) # J'appel la fonction qui calcul la distance et je met en string le resultat
        self.terminateur_lenght = Calculator.comput_distanceOrth(self.pos_rightClick) # J'appel la fonction qui calcul la distance et je met en string le resultat
        self.label_shadowLenght.config(text=f"Longueur de l'ombre = {str(round(self.shadow_lenght, 3))}")  # Met a jours le lable de distance.
        self.label_terminateur.config(text=f"Distance jours/nuit (Terminateur) = {str(round(self.terminateur_lenght, 3))}")  # Met a jours le lable de distance.

    def draw_clicks(self, tag):
        """Fonction qui dessine un cercle pour chaque click de self.pos_click"""
        if tag == 'left':
            clicks = self.pos_leftClick
            colors = ['red', 'yellow']
        else:
            clicks = self.pos_rightClick
            colors = ['blue', 'green']
        for index, pos in enumerate(clicks):
            circle_color = colors[index]
            self.draw_click(pos=pos, tag=tag, circle_color=circle_color)
        # Ensuite on dessine le trait!
        self.draw_link()

    def draw_click(self, pos, tag, circle_color="red"):
        """Appeler pour dessiner un cercle a une position"""
        r = 7  # Rayon du cercle
        posX = pos[0] - r
        posY = pos[1] - r
        posX1 = pos[0] + r
        posY1 = pos[1] + r
        # Draw!
        self.canvas.create_oval(posX, posY, posX1, posY1, outline=circle_color, width=2, tags=tag)

    def draw_link(self):
        """ Dessine le trait entre les click"""
        # Point de depart qui est egal au premier click de click_pos
        x0 = self.pos_leftClick[0][0]
        y0 = self.pos_leftClick[0][1]
        # Point darriver de notre trait qui est le second click
        x1 = self.pos_leftClick[1][0]
        y1 = self.pos_leftClick[1][1]
        # Draw!
        self.canvas.create_line(x0, y0, x1, y1, fill="lightgray", dash=(200, 200), tags="left")
        # Point de depart qui est egal au premier click de click_pos
        x0 = self.pos_rightClick[0][0]
        y0 = self.pos_rightClick[0][1]
        # Point darriver de notre trait qui est le second click
        x1 = self.pos_rightClick[1][0]
        y1 = self.pos_rightClick[1][1]
        self.canvas.create_line(x0, y0, x1, y1, fill="lightgray", dash=(200, 200), tags="right")


if __name__ == '__main__':
    astro_picture = Image.open(r"img\moon_6good.jpg")
    APP = WindowImage(astro_picture)
    APP.mainloop()