import tkinter as tk
from PIL import Image, ImageTk
import CalcFunctions as Calc
from SideMenu import SideMenu
from PlotFunctions import plot_circle, plot_ellipse, plot_rectangle, plot_isosceles_triangle

# MAIN WINDOW ---------------------------------------------------------------------------------------------------------------------------------
class window(tk.Tk):
    def __init__(self):
        super().__init__()
        # define main wondow paramters
        self.title("Statika calculator")
        self.geometry("1000x600")
        self.configure(bg = colors['main_color'])
        self.minsize(
            width = 600,
            height = 400
            )
        self.tk.call(
            'wm',
            'iconphoto',
            self._w,
            tk.PhotoImage(file='logo_A.png')
            )

        # Call AMSZ logo
        self.logo_img = Image.open("logo_Full.png")
        self.logo_img = ImageTk.PhotoImage(self.logo_img)
        self.logo_image = tk.Label(
            self,
            image=self.logo_img,
            bg = colors['main_color']
            )
        self.logo_image.image = self.logo_img
        self.logo_image.pack(side = tk.LEFT)
 
        # ??????????????????????????????????????? Ez mit csinál?
        # self.bind('<Return>', self.szamol)
        self.plotted = tk.BooleanVar(False)

        # call main window objects
        self.canvas = None
        self.sm = SideMenu(self)
        menubar = tk.Menu(self)
        self.config(menu = menubar)        
        keresztmetszet = tk.Menu(self, menubar, tearoff = 0)
        menubar.add_cascade(
            label = "Keresztmetszet",
            menu = keresztmetszet
            )
        menubar.add_command(
            label="Kilépés",
            command=self.destroy
            )
        keresztmetszet.add_command(
            label = "Téglalap",
            command = lambda: self.choose_object("Rectangle"))
        keresztmetszet.add_command(
            label = "Circle",
            command = lambda: self.choose_object("Circle")
            )
        keresztmetszet.add_command(
            label = "Ellipse",
            command = lambda: self.choose_object("Ellipse")
            )
        keresztmetszet.add_command(
            label = "ring",
            command = lambda: self.choose_object("ring")
            )
        keresztmetszet.add_command(
            label = "isosceles triangle",
            command = lambda: self.choose_object("Isosceles_triangle")
            )

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
        elif shape == "ring":
            self.sm.shape = "ring"
            self.sm.change_to_ring()
        elif shape == "Isosceles_triangle":
            self.sm.shape = "Isosceles_triangle"
            self.sm.change_to_isosceles_triangle()
            plot_isosceles_triangle(self, 2, 1, coordinate_on, dimension_lines_on)
        else:
            self.sm.shape = None
            print("Ez az alakzat még nincs definiálva...")
    
    def szamol(self, event=None):
        if self.sm.shape == "Rectangle":
            try:
                a = float(self.sm.e1.get().replace(',','.'))
            except:
                print("Hiba")
                self.sm.e1.config({"background": "#eb4034"})
                return -1
            try:
                b = float(self.sm.e2.get().replace(',','.'))
            except:
                self.sm.e2.config({"background": "#eb4034"})
                print("Hiba")
                return -1
            plot_rectangle(self,a,b, coordinate_on, dimension_lines_on)
            self.values = Calc.Rectangle(a,b)
            self.sm.eredmeny1.config(text="I_x = " + str(round(self.values["Ix"], 4)))
            self.sm.eredmeny2.config(text="I_y = " + str(round(self.values["Iy"], 4)))

        if self.sm.shape == "Ellipse":
            try:
                a = float(self.sm.e1.get().replace(',','.'))
            except:
                print("Hiba")
                self.sm.e1.config({"background": "#eb4034"})
                return -1
            try:
                b = float(self.sm.e2.get().replace(',','.'))
            except:
                self.sm.e2.config({"background": "#eb4034"})
                print("Hiba")
                return -1
            plot_ellipse(self, a, b, coordinate_on, dimension_lines_on)
            self.values = Calc.Ellipse(a, b)
            self.sm.eredmeny1.config(text="I_x = " + str(round(self.values["Ix"], 4)))
            self.sm.eredmeny2.config(text="I_y = " + str(round(self.values["Iy"], 4)))

        if self.sm.shape == "Circle":
            try:
                d = float(self.sm.e1.get().replace(',','.'))
            except:
                print("Hiba")
                self.sm.e1.config({"background": "#eb4034"})
                return -1
            plot_circle(self, coordinate_on)
            self.values = Calc.Circle(d)
            self.sm.eredmeny1.config(text="I_x = " + str(round(self.values["Ix"], 4)))
            self.sm.eredmeny2.config(text="I_y = " + str(round(self.values["Iy"], 4)))

        if self.sm.shape == "Isosceles_triangle":
            try:
                a = float(self.sm.e1.get().replace(',','.'))
            except:
                print("Hiba")
                self.sm.e1.config({"background": "#eb4034"})
                return -1
            try:
                b = float(self.sm.e2.get().replace(',','.'))
            except:
                self.sm.e2.config({"background": "#eb4034"})
                print("Hiba")
                return -1
            plot_isosceles_triangle(self, a, b, coordinate_on, dimension_lines_on)


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