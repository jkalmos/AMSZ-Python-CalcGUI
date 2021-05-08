import tkinter as tk
import numpy as np
from PIL import Image, ImageTk
import CrossSection as CS
from SideMenu import SideMenu
from plot import plot_rectangle
class window(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Próba GUI")
        self.geometry("1000x600")
        self.configure(bg="#2A3C4D")
        self.minsize(width=200, height=200)
        self.tk.call('wm', 'iconphoto', self._w, tk.PhotoImage(file='logo.png'))

        self.canvas = None
        #Side Menu
        self.sm = SideMenu(self)
        #self.sm.pack(side=tk.LEFT, fill=tk.Y)
        self.bind('<Return>', self.szamol)
        self.plotted = tk.BooleanVar(False)

        #Basic logo
        self.logo_img = Image.open("amsz_logo_full.png")
        self.logo_img = ImageTk.PhotoImage(self.logo_img)
        self.logo_image = tk.Label(self,image=self.logo_img,bg="#2A3C4D")
        self.logo_image.image=self.logo_img
        self.logo_image.pack(side=tk.LEFT)
        #menüszerkezet
        menubar = tk.Menu(self)#, background='gray', foreground='black',activebackground='#004c99', activeforeground='white')
        self.config(menu=menubar)        
        keresztmetszet = tk.Menu(self, menubar, tearoff=0)
        menubar.add_cascade(label="Keresztmetszet", menu=keresztmetszet)
        keresztmetszet.add_command(label="Téglalap", command = lambda: self.choose_object("Teglalap"))
        keresztmetszet.add_command(label="Kör", command = lambda: self.choose_object("Kor"))
        menubar.add_command(label="Kilépés", command=self.destroy)

    def choose_object(self,shape=None):
        if shape == self.sm.shape:
            return 0
        if self.canvas is not None:
            self.sm.clear()
        if shape == "Teglalap" and self.sm.shape != "Teglalap":
            self.sm.shape = "Teglalap"
            self.sm.change_to_recrangle()
            plot_rectangle(self,2,1)
        elif shape == "Kor" and self.sm.shape != "Kor":
            self.sm.shape = "Kor"
            self.sm.change_to_circle()
        else:
            self.sm.shape = None
            print("Ez az alakzat még nincs definiálva...")
    
    def szamol(self, event=None):
        try:
            a = float(self.sm.e1.get().replace(',','.'))
            b = float(self.sm.e2.get().replace(',','.'))
            plot_rectangle(self,a,b)
            self.values = CS.Rectangle(a,b)

            self.sm.eredmeny1.config(text="I_x = " + str(round(self.values["Ix"], 4)))
            self.sm.eredmeny2.config(text="I_y = " + str(round(self.values["Iy"], 4)))

        except:
            print("Hiba!")
    def doNothing(self):
        print("Ez a funkció jelenleg nem elérhető...")
    """
    def add_circle(self):
        self.canvas.delete('all')
        reduced_size = min(self.canvas.winfo_width(),self.canvas.winfo_height())*0.7/2
        c_x = self.canvas.winfo_width()/2
        c_y = self.canvas.winfo_height()/2
        self.canvas.create_oval(c_x-reduced_size,c_y-reduced_size, c_x+reduced_size,c_y+reduced_size, fill="#2A3C4D")
    def add_retangle(self):
        self.canvas.delete('all')
        reduced_size = min(self.canvas.winfo_width(),self.canvas.winfo_height())*0.7/2
        c_x = self.canvas.winfo_width()/2
        c_y = self.canvas.winfo_height()/2
        self.canvas.create_rectangle(c_x-reduced_size,c_y-reduced_size, c_x+reduced_size,c_y+reduced_size, fill="#2A3C4D")
    """
    

# ************ Toolbar ************
# class Eszkoztar(tk.Frame):
#     def __init__(self, root):
#         super().__init__(root, bg='#F5F5DC')
#         self.root=root
#         tegla = tk.Button(self, text="teglalap",compound="top", command=self.root.add_retangle)
#         tegla.pack(side=tk.LEFT, padx=2, pady=2)
#         kor = tk.Button(self, text="Kör", command=self.root.add_circle)
#         kor.pack(side=tk.LEFT, padx=2, pady=2)
#         haromszog = tk.Button(self, text="Háromszög", command=self.root.doNothing)
#         haromszog.pack(side=tk.LEFT, padx=2, pady=2)

#         calc = tk.Button(self, text="Calculate", command=self.root.szamol)
#         calc.pack(side=tk.RIGHT, padx=2, pady=2)

if __name__ == "__main__":
    root = window()
    root.mainloop()