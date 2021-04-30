import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageTk
import CrossSection as CS

class window(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Próba GUI")
        self.geometry("1000x600")
        self.configure(bg="#2A3C4D")
        self.minsize(width=200, height=200)

        self.canvas = None
        #Side Menu
        self.sm = SideMenu(self)
        self.sm.pack(side=tk.LEFT, fill=tk.Y)
        self.bind('<Return>', self.szamol)
        self.plotted = tk.BooleanVar(False)

        #Basic logo
        self.logo_img = Image.open("amsz_logo_full.png")
        self.logo_img = ImageTk.PhotoImage(self.logo_img)
        self.logo_image = tk.Label(self,image=self.logo_img,bg="#2A3C4D")
        self.logo_image.image=self.logo_img
        self.logo_image.pack(side=tk.LEFT)
        #menüszerkezet
        menubar = tk.Menu(self)#, background='gray', foreground='black',activebackground='#004c99', activeforeground='white')
        self.config(menu=menubar)        
        keresztmetszet = tk.Menu(self, menubar, tearoff=0)
        menubar.add_cascade(label="Keresztmetszet", menu=keresztmetszet)
        keresztmetszet.add_command(label="Téglalap", command = self.plot)
        keresztmetszet.add_command(label="Kör", command = self.plot)
        menubar.add_command(label="Kilépés", command=self.destroy)

    def plot(self):
        if self.plotted == True:
            self.canvas._tkcanvas.destroy()
        else:
            self.logo_image.pack_forget()


        self.fig = Figure()

        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.get_tk_widget().pack()
        self.canvas._tkcanvas.pack(side="top", fill="both", expand=1)
        self.plotted = True
        # self.canvas = FigureCanvasTkAgg(self.fig)
        # # self.canvas.show()
        # self.canvas.get_tk_widget().pack(side='right', fill = 'both', expand=1)

        self.ax = self.fig.add_subplot(111)
        self.ax.set_aspect("equal")
        self.fig.patch.set_facecolor(self["background"])
        self.ax.xaxis.set_visible(False)
        self.ax.yaxis.set_visible(False)
        self.ax.set_frame_on(False)
        # self.arrow1 = self.ax.arrow(0, 0, 0, 0, head_width=0, head_length=0, fc='grey', ec='grey',length_includes_head = True, lw = 0)
        
        N = 101
        x = float(self.sm.e1.get().replace(',','.'))
        y = float(self.sm.e2.get().replace(',','.'))
        rect_x = [-x/2, -x/2, x/2, x/2, -x/2]
        rect_y = [y/2, -y/2, -y/2, y/2, y/2]
        line1_x = [rect_x[0]+rect_x[0]/4, rect_x[0]]
        line1_y = [rect_y[0], rect_y[0]]
        line2_x = [rect_x[0]+rect_x[0]/4, rect_x[0]]
        line2_y = [rect_y[1], rect_y[1]]
        line3_x = [rect_x[1], rect_x[1]]
        line3_y = [rect_y[1]+rect_x[1]/4, rect_y[1]]
        line4_x = [rect_x[2], rect_x[2]]
        line4_y = [rect_y[2]+rect_x[1]/4, rect_y[2]]

        

        # self.canvas._tkcanvas.destroy()
        self.ax.arrow(line1_x[0]+x/32, line1_y[0], 0, -y, head_width=0.03*x, head_length=0.06*x, fc='grey', ec='grey',length_includes_head = True)
        self.ax.arrow(line1_x[0]+x/32, line2_y[0], 0, y, head_width=0.03*x, head_length=0.06*x, fc='grey', ec='grey',length_includes_head = True)
        self.ax.arrow(line3_x[0], line3_y[0]+x/32, x, 0, head_width=0.03*x, head_length=0.06*x, fc='grey', ec='grey',length_includes_head = True)
        self.ax.arrow(line4_x[0], line3_y[0]+x/32, -x, 0, head_width=0.03*x, head_length=0.06*x, fc='grey', ec='grey',length_includes_head = True)
        self.ax.plot(rect_x, rect_y, 'w', lw=2)
        self.ax.plot(line1_x, line1_y, 'grey',zorder=0)
        self.ax.plot(line2_x, line2_y, 'grey',zorder=0)
        self.ax.plot(line3_x, line3_y, 'grey',zorder=0)
        self.ax.plot(line4_x, line4_y, 'grey',zorder=0)
        self.canvas.draw()

        
        #seting up canvas
        # self.canvas = tk.Canvas(self, bg="#2A3C4D", highlightthickness=0)
        # self.canvas.pack(fill="both")

    def szamol(self, event=None):
        try:
            a = float(self.sm.e1.get().replace(',','.'))
            b = float(self.sm.e2.get().replace(',','.'))
            self.plot()
            self.values = CS.Rectangle(a,b)

            self.sm.eredmeny1.config(text="I_x = " + str(round(self.values["Ix"], 4)))
            self.sm.eredmeny2.config(text="I_y = " + str(round(self.values["Iy"], 4)))

        except:
            print("Hiba!")

    def doNothing(self):
        print("Ez a funkció jelenleg nem elérhető...")
    """
    def add_circle(self):
        self.canvas.delete('all')
        reduced_size = min(self.canvas.winfo_width(),self.canvas.winfo_height())*0.7/2
        c_x = self.canvas.winfo_width()/2
        c_y = self.canvas.winfo_height()/2
        self.canvas.create_oval(c_x-reduced_size,c_y-reduced_size, c_x+reduced_size,c_y+reduced_size, fill="#2A3C4D")
    def add_retangle(self):
        self.canvas.delete('all')
        reduced_size = min(self.canvas.winfo_width(),self.canvas.winfo_height())*0.7/2
        c_x = self.canvas.winfo_width()/2
        c_y = self.canvas.winfo_height()/2
        self.canvas.create_rectangle(c_x-reduced_size,c_y-reduced_size, c_x+reduced_size,c_y+reduced_size, fill="#2A3C4D")
    """
    

# ************ Toolbar ************
# class Eszkoztar(tk.Frame):
#     def __init__(self, root):
#         super().__init__(root, bg='#F5F5DC')
#         self.root=root
#         tegla = tk.Button(self, text="teglalap",compound="top", command=self.root.add_retangle)
#         tegla.pack(side=tk.LEFT, padx=2, pady=2)
#         kor = tk.Button(self, text="Kör", command=self.root.add_circle)
#         kor.pack(side=tk.LEFT, padx=2, pady=2)
#         haromszog = tk.Button(self, text="Háromszög", command=self.root.doNothing)
#         haromszog.pack(side=tk.LEFT, padx=2, pady=2)

#         calc = tk.Button(self, text="Calculate", command=self.root.szamol)
#         calc.pack(side=tk.RIGHT, padx=2, pady=2)

#*************** Side Menu **************
class SideMenu(tk.Frame):
    def __init__(self, root):
        super().__init__(root,width=400, bg='#314457')
        self.root = root
        title = tk.Label(self, text="This is a side menu", bg=self["background"], fg='white')
        title.grid(row=0)
        lbl = tk.Label(self, width = 20, bg=self["background"])
        lbl.grid(row=0)
        tk.Label(self, text="Width", bg=self["background"], fg='white').grid(row=1)
        tk.Label(self, text="Heigth", bg=self["background"], fg='white').grid(row=3)

        calc = tk.Button(self, text="Calculate", command=lambda: self.root.szamol())
        calc.grid(row=5, pady=5)

        self.e1 = tk.Entry(self, width = 10, bg="#475C6F", fg='white')
        self.e2 = tk.Entry(self, width = 10, bg="#475C6F", fg='white')
        self.e1.grid(row=2)
        self.e2.grid(row=4)

        self.eredmeny1 = tk.Label(self, text="", bg=self["background"], fg='white')
        self.eredmeny1.grid(row=6)
        self.eredmeny2 = tk.Label(self, text="", bg=self["background"], fg='white')
        self.eredmeny2.grid(row=7)

if __name__ == "__main__":
    root = window()
    root.mainloop()