import tkinter as tk
from PlotFunctions import plot
class SideMenu(tk.Frame):
    def __init__(self, root):
        super().__init__(root,width=400, bg=root.colors['secondary_color'])
        self.root = root
        self.shape = None
        self.controls=[]
        #title = tk.Label(self, text="This is a side menu", bg=self["background"], fg='white')
        #title.grid(row=0)
        lbl = tk.Label(self, width = 5, bg=self["background"])
        lbl.grid(row=0)
        self.l1=tk.Label(self, text="Width", bg=self["background"], fg='white')
        self.m1=tk.Label(self, text="mm", bg=self["background"], fg='white')
        #self.l1.grid(row=1)
        self.l2=tk.Label(self, text="Heigth", bg=self["background"], fg='white')
        self.m2=tk.Label(self, text="mm", bg=self["background"], fg='white')
        #self.l2.grid(row=3)

        self.calc = tk.Button(self, text="Calculate", command=lambda: self.root.calculate())
        #self.calc.grid(row=5, pady=5)

        self.e1 = tk.Entry(self, width = 10, bg="#475C6F", fg='white')
        self.e2 = tk.Entry(self, width = 10, bg="#475C6F", fg='white')
        #self.e1.grid(row=2)
        #self.e2.grid(row=4)
        self.controls.append({"nev":self.l1, "entry":self.e1, "mertekegyseg":self.m1})
        self.controls.append({"nev":self.l2, "entry":self.e2, "mertekegyseg":self.m2})
        #inner cut_offs:
        self.inner_e1 = tk.Entry(self, width = 10, bg="#475C6F", fg='white')
        self.inner_e2 = tk.Entry(self, width = 10, bg="#475C6F", fg='white')
        self.inner_l1=tk.Label(self, text="Width", bg=self["background"], fg='white')
        self.inner_m1=tk.Label(self, text="mm", bg=self["background"], fg='white')
        self.inner_l2=tk.Label(self, text="Heigth", bg=self["background"], fg='white')
        self.inner_m2=tk.Label(self, text="mm", bg=self["background"], fg='white')
        self.controls.append({"nev":self.inner_l1, "entry":self.inner_e1, "mertekegyseg":self.inner_m1})
        self.controls.append({"nev":self.inner_l2, "entry":self.inner_e2, "mertekegyseg":self.inner_m2})
        
        #Checkbox
        self.is_inner_cut_off = tk.BooleanVar()
        self.inner_cut_off = tk.Checkbutton(
            self, text="Falvastagság hozzáadása",
            variable=self.is_inner_cut_off, onvalue=True, offvalue=False,
            bg=self["background"], fg='white', selectcolor='grey',
            command=self.add_inner_cut_off)
        self.inner_cut_off.grid(row=0, column=0,columnspan=3)

        # Checkbox: coordinate system
        self.coordinate_system = tk.Checkbutton(
            self, text = "Koordináta rendszer",
            variable = self.root.coordinate_on, onvalue=True, offvalue=False,
            bg=self["background"], fg='white', selectcolor='grey',
            command=lambda: plot(root, self.root.dimensions, self.shape, self.root.coordinate_on.get(), self.root.dimension_lines_on.get(), self.root.transformed_coordinate_on.get()))
        self.coordinate_system.grid(row = 0, column = 0, columnspan = 4)

        self.indicators = []
        self.eredmeny1 = tk.Label(self, text="", bg=self["background"], fg='white')
        #self.eredmeny1.grid(row=6, column=1)
        self.eredmeny2 = tk.Label(self, text="", bg=self["background"], fg='white')
        #self.eredmeny2.grid(row=7, column=1)
        self.indicators.append(self.eredmeny1)
        self.indicators.append(self.eredmeny2)
    def add_inner_cut_off(self):
        if self.is_inner_cut_off.get():
            for i in self.indicators:
                i.config(text="")
                i.grid_forget()
            self.calc.grid_forget()
            self.inner_cut_off.grid_forget()
            self.inner_l1.grid(row=6, column=0)
            self.inner_m1.grid(row=6, column=2)
            self.inner_e1.grid(row=6, column=1)
            if self.shape != "Circle":
                self.inner_l2.grid(row=7, column=0)
                self.inner_m2.grid(row=7, column=2)
                self.inner_e2.grid(row=7, column=1)
            self.calc.grid(row=9,column=0, columnspan=3)
            self.inner_cut_off.grid(row=8,column=1, columnspan=3)
            for idx,i in enumerate(self.indicators):
                i.grid(row=10+idx, column=1)
                i.config(text="")
            print("Turned on")
        else:
            print("Turned off")
            self.inner_l1.grid_forget()
            self.inner_m1.grid_forget()
            self.inner_e1.grid_forget()
            self.inner_l2.grid_forget()
            self.inner_m2.grid_forget()
            self.inner_e2.grid_forget()
            for idx,i in enumerate(self.indicators):
                i.config(text="")
    def clear(self):
        for i in self.controls:
            i["nev"].grid_forget()
            i["entry"].grid_forget()
            i["entry"].delete(0,"end")
            i["mertekegyseg"].grid_forget()
        for i in self.indicators:
            i.config(text="")
            i.grid_forget()
        self.calc.grid_forget()
        self.inner_cut_off.grid_forget()
    def change_to_recrangle(self):
        #Szélesség
        self.controls[0]["nev"].config(text="a")
        self.controls[0]["nev"].grid(row=2,column=0)
        self.controls[0]["entry"].grid(row=2,column=1)
        self.controls[0]["mertekegyseg"].grid(row=2,column=2)
        #Magasság
        self.controls[1]["nev"].config(text="b")
        self.controls[1]["nev"].grid(row=3,column=0)
        self.controls[1]["entry"].grid(row=3,column=1)
        self.controls[1]["mertekegyseg"].grid(row=3,column=2)
        self.inner_cut_off.grid(row=4, column=0, columnspan=3)
        self.coordinate_system.grid(row=5, column=0, columnspan=3)
        self.calc.grid(row=6,column=1,pady=5)
        for idx,i in enumerate(self.indicators):
            i.grid(row=10+self.is_inner_cut_off.get()*2+idx, column=1)
    def change_to_circle(self):
        self.controls[0]["nev"].config(text="Átmérő")
        self.controls[0]["nev"].grid(row=2,column=0)
        self.controls[0]["entry"].grid(row=2,column=1)
        self.controls[0]["mertekegyseg"].grid(row=2,column=2)
        self.inner_cut_off.grid(row=4, column=0, columnspan=3)
        self.calc.grid(row=5,column=1,pady=5)
        for idx,i in enumerate(self.indicators):
            i.grid(row=7+self.is_inner_cut_off.get()*2+idx, column=1)
    def change_to_ellipse(self):
        #a
        self.controls[0]["nev"].config(text="a")
        self.controls[0]["nev"].grid(row=2,column=0)
        self.controls[0]["entry"].grid(row=2,column=1)
        self.controls[0]["mertekegyseg"].grid(row=2,column=2)
        #b
        self.controls[1]["nev"].config(text="b")
        self.controls[1]["nev"].grid(row=3,column=0)
        self.controls[1]["entry"].grid(row=3,column=1)
        self.controls[1]["mertekegyseg"].grid(row=3,column=2)
        self.inner_cut_off.grid(row=4, column=0,columnspan=3)
        self.calc.grid(row=5,column=1,pady=5)
        for idx,i in enumerate(self.indicators):
            i.grid(row=7+self.is_inner_cut_off.get()*2+idx, column=1)
    def change_to_isosceles_triangle(self):
        #w
        self.controls[0]["nev"].config(text="a")
        self.controls[0]["nev"].grid(row=2,column=0)
        self.controls[0]["entry"].grid(row=2,column=1)
        self.controls[0]["mertekegyseg"].grid(row=2,column=2)
        #h
        self.controls[1]["nev"].config(text="b")
        self.controls[1]["nev"].grid(row=3,column=0)
        self.controls[1]["entry"].grid(row=3,column=1)
        self.controls[1]["mertekegyseg"].grid(row=3,column=2)
        self.inner_cut_off.grid(row=4, column=0,columnspan=3)
        self.calc.grid(row=5,column=1,pady=5)
        for idx,i in enumerate(self.indicators):
            i.grid(row=7+self.is_inner_cut_off.get()*2+idx, column=1)
