import tkinter as tk
from tkinter import ttk
from tkinter.constants import FLAT
from PlotFunctions import plot
class SideMenu(tk.Frame):
    def __init__(self, root):
        super().__init__(root,width=30, bg=root.colors['secondary_color'])
        self.root = root
        self.shape = None

# DEFINE SIDEMENU OBJECTS --------------------------------------------------------------------------------------------------------------
        self.canvas = tk.Canvas(self, bg=self["background"], highlightthickness=0)
        self.canvas.grid(row=0, column=0, sticky="NSEW")

        # place holder label
        self.lbl = tk.Label(self.canvas, width = 40, bg = self["background"] , fg='white')
        self.lbl.grid(row=0, column=1)

        self.lbl2 = tk.Label(self.canvas, height = 300, bg = self["background"] , fg='white')
        self.lbl2.grid(row=200, column=1)

        def callback(shape):
            self.root.choose_object(shape)
        def shape_changed(self):
            current_shape = self.widget.get()
            print(current_shape)
            if current_shape == 'Téglalap':
                shape = "Rectangle"
            elif current_shape == 'Kör':
                shape = "Circle"
            elif current_shape == 'Ellipszis':
                shape = "Ellipse"
            elif current_shape == 'Egyenlőszárú háromszög':
                shape = "Isosceles_triangle"
            else:
                shape = None
            callback(shape)
        
        ## Custom combobox ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        # self.combo_buttons = []
        # self.combo_buttons.append(self.combo_rectangle)
        # self.combo_buttons.append(self.combo_circle)
        # self.combo_buttons.append(self.combo_ellipse)
        # self.combo_buttons.append(self.combo_isosceles)
        
        combo_open = tk.BooleanVar(False)
        default_open = tk.BooleanVar(False)
        rectangle_open = tk.BooleanVar(False)
        circle_open = tk.BooleanVar(False)
        ellipse_open = tk.BooleanVar(False)
        isosceles_open = tk.BooleanVar(False)
        def combo_clear():
            if default_open.get() == True:
                self.combo_default.grid_forget()
                self.combo_rectangle.place_forget()
                self.combo_circle.place_forget()
                self.combo_ellipse.place_forget()
                self.combo_isosceles.place_forget()
                default_open.set(False)
                combo_open.set(False)
            elif rectangle_open.get() == True:
                self.combo_rectangle.grid_forget()
                self.combo_circle.place_forget()
                self.combo_ellipse.place_forget()
                self.combo_isosceles.place_forget()
                rectangle_open.set(False)
                combo_open.set(False)
            elif circle_open.get() == True:
                self.combo_rectangle.place_forget()
                self.combo_circle.grid_forget()
                self.combo_ellipse.place_forget()
                self.combo_isosceles.place_forget()
                circle_open.set(False)
                combo_open.set(False)
            elif ellipse_open.get() == True:
                self.combo_rectangle.place_forget()
                self.combo_circle.place_forget()
                self.combo_ellipse.grid_forget()
                self.combo_isosceles.place_forget()
                ellipse_open.set(False)
                combo_open.set(False)
            elif isosceles_open.get() == True:
                self.combo_rectangle.place_forget()
                self.combo_circle.place_forget()
                self.combo_ellipse.place_forget()
                self.combo_isosceles.grid_forget()
                isosceles_open.set(False)
                combo_open.set(False)

        def rectangle_click():
            if combo_open.get() == False:
                self.combo_circle.place(bordermode=tk.OUTSIDE, relx=0.5,y=51, anchor=tk.N)
                self.combo_circle.lift()
                self.combo_ellipse.place(bordermode=tk.OUTSIDE, relx=0.5,y=81, anchor=tk.N)
                self.combo_ellipse.lift()
                self.combo_isosceles.place(bordermode=tk.OUTSIDE, relx=0.5,y=111, anchor=tk.N)
                self.combo_isosceles.lift()
                rectangle_open.set(True)
                combo_open.set(True)
            else:
                combo_clear()
                self.combo_rectangle.grid(row=1, column=1)
                self.root.choose_object("Rectangle")
        def circle_click():
            if combo_open.get() == False:
                self.combo_rectangle.place(bordermode=tk.OUTSIDE, relx=0.5,y=51, anchor=tk.N)
                self.combo_rectangle.lift()
                self.combo_ellipse.place(bordermode=tk.OUTSIDE, relx=0.5,y=81, anchor=tk.N)
                self.combo_ellipse.lift()
                self.combo_isosceles.place(bordermode=tk.OUTSIDE, relx=0.5,y=111, anchor=tk.N)
                self.combo_isosceles.lift()
                circle_open.set(True)
                combo_open.set(True)
            else:
                combo_clear()
                self.combo_circle.grid(row=1, column=1)
                self.root.choose_object("Circle")
        def ellipse_click():
            if combo_open.get() == False:
                self.combo_rectangle.place(bordermode=tk.OUTSIDE, relx=0.5,y=51, anchor=tk.N)
                self.combo_rectangle.lift()
                self.combo_circle.place(bordermode=tk.OUTSIDE, relx=0.5,y=81, anchor=tk.N)
                self.combo_circle.lift()
                self.combo_isosceles.place(bordermode=tk.OUTSIDE, relx=0.5,y=111, anchor=tk.N)
                self.combo_isosceles.lift()
                ellipse_open.set(True)
                combo_open.set(True)
            else:
                combo_clear()
                self.combo_ellipse.grid(row=1, column=1)
                self.root.choose_object("Ellipse")
        def isosceles_click():
            if combo_open.get() == False:
                self.combo_rectangle.place(bordermode=tk.OUTSIDE, relx=0.5,y=51, anchor=tk.N)
                self.combo_rectangle.lift()
                self.combo_circle.place(bordermode=tk.OUTSIDE, relx=0.5,y=81, anchor=tk.N)
                self.combo_circle.lift()
                self.combo_ellipse.place(bordermode=tk.OUTSIDE, relx=0.5,y=111, anchor=tk.N)
                self.combo_ellipse.lift()
                isosceles_open.set(True)
                combo_open.set(True)
            else:
                combo_clear()
                self.combo_isosceles.grid(row=1, column=1)
                self.root.choose_object("Isosceles_triangle")
        def combo_click():
            if combo_open.get() == False:
                # self.combo_under.place(bordermode=tk.OUTSIDE, x=31,y=20)
                # self.combo_under.lift()
                # self.combo_default.lift()
                self.combo_rectangle.place(bordermode=tk.OUTSIDE, relx=0.5,y=51, anchor=tk.N)
                self.combo_rectangle.lift()
                self.combo_circle.place(bordermode=tk.OUTSIDE, relx=0.5,y=72, anchor=tk.N)
                self.combo_circle.lift()
                self.combo_ellipse.place(bordermode=tk.OUTSIDE, relx=0.5,y=111, anchor=tk.N)
                self.combo_ellipse.lift()
                self.combo_isosceles.place(bordermode=tk.OUTSIDE, relx=0.5,y=141, anchor=tk.N)
                self.combo_isosceles.lift()
                default_open.set(True)
                combo_open.set(True)
            else:
                combo_clear()
                self.combo_default.grid(row=1, column=1)

        # Custom combobox
        self.combo_default_img = tk.PhotoImage(file='combo_default.png')
        self.combo_default = tk.Button(self.canvas, image=self.combo_default_img, bg=self["background"], activebackground=self["background"], command=combo_click)
        self.combo_default.grid(row=1, column=1)
        self.combo_default["border"] = "0"

        self.combo_under_img = tk.PhotoImage(file='combo_under.png')
        self.combo_under = tk.Label(self.canvas, image=self.combo_under_img, bg=self["background"])
        self.combo_rectangle_img = tk.PhotoImage(file='combo_rectangle.png')
        self.combo_rectangle = tk.Button(self.canvas, image=self.combo_rectangle_img, bg=self["background"], activebackground=self["background"], command=rectangle_click)
        self.combo_rectangle["border"] = "0"
        self.combo_circle_img = tk.PhotoImage(file='combo_circle.png')
        self.combo_circle = tk.Button(self.canvas, image=self.combo_circle_img, bg=self["background"], activebackground=self["background"], command=circle_click)
        self.combo_circle["border"] = "0"
        self.combo_ellipse_img = tk.PhotoImage(file='combo_ellipse.png')
        self.combo_ellipse = tk.Button(self.canvas, image=self.combo_ellipse_img, bg=self["background"], activebackground=self["background"], command=ellipse_click)
        self.combo_ellipse["border"] = "0"
        self.combo_isosceles_img = tk.PhotoImage(file='combo_isosceles.png')
        self.combo_isosceles = tk.Button(self.canvas, image=self.combo_isosceles_img, bg=self["background"], activebackground=self["background"], command=isosceles_click)
        self.combo_isosceles["border"] = "0"

        self.combo_circle_hover_img = tk.PhotoImage(file='combo_circle_hover.png')
        self.combo_circle.bind("<Enter>", func=lambda e: self.combo_circle.config(
        image=self.combo_circle_hover_img))
        self.combo_circle.bind("<Leave>", func=lambda e: self.combo_circle.config(
        image=self.combo_circle_img))
        # self.combo_default.bind("<Leave><Button>", func=combo_clear())
        
        # self.canvas.tag_bind(self.combo_default, '<Button>', print('clicked'))
        # self.canvas.delete(self.combo_default))

        # # combobox
        # self.n = tk.StringVar()
        # self.choose_shape = ttk.Combobox(self.canvas, width = 25, textvariable=self.n, state='readonly', text="x", justify='center')
        # self.choose_shape.set('Alakzat...')
        # self.choose_shape['values'] = ('Téglalap', 
        #                         'Kör',
        #                         'Ellipszis',
        #                         'Egyenlőszárú háromszög')
        # # self.choose_shape.place(x=0, y=0)
        # self.choose_shape.grid(row=1, column=1)
        # self.choose_shape.bind('<<ComboboxSelected>>', shape_changed)

        # dimension input labels
        self.l1 = tk.Label(self.canvas, text="Width", bg=self["background"], fg='white')
        self.m1 = tk.Label(self.canvas, text="mm", bg=self["background"], fg='white')
        self.l2 = tk.Label(self.canvas, text="Heigth", bg=self["background"], fg='white')
        self.m2 = tk.Label(self.canvas, text="mm", bg=self["background"], fg='white')

        # dimension input entries
        self.e1 = tk.Entry(self.canvas, width = 10, bg=self["background"], fg='white')
        self.e2 = tk.Entry(self.canvas, width = 10, bg=self["background"], fg='white')

        # transformed coordinate system input labels
        self.tl1 = tk.Label(self.canvas, text="x", bg=self["background"], fg='white')
        self.tm1 = tk.Label(self.canvas, text="mm", bg=self["background"], fg='white')
        self.tl2 = tk.Label(self.canvas, text="y", bg=self["background"], fg='white')
        self.tm2 = tk.Label(self.canvas, text="mm", bg=self["background"], fg='white')
        self.tl3 = tk.Label(self.canvas, text="phi", bg=self["background"], fg='white')
        self.tm3 = tk.Label(self.canvas, text="rad", bg=self["background"], fg='white')

        # transformed coordinate system input entries
        self.te1 = tk.Entry(self.canvas, width = 10, bg=self["background"], fg='white', state='disabled', disabledbackground="grey")
        self.te2 = tk.Entry(self.canvas, width = 10, bg=self["background"], fg='white', state='disabled', disabledbackground="grey")
        self.te3 = tk.Entry(self.canvas, width = 10, bg=self["background"], fg='white', state='disabled', disabledbackground="grey")

        # thickness input labels
        self.thl1 = tk.Label(self.canvas, text="t", bg=self["background"], fg='white')
        self.thm1 = tk.Label(self.canvas, text="mm", bg=self["background"], fg='white')

        # thickness input entry
        self.the1 = tk.Entry(self.canvas, width = 10, bg=self["background"], fg='white', state='disabled', disabledbackground="grey")

        # calculate button
        self.buttonimage = tk.PhotoImage(file="calc_button.png")
        self.calc = tk.Button(self.canvas, image=self.buttonimage, text="Calculate", command=lambda: self.root.calculate())
        # self.calc = tk.Button(self, text="Calculate", command=lambda: self.root.calculate())
        self.calc["bg"] = self["background"]
        self.calc["border"] = "0"
        self.calc["width"] = "73"
        self.calc["height"] = "21"

        # result labels
        self.result1 = tk.Label(self.canvas, text="", bg=self["background"], fg='white')
        self.result2 = tk.Label(self.canvas, text="", bg=self["background"], fg='white')
        self.result1.grid(row=12, column = 1)
        self.result2.grid(row=13, column = 1)

        # Checkbox: set thickness
        self.thickness = tk.Checkbutton(
            self.canvas, text = "Falvastagság hozzáadása",
            variable = self.root.thickness_on, onvalue=True, offvalue=False,
            bg = self["background"], fg='white', selectcolor='grey',
            command = lambda: [plot(root, self.shape, self.root.coordinate_on.get(), self.root.dimension_lines_on.get(), self.root.transformed_coordinate_on.get(), self.root.thickness_on.get(), root.colors),
            entry_enable(self.the1, self.root.thickness_on)])

        # Checkbox: transformed coordinate system
        self.transformed_coordinate_system = tk.Checkbutton(
            self.canvas, text = "Transzformált koordináta rendszer",
            variable = self.root.transformed_coordinate_on, onvalue=True, offvalue=False,
            bg = self["background"], fg='white', selectcolor='grey',
            command = lambda: [plot(root, self.shape, self.root.coordinate_on.get(), self.root.dimension_lines_on.get(), self.root.transformed_coordinate_on.get(), self.root.thickness_on.get(), root.colors),
            entry_enable(self.te1, self.root.transformed_coordinate_on),
            entry_enable(self.te2, self.root.transformed_coordinate_on),
            entry_enable(self.te3, self.root.transformed_coordinate_on)])

        # append entry objects to controls array
        self.controls = []
        self.controls.append({"name":self.l1, "entry":self.e1, "unit":self.m1, "unit_type": "length"})
        self.controls.append({"name":self.l2, "entry":self.e2, "unit":self.m2, "unit_type": "length"})
        self.controls.append({"name":self.tl1, "entry":self.te1, "unit":self.tm1, "unit_type": "length"})
        self.controls.append({"name":self.tl2, "entry":self.te2, "unit":self.tm2, "unit_type": "length"})
        self.controls.append({"name":self.tl3, "entry":self.te3, "unit":self.tm3, "unit_type": "degree"})
        self.controls.append({"name":self.thl1, "entry":self.the1, "unit":self.thm1, "unit_type": "length"})

        # append result label to indicators
        self.indicators = []
        self.indicators.append(self.result1)
        self.indicators.append(self.result2)
        self.indicators.append(self.lbl)
        self.indicators.append(self.calc)

        self.checkbox_indicators = []
        self.checkbox_indicators.append(self.transformed_coordinate_system)
        self.checkbox_indicators.append(self.thickness)

        def entry_enable(entry, var):
            if var.get() == False:
                entry.configure(state='disabled')
            elif var.get() == True:
                entry.configure(state='normal')

    def change_color(self, color):
        self["background"] = color["secondary_color"]
        self.canvas["bg"] = self["background"]
        for i in self.controls:
            i["entry"].config({"background": color["entry_color"]})
            i["entry"].config({"fg": color["text_color"]})
            i["name"].config({"fg": color["text_color"]})
            i["name"].config({"background": color["secondary_color"]})
            i["unit"].config({"fg": color["text_color"]})
            i["unit"].config({"background": color["secondary_color"]})
        for i in self.indicators:
            i.config({"fg": color["text_color"]})
            i.config({"background": color["secondary_color"]})
        for i in self.checkbox_indicators:
            i.config({"fg": color["text_color"]})
            i.config({"background": color["secondary_color"]})


## USEFUL FUNCTIONS -----------------------------------------------------------------------------------------------------------------------------------------------------------
    def clear(self):
        for i in self.controls:
            i["name"].grid_forget()
            i["entry"].grid_forget()
            i["entry"].delete(0,"end")
            i["unit"].grid_forget()
        for i in self.indicators:
            i.config(text="")
            #i.grid_forget()
        for i in self.checkbox_indicators:
            i.grid_forget()
        self.calc.grid_forget()
        self.thickness.grid_forget()
        self.transformed_coordinate_system.grid_forget()
        
    def change_to_recrangle(self):
        self.lbl.grid(row=0, column=1)
        # size a
        self.controls[0]["name"].config(text="a")
        self.controls[0]["name"].grid(row=2,column=0)
        self.controls[0]["entry"].grid(row=2,column=1)
        self.controls[0]["unit"].grid(row=2,column=2)
        # size b
        self.controls[1]["name"].config(text="b")
        self.controls[1]["name"].grid(row=3,column=0)
        self.controls[1]["entry"].grid(row=3,column=1)
        self.controls[1]["unit"].grid(row=3,column=2)
        # transformed checkbox
        self.transformed_coordinate_system.grid(row=5, column=0, columnspan=3)
        # transformed x
        self.controls[2]["name"].config(text="x")
        self.controls[2]["name"].grid(row=6,column=0)
        self.controls[2]["entry"].grid(row=6,column=1)
        self.controls[2]["unit"].grid(row=6,column=2)
        # transformed y
        self.controls[3]["name"].config(text="y")
        self.controls[3]["name"].grid(row=7,column=0)
        self.controls[3]["entry"].grid(row=7,column=1)
        self.controls[3]["unit"].grid(row=7,column=2)
        # transformed phi
        self.controls[4]["name"].config(text="φ")
        self.controls[4]["name"].grid(row=8,column=0)
        self.controls[4]["entry"].grid(row=8,column=1)
        self.controls[4]["unit"].grid(row=8,column=2)
        # thickness checkbox
        self.thickness.grid(row=9, column=0, columnspan=3)
        # thickness t
        self.controls[5]["name"].config(text="t")
        self.controls[5]["name"].grid(row=10,column=0)
        self.controls[5]["entry"].grid(row=10,column=1)
        self.controls[5]["unit"].grid(row=10,column=2)
        # calculate button
        self.calc.grid(row=11,column=1,pady=5)
    def change_to_circle(self):
        self.lbl.grid(row=0, column=1)
        # size d
        self.controls[0]["name"].config(text="Ød")
        self.controls[0]["name"].grid(row=2,column=0)
        self.controls[0]["entry"].grid(row=2,column=1)
        self.controls[0]["unit"].grid(row=2,column=2)
        # transformed checkbox
        self.transformed_coordinate_system.grid(row=5, column=0, columnspan=3)
        # transformed x
        self.controls[2]["name"].config(text="x")
        self.controls[2]["name"].grid(row=6,column=0)
        self.controls[2]["entry"].grid(row=6,column=1)
        self.controls[2]["unit"].grid(row=6,column=2)
        # transformed y
        self.controls[3]["name"].config(text="y")
        self.controls[3]["name"].grid(row=7,column=0)
        self.controls[3]["entry"].grid(row=7,column=1)
        self.controls[3]["unit"].grid(row=7,column=2)
        # transformed phi
        self.controls[4]["name"].config(text="φ")
        self.controls[4]["name"].grid(row=8,column=0)
        self.controls[4]["entry"].grid(row=8,column=1)
        self.controls[4]["unit"].grid(row=8,column=2)
        # thickness checkbox
        self.thickness.grid(row=9, column=0, columnspan=3)
        # thickness t
        self.controls[5]["name"].config(text="t")
        self.controls[5]["name"].grid(row=10,column=0)
        self.controls[5]["entry"].grid(row=10,column=1)
        self.controls[5]["unit"].grid(row=10,column=2)
        # calculate button
        self.calc.grid(row=11,column=1,pady=5)
    def change_to_ellipse(self):
        self.lbl.grid(row=0, column=1)
        # size a
        self.controls[0]["name"].config(text="a")
        self.controls[0]["name"].grid(row=2,column=0)
        self.controls[0]["entry"].grid(row=2,column=1)
        self.controls[0]["unit"].grid(row=2,column=2)
        # size b
        self.controls[1]["name"].config(text="b")
        self.controls[1]["name"].grid(row=3,column=0)
        self.controls[1]["entry"].grid(row=3,column=1)
        self.controls[1]["unit"].grid(row=3,column=2)
        # transformed checkbox
        self.transformed_coordinate_system.grid(row=5, column=0, columnspan=3)
        # transformed x
        self.controls[2]["name"].config(text="x")
        self.controls[2]["name"].grid(row=6,column=0)
        self.controls[2]["entry"].grid(row=6,column=1)
        self.controls[2]["unit"].grid(row=6,column=2)
        # transformed y
        self.controls[3]["name"].config(text="y")
        self.controls[3]["name"].grid(row=7,column=0)
        self.controls[3]["entry"].grid(row=7,column=1)
        self.controls[3]["unit"].grid(row=7,column=2)
        # transformed phi
        self.controls[4]["name"].config(text="φ")
        self.controls[4]["name"].grid(row=8,column=0)
        self.controls[4]["entry"].grid(row=8,column=1)
        self.controls[4]["unit"].grid(row=8,column=2)
        # thickness checkbox
        self.thickness.grid(row=9, column=0, columnspan=3)
        # thickness t
        self.controls[5]["name"].config(text="t")
        self.controls[5]["name"].grid(row=10,column=0)
        self.controls[5]["entry"].grid(row=10,column=1)
        self.controls[5]["unit"].grid(row=10,column=2)
        # calculate button
        self.calc.grid(row=11,column=1,pady=5)
    def change_to_isosceles_triangle(self):
        self.lbl.grid(row=0, column=1)
        # size a
        self.controls[0]["name"].config(text="a")
        self.controls[0]["name"].grid(row=2,column=0)
        self.controls[0]["entry"].grid(row=2,column=1)
        self.controls[0]["unit"].grid(row=2,column=2)
        # size b
        self.controls[1]["name"].config(text="b")
        self.controls[1]["name"].grid(row=3,column=0)
        self.controls[1]["entry"].grid(row=3,column=1)
        self.controls[1]["unit"].grid(row=3,column=2)
        # transformed checkbox
        self.transformed_coordinate_system.grid(row=5, column=0, columnspan=3)
        # transformed x
        self.controls[2]["name"].config(text="x")
        self.controls[2]["name"].grid(row=6,column=0)
        self.controls[2]["entry"].grid(row=6,column=1)
        self.controls[2]["unit"].grid(row=6,column=2)
        # transformed y
        self.controls[3]["name"].config(text="y")
        self.controls[3]["name"].grid(row=7,column=0)
        self.controls[3]["entry"].grid(row=7,column=1)
        self.controls[3]["unit"].grid(row=7,column=2)
        # transformed phi
        self.controls[4]["name"].config(text="φ")
        self.controls[4]["name"].grid(row=8,column=0)
        self.controls[4]["entry"].grid(row=8,column=1)
        self.controls[4]["unit"].grid(row=8,column=2)
        # thickness checkbox
        self.thickness.grid(row=9, column=0, columnspan=3)
        # thickness t
        self.controls[5]["name"].config(text="t")
        self.controls[5]["name"].grid(row=10,column=0)
        self.controls[5]["entry"].grid(row=10,column=1)
        self.controls[5]["unit"].grid(row=10,column=2)
        # calculate button
        self.calc.grid(row=11,column=1,pady=5)
