import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

# RECTANGLE --------------------------------------------------------------------------------------------------------------------------------------------------------
def plot_rectangle(parent, a, b, coordinate_on, dimension_lines_on):
    if parent.plotted == True:
        parent.canvas._tkcanvas.destroy()
    else:
        parent.logo_image.pack_forget()
        parent.sm.pack(side=tk.LEFT, fill=tk.Y)

    fig = Figure()
    parent.canvas = FigureCanvasTkAgg(fig, master = parent)
    parent.canvas.get_tk_widget().pack()
    parent.canvas._tkcanvas.pack(side="top", fill="both", expand=1)
    parent.plotted = True

    ax = fig.add_subplot(111)
    ax.set_aspect("equal")
    fig.patch.set_facecolor(parent["background"])
    ax.xaxis.set_visible(False)
    ax.yaxis.set_visible(False)
    ax.set_frame_on(False)
    
    x, y = set_dimensions(a, b)
    rect_x = [-x/2, -x/2, x/2, x/2, -x/2]
    rect_y = [y/2, -y/2, -y/2, y/2, y/2]
    
    ax.plot(rect_x, rect_y, 'w', lw=2)
    
    if coordinate_on:
        coordinate_system(x, y, ax, 0)
    if dimension_lines_on:
        dimension_lines(x, y, ax, r"$a$", r"$b$", 0)
        transformed_coordinate_system(x, y, ax, 15)
        transformation_dimensions(x, y, ax)
    parent.canvas.draw()

# ELLIPSE ------------------------------------------------------------------------------------------------------------------------------------------------------------------
def plot_ellipse(parent, a, b, coordinate_on, dimension_lines_on):
    if parent.plotted == True:
        parent.canvas._tkcanvas.destroy()
    else:
        parent.logo_image.pack_forget()
        parent.sm.pack(side=tk.LEFT, fill=tk.Y)

    fig = Figure()
    parent.canvas = FigureCanvasTkAgg(fig, master = parent)
    parent.canvas.get_tk_widget().pack()
    parent.canvas._tkcanvas.pack(side="top", fill="both", expand=1)
    parent.plotted = True

    ax = fig.add_subplot(111)
    ax.set_aspect("equal")
    fig.patch.set_facecolor(parent["background"])
    ax.xaxis.set_visible(False)
    ax.yaxis.set_visible(False)
    ax.set_frame_on(False)

    x, y = set_dimensions(a, b)
    t = np.linspace(0, 2*np.pi, 100)
    ell_x = x/2*np.cos(t)
    ell_y = y/2*np.sin(t)

    ax.plot(ell_x, ell_y, 'w', lw=2)

    if coordinate_on:
        coordinate_system(x, y, ax, 0)
    if dimension_lines_on:
        dimension_lines(x, y, ax, r"$a$", r"$b$", 0)
    parent.canvas.draw()

# # CIRCLE -------------------------------------------------------------------------------------------------------------------------------------------------------------------
def plot_circle(parent, coordinate_on):
    if parent.plotted == True:
        parent.canvas._tkcanvas.destroy()
    else:
        parent.logo_image.pack_forget()
        parent.sm.pack(side=tk.LEFT, fill=tk.Y)

    fig = Figure()
    parent.canvas = FigureCanvasTkAgg(fig, master = parent)
    parent.canvas.get_tk_widget().pack()
    parent.canvas._tkcanvas.pack(side="top", fill="both", expand=1)
    parent.plotted = True

    ax = fig.add_subplot(111)
    ax.set_aspect("equal")
    fig.patch.set_facecolor(parent["background"])
    ax.xaxis.set_visible(False)
    ax.yaxis.set_visible(False)
    ax.set_frame_on(False)

    t = np.linspace(0, 2*np.pi, 100)
    x = y = d = 2
    circ_x = d/2*np.cos(t)
    circ_y = d/2*np.sin(t)

    ax.plot(circ_x, circ_y, 'w', lw=2)

    if coordinate_on:
        coordinate_system(x, y, ax, 0)
    parent.canvas.draw()

# # ISOSCELES TRIANGLE -------------------------------------------------------------------------------------------------------------------------------------------------------
def plot_isosceles_triangle(parent, a, b, coordinate_on, dimension_lines_on):
    if parent.plotted == True:
        parent.canvas._tkcanvas.destroy()
    else:
        parent.logo_image.pack_forget()
        parent.sm.pack(side=tk.LEFT, fill=tk.Y)

    fig = Figure()
    parent.canvas = FigureCanvasTkAgg(fig, master = parent)
    parent.canvas.get_tk_widget().pack()
    parent.canvas._tkcanvas.pack(side="top", fill="both", expand=1)
    parent.plotted = True

    ax = fig.add_subplot(111)
    ax.set_aspect("equal")
    fig.patch.set_facecolor(parent["background"])
    ax.xaxis.set_visible(False)
    ax.yaxis.set_visible(False)
    ax.set_frame_on(False)

    x, y = set_dimensions(a, b)
    tri_x = [-x/2, x/2, 0, -x/2]
    tri_y = [-y/3, -y/3, y/3*2, -y/3]

    ax.plot(tri_x, tri_y, 'w', lw=2)

    if coordinate_on:
        coordinate_system(x, y, ax, y/6)
    if dimension_lines_on:
        dimension_lines(x, y, ax, r"$a$", r"$b$", y/6)
    parent.canvas.draw()

# USEFUL FUNCTIONS --------------------------------------------------------------------------------------------------------------------------------------------------------
def set_dimensions(a, b):
    ab_rate = a/b
    if ab_rate > 2.5:
        x = 3
        y = 1
    elif ab_rate > 1.05 and ab_rate <= 2.5:
        x = 2
        y = 1      
    elif ab_rate < 0.95 and ab_rate >= 0.4:
        x = 1
        y = 2
    elif ab_rate < 0.4:
        x = 1
        y = 3  
    else:
        x = 1
        y = 1
    return x, y

def dimension_lines(x, y, ax, t1, t2, e):
    transparency = 0.5
    hw = 0.03*x*y
    hl = 2*hw
    line1_x = [-x/2-x*y/4, 0]
    line1_y = [y/2+e, y/2+e]
    line2_x = [-x/2-x*y/4, 0]
    line2_y = [-y/2+e, -y/2+e]
    line3_x = [-x/2, -x/2]
    line3_y = [-y/2-x*y/4+e, -2*e]
    line4_x = [x/2, x/2]
    line4_y = [-y/2-x*y/4+e, -2*e]

    ax.arrow(line1_x[0]+x/32, line2_y[0], 0, y, head_width=hw, head_length=hl, fc='grey', ec='grey',length_includes_head = True)
    ax.arrow(line1_x[0]+x/32, line2_y[0], 0, y, head_width=hw, head_length=hl, fc='grey', ec='grey',length_includes_head = True)
    ax.arrow(line1_x[0]+x/32, line1_y[0], 0, -y, head_width=hw, head_length=hl, fc='grey', ec='grey',length_includes_head = True)
    ax.arrow(line3_x[0], line3_y[0]+x/32, x, 0, head_width=hw, head_length=hl, fc='grey', ec='grey',length_includes_head = True)
    ax.arrow(line4_x[0], line3_y[0]+x/32, -x, 0, head_width=hw, head_length=hl, fc='grey', ec='grey',length_includes_head = True)
    ax.plot(line1_x, line1_y, 'grey',zorder=0)
    ax.plot(line2_x, line2_y, 'grey',zorder=0)
    ax.plot(line3_x, line3_y, 'grey',zorder=0)
    ax.plot(line4_x, line4_y, 'grey',zorder=0)

    ax.text(
        0, -y/2-x*y/16*5+e,
        t1,
        horizontalalignment='center',
        verticalalignment='center',
        size='large',
        color = 'grey',
        alpha=transparency)
    ax.text(
        -x/2-x*y/16*5, e,
        t2,
        horizontalalignment='center',
        verticalalignment='center',
        size='large',
        color = 'grey',
        alpha=transparency)

def coordinate_system(x, y, ax, e):
    transparency = 0.5
    hw = 0.03*x*y
    hl = 2*hw
    ax.arrow(
        -x/2-x*y/8, 0, x+x*y/4, 0,
        head_width=hw,
        head_length=hl,
        fc='grey', ec='grey',
        length_includes_head = True,
        alpha=transparency)
    ax.arrow(
        0, -y/2-x*y/8+e, 0, y+x*y/4,
        head_width=hw,
        head_length=hl,
        fc='grey', ec='grey',
        length_includes_head = True,
        alpha=transparency)
    ax.text(
        x/2+x*y/5, x*y/20,
        r"$x$",
        horizontalalignment='center',
        verticalalignment='center',
        size='large',
        color = 'grey',
        alpha=transparency)
    ax.text(
        x*y/20, y/2+x*y/5+e,
        r"$y$",
        horizontalalignment='center',
        verticalalignment='center',
        size='large',
        color = 'grey',
        alpha=transparency)
    # center of gravity
    # ax.text(
    #     -x*y/20, x*y/20,
    #     r"$S$",
    #     horizontalalignment='center',
    #     verticalalignment='center',
    #     size='large',
    #     color = 'grey',
    #     alpha=transparency)

def transformed_coordinate_system(x, y, ax, phi):
    hw = 0.015*x*y
    hl = 2*hw
    phi = phi/180*np.pi
    ar1_x = (-x*3/4)*np.cos(phi)+x/4
    ar1_y = -x*3/4*np.sin(phi)+y/4
    ar1_dx = (x*3/2)*np.cos(phi)
    ar1_dy = x*3/2*np.sin(phi)
    ar2_x = y*3/4*np.sin(phi)+x/4
    ar2_y = -y*3/4*np.cos(phi)+y/4
    ar2_dx = (-y*3/2)*np.sin(phi)
    ar2_dy = y*3/2*np.cos(phi)

    ax.arrow(ar1_x, ar1_y, ar1_dx, ar1_dy,
                         head_width=hw, head_length=hl, fc='w', ec='w',length_includes_head = True)
    ax.arrow(ar2_x, ar2_y, ar2_dx, ar2_dy,
                         head_width=hw, head_length=hl, fc='w', ec='w',length_includes_head = True)
    ax.text(ar1_x+ar1_dx+x/20, ar1_y+ar1_dy+y/20,  r"$\xi$", horizontalalignment='center', color = 'w',
                        verticalalignment='center', size='large')
    ax.text(ar2_x+ar2_dx+x/20, ar2_y+ar2_dy+y/20, r"$\eta$", horizontalalignment='center', color = 'w',
                        verticalalignment='center', size='large')
def transformation_dimensions(x, y, ax):
    transparency = 0.7
    hw = 0.015*x*y
    hl = 2*hw
    y_disp_x = [x/4, x]
    y_disp_y = [y/4, y/4]
    ax.plot(y_disp_x, y_disp_y, 'grey', lw=1, zorder=5, alpha=transparency)
    ax.arrow(x/2+x/8, 0, 0, y/4,
                         head_width=hw, head_length=hl, fc='grey', ec='grey',length_includes_head = True, alpha=transparency)
    ax.arrow(x/2+x/8, y/4, 0, -y/4,
                         head_width=hw, head_length=hl, fc='grey', ec='grey',length_includes_head = True, alpha=transparency)
    ax.text(x/2+x/6, y/8, r"$y$", horizontalalignment='center', color = 'grey',
                        verticalalignment='center', alpha=transparency)
    x_disp_x = [x/4, x/4]
    x_disp_y = [y/4, -y/4]
    ax.plot(x_disp_x, x_disp_y, 'grey', lw=1, zorder=5, alpha=transparency)
    ax.arrow(0, -y/8, x/4, 0,
                        head_width=hw, head_length=hl, fc='grey', ec='grey',length_includes_head = True, alpha=transparency)
    ax.arrow(x/4, -y/8, -x/4, 0,
                        head_width=hw, head_length=hl, fc='grey', ec='grey',length_includes_head = True, alpha=transparency)
    ax.text(x/8, -y/12, r"$x$", horizontalalignment='center', color = 'grey',
                    verticalalignment='center', alpha=transparency)
    style = "Simple, tail_width=0.2, head_width=4, head_length=8"
    kw = dict(arrowstyle=style, color="grey")
    a3 = patches.FancyArrowPatch((x/2+x/3, y/4), (x/2+x/4+x/20, y/4+x*3/20),
                            connectionstyle="arc3,rad=.2", **kw, alpha=transparency)
    ax.add_patch(a3)
    ax.text(x/2+x/4+x/8, y/4+y/12, r"$\varphi$", horizontalalignment='center', color = 'grey',
                    verticalalignment='center', alpha=transparency)