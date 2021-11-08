import tkinter as tk
from tkinter import BooleanVar, Toplevel, ttk
from tkinter.constants import BOTH
from PIL import Image, ImageTk
from numpy.core.fromnumeric import shape
import CalcFunctions as Calc
import json
from SideMenu import SideMenu
from tkvideo import tkvideo
from PlotFunctions import plot, plot_principal_axes
import shape_builder
from SettingsWindow import settings_window
import numpy as np
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
        self.after(4500, lambda: self.destroy())

## MAIN WINDOW -----------------------------------------------------------------------------------------------------------------------------------------------------------
class main_window(tk.Tk):
    # def onExit(self):
    #     self.quit()
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
        self.window_open = BooleanVar(False)
        # Default unit, default theme
        self.unit = settings["default_unit"]#"mm"
        self.angle_unit = settings["angle_unit"] #! to settings
        self.theme = settings["theme"]#"dark"
        self.logo_enabled = settings["logo_enabled"]

        #shape builder configuration
        self.show_orig_axis = True
        self.show_orig_axis_bool = tk.BooleanVar()
        self.show_orig_axis_bool.set(self.show_orig_axis)
        self.orig_axis_dissapier = False
        self.orig_axis_dissapier_bool = tk.BooleanVar()
        self.orig_axis_dissapier_bool.set(self.orig_axis_dissapier)
        self.sb_ha_vis = True #visualizing hauptachsen in sb mode 
        self.sb_ha_vis_bool = tk.BooleanVar()
        self.sb_ha_vis_bool.set(self.sb_ha_vis)
        self.calc_for_orig_axis = False
        self.calc_for_orig_axis_bool = tk.BooleanVar()
        self.calc_for_orig_axis_bool.set(self.calc_for_orig_axis)

        # Play AMSZ logo on startup
        self.play_logo = tk.BooleanVar(False)
        if self.logo_enabled == 'True':
            self.play_logo.set(True)
        else:
            self.play_logo.set(False)

        # Colors
        if self.theme == "dark":
            self.colors = DARK_THEME
        else:
            self.colors = LIGHT_THEME

        ## Window -------------------------------------------------------------------------------------------------------------------------------------------------------------------
        self.title("Statika számító")
        if self.size_ok.get() == False:
            self.state("zoomed")          # Fullscreen
        self.geometry(f"{self.win_width}x{self.win_height}")
        self.configure(bg=self.colors['main_color'])
        self.minsize(width=200, height=200)
        self.tk.call('wm', 'iconphoto', self._w, tk.PhotoImage(file='logo_A.png'))
        # self.iconbitmap("AMSZ.ico")


        ## custom menubar -----------------------------------------------------------------------------------------------------------------------------------------------------------
        self.menu_canvas = tk.Canvas(self, bg=self.colors['secondary_color'], highlightthickness=0, height=26)
        self.menu_canvas.pack(fill = tk.X)
        # custom menubar objects
        self.setting_button_img = tk.PhotoImage(file=f"{self.colors['path']}menubar/settings.png")
        self.setting_button_hover_img = tk.PhotoImage(file=f"{self.colors['path']}menubar/settings_hover.png")
        self.setting_button = self.menu_canvas.create_image(0,0,anchor=tk.NW,image=self.setting_button_img)
        self.menu_canvas.tag_bind(self.setting_button, '<Button-1>', lambda e: settings_window(self))
        self.menu_canvas.tag_bind(self.setting_button, '<Enter>', lambda e:self.menu_canvas.itemconfig(self.setting_button,
        image=self.setting_button_hover_img))
        self.menu_canvas.tag_bind(self.setting_button, '<Leave>', lambda e:self.menu_canvas.itemconfig(self.setting_button,
        image=self.setting_button_img))

        self.basic_button_img = tk.PhotoImage(file=f"{self.colors['path']}/menubar/basic.png")
        self.basic_button_hover_img = tk.PhotoImage(file=f"{self.colors['path']}/menubar/basic_hover.png")
        self.change_button_img = tk.PhotoImage(file=f"{self.colors['path']}menubar/change.png")
        self.change_button_hover_img = tk.PhotoImage(file=f"{self.colors['path']}menubar/change_hover.png")
        self.change_button = self.menu_canvas.create_image(93,0,anchor=tk.NW,image=self.change_button_img)
        self.menu_canvas.tag_bind(self.change_button, '<Button-1>', lambda e: self.build_shape())
        self.menu_canvas.tag_bind(self.change_button, '<Enter>', lambda e:self.menu_canvas.itemconfig(self.change_button,
        image=self.change_button_hover_img))
        self.menu_canvas.tag_bind(self.change_button, '<Leave>', lambda e:self.menu_canvas.itemconfig(self.change_button,
        image=self.change_button_img))

        # Canvas for drawing
        self.canvas = None

        # Side Menu
        self.sm = SideMenu(self)
        self.sm.pack(side=tk.LEFT, padx = (20,10), pady = 20, fill=tk.Y)
        # self.sm.pack(side=tk.LEFT, fill=tk.Y)
        # calculate on pressing enter
        self.bind('<Return>', self.calculate)

        # canvas
        plot(self, None, False, False, False, False, self.colors)
        
    ## USEFUL FUNCTIONS ----------------------------------------------------------------------------------------------------------------------------------------------------------- 
    def theme_change(self, theme):
        if self.theme != theme:
            self.theme=theme
            if self.theme=="dark":
                self.colors=DARK_THEME
                self.sm.change_color(DARK_THEME)
            elif self.theme == "light":
                self.colors=LIGHT_THEME
                self.sm.change_color(LIGHT_THEME)
            else:
                print("ERROR: Unknown Theme")
                return -1
            self.configure(bg=self.colors['main_color'])
            settings['theme']=self.theme
            self.destroy()
            self.__init__()
            # plot(self, None, False, False, False, False, self.colors)
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
        try:
            for i in self.sb.controls:
                if i["unit_type"] == unit_type:
                    i["unit"].config(text = unit)
        except:
            None
    def build_shape(self):
        if not self.shape_builder_mode:
            print("opening sb")
            self.shape_builder_mode = True
            self.sm.pack_forget()
            self.sb_sm = shape_builder.sb_side_menu(self)
            self.sb_sm.pack(side=tk.LEFT, fill=tk.Y, padx = (20,10), pady = 20)
            self.sb = shape_builder.shapeBuilder(self, self.sb_sm)

            self.change_button_img = tk.PhotoImage(file=f"{self.colors['path']}menubar/basic.png")
            self.change_button_hover_img = tk.PhotoImage(file=f"{self.colors['path']}menubar/basic_hover.png")
            self.menu_canvas.itemconfig (self.change_button, image=self.change_button_img)
            if self.plotted==True:
                self.canvas._tkcanvas.destroy()
            self.sb.pack(expand=tk.YES, fill=tk.BOTH, padx = (10,20), pady = 20)
        else:
            print("closing sb")
            self.sb.pack_forget()
            self.sb_sm.pack_forget()
            self.sm.pack(side=tk.LEFT, fill=tk.Y, padx = (20,10), pady = 20)
            self.sm.clear()
            # self.sm.combo_clear()
            self.sm.combo_default.grid(row=1, column=0, columnspan=5)
            self.plotted = False
            self.shape_builder_mode = False
            self.shape = None
            plot(self, None, False, False, False, False, self.colors)

            self.change_button_img = tk.PhotoImage(file=f"{self.colors['path']}menubar/change.png")
            self.change_button_hover_img = tk.PhotoImage(file=f"{self.colors['path']}menubar/change_hover.png")
            self.menu_canvas.itemconfig (self.change_button, image=self.change_button_img)


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
        if shape == "Rectangle":
            self.sm.shape = "Rectangle"
            self.sm.change_to_recrangle()
        elif shape == "Circle":
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
                self.sm.controls[i]["entry"].config({"background": self.colors['entry_color']})
            except:
                print("Hiba")
                self.sm.controls[i]["entry"].config({"background": self.colors['error_color']})
                for i in self.sm.indicators:
                        i.config(text="")
                self.sm.result1.config(text="Hiba a bemeneti adatokban!")
                vissza.append(None)
        if self.thickness_on.get(): 
            if self.sm.shape == "Circle":
                t = float(self.sm.controls[-1]["entry"].get().replace(',','.'))
                d = float(self.sm.controls[0]["entry"].get().replace(',','.'))
                if t <= d/2:
                    print("kor lehetseges")
                    t = float(self.sm.controls[-1]["entry"].get().replace(',','.'))
                    self.sm.controls[-1]["entry"].config({"background": self.colors['entry_color']})
                else:
                    print("Hiba")
                    self.sm.controls[-1]["entry"].config({"background": self.colors['error_color']})
                    for i in self.sm.indicators:
                        i.config(text="")
                    self.sm.result1.config(text="Hiba a falvastagságban!")
                    vissza.append(None)
                    t = None
            elif self.sm.shape == "Isosceles_triangle":
                t = float(self.sm.controls[-1]["entry"].get().replace(',','.')) 
                a = float(self.sm.controls[0]["entry"].get().replace(',','.'))
                b = float(self.sm.controls[1]["entry"].get().replace(',','.'))
                phi = np.arctan(a / (b / 2))
                s1 = a * np.sin(phi)
                s2 = b
                if t < s1/2 and t < s2/2:
                    print("haromszog lehetseges")     
                    try:
                        t = float(self.sm.controls[-1]["entry"].get().replace(',','.'))
                        self.sm.controls[-1]["entry"].config({"background": "#475C6F"})
                    except:
                        print("Hiba")
                        self.sm.controls[-1]["entry"].config({"background": "#eb4034"})
                        for i in self.sm.indicators:
                            i.config(text="")
                        self.sm.result1.config(text="Hiba a bemeneti adatokban!")
                        self.sm.result2.config(text="Hiba a falvastagságban!")
                        vissza.append(None)
                        t = None
                else:
                    if t >= s1/2 and s1 == s2:
                        self.sm.controls[0]["entry"].config({"background": "#eb4034"})
                        self.sm.controls[1]["entry"].config({"background": "#eb4034"})
                        self.sm.controls[-1]["entry"].config({"background": "#eb4034"})
                        for i in self.sm.indicators:
                            i.config(text="")
                        self.sm.result1.config(text="Hiba a bemeneti adatokban!")
                        self.sm.result2.config(text="Hiba a falvastagságban!")
                    if t >= s1/2 and t <= s2/2:
                        self.sm.controls[0]["entry"].config({"background": "#eb4034"})
                        self.sm.controls[-1]["entry"].config({"background": "#eb4034"})
                        for i in self.sm.indicators:
                            i.config(text="")
                        self.sm.result1.config(text="Hiba a bemeneti adatokban!")
                        self.sm.result2.config(text="Hiba a falvastagságban!")
                        vissza.append(None)
                    elif t >= s2/2 and t <= s1/2:
                        self.sm.controls[1]["entry"].config({"background": "#eb4034"})
                        self.sm.controls[-1]["entry"].config({"background": "#eb4034"})
                        for i in self.sm.indicators:
                            i.config(text="")
                        self.sm.result1.config(text="Hiba a bemeneti adatokban!")
                        self.sm.result2.config(text="Hiba a falvastagságban!")
                        vissza.append(None)
                    elif t >= s2/2 and t >= s1/2:
                        self.sm.controls[0]["entry"].config({"background": "#eb4034"})
                        self.sm.controls[1]["entry"].config({"background": "#eb4034"})
                        for i in self.sm.indicators:
                            i.config(text="")
                        self.sm.result1.config(text="Hiba a bemeneti adatokban!")
                        self.sm.result2.config(text="Hiba a falvastagságban!")
                        vissza.append(None)
            else:
                t = float(self.sm.controls[-1]["entry"].get().replace(',','.')) 
                a = float(self.sm.controls[0]["entry"].get().replace(',','.'))
                b = float(self.sm.controls[1]["entry"].get().replace(',','.'))
                if t < a/2 and t < b/2:
                    print("lehetseges")     
                    try:
                        t = float(self.sm.controls[-1]["entry"].get().replace(',','.'))
                        self.sm.controls[-1]["entry"].config({"background": self.colors['entry_color']})
                    except:
                        print("Hiba")
                        self.sm.controls[-1]["entry"].config({"background": self.colors['error_color']})
                        for i in self.sm.indicators:
                            i.config(text="")
                        self.sm.result1.config(text="Hiba a bemeneti adatokban!")
                        self.sm.result2.config(text="Hiba a falvastagságban!")
                        vissza.append(None)
                        t = None
                else:
                    if t >= a/2 and a == b:
                        self.sm.controls[0]["entry"].config({"background": "#eb4034"})
                        self.sm.controls[1]["entry"].config({"background": "#eb4034"})
                        self.sm.controls[-1]["entry"].config({"background": "#eb4034"})
                        for i in self.sm.indicators:
                            i.config(text="")
                        self.sm.result1.config(text="Hiba a bemeneti adatokban!")
                        self.sm.result2.config(text="Hiba a falvastagságban!")
                    if t >= a/2 and t <= b/2:
                        self.sm.controls[0]["entry"].config({"background": "#eb4034"})
                        self.sm.controls[-1]["entry"].config({"background": "#eb4034"})
                        for i in self.sm.indicators:
                            i.config(text="")
                        self.sm.result1.config(text="Hiba a bemeneti adatokban!")
                        self.sm.result2.config(text="Hiba a falvastagságban!")
                        vissza.append(None)
                    elif t >= b/2 and t <= a/2:
                        self.sm.controls[1]["entry"].config({"background": "#eb4034"})
                        self.sm.controls[-1]["entry"].config({"background": "#eb4034"})
                        for i in self.sm.indicators:
                            i.config(text="")
                        self.sm.result1.config(text="Hiba a bemeneti adatokban!")
                        self.sm.result2.config(text="Hiba a falvastagságban!")
                        vissza.append(None)
                    elif t >= a/2 and t >= b/2:
                        self.sm.controls[0]["entry"].config({"background": "#eb4034"})
                        self.sm.controls[1]["entry"].config({"background": "#eb4034"})
                        for i in self.sm.indicators:
                            i.config(text="")
                        self.sm.result1.config(text="Hiba a bemeneti adatokban!")
                        self.sm.result2.config(text="Hiba a falvastagságban!")
                        vissza.append(None)
                    else:
                        self.sm.controls[0]["entry"].config({"background": "#eb4034"})
                        self.sm.controls[1]["entry"].config({"background": "#eb4034"})
                        self.sm.controls[-1]["entry"].config({"background": "#eb4034"})
                        for i in self.sm.indicators:
                            i.config(text="")
                        self.sm.result1.config(text="Hiba a bemeneti adatokban!")
                        self.sm.result2.config(text="Hiba a falvastagságban!")
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
            if self.transformed_coordinate_on.get() == True:
                print("transcoord")
                self.sm.result2.config(text="Iₓ₁ = " + str(round(self.values["Ixi"], 4)) + " " + self.unit + "\u2074")
                self.sm.result3.config(text="Iᵧ₁ = " + str(round(self.values["Ieta"], 4)) + " " + self.unit + "\u2074")
                self.sm.result4.config(text="Iₓ₁ᵧ₁ = " + str(round(self.values["Ixieta"], 4)) + " " + self.unit + "\u2074")
            else:
                print("notrans")
                self.sm.result2.config(text="Iₓ = " + str(round(self.values["Ix"], 4)) + " " + self.unit + "\u2074")
                self.sm.result3.config(text="Iᵧ = " + str(round(self.values["Iy"], 4)) + " " + self.unit + "\u2074")
                self.sm.result4.config(text="Iₓᵧ = " + str(round(self.values["Ixy"], 4)) + " " + self.unit + "\u2074")
            self.sm.result5.config(text="Főmásodrendű nyomatékok:")
            if round(self.values["Ix"], 4) > round(self.values["Iy"], 4):
                self.sm.result6.config(text="I₁ = " + str(round(self.values["Ix"], 4)) + " " + self.unit + "\u2074")
                self.sm.result7.config(text="I₂ = " + str(round(self.values["Iy"], 4)) + " " + self.unit + "\u2074")
            else:
                self.sm.result8.config(text="I₁ = " + str(round(self.values["Iy"], 4)) + " " + self.unit + "\u2074")
                self.sm.result9.config(text="I₂ = " + str(round(self.values["Ix"], 4)) + " " + self.unit + "\u2074")
            self.sm.result8.config(text="Keresztmetszeti tényezők:")
            self.sm.result9.config(text="Kₓ = " + str(round(self.values["Kx"], 4)) + " " + self.unit + "\u2074")
            self.sm.result10.config(text="Kᵧ = " + str(round(self.values["Ky"], 4)) + " " + self.unit + "\u2074")

        elif self.sm.shape == "Circle":
            vissza, t = self.get_entry(1)
            if None in vissza:
                return -1
            self.values = Calc.Circle(vissza[0], t, *vissza[1:],rad = self.angle_unit == "rad")
            self.sm.result1.config(text="A = " + str(round(self.values["A"], 4)) + " " + self.unit + "²")
            if self.transformed_coordinate_on.get() == True:
                self.sm.result2.config(text="Iₓ₁ = " + str(round(self.values["Ixi"], 4)) + " " + self.unit + "\u2074")
                self.sm.result3.config(text="Iᵧ₁ = " + str(round(self.values["Ieta"], 4)) + " " + self.unit + "\u2074")
                self.sm.result4.config(text="Iₓ₁ᵧ₁ = " + str(round(self.values["Ixieta"], 4)) + " " + self.unit + "\u2074")
            else:
                self.sm.result2.config(text="Iₓ = Iᵧ = " + str(round(self.values["Ix"], 4)) + " " + self.unit + "\u2074")
                self.sm.result3.config(text="Iₚ = " + str(round(self.values["Ip"], 4)) + " " + self.unit + "\u2074")
                self.sm.result4.config(text="Iₓᵧ = " + str(round(self.values["Ixy"], 4)) + " " + self.unit + "\u2074")
            self.sm.result5.config(text="Főmásodrendű nyomatékok:")
            if round(self.values["Ix"], 4) > round(self.values["Iy"], 4):
                self.sm.result6.config(text="I₁ = " + str(round(self.values["Ix"], 4)) + " " + self.unit + "\u2074")
                self.sm.result7.config(text="I₂ = " + str(round(self.values["Iy"], 4)) + " " + self.unit + "\u2074")
            else:
                self.sm.result6.config(text="I₁ = " + str(round(self.values["Iy"], 4)) + " " + self.unit + "\u2074")
                self.sm.result7.config(text="I₂ = " + str(round(self.values["Ix"], 4)) + " " + self.unit + "\u2074")
            self.sm.result8.config(text="Keresztmetszeti tényezők:")
            self.sm.result9.config(text="Kₓ = Kᵧ = " + str(round(self.values["Kx"], 4)) + " " + self.unit + "\u2074")
            self.sm.result10.config(text="Kₚ = " + str(round(self.values["Kp"], 4)) + " " + self.unit + "\u2074")

        elif self.sm.shape == "Ellipse":
            vissza, t = self.get_entry(2)
            if None in vissza:
                return -1
            self.values = Calc.Ellipse(*vissza[:2], t, *vissza[2:],rad = self.angle_unit == "rad")
            self.sm.result1.config(text="A = " + str(round(self.values["A"], 4)) + " " + self.unit + "²")
            if self.transformed_coordinate_on.get() == True:
                print("transcoord")
                self.sm.result2.config(text="Iₓ₁ = " + str(round(self.values["Ixi"], 4)) + " " + self.unit + "\u2074")
                self.sm.result3.config(text="Iᵧ₁ = " + str(round(self.values["Ieta"], 4)) + " " + self.unit + "\u2074")
                self.sm.result4.config(text="Iₓ₁ᵧ₁ = " + str(round(self.values["Ixieta"], 4)) + " " + self.unit + "\u2074")
            else:
                print("notrans")
                self.sm.result2.config(text="Iₓ = " + str(round(self.values["Ix"], 4)) + " " + self.unit + "\u2074")
                self.sm.result3.config(text="Iᵧ = " + str(round(self.values["Iy"], 4)) + " " + self.unit + "\u2074")
                self.sm.result4.config(text="Iₓᵧ = " + str(round(self.values["Ixy"], 4)) + " " + self.unit + "\u2074")
            self.sm.result5.config(text="Főmásodrendű nyomatékok:")
            if round(self.values["Ix"], 4) > round(self.values["Iy"], 4):
                self.sm.result6.config(text="I₁ = " + str(round(self.values["Ix"], 4)) + " " + self.unit + "\u2074")
                self.sm.result7.config(text="I₂ = " + str(round(self.values["Iy"], 4)) + " " + self.unit + "\u2074")
            else:
                self.sm.result8.config(text="I₁ = " + str(round(self.values["Iy"], 4)) + " " + self.unit + "\u2074")
                self.sm.result9.config(text="I₂ = " + str(round(self.values["Ix"], 4)) + " " + self.unit + "\u2074")
            self.sm.result8.config(text="Keresztmetszeti tényezők:")
            self.sm.result9.config(text="Kₓ = " + str(round(self.values["Kx"], 4)) + " " + self.unit + "\u2074")
            self.sm.result10.config(text="Kᵧ = " + str(round(self.values["Ky"], 4)) + " " + self.unit + "\u2074")

        elif self.sm.shape == "Isosceles_triangle":
            vissza, t = self.get_entry(2)
            if None in vissza:
                return -1
            self.values = Calc.IsoscelesTriangle(*vissza[:2], t, *vissza[2:],rad = self.angle_unit == "rad")
            self.sm.result1.config(text="A = " + str(round(self.values["A"], 4)) + " " + self.unit + "²")
            if self.transformed_coordinate_on.get() == True:
                print("transcoord")
                self.sm.result2.config(text="Iₓ₁ = " + str(round(self.values["Ixi"], 4)) + " " + self.unit + "\u2074")
                self.sm.result3.config(text="Iᵧ₁ = " + str(round(self.values["Ieta"], 4)) + " " + self.unit + "\u2074")
                self.sm.result4.config(text="Iₓ₁ᵧ₁ = " + str(round(self.values["Ixieta"], 4)) + " " + self.unit + "\u2074")
            else:
                print("notrans")
                self.sm.result2.config(text="Iₓ = " + str(round(self.values["Ix"], 4)) + " " + self.unit + "\u2074")
                self.sm.result3.config(text="Iᵧ = " + str(round(self.values["Iy"], 4)) + " " + self.unit + "\u2074")
                self.sm.result4.config(text="Iₓᵧ = " + str(round(self.values["Ixy"], 4)) + " " + self.unit + "\u2074")
            self.sm.result5.config(text="Főmásodrendű nyomatékok:")
            if round(self.values["Ix"], 4) > round(self.values["Iy"], 4):
                self.sm.result6.config(text="I₁ = " + str(round(self.values["Ix"], 4)) + " " + self.unit + "\u2074")
                self.sm.result7.config(text="I₂ = " + str(round(self.values["Iy"], 4)) + " " + self.unit + "\u2074")
            else:
                self.sm.result8.config(text="I₁ = " + str(round(self.values["Iy"], 4)) + " " + self.unit + "\u2074")
                self.sm.result9.config(text="I₂ = " + str(round(self.values["Ix"], 4)) + " " + self.unit + "\u2074")
            self.sm.result8.config(text="Keresztmetszeti tényezők:")
            self.sm.result9.config(text="Kₓ = " + str(round(self.values["Kx"], 4)) + " " + self.unit + "\u2074")
            self.sm.result10.config(text="Kᵧ = " + str(round(self.values["Ky"], 4)) + " " + self.unit + "\u2074")
        else:
            print("Hiba, az alakzat nem talalhato")
        if self.sm.shape == "Circle":
            plot(self, self.sm.shape, self.coordinate_on.get(), self.dimension_lines_on.get(), self.transformed_coordinate_on.get(), self.thickness_on.get(), self.colors)
            plot_principal_axes(self, self.colors,  self.ax, self.values["alpha"],self.angle_unit, self.transformed_coordinate_on.get(), self.sm.shape)
        else:
            plot(self, self.sm.shape, self.coordinate_on.get(), self.dimension_lines_on.get(), self.transformed_coordinate_on.get(), self.thickness_on.get(), self.colors, vissza[0], vissza[1], vissza[0])
            plot_principal_axes(self, self.colors,  self.ax, self.values["alpha"],self.angle_unit, self.transformed_coordinate_on.get(), self.sm.shape, vissza[0], vissza[1], vissza[0])

    def doNothing(self):
        print("Ez a funkció jelenleg nem elérhető...")
# VARIABLES ---------------------------------------------------------------------------------------------------------------------------------------------
DARK_THEME = {
        'main_color': '#1a1a1a',
        'secondary_color': '#333333',
        'text_color': '#cccccc',
        'entry_color': '#262626',
        'disabled_color':'#333333',
        'error_color':'red',
        'draw_main': '#87aade',
        'draw_secondary': '#1a1a1a',
        'draw_tertiary': 'grey',
        'draw_principal': 'red',
        'path': 'figures/dark_theme/'
        }
LIGHT_THEME = {
        'main_color': '#d9dcdf',
        'secondary_color': '#f4f2f4',
        'text_color': '#333333',
        'entry_color': '#d9dcdf',
        'disabled_color':'#f4f2f4',
        'error_color':'red',
        'draw_main': '#a4ade9',
        'draw_secondary': '#000000',
        'draw_tertiary': '#4d4d4d',
        'draw_principal': 'red',
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
        settings={'theme':'dark', 'default_unit':'mm', 'angle_unit':'rad', 'logo_enabled':'True'}
    if settings['logo_enabled'] == 'True':
        master = starting_window()
        master.mainloop()
    root = main_window()
    root.mainloop()
    with open('app_settings.json', 'w') as json_file:
        json.dump({'theme':root.theme, 'default_unit':root.unit, 'angle_unit':root.angle_unit, 'logo_enabled':root.logo_enabled}, json_file)
