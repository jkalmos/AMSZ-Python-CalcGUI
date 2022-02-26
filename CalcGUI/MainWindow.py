from ast import Return
import tkinter as tk
from tkinter import BooleanVar, Toplevel, ttk
from tkinter.constants import BOTH
from PIL import Image, ImageTk
from PIL import ImageGrab
import CalcFunctions as Calc
import json
from SideMenu import SideMenu
from tkvideo import tkvideo
from PlotFunctions import plot, plot_principal_axes
import shape_builder
from SettingsWindow import settings_window
from tkinter.filedialog import asksaveasfile
from tkinter import messagebox
import datetime as dt
from fpdf import FPDF
import numpy as np

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.patches as patches

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
        self.win_width = 1201
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
        self.valid_sol = BooleanVar(False)

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

        self.menu_is_on = False
        self.create_menubar(self.shape_builder_mode, self.menu_is_on)

        # Canvas for drawing
        self.canvas = None

        # Side Menu
        self.sm = SideMenu(self)
        self.sm.pack(side=tk.LEFT, padx = (20,10), pady = 20, fill=tk.Y)
        # self.sm.pack(side=tk.LEFT, fill=tk.Y)
        # angle_unit on pressing enter
        self.bind('<Return>', self.calculate)
        plot(self, None, False, False, False, False, self.colors, self.angle_unit)
        
    ## USEFUL FUNCTIONS ----------------------------------------------------------------------------------------------------------------------------------------------------------- 
    
    def create_menubar(self, shape_builder_mode, menu_is_on):
        if menu_is_on == True:
            self.menu_canvas.pack_forget()
        else:
            self.menu_is_on = True
        ## custom menubar -----------------------------------------------------------------------------------------------------------------------------------------------------------
        self.menu_canvas = tk.Canvas(self, bg=self.colors['secondary_color'], highlightthickness=0, height=26)
        self.menu_canvas.pack(fill = tk.X)

        # custom menubar objects

        self.sol_save_button_img = tk.PhotoImage(file=f"{self.colors['path']}menubar/sol_save.png")
        self.sol_save_button_hover_img = tk.PhotoImage(file=f"{self.colors['path']}menubar/sol_save_hover.png")
        self.sol_save_button = self.menu_canvas.create_image(0,0,anchor=tk.NW,image=self.sol_save_button_img)
        self.menu_canvas.tag_bind(self.sol_save_button, '<Button-1>', lambda e: self.save_file())
        self.menu_canvas.tag_bind(self.sol_save_button, '<Enter>', lambda e:self.menu_canvas.itemconfig(self.sol_save_button,
        image=self.sol_save_button_hover_img))
        self.menu_canvas.tag_bind(self.sol_save_button, '<Leave>', lambda e:self.menu_canvas.itemconfig(self.sol_save_button,
        image=self.sol_save_button_img))

        self.setting_button_img = tk.PhotoImage(file=f"{self.colors['path']}menubar/settings.png")
        self.setting_button_hover_img = tk.PhotoImage(file=f"{self.colors['path']}menubar/settings_hover.png")
        self.setting_button = self.menu_canvas.create_image(167,0,anchor=tk.NW,image=self.setting_button_img)
        self.menu_canvas.tag_bind(self.setting_button, '<Button-1>', lambda e: settings_window(self))
        self.menu_canvas.tag_bind(self.setting_button, '<Enter>', lambda e:self.menu_canvas.itemconfig(self.setting_button,
        image=self.setting_button_hover_img))
        self.menu_canvas.tag_bind(self.setting_button, '<Leave>', lambda e:self.menu_canvas.itemconfig(self.setting_button,
        image=self.setting_button_img))

        self.basic_button_img = tk.PhotoImage(file=f"{self.colors['path']}/menubar/basic.png")
        self.basic_button_hover_img = tk.PhotoImage(file=f"{self.colors['path']}/menubar/basic_hover.png")

        self.change_button_img = tk.PhotoImage(file=f"{self.colors['path']}menubar/change.png")
        self.change_button_hover_img = tk.PhotoImage(file=f"{self.colors['path']}menubar/change_hover.png")
        self.change_button = self.menu_canvas.create_image(261,0,anchor=tk.NW,image=self.change_button_img)
        self.menu_canvas.tag_bind(self.change_button, '<Button-1>', lambda e: self.build_shape())
        self.menu_canvas.tag_bind(self.change_button, '<Enter>', lambda e:self.menu_canvas.itemconfig(self.change_button,
        image=self.change_button_hover_img))
        self.menu_canvas.tag_bind(self.change_button, '<Leave>', lambda e:self.menu_canvas.itemconfig(self.change_button,
        image=self.change_button_img))

        if shape_builder_mode == False:
            forms_posx = 167 + 94 + 104
            help_posx = 167 + 94 + 104 + 97 
        else:
            forms_posx = 167 + 94 + 118
            help_posx = 167 + 94 + 118 + 97 
        
        self.forms_button_img = tk.PhotoImage(file=f"{self.colors['path']}menubar/forms.png")
        self.forms_button_hover_img = tk.PhotoImage(file=f"{self.colors['path']}menubar/forms_hover.png")
        self.forms_button = self.menu_canvas.create_image(forms_posx,0,anchor=tk.NW,image=self.forms_button_img)
        #self.menu_canvas.tag_bind(self.forms_button, '<Button-1>', lambda e: self.save_file())
        self.menu_canvas.tag_bind(self.forms_button, '<Enter>', lambda e:self.menu_canvas.itemconfig(self.forms_button,
        image=self.forms_button_hover_img))
        self.menu_canvas.tag_bind(self.forms_button, '<Leave>', lambda e:self.menu_canvas.itemconfig(self.forms_button,
        image=self.forms_button_img))


        self.help_button_img = tk.PhotoImage(file=f"{self.colors['path']}menubar/help.png")
        self.help_button_hover_img = tk.PhotoImage(file=f"{self.colors['path']}menubar/help_hover.png")
        self.help_button = self.menu_canvas.create_image(help_posx,0,anchor=tk.NW,image=self.help_button_img)
        #self.menu_canvas.tag_bind(self.help_button, '<Button-1>', lambda e: self.save_file())
        self.menu_canvas.tag_bind(self.help_button, '<Enter>', lambda e:self.menu_canvas.itemconfig(self.help_button,
        image=self.help_button_hover_img))
        self.menu_canvas.tag_bind(self.help_button, '<Leave>', lambda e:self.menu_canvas.itemconfig(self.help_button,
        image=self.help_button_img))

    def theme_change(self, theme):
        if self.theme != theme:
            self.theme=theme
            if self.theme=="dark":
                self.colors=DARK_THEME
                self.sm.change_color(DARK_THEME)
                # if self.plotted==True:
                #     plot(self, self.sm.shape, self.coordinate_on.get(), self.dimension_lines_on.get(), self.transformed_coordinate_on.get(), self.thickness_on.get(), self.colors)
            elif self.theme == "light":
                self.colors=LIGHT_THEME
                self.sm.change_color(LIGHT_THEME)
                # if self.plotted==True:
                #     plot(self, self.sm.shape, self.coordinate_on.get(), self.dimension_lines_on.get(), self.transformed_coordinate_on.get(), self.thickness_on.get(), self.colors)
            else:
                print("ERROR: Unknown Theme")
                return -1
            self.configure(bg=self.colors['main_color'])
            settings['theme']=self.theme
            self.destroy()
            self.__init__()
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
            self.create_menubar(self.shape_builder_mode, self.menu_is_on)
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
            self.shape_builder_mode = False
            self.create_menubar(self.shape_builder_mode, self.menu_is_on)
            self.sm.pack(side=tk.LEFT, fill=tk.Y, padx = (20,10), pady = 20)
            # calling = eval(f'self.sm.{self.sm.shape.lower()}_click')
            # calling()

            self.sm.combo_clear()
            # self.combo_rectangle.grid(row=1, column=0, columnspan=5)
            self.sm.combo_default_img = tk.PhotoImage(file=f"{self.colors['path']}combobox/combo_default.png")
            self.sm.combo_default = tk.Label(self.sm.canvas, image=self.sm.combo_default_img, bg=self["background"], activebackground=self["background"])
            self.sm.combo_default.bind('<Button-1>', func=lambda e:self.sm.combo_click())
            self.sm.combo_default.grid(row=1, column=0, columnspan=5)
            self.sm.combo_default["border"] = "0"
            self.sm.clear()
            # self.sm.combo_clear()
            # self.sm.combo_rectangle.grid_forget() ## TODO eval func stringet códdá alakít
            # self.sm.combo_default.grid(row=1, column=0, columnspan=5)
            # self.sm.calling
            self.plotted = False
            
            self.sm.shape = None
            plot(self, None, False, False, False, False, self.colors, self.angle_unit)

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
        if shape == "Rectangle" and self.sm.shape != "Rectangle":
            self.sm.shape = "Rectangle"
            self.sm.change_to_recrangle()
        elif shape == "Circle" and self.sm.shape != "Circle":
            self.sm.shape = "Circle"
            self.sm.change_to_circle()
        elif shape == "Ellipse" and self.sm.shape != "Ellipse":
            self.sm.shape = "Ellipse"
            self.sm.change_to_ellipse()
        elif shape == "Isosceles_triangle" and self.sm.shape != "Isosceles_triangle":
            self.sm.shape = "Isosceles_triangle"
            self.sm.change_to_isosceles_triangle()
            print(self.sm.shape)
        elif shape == "Right_triangle" and self.sm.shape != "Right_triangle":
            self.sm.shape = "Right_triangle"
            self.sm.change_to_right_triangle()
            print(self.sm.shape)
        else:
            self.sm.shape = None
            print("Ez az alakzat még nincs definiálva...")
        plot(self, self.sm.shape, self.coordinate_on.get(), self.dimension_lines_on.get(), self.transformed_coordinate_on.get(), self.thickness_on.get(), self.colors, self.angle_unit)
    
    def get_entry(self, number_of_entries):
        vissza = []
        for i in range(number_of_entries + self.transformed_coordinate_on.get() * 3):
            if i >= 1 and self.sm.shape == "Circle": #! Jujj de csúnya...
                i+=1
            try:
                vissza.append(float(self.sm.controls[i]["entry"].get().replace(',','.')))
                self.sm.controls[i]["entry"].config({"background": self.colors['entry_color']})
                self.valid_sol.set(True)
            except:
                print("Hiba")
                self.sm.controls[i]["entry"].config({"background": self.colors['error_color']})
                for i in self.sm.indicators:
                        i.config(text="")
                self.sm.result1.config(text="Hiba a bemeneti adatokban!")
                vissza.append(None)
        if self.thickness_on.get():
            if self.sm.shape == "Circle":
                print("Kor szamitas")
                t = float(self.sm.controls[-1]["entry"].get().replace(',','.'))
                d = float(self.sm.controls[0]["entry"].get().replace(',','.'))
                if 0 < t < d/2:
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
            elif self.sm.shape == "Right_triangle":
                print("Derekszogu haromszog szamitas")
                t = float(self.sm.controls[-1]["entry"].get().replace(',','.'))
                a = float(self.sm.controls[0]["entry"].get().replace(',','.'))
                b = float(self.sm.controls[1]["entry"].get().replace(',','.'))
                phi = np.arctan(b/a)
                c = np.sqrt(a**2 + b**2)
                print('phi: ' + str(phi*180/np.pi))
                print('c: ' + str(c))
                s1 = np.sqrt(b**2 + (a/2)**2)
                s2 = np.sqrt(a**2 + (c/2)**2 - 2*a*(c/2)*np.cos(phi))
                s3 = np.sqrt(a**2 + (b/2)**2)

                print('s2: ' + str(s2))
                print('s3: ' + str(s3))

                t1 = a/3
                t2 = b/3

                beta = np.arccos( ( (s2/3)**2 - (2*s3/3)**2 - (c/2)**2 ) / ( -2 * (2*s3/3) * (c/2) ) )
                print('beta: ' + str(beta))

                t3 = (2*s3/3)*np.sin(beta)
                

                print('t1: ' + str(t1))
                print('t2: ' + str(t2)) 
                print('t3: ' + str(t3))

                # selecting the smallest

                t_min = min(t1, t2, t3)
                print('legkisebb: ' + str(t_min))

                if 0 < t:
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
                
                if 0 < t >= t_min:
                    self.sm.controls[0]["entry"].config({"background": self.colors['error_color']})
                    self.sm.controls[1]["entry"].config({"background": self.colors['error_color']})
                    self.sm.controls[-1]["entry"].config({"background": self.colors['error_color']})
                    for i in self.sm.indicators:
                        i.config(text="")
                    self.sm.result1.config(text="Hiba a bemeneti adatokban!")
                    self.sm.result2.config(text="Hiba a falvastagságban!")
                    vissza.append(None)

            elif self.sm.shape == "Isosceles_triangle":
                print("Egyenloszaru haromszog szamitas")
                t = float(self.sm.controls[-1]["entry"].get().replace(',','.'))
                a = float(self.sm.controls[0]["entry"].get().replace(',','.'))
                b = float(self.sm.controls[1]["entry"].get().replace(',','.'))
                phi = np.arctan(b/ (a/2))
                c = np.sqrt((a/2)**2 + b**2)

                print('phi: ' + str(phi*180/np.pi))
                print('c: ' + str(c))

                s1 = b
                s2 = np.sqrt(a**2 + (c/2)**2 - 2*a*(c/2)*np.cos(phi))
                s3 = s2

                print('s2: ' + str(s2))
                print('s3: ' + str(s3))

                t1 = a/3
                

                beta = np.arccos( ( (s2/3)**2 - (2*s3/3)**2 - (c/2)**2 ) / ( -2 * (2*s3/3) * (c/2) ) )
                print('beta: ' + str(beta))

                t2 = (2*s2/3)*np.sin(beta)
                t3 =t2
                

                print('t1: ' + str(t1))
                print('t2: ' + str(t2)) 
                print('t3: ' + str(t3))

                # selecting the smallest

                t_min = min(t1, t2, t3)
                print('legkisebb: ' + str(t_min))

                if 0 < t:
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
                
                if 0 < t >= t_min:
                    self.sm.controls[0]["entry"].config({"background": self.colors['error_color']})
                    self.sm.controls[1]["entry"].config({"background": self.colors['error_color']})
                    self.sm.controls[-1]["entry"].config({"background": self.colors['error_color']})
                    for i in self.sm.indicators:
                        i.config(text="")
                    self.sm.result1.config(text="Hiba a bemeneti adatokban!")
                    self.sm.result2.config(text="Hiba a falvastagságban!")
                    vissza.append(None)
            else:
                print("Teglalap szamitas (egyenlore minden mas is)")

                t = float(self.sm.controls[-1]["entry"].get().replace(',','.'))
                a = float(self.sm.controls[0]["entry"].get().replace(',','.'))
                b = float(self.sm.controls[1]["entry"].get().replace(',','.'))
                if 0 < t < a/2 and 0 < t < b/2:
                    
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
                    if 0 < t >= a/2 and a == b: 
                        self.sm.controls[0]["entry"].config({"background": self.colors['error_color']})
                        self.sm.controls[1]["entry"].config({"background": self.colors['error_color']})
                        self.sm.controls[-1]["entry"].config({"background": self.colors['error_color']})
                        for i in self.sm.indicators:
                            i.config(text="")
                        self.sm.result1.config(text="Hiba a bemeneti adatokban!")
                        self.sm.result2.config(text="Hiba a falvastagságban!")
                    if 0 < t >= a/2 and 0 < t < b/2:
                        self.sm.controls[0]["entry"].config({"background": self.colors['error_color']})
                        self.sm.controls[-1]["entry"].config({"background": self.colors['error_color']})
                        for i in self.sm.indicators:
                            i.config(text="")
                        self.sm.result1.config(text="Hiba a bemeneti adatokban!")
                        self.sm.result2.config(text="Hiba a falvastagságban!")
                        vissza.append(None)
                    elif 0 < t >= b/2 and 0 < t < a/2: 
                        self.sm.controls[1]["entry"].config({"background": self.colors['error_color']})
                        self.sm.controls[-1]["entry"].config({"background": self.colors['error_color']})
                        for i in self.sm.indicators:
                            i.config(text="")
                        self.sm.result1.config(text="Hiba a bemeneti adatokban!")
                        self.sm.result2.config(text="Hiba a falvastagságban!")
                        vissza.append(None)
                    elif t >= a/2 and t >= b/2:
                        self.sm.controls[0]["entry"].config({"background": self.colors['error_color']})
                        self.sm.controls[1]["entry"].config({"background": self.colors['error_color']})
                        for i in self.sm.indicators:
                            i.config(text="")
                        self.sm.result1.config(text="Hiba a bemeneti adatokban!")
                        self.sm.result2.config(text="Hiba a falvastagságban!")
                        vissza.append(None)
                    else:
                        self.sm.controls[0]["entry"].config({"background": self.colors['error_color']})
                        self.sm.controls[1]["entry"].config({"background": self.colors['error_color']})
                        self.sm.controls[-1]["entry"].config({"background": self.colors['error_color']})
                        for i in self.sm.indicators:
                            i.config(text="")
                        self.sm.result1.config(text="Hiba a bemeneti adatokban!")
                        self.sm.result2.config(text="Hiba a falvastagságban!")
                        vissza.append(None)
        else:
            t = 0
        #self.sm.e2.config({"background": self.colors['entry_color']})
        return vissza,t

    def calculate(self, event=None):
        if not self.shape_builder_mode:
            if self.sm.shape == "Rectangle":
                vissza, t = self.get_entry(2)
                if None in vissza:
                    return -1
                self.values = Calc.Rectangle(*vissza[:2], t, *vissza[2:], rad = self.angle_unit == "rad")
                self.sm.result1.config(text="A = " + str(round(self.values["A"], 4)) + " " + self.unit + "²")
                if self.transformed_coordinate_on.get() == True:
                    print("transformed")
                    self.sm.result2.config(text="Iₓ₁ = " + str(round(self.values["Ixi"], 4)) + " " + self.unit + "\u2074")
                    self.sm.result3.config(text="Iᵧ₁ = " + str(round(self.values["Ieta"], 4)) + " " + self.unit + "\u2074")
                    self.sm.result4.config(text="Iₓ₁ᵧ₁ = " + str(round(self.values["Ixieta"], 4)) + " " + self.unit + "\u2074")
                    self.sm.result5.config(text="Iₚ = " + str(round(self.values["Ip"], 4)) + " " + self.unit + "\u2074")
                else:
                    print("notransformed")
                    self.sm.result2.config(text="Iₓ = " + str(round(self.values["Ix"], 4)) + " " + self.unit + "\u2074")
                    self.sm.result3.config(text="Iᵧ = " + str(round(self.values["Iy"], 4)) + " " + self.unit + "\u2074")
                    self.sm.result4.config(text="Iₓᵧ = " + str(round(self.values["Ixy"], 4)) + " " + self.unit + "\u2074")
                    self.sm.result5.config(text="Iₚ = " + str(round(self.values["Ip"], 4)) + " " + self.unit + "\u2074")
                self.sm.result6.config(text="Főmásodrendű nyomatékok:")
                if round(self.values["Ix"], 4) >= round(self.values["Iy"], 4):
                    self.sm.result7.config(text="I₁ = " + str(round(self.values["Ix"], 4)) + " " + self.unit + "\u2074")
                    self.sm.result8.config(text="I₂ = " + str(round(self.values["Iy"], 4)) + " " + self.unit + "\u2074")
                    print("x nagyobb")
                else:
                    self.sm.result7.config(text="I₁ = " + str(round(self.values["Iy"], 4)) + " " + self.unit + "\u2074")
                    self.sm.result8.config(text="I₂ = " + str(round(self.values["Ix"], 4)) + " " + self.unit + "\u2074")
                    print("y nagyobb")
                self.sm.result9.config(text="Keresztmetszeti tényezők:")
                self.sm.result10.config(text="Kₓ = " + str(round(self.values["Kx"], 4)) + " " + self.unit + "\u00B3")
                self.sm.result11.config(text="Kᵧ = " + str(round(self.values["Ky"], 4)) + " " + self.unit + "\u00B3")

            elif self.sm.shape == "Circle":
                vissza, t = self.get_entry(1)
                if None in vissza:
                    return -1
                self.values = Calc.Circle(vissza[0], t, *vissza[1:],rad = self.angle_unit == "rad")
                self.sm.result1.config(text="A = " + str(round(self.values["A"], 4)) + " " + self.unit + "²")
                if self.transformed_coordinate_on.get() == True:
                    print("transformed")
                    self.sm.result2.config(text="Iₓ₁ = " + str(round(self.values["Ixi"], 4)) + " " + self.unit + "\u2074")
                    self.sm.result3.config(text="Iᵧ₁ = " + str(round(self.values["Ieta"], 4)) + " " + self.unit + "\u2074")
                    self.sm.result4.config(text="Iₓ₁ᵧ₁ = " + str(round(self.values["Ixieta"], 4)) + " " + self.unit + "\u2074")
                    self.sm.result5.config(text="Iₚ = " + str(round(self.values["Ip"], 4)) + " " + self.unit + "\u2074")
                else:
                    print("notransformed")
                    self.sm.result2.config(text="Iₓ = " + str(round(self.values["Ix"], 4)) + " " + self.unit + "\u2074")
                    self.sm.result3.config(text="Iᵧ = " + str(round(self.values["Iy"], 4)) + " " + self.unit + "\u2074")
                    self.sm.result4.config(text="Iₓᵧ = " + str(round(self.values["Ixy"], 4)) + " " + self.unit + "\u2074")
                    self.sm.result5.config(text="Iₚ = " + str(round(self.values["Ip"], 4)) + " " + self.unit + "\u2074")
                self.sm.result6.config(text="Főmásodrendű nyomatékok:")
                self.sm.result7.config(text="I₁ = " + str(round(self.values["Ix"], 4)) + " " + self.unit + "\u2074")
                self.sm.result8.config(text="I₂ = " + str(round(self.values["Iy"], 4)) + " " + self.unit + "\u2074")
                self.sm.result9.config(text="Keresztmetszeti tényezők:")
                self.sm.result10.config(text="Kₓ = Kᵧ = " + str(round(self.values["Kx"], 4)) + " " + self.unit + "\u00B3")
                self.sm.result11.config(text="Kₚ = " + str(round(self.values["Kp"], 4)) + " " + self.unit + "\u00B3")

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
                    self.sm.result5.config(text="Iₚ = " + str(round(self.values["Ip"], 4)) + " " + self.unit + "\u2074")
                else:
                    print("notrans")
                    self.sm.result2.config(text="Iₓ = " + str(round(self.values["Ix"], 4)) + " " + self.unit + "\u2074")
                    self.sm.result3.config(text="Iᵧ = " + str(round(self.values["Iy"], 4)) + " " + self.unit + "\u2074")
                    self.sm.result4.config(text="Iₓᵧ = " + str(round(self.values["Ixy"], 4)) + " " + self.unit + "\u2074")
                    self.sm.result5.config(text="Iₚ = " + str(round(self.values["Ip"], 4)) + " " + self.unit + "\u2074")
                self.sm.result6.config(text="Főmásodrendű nyomatékok:")
                if round(self.values["Ix"], 4) >= round(self.values["Iy"], 4):
                    self.sm.result7.config(text="I₁ = " + str(round(self.values["Ix"], 4)) + " " + self.unit + "\u2074")
                    self.sm.result8.config(text="I₂ = " + str(round(self.values["Iy"], 4)) + " " + self.unit + "\u2074")
                else:
                    self.sm.result7.config(text="I₁ = " + str(round(self.values["Iy"], 4)) + " " + self.unit + "\u2074")
                    self.sm.result8.config(text="I₂ = " + str(round(self.values["Ix"], 4)) + " " + self.unit + "\u2074")
                self.sm.result9.config(text="Keresztmetszeti tényezők:")
                self.sm.result10.config(text="Kₓ = " + str(round(self.values["Kx"], 4)) + " " + self.unit + "\u00B3")
                self.sm.result11.config(text="Kᵧ = " + str(round(self.values["Ky"], 4)) + " " + self.unit + "\u00B3")

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
                    self.sm.result5.config(text="Iₚ = " + str(round(self.values["Ip"], 4)) + " " + self.unit + "\u2074")
                else:
                    print("notrans")
                    self.sm.result2.config(text="Iₓ = " + str(round(self.values["Ix"], 4)) + " " + self.unit + "\u2074")
                    self.sm.result3.config(text="Iᵧ = " + str(round(self.values["Iy"], 4)) + " " + self.unit + "\u2074")
                    self.sm.result4.config(text="Iₓᵧ = " + str(round(self.values["Ixy"], 4)) + " " + self.unit + "\u2074")
                    self.sm.result5.config(text="Iₚ = " + str(round(self.values["Ip"], 4)) + " " + self.unit + "\u2074")
                self.sm.result6.config(text="Főmásodrendű nyomatékok:")
                if round(self.values["Ix"], 4) >= round(self.values["Iy"], 4):
                    self.sm.result7.config(text="I₁ = " + str(round(self.values["Ix"], 4)) + " " + self.unit + "\u2074")
                    self.sm.result8.config(text="I₂ = " + str(round(self.values["Iy"], 4)) + " " + self.unit + "\u2074")
                else:
                    self.sm.result7.config(text="I₁ = " + str(round(self.values["Iy"], 4)) + " " + self.unit + "\u2074")
                    self.sm.result8.config(text="I₂ = " + str(round(self.values["Ix"], 4)) + " " + self.unit + "\u2074")
                self.sm.result9.config(text="Keresztmetszeti tényezők:")
                self.sm.result10.config(text="Kₓ = " + str(round(self.values["Kx"], 4)) + " " + self.unit + "\u00B3")
                self.sm.result11.config(text="Kᵧ = " + str(round(self.values["Ky"], 4)) + " " + self.unit + "\u00B3")
            elif self.sm.shape == "Right_triangle":
                vissza, t = self.get_entry(2)
                if None in vissza:
                    return -1
                self.values = Calc.RightTriangle(*vissza[:2], t, *vissza[2:],rad = self.angle_unit == "rad")
                self.sm.result1.config(text="A = " + str(round(self.values["A"], 4)) + " " + self.unit + "²")
                if self.transformed_coordinate_on.get() == True:
                    print("transcoord")
                    self.sm.result2.config(text="Iₓ₁ = " + str(round(self.values["Ixi"], 4)) + " " + self.unit + "\u2074")
                    self.sm.result3.config(text="Iᵧ₁ = " + str(round(self.values["Ieta"], 4)) + " " + self.unit + "\u2074")
                    self.sm.result4.config(text="Iₓ₁ᵧ₁ = " + str(round(self.values["Ixieta"], 4)) + " " + self.unit + "\u2074")
                    self.sm.result5.config(text="Iₚ = " + str(round(self.values["Ip"], 4)) + " " + self.unit + "\u2074")
                else:
                    print("notrans")
                    self.sm.result2.config(text="Iₓ = " + str(round(self.values["Ix"], 4)) + " " + self.unit + "\u2074")
                    self.sm.result3.config(text="Iᵧ = " + str(round(self.values["Iy"], 4)) + " " + self.unit + "\u2074")
                    self.sm.result4.config(text="Iₓᵧ = " + str(round(self.values["Ixy"], 4)) + " " + self.unit + "\u2074")
                    self.sm.result5.config(text="Iₚ = " + str(round(self.values["Ip"], 4)) + " " + self.unit + "\u2074")
                self.sm.result6.config(text="Főmásodrendű nyomatékok:")
                if round(self.values["Ix"], 4) >= round(self.values["Iy"], 4):
                    self.sm.result7.config(text="I₁ = " + str(round(self.values["Ix"], 4)) + " " + self.unit + "\u2074")
                    self.sm.result8.config(text="I₂ = " + str(round(self.values["Iy"], 4)) + " " + self.unit + "\u2074")
                else:
                    self.sm.result7.config(text="I₁ = " + str(round(self.values["Iy"], 4)) + " " + self.unit + "\u2074")
                    self.sm.result8.config(text="I₂ = " + str(round(self.values["Ix"], 4)) + " " + self.unit + "\u2074")
                self.sm.result9.config(text="Keresztmetszeti tényezők:")
                self.sm.result10.config(text="Kₓ = " + str(round(self.values["Kx"], 4)) + " " + self.unit + "\u00B3")
                self.sm.result11.config(text="Kᵧ = " + str(round(self.values["Ky"], 4)) + " " + self.unit + "\u00B3")
            else:
                print("Hiba, az alakzat nem talalhato")
            if self.transformed_coordinate_on.get() == False:
                if self.sm.shape == "Circle":
                    plot(self, self.sm.shape, self.coordinate_on.get(), self.dimension_lines_on.get(), self.transformed_coordinate_on.get(), self.thickness_on.get(), self.colors, self.angle_unit)
                    plot_principal_axes(self, self.colors,  self.ax, self.values["alpha"],self.angle_unit, self.transformed_coordinate_on.get(), self.sm.shape)
                else:
                    plot(self, self.sm.shape, self.coordinate_on.get(), self.dimension_lines_on.get(), self.transformed_coordinate_on.get(), self.thickness_on.get(), self.colors, self.angle_unit, vissza[0], vissza[1], vissza[0])
                    plot_principal_axes(self, self.colors,  self.ax, self.values["alpha"],self.angle_unit, self.transformed_coordinate_on.get(), self.sm.shape, vissza[0], vissza[1], vissza[0])
            else:
                u = float(self.sm.te1.get().replace(',','.'))
                v = float(self.sm.te2.get().replace(',','.'))
                rot = float(self.sm.te3.get().replace(',','.'))
                if self.sm.shape == "Circle":
                    plot(self, self.sm.shape, self.coordinate_on.get(), self.dimension_lines_on.get(), self.transformed_coordinate_on.get(), self.thickness_on.get(), self.colors, self.angle_unit, calculated = True, u=u, v=v, rot=rot)
                else:
                    plot(self, self.sm.shape, self.coordinate_on.get(), self.dimension_lines_on.get(), self.transformed_coordinate_on.get(), self.thickness_on.get(), self.colors, self.angle_unit, vissza[0], vissza[1], vissza[0], calculated = True, u=u, v=v, rot=rot)


    def save_file(self):
        if self.valid_sol.get() == True:
            if self.shape_builder_mode == False:
                print('Alap mod mentes')
                date=dt.datetime.now()
                filename = "eredmenyek_" + f"{date:%y_%m_%d_%H_%M}"

                f = asksaveasfile(initialfile = filename,
                defaultextension=".pdf",filetypes=[("All Files","*.*"),("PDF files","*.pdf")])
                if f is None:
                    return

                if self.sm.shape == "Circle":
                    d = float(self.sm.controls[0]["entry"].get().replace(',','.'))
                    
                else:
                    a = float(self.sm.controls[0]["entry"].get().replace(',','.'))
                    b = float(self.sm.controls[1]["entry"].get().replace(',','.'))
                
                if self.thickness_on.get() == True:
                    t = float(self.sm.controls[-1]["entry"].get().replace(',','.'))
                else:
                    t = 0

                # saving to pdf

                pdf = FPDF()
                pdf.add_page()
                pdf.add_font('DejaVu', '', 'DejaVuSansCondensed.ttf', uni=True)
                pdf.set_font('DejaVu', '', 14)

                self.fig.patch.set_facecolor("#FFFFFF")
                self.canvas.draw()

                self.canvas.print_figure('tempfig.png', 200)
                self.fig.patch.set_facecolor(self.colors["secondary_color"])
                self.canvas.draw()
      
                background_img = Image.new('RGB', (210,297), "#FFFFFF")
                pdf.set_text_color(0,0,0) 
            

                background_img.save('background_img.png')
                pdf.image('background_img.png', x = 0, y = 0, w = 210, h = 297, type = 'PNG')
                pdf.image('tempfig.png', x = 65, y = 15, w = 140, h = 0, type = 'PNG')
                

                if self.sm.shape == "Circle": 
                    pdf.cell(200, 10, txt = 'Az alakzat: ' + self.sm.shape +  ' (d = ' + str(round(d, 4)) + " " + self.unit + ', t = ' + str(round(t, 4)) + " " + self.unit + ')' , ln = 1, align = 'L')
                    pdf.cell(200, 10, txt = 'A = '    + str(round(self.values["A"], 4))   + " " + self.unit + "²" , ln = 2, align = 'L')
                    pdf.cell(200, 10, txt = 'Iₓ = '   + str(round(self.values["Ix"], 4))  + " " + self.unit + "\u2074", ln = 3, align = 'L')
                    pdf.cell(200, 10, txt = 'Iᵧ = '   + str(round(self.values["Iy"], 4))  + " " + self.unit + "\u2074", ln = 4, align = 'L')
                    pdf.cell(200, 10, txt = 'Iₚ = '   + str(round(self.values["Ip"], 4))  + " " + self.unit + "\u2074", ln = 5, align = 'L')
                    pdf.cell(200, 10, txt = 'Iₓᵧ = '  + str(round(self.values["Ixy"], 4)) + " " + self.unit + "\u2074", ln = 6, align = 'L')
                    pdf.cell(200, 10, txt = 'I₁ = '   + str(round(self.values["I1"], 4))  + " " + self.unit + "\u2074", ln = 7, align = 'L')
                    pdf.cell(200, 10, txt = 'I₂ = '   + str(round(self.values["I2"], 4))  + " " + self.unit + "\u2074", ln = 8, align = 'L')
                    pdf.cell(200, 10, txt = 'Kₓ = Kᵧ = '   + str(round(self.values["Kx"], 4))  + " " + self.unit + "\u00B3", ln = 9, align = 'L')
                    pdf.cell(200, 10, txt = 'Kₚ = '   + str(round(self.values["Kp"], 4))  + " " + self.unit + "\u00B3", ln = 10, align = 'L')
                else:

                    if round(self.values["I1"], 4) >= round(self.values["I2"], 4):
                        pdf.cell(200, 10, txt = 'Az alakzat: ' + self.sm.shape +  ' (a = ' + str(round(a, 4)) + " "  + self.unit + ', b = ' + str(round(b, 4)) + " "  + self.unit + ', t = ' + str(round(t, 4)) + " "  + self.unit + ')', ln = 1, align = 'L')
                        pdf.cell(200, 10, txt = 'A = '    + str(round(self.values["A"], 4))   + " " + self.unit + "²" , ln = 2, align = 'L')
                        pdf.cell(200, 10, txt = 'Iₓ = '   + str(round(self.values["Ix"], 4))  + " " + self.unit + "\u2074", ln = 3, align = 'L')
                        pdf.cell(200, 10, txt = 'Iᵧ = '   + str(round(self.values["Iy"], 4))  + " " + self.unit + "\u2074", ln = 4, align = 'L')
                        pdf.cell(200, 10, txt = 'Iₚ = '   + str(round(self.values["Ip"], 4))  + " " + self.unit + "\u2074", ln = 5, align = 'L')
                        pdf.cell(200, 10, txt = 'Iₓᵧ = '  + str(round(self.values["Ixy"], 4)) + " " + self.unit + "\u2074", ln = 6, align = 'L')
                        pdf.cell(200, 10, txt = 'I₁ = '   + str(round(self.values["I1"], 4))  + " " + self.unit + "\u2074", ln = 7, align = 'L')
                        pdf.cell(200, 10, txt = 'I₂ = '   + str(round(self.values["I2"], 4))  + " " + self.unit + "\u2074", ln = 8, align = 'L')
                        pdf.cell(200, 10, txt = 'Kₓ = '   + str(round(self.values["Kx"], 4))  + " " + self.unit + "\u00B3", ln = 9, align = 'L')
                        pdf.cell(200, 10, txt = 'Kᵧ = '   + str(round(self.values["Ky"], 4))  + " " + self.unit + "\u00B3", ln = 10, align = 'L')
                    else:
                        pdf.cell(200, 10, txt = 'Az alakzat: ' + self.sm.shape +  ' (a = ' + str(round(a, 4)) + " "  + self.unit + ', b = ' + str(round(b, 4)) + " "  + self.unit + ', t = ' + str(round(t, 4)) + " "  + self.unit + ')', ln = 1, align = 'L')
                        pdf.cell(200, 10, txt = 'A = '    + str(round(self.values["A"], 4))   + " " + self.unit + "²" , ln = 2, align = 'L')
                        pdf.cell(200, 10, txt = 'Iₓ = '   + str(round(self.values["Ix"], 4))  + " " + self.unit + "\u2074", ln = 3, align = 'L')
                        pdf.cell(200, 10, txt = 'Iᵧ = '   + str(round(self.values["Iy"], 4))  + " " + self.unit + "\u2074", ln = 4, align = 'L')
                        pdf.cell(200, 10, txt = 'Iₚ = '   + str(round(self.values["Ip"], 4))  + " " + self.unit + "\u2074", ln = 5, align = 'L')
                        pdf.cell(200, 10, txt = 'Iₓᵧ = '  + str(round(self.values["Ixy"], 4)) + " " + self.unit + "\u2074", ln = 6, align = 'L')
                        pdf.cell(200, 10, txt = 'I₁ = '   + str(round(self.values["I2"], 4))  + " " + self.unit + "\u2074", ln = 7, align = 'L')
                        pdf.cell(200, 10, txt = 'I₂ = '   + str(round(self.values["I1"], 4))  + " " + self.unit + "\u2074", ln = 8, align = 'L')
                        pdf.cell(200, 10, txt = 'Kₓ = '   + str(round(self.values["Kx"], 4))  + " " + self.unit + "\u00B3", ln = 9, align = 'L')
                        pdf.cell(200, 10, txt = 'Kᵧ = '   + str(round(self.values["Ky"], 4))  + " " + self.unit + "\u00B3", ln = 10, align = 'L')

                
                pdf.output(f.name, 'F') 
                pdf.close()

            else:
                print('Mentes shapebuilder')
                self.getter(self.sb)


        else:
            messagebox.showerror("Hiba a mentés közben", "Nincs kiszámolt adat, amit menteni lehetne!")

    def getter(self, widget):
        print("inside getter")
        x=root.winfo_rootx()+widget.winfo_x()
        y=root.winfo_rooty()+widget.winfo_y()
        x1=x+widget.winfo_width()
        y1=y+widget.winfo_height()
        ImageGrab.grab().crop((x,y,x1,y1)).save("teszt.png")

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
        'sb_draw':'#87aade',
        'sb_draw_2nd':'#008080',
        'sb_selected':'',
        'sb_error':'',
        'sb_negative':'',
        'sb_grid':'#3f3f3f',
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
        'sb_draw':'#a4ade9',
        'sb_draw_2nd':'#5d93d1',
        'sb_selected':'',
        'sb_error':'',
        'sb_negative':'',
        'sb_grid':'#3f3f3f',
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
