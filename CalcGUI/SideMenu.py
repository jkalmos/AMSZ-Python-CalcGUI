import tkinter as tk
class SideMenu(tk.Frame):
    def __init__(self, root):
        super().__init__(root,width=400, bg='#314457')
        self.root = root
        self.shape = None
        self.controls=[]
        #title = tk.Label(self, text="This is a side menu", bg=self["background"], fg='white')
        #title.grid(row=0)
        lbl = tk.Label(self, width = 20, bg=self["background"])
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
        self.indicators = []
        self.eredmeny1 = tk.Label(self, text="", bg=self["background"], fg='white')
        #self.eredmeny1.grid(row=6)
        self.eredmeny2 = tk.Label(self, text="", bg=self["background"], fg='white')
        #self.eredmeny2.grid(row=7)
        self.indicators.append(self.eredmeny1)
        self.indicators.append(self.eredmeny2)
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
    def change_to_recrangle(self):
        #Szélesség
        self.controls[0]["nev"].config(text="Width")
        self.controls[0]["nev"].grid(row=2,column=0)
        self.controls[0]["entry"].grid(row=2,column=1)
        self.controls[0]["mertekegyseg"].grid(row=2,column=2)
        #Magasság
        self.controls[1]["nev"].config(text="Height")
        self.controls[1]["nev"].grid(row=3,column=0)
        self.controls[1]["entry"].grid(row=3,column=1)
        self.controls[1]["mertekegyseg"].grid(row=3,column=2)
        self.calc.grid(row=4,column=1,pady=5)
        for idx,i in enumerate(self.indicators):
            i.grid(row=5+idx)
    def change_to_circle(self):
        self.controls[0]["nev"].config(text="Átmérő")
        self.controls[0]["nev"].grid(row=2,column=0)
        self.controls[0]["entry"].grid(row=2,column=1)
        self.controls[0]["mertekegyseg"].grid(row=2,column=2)
        self.calc.grid(row=4,column=1,pady=5)
        for idx,i in enumerate(self.indicators):
            i.grid(row=5+idx)
    def change_to_ring(self):
        #d1
        self.controls[0]["nev"].config(text="d1")
        self.controls[0]["nev"].grid(row=2,column=0)
        self.controls[0]["entry"].grid(row=2,column=1)
        self.controls[0]["mertekegyseg"].grid(row=2,column=2)
        #d2
        self.controls[1]["nev"].config(text="d2")
        self.controls[1]["nev"].grid(row=3,column=0)
        self.controls[1]["entry"].grid(row=3,column=1)
        self.controls[1]["mertekegyseg"].grid(row=3,column=2)
        self.calc.grid(row=4,column=1,pady=5)
        for idx,i in enumerate(self.indicators):
            i.grid(row=5+idx)
    def change_to_RectangularHS(self):
        #w1 h1 w2 h2
        #TODO
        pass
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
        self.calc.grid(row=4,column=1,pady=5)
        for idx,i in enumerate(self.indicators):
            i.grid(row=5+idx)
    def change_to_isosceles_triangle(self):
        #w
        self.controls[0]["nev"].config(text="Width")
        self.controls[0]["nev"].grid(row=2,column=0)
        self.controls[0]["entry"].grid(row=2,column=1)
        self.controls[0]["mertekegyseg"].grid(row=2,column=2)
        #h
        self.controls[1]["nev"].config(text="Height")
        self.controls[1]["nev"].grid(row=3,column=0)
        self.controls[1]["entry"].grid(row=3,column=1)
        self.controls[1]["mertekegyseg"].grid(row=3,column=2)
        self.calc.grid(row=4,column=1,pady=5)
        for idx,i in enumerate(self.indicators):
            i.grid(row=5+idx)