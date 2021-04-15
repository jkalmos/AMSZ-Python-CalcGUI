import tkinter as tk

def doNothing():
    print("i wont")



class window(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Próba GUI")
        self.geometry("1000x600")
        self.minsize(width=200, height=200)

        # seting up toolbar
        self.eszkoztar = Eszkoztar(self)
        self.eszkoztar.pack(side=tk.TOP, fill=tk.X)

        #seting up side menu

        self.sm = SideMenu(self)
        self.sm.pack(side=tk.LEFT, fill=tk.Y)
        #seting up canvas
        self.canvas = tk.Canvas(self, width=800, height = 500, bg="white")
        self.canvas.pack()

    def doNothing(self):
        print("Ez a funkció jelenleg nem elérhető...")
    def add_circle(self):
        self.canvas.delete('all')
        reduced_size = min(self.canvas.winfo_width(),self.canvas.winfo_height())*0.7/2
        c_x = self.canvas.winfo_width()/2
        c_y = self.canvas.winfo_height()/2
        self.canvas.create_oval(c_x-reduced_size,c_y-reduced_size, c_x+reduced_size,c_y+reduced_size, fill="blue")
    def add_retangle(self):
        self.canvas.delete('all')
        reduced_size = min(self.canvas.winfo_width(),self.canvas.winfo_height())*0.7/2
        c_x = self.canvas.winfo_width()/2
        c_y = self.canvas.winfo_height()/2
        self.canvas.create_rectangle(c_x-reduced_size,c_y-reduced_size, c_x+reduced_size,c_y+reduced_size, fill="blue")
    def szamol(self):
        try:
            a = int(self.sm.e1.get())
            b = int(self.sm.e2.get())
            print(a*b)
        except:
            print("Hiba!")

# ************ Toolbar ************
class Eszkoztar(tk.Frame):
    def __init__(self, root):
        super().__init__(root, bg='#F5F5DC')
        self.root=root
        kep = tk.PhotoImage(file='./source/images/teglalap.png')
        kep = kep.subsample(10,10)
        label = tk.Label(image=kep)
        label.image = kep # keep a reference!
        tegla = tk.Button(self, text="teglalap",image=kep,compound="top", command=self.root.add_retangle)
        tegla.pack(side=tk.LEFT, padx=2, pady=2)
        kor = tk.Button(self, text="Kör", command=self.root.add_circle)
        kor.pack(side=tk.LEFT, padx=2, pady=2)
        haromszog = tk.Button(self, text="Háromszög", command=self.root.doNothing)
        haromszog.pack(side=tk.LEFT, padx=2, pady=2)

        calc = tk.Button(self, text="Calculate", command=self.root.szamol)
        calc.pack(side=tk.RIGHT, padx=2, pady=2)

class SideMenu(tk.Frame):
    def __init__(self, root):
        super().__init__(root, bg='#707070')
        self.root=root
        title = tk.Label(self, text="This is a side menu", bg=self["background"])
        title.grid(row=0, columnspan=2)
        tk.Label(self, text="Width", bg=self["background"]).grid(row=1)
        tk.Label(self, text="Heigth", bg=self["background"]).grid(row=2)
        self.e1 = tk.Entry(self)
        self.e2 = tk.Entry(self)
        self.e1.grid(row=1, column=1)
        self.e2.grid(row=2, column=1)


