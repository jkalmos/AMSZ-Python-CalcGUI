import tkinter as tk
from tkinter import ttk
from typing import Collection
from PlotFunctions import plot
class SideMenu(tk.Frame):
    def __init__(self, root):
        super().__init__(root,width=30, bg=root.colors['secondary_color'])
        self.root = root
        self.shape = None

# DEFINE SIDEMENU OBJECTS --------------------------------------------------------------------------------------------------------------
        self.canvas = tk.Canvas(self, bg=self["background"], highlightthickness=0)
        #self.canvas.create_text(50,10, anchor="nw", text="")
        self.canvas.grid(row=0, column=0, sticky="nsew")

        # place holder label
        self.lbl = tk.Label(self.canvas, width = 30, bg = self["background"] , fg='white')
        self.lbl.grid(row=0, column=1)

        # combobox
        # style= ttk.Style()
        # # style.theme_use('clam')
        # style.configure("TCombobox", fieldbackground= self["background"], background=self["background"])

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

        self.n = tk.StringVar()
        self.choose_shape = ttk.Combobox(self.canvas, width = 25, textvariable=self.n, state='readonly', text="x", justify='center')
        self.choose_shape.set('--- Alakzat ---')
        self.choose_shape['values'] = ('Téglalap', 
                                'Kör',
                                'Ellipszis',
                                'Egyenlőszárú háromszög')
        # self.choose_shape.place(x=0, y=0)
        self.choose_shape.grid(row=1, column=0, columnspan=5)
        self.choose_shape.bind('<<ComboboxSelected>>', shape_changed)

        # input labels font
        input_font = "Roboto", 11

        # dimension input labels
        self.l1 = tk.Label(self.canvas, text="Width", bg=self["background"], fg='white', font=input_font)
        self.m1 = tk.Label(self.canvas, text="mm", bg=self["background"], fg='white', font=input_font)
        self.l2 = tk.Label(self.canvas, text="Heigth", bg=self["background"], fg='white', font=input_font)
        self.m2 = tk.Label(self.canvas, text="mm", bg=self["background"], fg='white', font=input_font)

        # dimension input entries
        self.e1 = tk.Entry(self.canvas, width = 10, bg=self["background"], fg='white')
        self.e2 = tk.Entry(self.canvas, width = 10, bg=self["background"], fg='white')

        # transformed coordinate system input labels
        self.tl1 = tk.Label(self.canvas, text="x", bg=self["background"], fg='white', font=input_font)
        self.tm1 = tk.Label(self.canvas, text="mm", bg=self["background"], fg='white', font=input_font)
        self.tl2 = tk.Label(self.canvas, text="y", bg=self["background"], fg='white', font=input_font)
        self.tm2 = tk.Label(self.canvas, text="mm", bg=self["background"], fg='white', font=input_font)
        self.tl3 = tk.Label(self.canvas, text="phi", bg=self["background"], fg='white', font=input_font)
        self.tm3 = tk.Label(self.canvas, text="rad", bg=self["background"], fg='white', font=input_font)

        # transformed coordinate system input entries
        self.te1 = tk.Entry(self.canvas, width = 10, bg=self["background"], fg='white', state='disabled', disabledbackground="grey")
        self.te2 = tk.Entry(self.canvas, width = 10, bg=self["background"], fg='white', state='disabled', disabledbackground="grey")
        self.te3 = tk.Entry(self.canvas, width = 10, bg=self["background"], fg='white', state='disabled', disabledbackground="grey")

        # thickness input labels
        self.thl1 = tk.Label(self.canvas, text="t", bg=self["background"], fg='white', font=input_font)
        self.thm1 = tk.Label(self.canvas, text="mm", bg=self["background"], fg='white', font=input_font)

        # thickness input entry
        self.the1 = tk.Entry(self.canvas, width = 10, bg=self["background"], fg='white', state='disabled', disabledbackground="grey")

        # calculate button
        self.buttonimage = tk.PhotoImage(file="calc_button.png")
        self.calc = tk.Button(self.canvas, image=self.buttonimage, text="Calculate", command=lambda: self.root.calculate(), activebackground=self["background"])
        # self.calc = tk.Button(self, text="Calculate", command=lambda: self.root.calculate())
        self.calc["bg"] = self["background"]
        self.calc["border"] = "0"
        self.calc["width"] = "73"
        self.calc["height"] = "21"

        # result label font
        result_font = "Roboto", 12

        # result labels
        self.result1 = tk.Label(self.canvas, text="", bg=self["background"], fg='white', font=result_font)
        self.result2 = tk.Label(self.canvas, text="", bg=self["background"], fg='white', font=result_font)
        self.result3 = tk.Label(self.canvas, text="", bg=self["background"], fg='white', font=result_font)
        self.result4 = tk.Label(self.canvas, text="", bg=self["background"], fg='white', font=result_font)
        self.result5 = tk.Label(self.canvas, text="", bg=self["background"], fg='white', font=result_font)
        self.result6 = tk.Label(self.canvas, text="", bg=self["background"], fg='white', font=result_font)
        self.result1.grid(row=12, column = 1, columnspan=3, padx=5, pady=5)
        self.result2.grid(row=13, column = 1, columnspan=3, padx=5, pady=5)
        self.result3.grid(row=14, column = 1, columnspan=3, padx=5, pady=5)
        self.result4.grid(row=15, column = 1, columnspan=3, padx=5, pady=5)
        self.result5.grid(row=16, column = 1, columnspan=3, padx=5, pady=5)
        self.result6.grid(row=17, column = 1, columnspan=3, padx=5, pady=5)

        # Checkbox: set thickness
        self.thickness = tk.Checkbutton(
            self.canvas, text = "Falvastagság hozzáadása",
            variable = self.root.thickness_on, onvalue=True, offvalue=False, font=input_font, 
            bg = self["background"], fg='white', selectcolor='grey',
            command = lambda: [plot(root, self.shape, self.root.coordinate_on.get(), self.root.dimension_lines_on.get(), self.root.transformed_coordinate_on.get(), self.root.thickness_on.get(), root.colors),
            entry_enable(self.the1, self.root.thickness_on)])

        # Checkbox: transformed coordinate system
        self.transformed_coordinate_system = tk.Checkbutton(
            self.canvas, text = "Transzformált koordináta rendszer", font=input_font, 
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
        self.indicators.append(self.result3)
        self.indicators.append(self.result4)
        self.indicators.append(self.result5)
        self.indicators.append(self.result6)
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


# USEFUL FUNCTIONS --------------------------------------------------------------------------------------
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
        self.lbl.grid(row=1, column=0, columnspan=5, pady=10)
        # size a
        self.controls[0]["name"].config(text="a")
        self.controls[0]["name"].grid(row=2,column=1, sticky='e', pady=5)
        self.controls[0]["entry"].grid(row=2,column=2, pady=5)
        self.controls[0]["unit"].grid(row=2,column=3, sticky='w', pady=5)
        # size b
        self.controls[1]["name"].config(text="b")
        self.controls[1]["name"].grid(row=3,column=1, sticky='e', pady=5)
        self.controls[1]["entry"].grid(row=3,column=2, pady=5)
        self.controls[1]["unit"].grid(row=3,column=3, sticky='w', pady=5)
        # transformed checkbox
        self.transformed_coordinate_system.grid(row=4, column=1, columnspan=3, pady=5)
        # transformed x
        self.controls[2]["name"].config(text="x")
        self.controls[2]["name"].grid(row=5,column=1, sticky='e', pady=5)
        self.controls[2]["entry"].grid(row=5,column=2, pady=5)
        self.controls[2]["unit"].grid(row=5,column=3, sticky='w', pady=5)
        # transformed y
        self.controls[3]["name"].config(text="y")
        self.controls[3]["name"].grid(row=6,column=1, sticky='e', pady=5)
        self.controls[3]["entry"].grid(row=6,column=2, pady=5)
        self.controls[3]["unit"].grid(row=6,column=3, sticky='w', pady=5)
        # transformed phi
        self.controls[4]["name"].config(text="φ")
        self.controls[4]["name"].grid(row=7,column=1, sticky='e', pady=5)
        self.controls[4]["entry"].grid(row=7,column=2, pady=5)
        self.controls[4]["unit"].grid(row=7,column=3, sticky='w', pady=5)
        # thickness checkbox
        self.thickness.grid(row=8, column=1, columnspan=3, pady=5)
        # thickness t
        self.controls[5]["name"].config(text="t")
        self.controls[5]["name"].grid(row=9,column=1, sticky='e', pady=5)
        self.controls[5]["entry"].grid(row=9,column=2, pady=5)
        self.controls[5]["unit"].grid(row=9,column=3, sticky='w', pady=5)
        # calculate button
        self.calc.grid(row=10,column=1, columnspan=3, pady=5)
    def change_to_circle(self):
        self.lbl.grid(row=1, column=0, columnspan=5, pady=10)
        # diameter d
        self.controls[0]["name"].config(text="d")
        self.controls[0]["name"].grid(row=2,column=1, sticky='e', pady=5)
        self.controls[0]["entry"].grid(row=2,column=2, pady=5)
        self.controls[0]["unit"].grid(row=2,column=3, sticky='w', pady=5)
        # transformed checkbox
        self.transformed_coordinate_system.grid(row=3, column=1, columnspan=3, pady=5)
        # transformed x
        self.controls[2]["name"].config(text="x")
        self.controls[2]["name"].grid(row=4,column=1, sticky='e', pady=5)
        self.controls[2]["entry"].grid(row=4,column=2, pady=5)
        self.controls[2]["unit"].grid(row=4,column=3, sticky='w', pady=5)
        # transformed y
        self.controls[3]["name"].config(text="y")
        self.controls[3]["name"].grid(row=5,column=1, sticky='e', pady=5)
        self.controls[3]["entry"].grid(row=5,column=2, pady=5)
        self.controls[3]["unit"].grid(row=5,column=3, sticky='w', pady=5)
        # transformed phi
        self.controls[4]["name"].config(text="φ")
        self.controls[4]["name"].grid(row=6,column=1, sticky='e', pady=5)
        self.controls[4]["entry"].grid(row=6,column=2, pady=5)
        self.controls[4]["unit"].grid(row=6,column=3, sticky='w', pady=5)
        # thickness checkbox
        self.thickness.grid(row=7, column=1, columnspan=3)
        # thickness t
        self.controls[5]["name"].config(text="t")
        self.controls[5]["name"].grid(row=8,column=1, sticky='e', pady=5)
        self.controls[5]["entry"].grid(row=8,column=2, pady=5)
        self.controls[5]["unit"].grid(row=8,column=3, sticky='w', pady=5)
        # calculate button
        self.calc.grid(row=10,column=1, columnspan=3, pady=5)
    def change_to_ellipse(self):
        self.lbl.grid(row=1, column=0, columnspan=5, pady=10)
        # size a
        self.controls[0]["name"].config(text="a")
        self.controls[0]["name"].grid(row=2,column=1, sticky='e', pady=5)
        self.controls[0]["entry"].grid(row=2,column=2, pady=5)
        self.controls[0]["unit"].grid(row=2,column=3, sticky='w', pady=5)
        # size b
        self.controls[1]["name"].config(text="b")
        self.controls[1]["name"].grid(row=3,column=1, sticky='e', pady=5)
        self.controls[1]["entry"].grid(row=3,column=2, pady=5)
        self.controls[1]["unit"].grid(row=3,column=3, sticky='w', pady=5)
        # transformed checkbox
        self.transformed_coordinate_system.grid(row=4, column=1, columnspan=3, pady=5)
        # transformed x
        self.controls[2]["name"].config(text="x")
        self.controls[2]["name"].grid(row=5,column=1, sticky='e', pady=5)
        self.controls[2]["entry"].grid(row=5,column=2, pady=5)
        self.controls[2]["unit"].grid(row=5,column=3, sticky='w', pady=5)
        # transformed y
        self.controls[3]["name"].config(text="y")
        self.controls[3]["name"].grid(row=6,column=1, sticky='e', pady=5)
        self.controls[3]["entry"].grid(row=6,column=2, pady=5)
        self.controls[3]["unit"].grid(row=6,column=3, sticky='w', pady=5)
        # transformed phi
        self.controls[4]["name"].config(text="φ")
        self.controls[4]["name"].grid(row=7,column=1, sticky='e', pady=5)
        self.controls[4]["entry"].grid(row=7,column=2, pady=5)
        self.controls[4]["unit"].grid(row=7,column=3, sticky='w', pady=5)
        # thickness checkbox
        self.thickness.grid(row=8, column=1, columnspan=3, pady=5)
        # thickness t
        self.controls[5]["name"].config(text="t")
        self.controls[5]["name"].grid(row=9,column=1, sticky='e', pady=5)
        self.controls[5]["entry"].grid(row=9,column=2, pady=5)
        self.controls[5]["unit"].grid(row=9,column=3, sticky='w', pady=5)
        # calculate button
        self.calc.grid(row=10,column=1, columnspan=3, pady=5)
    def change_to_isosceles_triangle(self):
        self.lbl.grid(row=1, column=0, columnspan=5, pady=10)
        # size a
        self.controls[0]["name"].config(text="a")
        self.controls[0]["name"].grid(row=2,column=1, sticky='e', pady=5)
        self.controls[0]["entry"].grid(row=2,column=2, pady=5)
        self.controls[0]["unit"].grid(row=2,column=3, sticky='w', pady=5)
        # size b
        self.controls[1]["name"].config(text="b")
        self.controls[1]["name"].grid(row=3,column=1, sticky='e', pady=5)
        self.controls[1]["entry"].grid(row=3,column=2, pady=5)
        self.controls[1]["unit"].grid(row=3,column=3, sticky='w', pady=5)
        # transformed checkbox
        self.transformed_coordinate_system.grid(row=4, column=1, columnspan=3, pady=5)
        # transformed x
        self.controls[2]["name"].config(text="x")
        self.controls[2]["name"].grid(row=5,column=1, sticky='e', pady=5)
        self.controls[2]["entry"].grid(row=5,column=2, pady=5)
        self.controls[2]["unit"].grid(row=5,column=3, sticky='w', pady=5)
        # transformed y
        self.controls[3]["name"].config(text="y")
        self.controls[3]["name"].grid(row=6,column=1, sticky='e', pady=5)
        self.controls[3]["entry"].grid(row=6,column=2, pady=5)
        self.controls[3]["unit"].grid(row=6,column=3, sticky='w', pady=5)
        # transformed phi
        self.controls[4]["name"].config(text="φ")
        self.controls[4]["name"].grid(row=7,column=1, sticky='e', pady=5)
        self.controls[4]["entry"].grid(row=7,column=2, pady=5)
        self.controls[4]["unit"].grid(row=7,column=3, sticky='w', pady=5)
        # thickness checkbox
        self.thickness.grid(row=8, column=1, columnspan=3)
        # thickness t
        self.controls[5]["name"].config(text="t")
        self.controls[5]["name"].grid(row=9,column=1, sticky='e', pady=5)
        self.controls[5]["entry"].grid(row=9,column=2, pady=5)
        self.controls[5]["unit"].grid(row=9,column=3, sticky='w', pady=5)
        # calculate button
        self.calc.grid(row=10,column=1, columnspan=3, pady=5)
