import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

def plot_rectangle(parent,x,y):
        if parent.plotted == True:
            parent.canvas._tkcanvas.destroy()
        else:
            parent.logo_image.pack_forget()
            parent.sm.pack(side=tk.LEFT, fill=tk.Y)


        fig = Figure()

        parent.canvas = FigureCanvasTkAgg(fig, master=parent)
        parent.canvas.get_tk_widget().pack()
        parent.canvas._tkcanvas.pack(side="top", fill="both", expand=1)
        parent.plotted = True
        # self.canvas = FigureCanvasTkAgg(self.fig)
        # # self.canvas.show()
        # self.canvas.get_tk_widget().pack(side='right', fill = 'both', expand=1)

        ax = fig.add_subplot(111)
        ax.set_aspect("equal")
        fig.patch.set_facecolor(parent["background"])
        ax.xaxis.set_visible(False)
        ax.yaxis.set_visible(False)
        ax.set_frame_on(False)
        # self.arrow1 = self.ax.arrow(0, 0, 0, 0, head_width=0, head_length=0, fc='grey', ec='grey',length_includes_head = True, lw = 0)
        
        N = 101
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
        ax.arrow(line1_x[0]+x/32, line2_y[0], 0, y, head_width=0.03*x, head_length=0.06*x, fc='grey', ec='grey',length_includes_head = True)
        ax.arrow(line1_x[0]+x/32, line2_y[0], 0, y, head_width=0.03*x, head_length=0.06*x, fc='grey', ec='grey',length_includes_head = True)
        ax.arrow(line1_x[0]+x/32, line1_y[0], 0, -y, head_width=0.03*x, head_length=0.06*x, fc='grey', ec='grey',length_includes_head = True)
        ax.arrow(line3_x[0], line3_y[0]+x/32, x, 0, head_width=0.03*x, head_length=0.06*x, fc='grey', ec='grey',length_includes_head = True)
        ax.arrow(line4_x[0], line3_y[0]+x/32, -x, 0, head_width=0.03*x, head_length=0.06*x, fc='grey', ec='grey',length_includes_head = True)
        ax.plot(rect_x, rect_y, 'w', lw=2)
        ax.plot(line1_x, line1_y, 'grey',zorder=0)
        ax.plot(line2_x, line2_y, 'grey',zorder=0)
        ax.plot(line3_x, line3_y, 'grey',zorder=0)
        ax.plot(line4_x, line4_y, 'grey',zorder=0)
        parent.canvas.draw()

        
        #seting up canvas
        # self.canvas = tk.Canvas(self, bg="#2A3C4D", highlightthickness=0)
        # self.canvas.pack(fill="both")

