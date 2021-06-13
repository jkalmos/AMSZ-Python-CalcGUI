import tkinter as tk
import numpy as np
from PIL import Image, ImageTk
import CalcFunctions as Calc
from SideMenu import SideMenu
from PlotFunctions import plot_circle, plot_ellipse, plot_rectangle, plot_isosceles_triangle
class window(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Statika számító")
        self.geometry("1000x600")
        self.configure(bg="#2A3C4D")
        self.minsize(width=200, height=200)
        self.tk.call('wm', 'iconphoto', self._w, tk.PhotoImage(file='logo_A.png'))

        self.canvas = None
        #Side Menu
        self.sm = SideMenu(self)
        #self.sm.pack(side=tk.LEFT, fill=tk.Y)
        self.bind('<Return>', self.calculate)
        self.plotted = tk.BooleanVar(False)

        #Basic logo
        self.logo_img = Image.open("logo_Full.png")
        self.logo_img = ImageTk.PhotoImage(self.logo_img)
        self.logo_image = tk.Label(self,image=self.logo_img,bg="#2A3C4D")
        self.logo_image.image=self.logo_img
        self.logo_image.pack(side=tk.LEFT)
        #menüszerkezet
        menubar = tk.Menu(self)#, background='gray', foreground='black',activebackground='#004c99', activeforeground='white')
        self.config(menu=menubar)        
        keresztmetszet = tk.Menu(self, menubar, tearoff=0)
        menubar.add_cascade(label="Keresztmetszet", menu=keresztmetszet)
        keresztmetszet.add_command(label="Téglalap", command = lambda: self.choose_object("Rectangle"))
        keresztmetszet.add_command(label="Kör", command = lambda: self.choose_object("Circle"))
        keresztmetszet.add_command(label="Ellipszis", command = lambda: self.choose_object("Ellipse"))
        keresztmetszet.add_command(label="Körgyűrű", command = lambda: self.choose_object("Ring"))
        keresztmetszet.add_command(label="Egyenlő szárú háromszög", command = lambda: self.choose_object("Isosceles_triangle"))
        menubar.add_command(label="Kilépés", command=self.destroy)

    def choose_object(self, shape = None):
        if shape == self.sm.shape:
            return 0
        if self.canvas is not None:
            self.sm.clear()
        if shape == "Rectangle" and self.sm.shape != "Rectangle":
            self.sm.shape = "Rectangle"
            self.sm.change_to_recrangle()
            plot_rectangle(self,2,1, coordinate_on, dimension_lines_on)
        elif shape == "Circle" and self.sm.shape != "Circle":
            self.sm.shape = "Circle"
            self.sm.change_to_circle()
            plot_circle(self, coordinate_on)
        elif shape == "Ellipse":
            self.sm.shape = "Ellipse"
            self.sm.change_to_ellipse()
            plot_ellipse(self, 2, 1, coordinate_on, dimension_lines_on)
        elif shape == "Ring":
            self.sm.shape = "Ring"
            self.sm.change_to_ring()
        elif shape == "Isosceles_triangle":
            self.sm.shape = "Isosceles_triangle"
            self.sm.change_to_isosceles_triangle()
            plot_isosceles_triangle(self, 2, 1, coordinate_on, dimension_lines_on)
        else:
            self.sm.shape = None
            print("Ez az alakzat még nincs definiálva...")
    
    def get_entry(self, mennyi):
        vissza = []
        for i in range(mennyi):
            try:
                vissza.append(float(self.sm.controls[i]["entry"].get().replace(',','.')))
                self.sm.controls[i]["entry"].config({"background": "#475C6F"})
            except:
                print("Hiba")
                self.sm.controls[i]["entry"].config({"background": "#eb4034"})
                vissza.append(None)
        #self.sm.e2.config({"background": "#475C6F"})    
        return vissza
    def calculate(self, event=None):
        if self.sm.shape == "Rectangle":
            a,b= self.get_entry(2)
            if a is None or b is None:
                return -1
            plot_rectangle(self,a,b, coordinate_on, dimension_lines_on)
            self.values = Calc.Rectangle(a,b)
            self.sm.eredmeny1.config(text="I_x = " + str(round(self.values["Ix"], 4)))
            self.sm.eredmeny2.config(text="I_y = " + str(round(self.values["Iy"], 4)))
        elif self.sm.shape == "Circle":
            r = self.get_entry(1)[0]
            if r is None:
                return -1
            plot_circle(self, coordinate_on)
            self.values = Calc.Circle(r)
            self.sm.eredmeny1.config(text="I_x = " + str(round(self.values["Ix"], 4)))
            self.sm.eredmeny2.config(text="I_y = " + str(round(self.values["Iy"], 4)))
        elif self.sm.shape == "Ellipse":
            a,b = self.get_entry(2)
            if a is None or b is None:
                return -1
            plot_ellipse(self,a,b, coordinate_on, dimension_lines_on)
            self.values = Calc.Ellipse(a,b)
            self.sm.eredmeny1.config(text="I_x = " + str(round(self.values["Ix"], 4)))
            self.sm.eredmeny2.config(text="I_y = " + str(round(self.values["Iy"], 4)))
        elif self.sm.shape == "Ring":
            a,b = self.get_entry(2)
            if a is None or b is None:
                return -1
            #plot_isosceles_triangle(self,a,b, coordinate_on, dimension_lines_on)
            self.values = Calc.Ring(a,b)
            self.sm.eredmeny1.config(text="I_x = " + str(round(self.values["Ix"], 4)))
            self.sm.eredmeny2.config(text="I_y = " + str(round(self.values["Iy"], 4)))
        elif self.sm.shape == "Isosceles_triangle":
            a,b = self.get_entry(2)
            if a is None or b is None:
                return -1
            plot_isosceles_triangle(self,a,b, coordinate_on, dimension_lines_on)
            self.values = Calc.IsoscelesTriangle(a,b)
            self.sm.eredmeny1.config(text="I_x = " + str(round(self.values["Ix"], 4)))
            self.sm.eredmeny2.config(text="I_y = " + str(round(self.values["Iy"], 4)))
        else:
            print("Hiba, az alakzat nem talalhato")


    def doNothing(self):
        print("Ez a funkció jelenleg nem elérhető...")
 

 # VARIABLES --------------------------------------------------------------------------------------------------------------------------------------------
colors = {
    'main_color': '#2A3C4D',
    'secondary_color': '#314457'
    }
coordinate_on = True
dimension_lines_on = True

# CALL THE WINDOW ---------------------------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    root = window()
    root.mainloop()