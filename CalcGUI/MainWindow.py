import tkinter as tk
from PIL import Image, ImageTk
import CalcFunctions as Calc
from SideMenu import SideMenu
from PlotFunctions import plot
class window(tk.Tk):
    def __init__(self):
        super().__init__()

        #Colors
        self.colors = {
        'main_color': '#2A3C4D',
        'secondary_color': '#314457'
        }
        # Variables
        self.coordinate_on = tk.BooleanVar(False)
        self.dimension_lines_on = tk.BooleanVar(False)

        self.title("Statika számító")
        self.geometry("1000x600")
        self.configure(bg=self.colors['main_color'])
        self.minsize(width=200, height=200)
        self.tk.call('wm', 'iconphoto', self._w, tk.PhotoImage(file='logo_A.png'))

        

        #Default unit
        self.unit = "mm"

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

        #Menu
        menubar = tk.Menu(self)#, background='gray', foreground='black',activebackground='#004c99', activeforeground='white')
        self.config(menu=menubar)        
        keresztmetszet = tk.Menu(self, menubar, tearoff=0)
        menubar.add_cascade(label="Keresztmetszet", menu=keresztmetszet)
        keresztmetszet.add_command(label="Téglalap", command = lambda: self.choose_object("Rectangle"))
        keresztmetszet.add_command(label="Kör", command = lambda: self.choose_object("Circle"))
        keresztmetszet.add_command(label="Ellipszis", command = lambda: self.choose_object("Ellipse"))
        keresztmetszet.add_command(label="Egyenlő szárú háromszög", command = lambda: self.choose_object("Isosceles_triangle"))

        beallitasok = tk.Menu(self, menubar, tearoff=0)
        menubar.add_cascade(label="Beállítások", menu=beallitasok)

        mertekegyseg = tk.Menu(self, beallitasok, tearoff=0)
        mertekegyseg.add_command(label="Milliméter [mm]", command=lambda: self.unit_change("mm"))
        mertekegyseg.add_command(label="Centiméter [cm]", command=lambda: self.unit_change("cm"))
        mertekegyseg.add_command(label="Méter [m]", command=lambda: self.unit_change("m"))

        tema = tk.Menu(self, beallitasok, tearoff=0)
        tema.add_command(label="Világos")
        tema.add_command(label="Sötét")

        beallitasok.add_cascade(label="Téma", menu=tema)

        beallitasok.add_cascade(label="Mértékegység", menu=mertekegyseg)
        menubar.add_command(label="Kilépés", command=self.destroy)

    def unit_change(self, unit):
        self.unit = unit

        for i in self.sm.controls:
            i["mertekegyseg"].config(text = unit)

    def choose_object(self, shape = None):
        self.dimensions = {
            "a": 2,
            "b": 1,
            "d": 1
        }
        if shape == self.sm.shape:
            return 0
        if self.canvas is not None:
            self.sm.clear()
        if shape == "Rectangle" and self.sm.shape != "Rectangle":
            self.sm.shape = "Rectangle"
            self.sm.change_to_recrangle()
        elif shape == "Circle" and self.sm.shape != "Circle":
            self.sm.shape = "Circle"
            self.sm.change_to_circle()
        elif shape == "Ellipse":
            self.sm.shape = "Ellipse"
            self.sm.change_to_ellipse()
        elif shape == "Isosceles_triangle":
            self.sm.shape = "Isosceles_triangle"
            self.sm.change_to_isosceles_triangle()
        else:
            self.sm.shape = None
            print("Ez az alakzat még nincs definiálva...")
        plot(self, self.dimensions, self.sm.shape, self.coordinate_on, self.dimension_lines_on)
    
    def get_entry(self, number_of_entries):
        vissza = []
        for i in range(number_of_entries):
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
            self.dimensions["a"], self.dimensions["b"] = self.get_entry(2)
            if self.dimensions["a"] is None or self.dimensions["b"] is None:
                return -1
            self.values = Calc.Rectangle(self.dimensions["a"],self.dimensions["b"])
            self.sm.eredmeny1.config(text="I_x = " + str(round(self.values["Ix"], 4)) + " " + self.unit + "\u2074")
            self.sm.eredmeny2.config(text="I_y = " + str(round(self.values["Iy"], 4)) + " " + self.unit + "\u2074")
        elif self.sm.shape == "Circle":
            self.dimensions["d"] = self.get_entry(1)[0]
            if self.dimensions["d"] is None:
                return -1
            self.values = Calc.Circle(self.dimensions["d"])
            self.sm.eredmeny1.config(text="I_x = " + str(round(self.values["Ix"], 4)) + " " + self.unit + "\u2074")
            self.sm.eredmeny2.config(text="I_y = " + str(round(self.values["Iy"], 4)) + " " + self.unit + "\u2074")
        elif self.sm.shape == "Ellipse":
            self.dimensions["a"], self.dimensions["b"] = self.get_entry(2)
            if self.dimensions["a"] is None or self.dimensions["b"] is None:
                return -1
            self.values = Calc.Ellipse(self.dimensions["a"],self.dimensions["b"])
            self.sm.eredmeny1.config(text="I_x = " + str(round(self.values["Ix"], 4)) + " " + self.unit + "\u2074")
            self.sm.eredmeny2.config(text="I_y = " + str(round(self.values["Iy"], 4)) + " " + self.unit + "\u2074")
        elif self.sm.shape == "Isosceles_triangle":
            self.dimensions["a"], self.dimensions["b"] = self.get_entry(2)
            if self.dimensions["a"] is None or self.dimensions["b"] is None:
                return -1
            self.values = Calc.IsoscelesTriangle(self.dimensions["a"],self.dimensions["b"])
            self.sm.eredmeny1.config(text="I_x = " + str(round(self.values["Ix"], 4)) + " " + self.unit + "\u2074")
            self.sm.eredmeny2.config(text="I_y = " + str(round(self.values["Iy"], 4)) + " " + self.unit + "\u2074")
        else:
            print("Hiba, az alakzat nem talalhato")
        plot(self, self.dimensions, self.sm.shape, self.coordinate_on, self.dimension_lines_on)


    def doNothing(self):
        print("Ez a funkció jelenleg nem elérhető...")

# CALL THE WINDOW ---------------------------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    root = window()
    root.mainloop()