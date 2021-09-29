import tkinter as tk
from tkinter import BooleanVar, Toplevel, ttk
from tkinter.constants import BOTH
from PIL import Image, ImageTk
import CalcFunctions as Calc
import json
from SideMenu import SideMenu
from tkvideo import tkvideo
from PlotFunctions import plot
import shape_builder

## ANIMATION WINDOW -----------------------------------------------------------------------------------------------------------------------------------------------------------
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

## MAIN WINDOW -----------------------------------------------------------------------------------------------------------------------------------------------------------
class main_window(tk.Tk):
    def __init__(self):
        super().__init__()

        # main window opening size
        self.win_width = 1200
        self.win_height = 650

        # screen size
        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()

        # boolean to decide if the window can fit to the screen
        self.size_ok = tk.BooleanVar(False)
        if self.win_width<self.screen_width/4*3 or self.win_height<self.screen_height/4*3:
            self.size_ok.set(True)

        # Position the window in the center of the page.
        positionRight = int(self.winfo_screenwidth()/2 - self.win_width/2)
        positionDown = int(self.winfo_screenheight()/2 - self.win_height/2)
        self.geometry("+{}+{}".format(positionRight, positionDown))

        # Variables
        self.coordinate_on = tk.BooleanVar(False)
        self.dimension_lines_on = tk.BooleanVar(False)
        self.transformed_coordinate_on = tk.BooleanVar(False)
        self.thickness_on = tk.BooleanVar(False)
        self.coordinate_on.set(True)
        self.dimension_lines_on.set(True)
        self.plotted = tk.BooleanVar(False)
        self.shape_builder_mode = False
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
        if self.size_ok.get() == False:
            self.state("zoomed")          # Fullscreen
        self.geometry(f"{self.win_width}x{self.win_height}")
        self.configure(bg=self.colors['main_color'])
        self.minsize(width=200, height=200)
        self.tk.call('wm', 'iconphoto', self._w, tk.PhotoImage(file='logo_A.png'))
        # self.iconbitmap("AMSZ.ico")


        # custom menubar
        self.menu_canvas = tk.Canvas(self, bg=self.colors['secondary_color'], highlightthickness=0, height=26)
        self.menu_canvas.pack(fill = tk.X)
        # custom menubar objects
        self.setting_button_img = tk.PhotoImage(file=f"{self.colors['path']}menubar/settings.png")
        self.setting_button = self.menu_canvas.create_image(0,0,anchor=tk.NW,image=self.setting_button_img)
        self.menu_canvas.tag_bind(self.setting_button, '<Button-1>', lambda e: settings_window(self))

        self.basic_button_img = tk.PhotoImage(file=f"{self.colors['path']}/menubar/basic.png")
        self.change_button_img = tk.PhotoImage(file='figures/menubar/change.png')
        self.change_button = self.menu_canvas.create_image(143,0,anchor=tk.NW,image=self.change_button_img)
        self.menu_canvas.tag_bind(self.change_button, '<Button-1>', lambda e: self.build_shape())

        def settings_window(self):
            # Variables:
            unit_clicked = BooleanVar(False)
            theme_clicked = BooleanVar(False)

            win_width = 330
            win_height = 220
            # Position the window in the center of the page.
            positionRight = int(self.winfo_screenwidth()/2 - win_width/2)
            positionDown = int(self.winfo_screenheight()/2 - win_height/2)

            self.settings_window = tk.Toplevel(self, takefocus = True, bg=self.colors['main_color'])
            self.settings_window.geometry("+{}+{}".format(positionRight, positionDown))
            self.settings_window.lift()
            self.settings_window.wm_attributes('-topmost',True)
            self.settings_window.title("Beállítások")
            self.settings_window.geometry(f"{win_width}x{win_height}")
            self.settings_window.resizable(0, 0)

            # setting window menubar
            self.settings_menu = tk.Canvas(self.settings_window, bg=self.colors['secondary_color'], highlightthickness=0, height=26)
            self.settings_menu.pack(fill = tk.X)

            self.settings_menu_options = tk.Canvas(self.settings_window, bg=self.colors['main_color'], highlightthickness=0)
            self.settings_menu_options.pack(fill = tk.BOTH)

            # menubar objects
            self.unit_button_img = tk.PhotoImage(file='figures/settings/unit.png')
            self.unit_button = self.settings_menu.create_image(0,0,anchor=tk.NW,image=self.unit_button_img)
            self.settings_menu.tag_bind(self.unit_button, '<Button-1>', lambda e:unit_button_click())

            self.mm_img = tk.PhotoImage(file='figures/settings/mm.png')
            self.cm_img = tk.PhotoImage(file='figures/settings/cm.png')
            self.m_img = tk.PhotoImage(file='figures/settings/m.png')
            self.deg_img = tk.PhotoImage(file='figures/settings/deg.png')
            self.rad_img = tk.PhotoImage(file='figures/settings/rad.png')
            self.mm_clicked_img = tk.PhotoImage(file='figures/settings/mm_clicked.png')
            self.cm_clicked_img = tk.PhotoImage(file='figures/settings/cm_clicked.png')
            self.m_clicked_img = tk.PhotoImage(file='figures/settings/m_clicked.png')
            self.deg_clicked_img = tk.PhotoImage(file='figures/settings/deg_clicked.png')
            self.rad_clicked_img = tk.PhotoImage(file='figures/settings/rad_clicked.png')

            self.theme_button_img = tk.PhotoImage(file='figures/settings/theme.png')
            self.theme_button = self.settings_menu.create_image(135,0,anchor=tk.NW,image=self.theme_button_img)
            self.settings_menu.tag_bind(self.theme_button, '<Button-1>', lambda e:theme_button_click())

            self.light_img = tk.PhotoImage(file='figures/settings/light.png')
            self.dark_img = tk.PhotoImage(file='figures/settings/dark.png')
            self.light_clicked_img = tk.PhotoImage(file='figures/settings/light_clicked.png')
            self.dark_clicked_img = tk.PhotoImage(file='figures/settings/dark_clicked.png')

            self.ok_img = tk.PhotoImage(file='figures/settings/ok.png')

            def unit_button_click():
                if unit_clicked.get() == False:
                    unit_clicked.set(True)
                    if theme_clicked.get() == False:
                        theme_clicked.set(False)
                        self.mm = self.settings_menu_options.create_image(20,20,anchor=tk.NW,image=self.mm_img)
                        self.cm = self.settings_menu_options.create_image(20,41,anchor=tk.NW,image=self.cm_img)
                        self.m = self.settings_menu_options.create_image(20,62,anchor=tk.NW,image=self.m_img)
                        self.deg = self.settings_menu_options.create_image(173,20,anchor=tk.NW,image=self.deg_img)
                        self.rad = self.settings_menu_options.create_image(173,41,anchor=tk.NW,image=self.rad_img)
                        self.ok = self.settings_menu_options.create_image(190,150,anchor=tk.NW,image=self.ok_img)
                    else:
                        theme_clicked.set(False)
                        self.settings_menu_options.delete('all')
                        self.mm = self.settings_menu_options.create_image(20,20,anchor=tk.NW,image=self.mm_img)
                        self.cm = self.settings_menu_options.create_image(20,41,anchor=tk.NW,image=self.cm_img)
                        self.m = self.settings_menu_options.create_image(20,62,anchor=tk.NW,image=self.m_img)
                        self.deg = self.settings_menu_options.create_image(173,20,anchor=tk.NW,image=self.deg_img)
                        self.rad = self.settings_menu_options.create_image(173,41,anchor=tk.NW,image=self.rad_img)
                        self.ok = self.settings_menu_options.create_image(190,150,anchor=tk.NW,image=self.ok_img)
                        # self.settings_menu_options.delete(self.light)
                        # self.settings_menu_options.delete(self.dark)
                        # self.settings_menu_options.delete(self.ok)
            def theme_button_click():
                if theme_clicked.get() == False:
                    theme_clicked.set(True)
                    if unit_clicked.get() == False:
                        unit_clicked.set(False)
                        self.light = self.settings_menu_options.create_image(30,20,anchor=tk.NW,image=self.light_img)
                        self.dark = self.settings_menu_options.create_image(180,20,anchor=tk.NW,image=self.dark_img)
                        self.ok = self.settings_menu_options.create_image(190,150,anchor=tk.NW,image=self.ok_img)
                    else:
                        unit_clicked.set(False)
                        self.settings_menu_options.delete('all')
                        self.light = self.settings_menu_options.create_image(30,20,anchor=tk.NW,image=self.light_img)
                        self.dark = self.settings_menu_options.create_image(180,20,anchor=tk.NW,image=self.dark_img)
                        self.ok = self.settings_menu_options.create_image(190,150,anchor=tk.NW,image=self.ok_img)
                        # self.settings_menu_options.delete(self.mm)
                        # self.settings_menu_options.delete(self.cm)
                        # self.settings_menu_options.delete(self.m)
                        # self.settings_menu_options.delete(self.deg)
                        # self.settings_menu_options.delete(self.rad)
                        # self.settings_menu_options.delete(self.ok)

        # Canvas for drawing
        self.canvas = None

        # Side Menu
        self.sm = SideMenu(self)
        self.sm.pack(side=tk.LEFT, padx = (20,10), pady = 20, fill=tk.Y)
        # self.sm.pack(side=tk.LEFT, fill=tk.Y)
        # calculate on pressing enter
        self.bind('<Return>', self.calculate)

        # # Menubar
        # self.menubar = tk.Menu(self)
        # self.config(menu=self.menubar)

        # # Add settings to menubar
        # settings_menu = tk.Menu(self, self.menubar, tearoff=0)
        # self.menubar.add_cascade(label="Beállítások", menu = settings_menu)

        # # Add units menu to settings menu
        # units_menu = tk.Menu(self, settings_menu, tearoff=0)
        # units_menu.add_command(label="Milliméter [mm]", command=lambda: self.unit_change("length", "mm"))
        # units_menu.add_command(label="Centiméter [cm]", command=lambda: self.unit_change("length", "cm"))
        # units_menu.add_command(label="Méter [m]", command=lambda: self.unit_change("length", "m"))
        # units_menu.add_command(label="Fok [°]", command=lambda: self.unit_change("degree", "°"))
        # units_menu.add_command(label="Radián [rad]", command=lambda: self.unit_change("degree", "rad"))
        # settings_menu.add_cascade(label="Mértékegység", menu=units_menu)

        # # Add themes menu to setting menu
        # themes_menu = tk.Menu(self, settings_menu, tearoff=0)
        # themes_menu.add_command(label="Világos", command=lambda: self.theme_change("light"))
        # themes_menu.add_command(label="Sötét",command=lambda: self.theme_change("dark"))
        # settings_menu.add_cascade(label="Téma", menu=themes_menu)

        # #Changing to shape builder
        # self.menubar.add_command(label="Saját alakzat", command=self.build_shape)
        # # Add exit button to menubar
        # self.menubar.add_command(label="Kilépés", command=self.destroy)
        
    ## USEFUL FUNCTIONS -----------------------------------------------------------------------------------------------------------------------------------------------------------
    # def start_move(self, event):
    #     self.x = event.x
    #     self.y = event.y

    # def stop_move(self,event):
    #     self.x = None
    #     self.y = None

    # def do_move(self, event):
    #     deltax = event.x - self.x
    #     deltay = event.y - self.y
    #     x = self.winfo_x() + deltax
    #     y = self.winfo_y() + deltay
    #     self.geometry(f"+{x}+{y}")
    
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

    def build_shape(self):
        if not self.shape_builder_mode:
            print("opening sb")
            self.shape_builder_mode = True
            self.sm.pack_forget()
            self.sb_sm = shape_builder.sb_side_menu(self)
            self.sb_sm.pack(side=tk.LEFT, fill=tk.Y)
            self.sb = shape_builder.shapeBuilder(self, self.sb_sm)
            self.menu_canvas.itemconfig (self.change_button, image=self.basic_button_img)
            # self.menubar.entryconfig(2,label="Alap alakzatok")
            # self.menubar.entryconfig(1, state="disabled")
            if self.plotted==True:
                self.canvas._tkcanvas.destroy()
            self.sb.pack(expand=tk.YES, fill=tk.BOTH, padx = (20,10), pady = 20)
        else:
            print("closing sb")
            self.sb.pack_forget()
            self.sb_sm.pack_forget()
            self.sm.pack(side=tk.LEFT, fill=tk.Y, padx = (20,10), pady = 20)
            self.plotted = False
            self.shape_builder_mode = False
            self.menu_canvas.itemconfig (self.change_button, image=self.change_button_img)
            # self.menubar.entryconfig(2,label="Saját alakzat")
            # self.menubar.entryconfig(1, state="normal")


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
                self.sm.controls[i]["entry"].config({"background": self.colors['secondary_color']})
            except:
                print("Hiba")
                self.sm.controls[i]["entry"].config({"background": "#eb4034"})
                vissza.append(None)
        if self.thickness_on.get():
            t = float(self.sm.controls[-1]["entry"].get().replace(',','.')) # ITT VALAMI NEM JÓ MÉG
            a = float(self.sm.controls[0]["entry"].get().replace(',','.'))
            b = float(self.sm.controls[1]["entry"].get().replace(',','.'))
            if t < a/2 and t < b/2:    
                try:
                    t = float(self.sm.controls[-1]["entry"].get().replace(',','.'))
                    self.sm.controls[-1]["entry"].config({"background": "#475C6F"})
                except:
                    print("Hiba")
                    self.sm.controls[-1]["entry"].config({"background": "#eb4034"})
                    vissza.append(None)
                    t = None
            else:
                if t >= a/2 and t <= b/2:
                    self.sm.controls[0]["entry"].config({"background": "#eb4034"})
                    vissza.append(None)
                elif t >= b/2 and t <= a/2:
                    self.sm.controls[1]["entry"].config({"background": "#eb4034"})
                    vissza.append(None)
                elif t >= b/2 and t >= a/2:
                    self.sm.controls[0]["entry"].config({"background": "#eb4034"})
                    self.sm.controls[1]["entry"].config({"background": "#eb4034"})
                    vissza.append(None)
                
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
            self.sm.result1.config(text="A = " + str(round(self.values["A"], 4)) + " " + self.unit + "²")
            self.sm.result2.config(text="Iₓ = " + str(round(self.values["Ix"], 4)) + " " + self.unit + "\u2074")
            self.sm.result3.config(text="Iᵧ = " + str(round(self.values["Iy"], 4)) + " " + self.unit + "\u2074")
            self.sm.result4.config(text="Iₓᵧ = " + str(round(self.values["Ixy"], 4)) + " " + self.unit + "\u2074")
            self.sm.result5.config(text="Kₓ = " + str(round(self.values["Kx"], 4)) + " " + self.unit + "\u2074")
            self.sm.result6.config(text="Kᵧ = " + str(round(self.values["Ky"], 4)) + " " + self.unit + "\u2074")
        elif self.sm.shape == "Circle":
            vissza, t = self.get_entry(1)
            if None in vissza:
                return -1
            self.values = Calc.Circle(vissza[0], t, *vissza[1:],rad = self.angle_unit == "rad")
            self.sm.result1.config(text="A = " + str(round(self.values["A"], 4)) + " " + self.unit + "²")
            self.sm.result2.config(text="Iₓ = Iᵧ = " + str(round(self.values["Ix"], 4)) + " " + self.unit + "\u2074")
            self.sm.result3.config(text="Iₓᵧ = " + str(round(self.values["Ixy"], 4)) + " " + self.unit + "\u2074")
            self.sm.result4.config(text="Kₓ = " + str(round(self.values["Kx"], 4)) + " " + self.unit + "\u2074")
            self.sm.result5.config(text="Kᵧ = " + str(round(self.values["Ky"], 4)) + " " + self.unit + "\u2074")
        elif self.sm.shape == "Ellipse":
            vissza, t = self.get_entry(2)
            if None in vissza:
                return -1
            self.values = Calc.Ellipse(*vissza[:2], t, *vissza[2:],rad = self.angle_unit == "rad")
            self.sm.result1.config(text="A = " + str(round(self.values["A"], 4)) + " " + self.unit + "²")
            self.sm.result2.config(text="Iₓ = " + str(round(self.values["Ix"], 4)) + " " + self.unit + "\u2074")
            self.sm.result3.config(text="Iᵧ = " + str(round(self.values["Iy"], 4)) + " " + self.unit + "\u2074")
            self.sm.result4.config(text="Iₓᵧ = " + str(round(self.values["Ixy"], 4)) + " " + self.unit + "\u2074")
            self.sm.result5.config(text="Kₓ = " + str(round(self.values["Kx"], 4)) + " " + self.unit + "\u2074")
            self.sm.result6.config(text="Kᵧ = " + str(round(self.values["Ky"], 4)) + " " + self.unit + "\u2074")
        elif self.sm.shape == "Isosceles_triangle":
            vissza, t = self.get_entry(2)
            if None in vissza:
                return -1
            self.values = Calc.IsoscelesTriangle(*vissza[:2], t, *vissza[2:],rad = self.angle_unit == "rad")
            self.sm.result1.config(text="A = " + str(round(self.values["A"], 4)) + " " + self.unit + "²")
            self.sm.result2.config(text="Iₓ = " + str(round(self.values["Ix"], 4)) + " " + self.unit + "\u2074")
            self.sm.result3.config(text="Iᵧ = " + str(round(self.values["Iy"], 4)) + " " + self.unit + "\u2074")
            self.sm.result4.config(text="Iₓᵧ = " + str(round(self.values["Ixy"], 4)) + " " + self.unit + "\u2074")
            self.sm.result5.config(text="Kₓ = " + str(round(self.values["Kx"], 4)) + " " + self.unit + "\u2074")
            self.sm.result6.config(text="Kᵧ = " + str(round(self.values["Ky"], 4)) + " " + self.unit + "\u2074")
        else:
            print("Hiba, az alakzat nem talalhato")
        # plot(self, self.dimensions, self.sm.shape, self.coordinate_on.get(), self.dimension_lines_on.get(), self.transformed_coordinate_on.get())


    def doNothing(self):
        print("Ez a funkció jelenleg nem elérhető...")
# VARIABLES ---------------------------------------------------------------------------------------------------------------------------------------------
DARK_THEME = {
        # 'main_color': '#2C394B',
        # 'secondary_color': '#082032',
        'main_color': '#1a1a1a',
        'secondary_color': '#333333',
        'text_color': '#cccccc',
        'entry_color': '#334756',
        'draw_main': '#87aade',
        'draw_secondary': '#1a1a1a',
        'draw_tertiary': 'grey',
        'path': 'figures/dark_theme/'
        }
LIGHT_THEME = {
        'main_color': '#FFFFFF',
        'secondary_color': '#999999',
        'text_color': '#000000',
        'entry_color': '#FFFFFF',
        'draw_main': '#1034A6',
        'draw_secondary': 'black',
        'draw_tertiary': 'grey',
        'path': 'figures/light_theme/'
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
    # master = starting_window()
    # master.mainloop()
    root = main_window()
    root.mainloop()
    with open('app_settings.json', 'w') as json_file:
        json.dump({'theme':root.theme, 'default_unit':root.unit, 'angle_unit':root.angle_unit}, json_file)
