import tkinter as tk
from PIL import Image, ImageTk
import CalcFunctions as Calc
import json
from SideMenu import SideMenu
from tkvideo import tkvideo
from PlotFunctions import plot

class starting_window(tk.Tk):
    def __init__(self):
        super().__init__()
        self.overrideredirect(1)

        # Position the window in the center of the page.
        positionRight = int(self.winfo_screenwidth()/2 - 240)
        positionDown = int(self.winfo_screenheight()/2 - 120)
        self.geometry("+{}+{}".format(positionRight, positionDown))

        # Play animation on tkinter widget
        my_label = tk.Label(self)
        my_label.pack()
        player = tkvideo("AMSZ_animation_short.mp4", my_label, loop = 0, size = (480,240))
        player.play()
        self.after(4000, lambda: self.destroy())

class main_window(tk.Tk):
    def __init__(self):
        super().__init__()

        # Variables
        self.coordinate_on = tk.BooleanVar(False)
        self.dimension_lines_on = tk.BooleanVar(False)
        self.transformed_coordinate_on = tk.BooleanVar(False)
        self.thickness_on = tk.BooleanVar(False)
        self.coordinate_on.set(True)
        self.dimension_lines_on.set(True)
        self.plotted = tk.BooleanVar(False)
        
        # Default unit, default theme
        self.unit = settings["default_unit"]#"mm"
        self.angle_unit = settings["angle_unit"] #! to settings
        self.theme = settings["theme"]#"dark"

        # Colors
        if self.theme == "dark":
            self.colors = DARK_THEME
        else:
            self.colors = LIGHT_THEME

        # Window 
        self.title("Statika számító")
        self.geometry("1000x600")
        self.configure(bg=self.colors['main_color'])
        self.minsize(width=200, height=200)
        self.tk.call('wm', 'iconphoto', self._w, tk.PhotoImage(file='logo_A.png'))

        # Canvas for drawing
        self.canvas = None

        # # Toolbar
        # self.toolbar = tk.Frame(self, bd=1, relief=tk.RAISED, bg=self.colors['main_color'])
        # self.img = Image.open("calc_button.png")
        # self.eimg = ImageTk.PhotoImage(self.img)
        # self.exitButton = tk.Button(self.toolbar, image=self.eimg, relief=tk.FLAT,
        #     command=self.quit)
        # self.exitButton.image = self.eimg
        # self.exitButton.pack(side=tk.LEFT, padx=2, pady=2)
        # self.toolbar.pack(side=tk.TOP, fill=tk.X)

        # Side Menu
        self.sm = SideMenu(self)
        self.sm.pack(side=tk.LEFT, fill=tk.Y)
        # calculate on pressing enter
        self.bind('<Return>', self.calculate)

        # Menubar
        menubar = tk.Menu(self)
        self.config(menu=menubar)

        # Add settings to menubar
        settings_menu = tk.Menu(self, menubar, tearoff=0)
        menubar.add_cascade(label="Beállítások", menu = settings_menu)

        # Add units menu to settings menu
        units_menu = tk.Menu(self, settings_menu, tearoff=0)
        units_menu.add_command(label="Milliméter [mm]", command=lambda: self.unit_change("length", "mm"))
        units_menu.add_command(label="Centiméter [cm]", command=lambda: self.unit_change("length", "cm"))
        units_menu.add_command(label="Méter [m]", command=lambda: self.unit_change("length", "m"))
        units_menu.add_command(label="Fok [°]", command=lambda: self.unit_change("degree", "°"))
        units_menu.add_command(label="Radián [rad]", command=lambda: self.unit_change("degree", "rad"))
        settings_menu.add_cascade(label="Mértékegység", menu=units_menu)

        # Add themes menu to setting menu
        themes_menu = tk.Menu(self, settings_menu, tearoff=0)
        themes_menu.add_command(label="Világos", command=lambda: self.theme_change("light"))
        themes_menu.add_command(label="Sötét",command=lambda: self.theme_change("dark"))
        settings_menu.add_cascade(label="Téma", menu=themes_menu)

        # Add exit button to menubar
        menubar.add_command(label="Kilépés", command=self.destroy)
    ## USEFUL FUNCTIONS -----------------------------------------------------------
    def theme_change(self, theme):
        if self.theme != theme:
            self.theme=theme
            if self.theme=="dark":
                self.colors=DARK_THEME
                self.sm.change_color(DARK_THEME)
                plot(self, self.sm.shape, self.coordinate_on.get(), self.dimension_lines_on.get(), self.transformed_coordinate_on.get(), self.thickness_on.get(), self.colors)
            elif self.theme == "light":
                self.colors=LIGHT_THEME
                self.sm.change_color(LIGHT_THEME)
                plot(self, self.sm.shape, self.coordinate_on.get(), self.dimension_lines_on.get(), self.transformed_coordinate_on.get(), self.thickness_on.get(), self.colors)
            else:
                print("ERROR: Unknown Theme")
                return -1
            self.configure(bg=self.colors['main_color'])
            #TODO: canvas color???? + plot
            print(f"Theme set to {theme}")

    def unit_change(self, unit_type, unit):
        if unit_type == "degree":
            self.angle_unit = unit
        else:
            self.unit = unit
        for i in self.sm.controls:
            if i["unit_type"] == unit_type:
                i["unit"].config(text = unit)

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
        plot(self, self.sm.shape, self.coordinate_on.get(), self.dimension_lines_on.get(), self.transformed_coordinate_on.get(), self.thickness_on.get(), self.colors)
    
    def get_entry(self, number_of_entries):
        vissza = []
        for i in range(number_of_entries + self.transformed_coordinate_on.get() * 3):
            if i >= 1 and self.sm.shape == "Circle": #! Jujj de csúnya...
                i+=1
            try:
                vissza.append(float(self.sm.controls[i]["entry"].get().replace(',','.')))
                self.sm.controls[i]["entry"].config({"background": "#475C6F"})
            except:
                print("Hiba")
                self.sm.controls[i]["entry"].config({"background": "#eb4034"})
                vissza.append(None)
        if self.thickness_on.get():
            try:
                t = float(self.sm.controls[-1]["entry"].get().replace(',','.'))
                self.sm.controls[-1]["entry"].config({"background": "#475C6F"})
            except:
                print("Hiba")
                self.sm.controls[-1]["entry"].config({"background": "#eb4034"})
                vissza.append(None)
                t = None
        else:
            t = 0
        #self.sm.e2.config({"background": "#475C6F"})    
        return vissza,t

    def calculate(self, event=None):
        if self.sm.shape == "Rectangle":
            vissza, t = self.get_entry(2)
            if None in vissza:
                return -1
            self.values = Calc.Rectangle(*vissza[:2], t, *vissza[2:], rad = self.angle_unit == "rad")
            self.sm.result1.config(text="I_x = " + str(round(self.values["Ix"], 4)) + " " + self.unit + "\u2074")
            self.sm.result2.config(text="I_y = " + str(round(self.values["Iy"], 4)) + " " + self.unit + "\u2074")
        elif self.sm.shape == "Circle":
            vissza, t = self.get_entry(1)
            if None in vissza:
                return -1
            self.values = Calc.Circle(vissza[0], t, *vissza[1:],rad = self.angle_unit == "rad")
            self.sm.result1.config(text="I_x = " + str(round(self.values["Ix"], 4)) + " " + self.unit + "\u2074")
            self.sm.result2.config(text="I_y = " + str(round(self.values["Iy"], 4)) + " " + self.unit + "\u2074")
        elif self.sm.shape == "Ellipse":
            vissza, t = self.get_entry(2)
            if None in vissza:
                return -1
            self.values = Calc.Ellipse(*vissza[:2], t, *vissza[2:],rad = self.angle_unit == "rad")
            self.sm.result1.config(text="I_x = " + str(round(self.values["Ix"], 4)) + " " + self.unit + "\u2074")
            self.sm.result2.config(text="I_y = " + str(round(self.values["Iy"], 4)) + " " + self.unit + "\u2074")
        elif self.sm.shape == "Isosceles_triangle":
            vissza, t = self.get_entry(2)
            if None in vissza:
                return -1
            self.values = Calc.IsoscelesTriangle(*vissza[:2], t, *vissza[2:],rad = self.angle_unit == "rad")
            self.sm.result1.config(text="I_x = " + str(round(self.values["Ix"], 4)) + " " + self.unit + "\u2074")
            self.sm.result2.config(text="I_y = " + str(round(self.values["Iy"], 4)) + " " + self.unit + "\u2074")
        else:
            print("Hiba, az alakzat nem talalhato")
        # plot(self, self.dimensions, self.sm.shape, self.coordinate_on.get(), self.dimension_lines_on.get(), self.transformed_coordinate_on.get())


    def doNothing(self):
        print("Ez a funkció jelenleg nem elérhető...")
# VARIABLES ---------------------------------------------------------------------------------------------------------------------------------------------
DARK_THEME = {
        'main_color': '#2C394B',
        'secondary_color': '#082032',
        'text_color': '#FF4C29',
        'entry_color': '#334756',
        'draw_main': '#FF4C29',
        'draw_secondary': 'black',
        'draw_tertiary': 'grey'
        }
LIGHT_THEME = {
        'main_color': '#FFFFFF',
        'secondary_color': '#999999',
        'text_color': '#000000',
        'entry_color': '#FFFFFF',
        'draw_main': '#1034A6',
        'draw_secondary': 'black',
        'draw_tertiary': 'grey'
        }

# CALL THE WINDOW ---------------------------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    # Load settings from JSON file
    try:
        with open('app_settings.json') as f:
            settings = json.load(f)
    except:
        print("404 app_settings.json not found")
        settings={'theme':'dark', 'default_unit':'mm', 'angle_unit':'rad'}
    master = starting_window()
    master.mainloop()
    root = main_window()
    root.mainloop()
    with open('app_settings.json', 'w') as json_file:
        json.dump({'theme':root.theme, 'default_unit':root.unit, 'angle_unit':root.angle_unit}, json_file)
