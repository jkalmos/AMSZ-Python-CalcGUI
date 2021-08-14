import tkinter as tk
from tkinter import ttk
from PlotFunctions import plot
class SideMenu(tk.Frame):
    def __init__(self, root):
        super().__init__(root,width=400, bg=root.colors['secondary_color'])
        self.root = root
        self.shape = None

# DEFINE SIDEMENU OBJECTS ------------------------------------------------------------------------------
        # place holder label
        lbl = tk.Label(self, text="Alakzat:", width = 0, bg=self["background"] , fg='white')
        lbl.grid(row=0, column=1)

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
        self.choose_shape = ttk.Combobox(self, width = 25, textvariable=self.n, state='readonly', text="x")
        self.choose_shape['values'] = ('Téglalap', 
                                'Kör',
                                'Ellipszis',
                                'Egyenlőszárú háromszög')
        self.choose_shape.grid(column = 1, row = 1)
        self.choose_shape.bind('<<ComboboxSelected>>', shape_changed)

        # dimension input labels
        self.l1 = tk.Label(self, text="Width", bg=self["background"], fg='white')
        self.m1 = tk.Label(self, text="mm", bg=self["background"], fg='white')
        self.l2 = tk.Label(self, text="Heigth", bg=self["background"], fg='white')
        self.m2 = tk.Label(self, text="mm", bg=self["background"], fg='white')

        # dimension input entries
        self.e1 = tk.Entry(self, width = 10, bg="#475C6F", fg='white')
        self.e2 = tk.Entry(self, width = 10, bg="#475C6F", fg='white')

        # transformed coordinate system input labels
        self.tl1 = tk.Label(self, text="x", bg=self["background"], fg='white')
        self.tm1 = tk.Label(self, text="mm", bg=self["background"], fg='white')
        self.tl2 = tk.Label(self, text="y", bg=self["background"], fg='white')
        self.tm2 = tk.Label(self, text="mm", bg=self["background"], fg='white')
        self.tl3 = tk.Label(self, text="phi", bg=self["background"], fg='white')
        self.tm3 = tk.Label(self, text="rad", bg=self["background"], fg='white')

        # transformed coordinate system input entries
        self.te1 = tk.Entry(self, width = 10, bg="#475C6F", fg='white', state='disabled', disabledbackground="grey")
        self.te2 = tk.Entry(self, width = 10, bg="#475C6F", fg='white', state='disabled', disabledbackground="grey")
        self.te3 = tk.Entry(self, width = 10, bg="#475C6F", fg='white', state='disabled', disabledbackground="grey")

        # thickness input labels
        self.thl1 = tk.Label(self, text="t", bg=self["background"], fg='white')
        self.thm1 = tk.Label(self, text="mm", bg=self["background"], fg='white')

        # thickness input entry
        self.the1 = tk.Entry(self, width = 10, bg="#475C6F", fg='white', state='disabled', disabledbackground="grey")

        # calculate button
        self.buttonimage = tk.PhotoImage(file="calc_button.png")
        self.calc = tk.Button(self, image=self.buttonimage, text="Calculate", command=lambda: self.root.calculate())
        # self.calc = tk.Button(self, text="Calculate", command=lambda: self.root.calculate())
        self.calc["bg"] = '#082032'
        self.calc["border"] = "0"
        self.calc["width"] = "73"
        self.calc["height"] = "21"

        # append entry objects to controls array
        self.controls = []
        self.controls.append({"nev":self.l1, "entry":self.e1, "unit":self.m1, "unit_type": "length"})
        self.controls.append({"nev":self.l2, "entry":self.e2, "unit":self.m2, "unit_type": "length"})
        self.controls.append({"nev":self.tl1, "entry":self.te1, "unit":self.tm1, "unit_type": "length"})
        self.controls.append({"nev":self.tl2, "entry":self.te2, "unit":self.tm2, "unit_type": "length"})
        self.controls.append({"nev":self.tl3, "entry":self.te3, "unit":self.tm3, "unit_type": "degree"})
        self.controls.append({"nev":self.thl1, "entry":self.the1, "unit":self.thm1, "unit_type": "length"})

        # result labels
        self.indicators = []
        self.result1 = tk.Label(self, text="", bg=self["background"], fg='white')
        self.result2 = tk.Label(self, text="", bg=self["background"], fg='white')
        self.result1.grid(row=12, column = 1)
        self.result2.grid(row=13, column = 1)
        self.indicators.append(self.result1)
        self.indicators.append(self.result2)

        # Checkbox: set thickness
        self.thickness = tk.Checkbutton(
            self, text = "Falvastagság hozzáadása",
            variable = self.root.thickness_on, onvalue=True, offvalue=False,
            bg = self["background"], fg='white', selectcolor='grey',
            command = lambda: [plot(root, self.shape, self.root.coordinate_on.get(), self.root.dimension_lines_on.get(), self.root.transformed_coordinate_on.get(), self.root.thickness_on.get()),
            entry_enable(self.the1, self.root.thickness_on)])

        # Checkbox: transformed coordinate system
        self.transformed_coordinate_system = tk.Checkbutton(
            self, text = "Transzformált koordináta rendszer",
            variable = self.root.transformed_coordinate_on, onvalue=True, offvalue=False,
            bg = self["background"], fg='white', selectcolor='grey',
            command = lambda: [plot(root, self.shape, self.root.coordinate_on.get(), self.root.dimension_lines_on.get(), self.root.transformed_coordinate_on.get(), self.root.thickness_on.get()),
            entry_enable(self.te1, self.root.transformed_coordinate_on),
            entry_enable(self.te2, self.root.transformed_coordinate_on),
            entry_enable(self.te3, self.root.transformed_coordinate_on)])

        def entry_enable(entry, var):
            if var.get() == False:
                entry.configure(state='disabled')
            elif var.get() == True:
                entry.configure(state='normal')

# USEFUL FUNCTIONS --------------------------------------------------------------------------------------
    def clear(self):
        for i in self.controls:
            i["nev"].grid_forget()
            i["entry"].grid_forget()
            i["entry"].delete(0,"end")
            i["unit"].grid_forget()
        for i in self.indicators:
            i.config(text="")
            i.grid_forget()
        self.calc.grid_forget()
        self.thickness.grid_forget()
        self.transformed_coordinate_system.grid_forget()
        
    def change_to_recrangle(self):
        # size a
        self.controls[0]["nev"].config(text="a")
        self.controls[0]["nev"].grid(row=2,column=0)
        self.controls[0]["entry"].grid(row=2,column=1)
        self.controls[0]["unit"].grid(row=2,column=2)
        # size b
        self.controls[1]["nev"].config(text="b")
        self.controls[1]["nev"].grid(row=3,column=0)
        self.controls[1]["entry"].grid(row=3,column=1)
        self.controls[1]["unit"].grid(row=3,column=2)
        # transformed checkbox
        self.transformed_coordinate_system.grid(row=5, column=0, columnspan=3)
        # transformed x
        self.controls[2]["nev"].config(text="x")
        self.controls[2]["nev"].grid(row=6,column=0)
        self.controls[2]["entry"].grid(row=6,column=1)
        self.controls[2]["unit"].grid(row=6,column=2)
        # transformed y
        self.controls[3]["nev"].config(text="y")
        self.controls[3]["nev"].grid(row=7,column=0)
        self.controls[3]["entry"].grid(row=7,column=1)
        self.controls[3]["unit"].grid(row=7,column=2)
        # transformed phi
        self.controls[4]["nev"].config(text="φ")
        self.controls[4]["nev"].grid(row=8,column=0)
        self.controls[4]["entry"].grid(row=8,column=1)
        self.controls[4]["unit"].grid(row=8,column=2)
        # thickness checkbox
        self.thickness.grid(row=9, column=0, columnspan=3)
        # thickness t
        self.controls[5]["nev"].config(text="t")
        self.controls[5]["nev"].grid(row=10,column=0)
        self.controls[5]["entry"].grid(row=10,column=1)
        self.controls[5]["unit"].grid(row=10,column=2)
        # calculate button
        self.calc.grid(row=11,column=1,pady=5)
    def change_to_circle(self):
        # size d
        self.controls[0]["nev"].config(text="Ød")
        self.controls[0]["nev"].grid(row=2,column=0)
        self.controls[0]["entry"].grid(row=2,column=1)
        self.controls[0]["unit"].grid(row=2,column=2)
        # transformed checkbox
        self.transformed_coordinate_system.grid(row=5, column=0, columnspan=3)
        # transformed x
        self.controls[2]["nev"].config(text="x")
        self.controls[2]["nev"].grid(row=6,column=0)
        self.controls[2]["entry"].grid(row=6,column=1)
        self.controls[2]["unit"].grid(row=6,column=2)
        # transformed y
        self.controls[3]["nev"].config(text="y")
        self.controls[3]["nev"].grid(row=7,column=0)
        self.controls[3]["entry"].grid(row=7,column=1)
        self.controls[3]["unit"].grid(row=7,column=2)
        # transformed phi
        self.controls[4]["nev"].config(text="φ")
        self.controls[4]["nev"].grid(row=8,column=0)
        self.controls[4]["entry"].grid(row=8,column=1)
        self.controls[4]["unit"].grid(row=8,column=2)
        # thickness checkbox
        self.thickness.grid(row=9, column=0, columnspan=3)
        # thickness t
        self.controls[5]["nev"].config(text="t")
        self.controls[5]["nev"].grid(row=10,column=0)
        self.controls[5]["entry"].grid(row=10,column=1)
        self.controls[5]["unit"].grid(row=10,column=2)
        # calculate button
        self.calc.grid(row=11,column=1,pady=5)
    def change_to_ellipse(self):
        # size a
        self.controls[0]["nev"].config(text="a")
        self.controls[0]["nev"].grid(row=2,column=0)
        self.controls[0]["entry"].grid(row=2,column=1)
        self.controls[0]["unit"].grid(row=2,column=2)
        # size b
        self.controls[1]["nev"].config(text="b")
        self.controls[1]["nev"].grid(row=3,column=0)
        self.controls[1]["entry"].grid(row=3,column=1)
        self.controls[1]["unit"].grid(row=3,column=2)
        # transformed checkbox
        self.transformed_coordinate_system.grid(row=5, column=0, columnspan=3)
        # transformed x
        self.controls[2]["nev"].config(text="x")
        self.controls[2]["nev"].grid(row=6,column=0)
        self.controls[2]["entry"].grid(row=6,column=1)
        self.controls[2]["unit"].grid(row=6,column=2)
        # transformed y
        self.controls[3]["nev"].config(text="y")
        self.controls[3]["nev"].grid(row=7,column=0)
        self.controls[3]["entry"].grid(row=7,column=1)
        self.controls[3]["unit"].grid(row=7,column=2)
        # transformed phi
        self.controls[4]["nev"].config(text="φ")
        self.controls[4]["nev"].grid(row=8,column=0)
        self.controls[4]["entry"].grid(row=8,column=1)
        self.controls[4]["unit"].grid(row=8,column=2)
        # thickness checkbox
        self.thickness.grid(row=9, column=0, columnspan=3)
        # thickness t
        self.controls[5]["nev"].config(text="t")
        self.controls[5]["nev"].grid(row=10,column=0)
        self.controls[5]["entry"].grid(row=10,column=1)
        self.controls[5]["unit"].grid(row=10,column=2)
        # calculate button
        self.calc.grid(row=11,column=1,pady=5)
    def change_to_isosceles_triangle(self):
        # size a
        self.controls[0]["nev"].config(text="a")
        self.controls[0]["nev"].grid(row=2,column=0)
        self.controls[0]["entry"].grid(row=2,column=1)
        self.controls[0]["unit"].grid(row=2,column=2)
        # size b
        self.controls[1]["nev"].config(text="b")
        self.controls[1]["nev"].grid(row=3,column=0)
        self.controls[1]["entry"].grid(row=3,column=1)
        self.controls[1]["unit"].grid(row=3,column=2)
        # transformed checkbox
        self.transformed_coordinate_system.grid(row=5, column=0, columnspan=3)
        # transformed x
        self.controls[2]["nev"].config(text="x")
        self.controls[2]["nev"].grid(row=6,column=0)
        self.controls[2]["entry"].grid(row=6,column=1)
        self.controls[2]["unit"].grid(row=6,column=2)
        # transformed y
        self.controls[3]["nev"].config(text="y")
        self.controls[3]["nev"].grid(row=7,column=0)
        self.controls[3]["entry"].grid(row=7,column=1)
        self.controls[3]["unit"].grid(row=7,column=2)
        # transformed phi
        self.controls[4]["nev"].config(text="φ")
        self.controls[4]["nev"].grid(row=8,column=0)
        self.controls[4]["entry"].grid(row=8,column=1)
        self.controls[4]["unit"].grid(row=8,column=2)
        # thickness checkbox
        self.thickness.grid(row=9, column=0, columnspan=3)
        # thickness t
        self.controls[5]["nev"].config(text="t")
        self.controls[5]["nev"].grid(row=10,column=0)
        self.controls[5]["entry"].grid(row=10,column=1)
        self.controls[5]["unit"].grid(row=10,column=2)
        # calculate button
        self.calc.grid(row=11,column=1,pady=5)
