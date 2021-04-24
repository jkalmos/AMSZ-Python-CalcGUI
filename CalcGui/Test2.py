from matplotlib.figure import Figure
from tkinter import *
import os

import xlrd
from xlrd import open_workbook
import pandas as pd
import tkinter as tk
from tkinter import filedialog
from tkinter import ALL

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import matplotlib.tri as mtri
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg #new
import numpy as np #new


class mclass:
    def __init__(self, window):
        self.window = window
        self.canvas = None
        self.button = Button(window, text="Plot Surface", command=self.plot_IBL)
        self.clear_button = Button(window, text="Clear Space", command=self.clear_space)
        self.button.pack(side="left")
        self.clear_button.pack(side="left")

    def clear_space(self): #new
        self.canvas._tkcanvas.destroy()
        #global main, root
        #main.destroy()
        #main = Frame(root)
        #main.pack()

    def plot_IBL(self):
        fig = Figure(figsize=(4, 4))
        self.canvas = FigureCanvasTkAgg(fig, master=self.window)
        self.canvas.get_tk_widget().pack()
        self.canvas._tkcanvas.pack(side="top", fill="both", expand=1)
        base = "dummy text" #new
        a = fig.add_subplot(111, projection="3d")
        a.set_title(base, fontsize=16)
        a.set_ylabel("Y", fontsize=14)
        a.set_xlabel("X", fontsize=14)
        a.set_zlabel("Z", fontsize=14)
        
        #new: draw something
        # https://matplotlib.org/2.0.0/examples/mplot3d/trisurf3d_demo.html
        n_radii = 8
        n_angles = 36

        # Make radii and angles spaces (radius r=0 omitted to eliminate duplication).
        radii = np.linspace(0.125, 1.0, n_radii)
        angles = np.linspace(0, 2*np.pi, n_angles, endpoint=False)

        # Repeat all angles for each radius.
        angles = np.repeat(angles[..., np.newaxis], n_radii, axis=1)

        # Convert polar (radii, angles) coords to cartesian (x, y) coords.
        # (0, 0) is manually added at this stage,  so there will be no duplicate
        # points in the (x, y) plane.
        x = np.append(0, (radii*np.cos(angles)).flatten())
        y = np.append(0, (radii*np.sin(angles)).flatten())

        # Compute z to make the pringle surface.
        z = np.sin(-x*y)
        a.plot_trisurf(x, y, z)
        
        '''
        a.plot_trisurf(x_prime, y_prime, z_prime, triangles=tri.triangles)
        a.plot_trisurf(x_negprime, y_prime, z_prime, triangles=tri.triangles)
        a.plot_trisurf(x_negprime, y_negprime, z_prime, triangles=tri.triangles)
        '''
        self.canvas.draw()

root = Tk() #new
my_mclass = mclass(root) #new
root.mainloop() #new