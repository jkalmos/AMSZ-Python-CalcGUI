from __future__ import unicode_literals
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.patches as patches
import matplotlib.pyplot as plt
import numpy as np
import CrossSection as cs



class window(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Próba GUI")
        self.geometry("1000x600")
        self.configure(bg="#2A3C4D")
        self.minsize(width=200, height=200)

        self.canvas = None

        self.sm = SideMenu(self)
        self.sm.pack(side=tk.LEFT, fill=tk.Y)
        self.plotted = tk.BooleanVar(False)
    


    def plot(self):
        


        if self.plotted == True:
            self.canvas._tkcanvas.destroy()


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
        
        ## Rectangle
        x = int(self.sm.e1.get())
        y = int(self.sm.e2.get())
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


        ## Circle
        # N = 100
        # r = 1
        # phi = np.linspace(0,2*np.pi,N)
        # circ_x = r*np.cos(phi)
        # circ_y = r*np.sin(phi)

        # self.ax.plot(circ_x, circ_y, 'grey')

        # ## Triangle
        # alpha = 50/180*np.pi
        # beta = 70/180*np.pi
        # gamma = 60/180*np.pi
        # a = 10
        # b = 

        ## Main Coordinate system
        self.ax.arrow(-x*3/4, 0, 3/2*x, 0, head_width=0.03*x, head_length=0.06*x, fc='grey',
                         ec='grey',length_includes_head = True, alpha=0.5)
        self.ax.arrow(0, -y*3/4, 0, 2*y*3/4, head_width=0.03*x, head_length=0.06*x, fc='grey',
                         ec='grey',length_includes_head = True, alpha=0.5)
        self.ax.text(x*3/4+x/20, y/20,  r"$x$", horizontalalignment='center', color = 'grey',
                        verticalalignment='center', size='large', alpha=0.5)
        self.ax.text(x/20, y*3/4+y/20, r"$y$", horizontalalignment='center', color = 'grey',
                        verticalalignment='center', size='large', alpha=0.5)

        ## Second Coordinate system
        trans = 0.7
        ar1_x = (-x*3/4)*0.9659+x/4
        ar1_y = -x*3/4*0.2588+y/4
        ar1_dx = (x*3/2)*0.9659
        ar1_dy = x*3/2*0.2588
        ar2_x = y*3/4*0.2588+x/4
        ar2_y = -y*3/4*0.9659+y/4
        ar2_dx = (-y*3/2)*0.2588
        ar2_dy = y*3/2*0.9659
        self.ax.arrow(ar1_x, ar1_y, ar1_dx, ar1_dy,
                         head_width=0.03*x, head_length=0.06*x, fc='w', ec='w',length_includes_head = True)
        self.ax.arrow(ar2_x, ar2_y, ar2_dx, ar2_dy,
                         head_width=0.03*x, head_length=0.06*x, fc='w', ec='w',length_includes_head = True)
        self.ax.text(ar1_x+ar1_dx+x/20, ar1_y+ar1_dy+y/20,  r"$\xi$", horizontalalignment='center', color = 'w',
                        verticalalignment='center', size='large')
        self.ax.text(ar2_x+ar2_dx+x/20, ar2_y+ar2_dy+y/20, r"$\eta$", horizontalalignment='center', color = 'w',
                        verticalalignment='center', size='large')
        ## Second cordinate system displacement
        y_disp_x = [x/4, x]
        y_disp_y = [y/4, y/4]
        self.ax.plot(y_disp_x, y_disp_y, 'grey', lw=1, zorder=5, alpha=trans)
        self.ax.arrow(x/2+x/8, 0, 0, y/4,
                         head_width=0.03*x, head_length=0.06*x, fc='grey', ec='grey',length_includes_head = True, alpha=trans)
        self.ax.arrow(x/2+x/8, y/4, 0, -y/4,
                         head_width=0.03*x, head_length=0.06*x, fc='grey', ec='grey',length_includes_head = True, alpha=trans)
        self.ax.text(x/2+x/6, y/8, r"$y$", horizontalalignment='center', color = 'grey',
                        verticalalignment='center', alpha=trans)
        x_disp_x = [x/4, x/4]
        x_disp_y = [y/4, -y/4]
        self.ax.plot(x_disp_x, x_disp_y, 'grey', lw=1, zorder=5, alpha=trans)
        self.ax.arrow(0, -y/8, x/4, 0,
                         head_width=0.03*x, head_length=0.06*x, fc='grey', ec='grey',length_includes_head = True, alpha=trans)
        self.ax.arrow(x/4, -y/8, -x/4, 0,
                         head_width=0.03*x, head_length=0.06*x, fc='grey', ec='grey',length_includes_head = True, alpha=trans)
        self.ax.text(x/8, -y/12, r"$x$", horizontalalignment='center', color = 'grey',
                        verticalalignment='center', alpha=trans)
        style = "Simple, tail_width=0.2, head_width=4, head_length=8"
        kw = dict(arrowstyle=style, color="grey")
        a3 = patches.FancyArrowPatch((x/2+x/3, y/4), (x/2+x/4+x/20, y/4+x*3/20),
                             connectionstyle="arc3,rad=.2", **kw, alpha=trans)
        self.ax.add_patch(a3)
        self.ax.text(x/2+x/4+x/8, y/4+y/12, r"$\varphi$", horizontalalignment='center', color = 'grey',
                        verticalalignment='center', alpha=trans)

        # if abs(alpha-np.pi/2) < 0.001:
        #     I1_x = [0, 0]
        # I1_x = [-1.2*x/2, 1.2*x/2]
        # I1_y = [np.tan(self.alpha)]

        if x>y:
            I1_x = [0, 0]
            I1_y = [-1.5*y/2, 1.5*y/2]
        else:
            I1_x = [-1.5*x/2, 1.5*x/2]
            I1_y = [0, 0]

        # print(self.alpha)
        # I_1
        # self.ax.arrow(I1_x[0], I1_y[0], I1_x[1]-I1_x[0], I1_y[1]-I1_y[0], head_width=0.03*x, head_length=0.06*x, fc='red', ec='red',length_includes_head = True,zorder=10)
        # self.ax.text(I1_x[1]+x/20, I1_y[1]+y/20, 'Ｉ𝙰₁', horizontalalignment='center',
        #                 verticalalignment='center', color = 'red')

        # #### Méret nyilak
        # self.ax.arrow(line1_x[0]+x/32, line1_y[0], 0, -y, head_width=0.03*x, head_length=0.06*x, fc='grey', ec='grey',length_includes_head = True)
        # self.ax.arrow(line1_x[0]+x/32, line2_y[0], 0, y, head_width=0.03*x, head_length=0.06*x, fc='grey', ec='grey',length_includes_head = True)
        # self.ax.arrow(line3_x[0], line3_y[0]+x/32, x, 0, head_width=0.03*x, head_length=0.06*x, fc='grey', ec='grey',length_includes_head = True)
        # self.ax.arrow(line4_x[0], line3_y[0]+x/32, -x, 0, head_width=0.03*x, head_length=0.06*x, fc='grey', ec='grey',length_includes_head = True)
        # self.ax.plot(line1_x, line1_y, 'grey',zorder=0)
        # self.ax.plot(line2_x, line2_y, 'grey',zorder=0)
        # self.ax.plot(line3_x, line3_y, 'grey',zorder=0)
        # self.ax.plot(line4_x, line4_y, 'grey',zorder=0)

        ## Négyzet
        self.ax.plot(rect_x, rect_y, 'w', lw=2, zorder=5)
        self.canvas.draw()

        
        #seting up canvas
        # self.canvas = tk.Canvas(self, bg="#2A3C4D", highlightthickness=0)
        # self.canvas.pack(fill="both")


    def doNothing(self):
        print("Ez a funkció jelenleg nem elérhető...")
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

    def szamol(self):
        try:
            w = int(self.sm.e1.get())
            h = int(self.sm.e2.get())
            self.alpha = (cs.Rectangle(w,h))[6]
            
        except:
            print("Hiba!")

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
        super().__init__(root, bg='#314457')
        self.root = root
        title = tk.Label(self, text="This is a side menu", bg=self["background"], fg='white')
        title.grid(row=0)
        lbl = tk.Label(self, width = 14, bg=self["background"])
        lbl.grid(row=0)
        tk.Label(self, text="Width", bg=self["background"], fg='white').grid(row=1)
        tk.Label(self, text="Heigth", bg=self["background"], fg='white').grid(row=3)

        calc = tk.Button(self, text="Calculate", command=lambda:[self.root.szamol(), self.root.plot()])
        calc.grid(row=5, pady=5)

        self.e1 = tk.Entry(self, width = 10, bg="#475C6F", fg='white')
        self.e2 = tk.Entry(self, width = 10, bg="#475C6F", fg='white')
        self.e1.grid(row=2)
        self.e2.grid(row=4)


root = window()
root.mainloop()