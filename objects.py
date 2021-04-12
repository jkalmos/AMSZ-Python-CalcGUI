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
        self.toolbar = Toolbar(self)
        self.toolbar.pack(side=tk.TOP, fill=tk.X)

        #seting up side menu

        self.sm = SideMenu(self)
        self.sm.pack(side=tk.LEFT, fill=tk.Y)
        #seting up canvas
        self.canvas = tk.Canvas(self, width=800, height = 500, bg="white")
        self.canvas.pack()

    def doNothing(self):
        print("A buuton has been pushed")
    def add_circle(self):
        self.canvas.create_oval(25,25,50,50,fill="blue")
# ************ Toolbar ************
class Toolbar(tk.Frame):
    def __init__(self, root):
        super().__init__(root, bg='#F5F5DC')
        self.root=root
        tegla = tk.Button(self, text="Téglalap", command=self.root.doNothing)
        tegla.pack(side=tk.LEFT, padx=2, pady=2)
        kor = tk.Button(self, text="Kör", command=self.root.add_circle)
        kor.pack(side=tk.LEFT, padx=2, pady=2)
        haromszog = tk.Button(self, text="Háromszög", command=self.root.doNothing)
        haromszog.pack(side=tk.LEFT, padx=2, pady=2)

        calc = tk.Button(self, text="Calculate", command=self.root.doNothing)
        calc.pack(side=tk.RIGHT, padx=2, pady=2)

class SideMenu(tk.Frame):
    def __init__(self, root):
        super().__init__(root, bg='#707070')
        self.root=root
        title = tk.Label(self, text="This is a side menu")
        title.grid(row=0, columnspan=2)
        tk.Label(self, text="First Name").grid(row=1)
        tk.Label(self, text="Last Name").grid(row=2)
        e1 = tk.Entry(self)
        e2 = tk.Entry(self)
        e1.grid(row=1, column=1)
        e2.grid(row=2, column=1)

# *********** Status bar ********
#status = tk.Label(root, text="this is a status bar", bd=1, relief=tk.SUNKEN, anchor=tk.W)
#status.pack(side=tk.BOTTOM, fill=tk.X)
# ************ Menu ************
"""
menu = tk.Menu(root, bg="gray")
root.config(menu=menu)

subMenu = tk.Menu(menu)
menu.add_cascade(label="File", menu=subMenu)
subMenu.add_command(label="New project", command=doNothing)
subMenu.add_command(label="New ...", command=doNothing)
subMenu.add_separator()
subMenu.add_command(label="Exit", command=doNothing)

editMenu = tk.Menu(menu)
menu.add_cascade(label="Edit", menu=editMenu)
editMenu.add_command(label="revwerv",command=doNothing)
"""
