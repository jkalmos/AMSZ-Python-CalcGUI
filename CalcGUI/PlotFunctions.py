import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.patches as patches
import numpy as np

# PLOT SHAPE --------------------------------------------------------------------------------------------------------------------------------------------------------
def plot(parent, shape, coordinate_on, dimension_lines_on, transformed_coordinate_on, thickness_on, colors):
    if parent.plotted == True:
        parent.canvas._tkcanvas.destroy()

    a = 1.6
    b = 0.8
    d = 0.8
    circ = False

    fig = Figure()
    parent.canvas = FigureCanvasTkAgg(fig, master = parent)
    parent.canvas.get_tk_widget().pack()
    parent.canvas._tkcanvas.pack(side="top", fill="both", expand=1,padx = (10,20), pady = 20)
    parent.plotted = True

    parent.ax = fig.add_subplot(111)
    parent.ax.set_aspect("equal")
    fig.patch.set_facecolor(colors["secondary_color"])
    parent.ax.xaxis.set_visible(False)
    parent.ax.yaxis.set_visible(False)
    parent.ax.set_frame_on(False)

    if shape == "Rectangle":
        x, y = set_dimensions(a, b)
        rect_x = [-x/2, -x/2, x/2, x/2, -x/2]
        rect_y = [y/2, -y/2, -y/2, y/2, y/2]

        rect_x_th = [-x/2+0.1, -x/2+0.1, x/2-0.1, x/2-0.1, -x/2+0.1]
        rect_y_th = [y/2-0.1, -y/2+0.1, -y/2+0.1, y/2-0.1, y/2-0.1]
        
        parent.ax.plot(rect_x, rect_y, colors["draw_main"], lw=2)
        parent.ax.fill(rect_x,rect_y,color=colors["draw_main"],alpha=0.9) 
        if thickness_on == True:
            parent.ax.plot(rect_x_th, rect_y_th, colors["draw_main"], lw=2)
            parent.ax.fill(rect_x_th,rect_y_th,color=colors["secondary_color"])
        coordinate_displacement = 0
    elif shape == "Ellipse":
        x, y = set_dimensions(a, b)
        t = np.linspace(0, 2*np.pi, 100)
        ell_x = x/2*np.cos(t)
        ell_y = y/2*np.sin(t)

        ell_x_th = (x/2-0.1)*np.cos(t)
        ell_y_th = (y/2-0.1)*np.sin(t)

        parent.ax.plot(ell_x, ell_y, colors["draw_main"], lw=2)
        parent.ax.fill(ell_x,ell_y,color=colors["draw_main"],alpha=0.9) 
        if thickness_on == True:
            parent.ax.plot(ell_x_th, ell_y_th, colors["draw_main"], lw=2)
            parent.ax.fill(ell_x_th,ell_y_th,color=colors["secondary_color"])
        coordinate_displacement = 0
    elif shape == "Circle":
        t = np.linspace(0, 2*np.pi, 100)
        x = y = d = 2
        circ_x = d/2*np.cos(t)
        circ_y = d/2*np.sin(t)

        circ_x_th = (d/2-0.1)*np.cos(t)
        circ_y_th = (d/2-0.1)*np.sin(t)

        circ = True

        parent.ax.plot(circ_x, circ_y, colors["draw_main"], lw=2)
        parent.ax.fill(circ_x,circ_y,color=colors["draw_main"],alpha=0.9) 
        if thickness_on == True:
            parent.ax.plot(circ_x_th, circ_y_th, colors["draw_main"], lw=2)
            parent.ax.fill(circ_x_th,circ_y_th,color=colors["secondary_color"])
        coordinate_displacement = 0
    elif shape == "Isosceles_triangle":
        x, y = set_dimensions(a, b)
        tri_x = [-x/2, x/2, 0, -x/2]
        tri_y = [-y/3, -y/3, y/3*2, -y/3]

        tri_x_th = [-x/2+0.175, x/2-0.175, 0, -x/2+0.175]
        tri_y_th = [-y/3+0.075, -y/3+0.075, y/3*2-0.1, -y/3+0.075]

        parent.ax.plot(tri_x, tri_y, colors["draw_main"], lw=2)
        parent.ax.fill(tri_x,tri_y,color=colors["draw_main"],alpha=0.9) 
        if thickness_on == True:
            parent.ax.plot(tri_x_th, tri_y_th, colors["draw_main"], lw=2)
            parent.ax.fill(tri_x_th,tri_y_th,color=colors["secondary_color"])
        coordinate_displacement = y/6
    elif shape == None:
        None

    if coordinate_on == True:
        coordinate_system(x, y, parent.ax, coordinate_displacement, colors)
    if dimension_lines_on == True:
        dimension_lines(x, y, parent.ax, r"$a$", r"$b$", coordinate_displacement, colors, circ)
    if transformed_coordinate_on == True:
        transformed_coordinate_system(x, y, parent.ax, 15, colors)
        transformation_dimensions(x, y, parent.ax, colors)
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

def dimension_lines(x, y, ax, t1, t2, e, colors, circ = False):
    transparency = 1
    color = colors['draw_tertiary']
    hw = 0.015*x*y
    hl = 2*hw
    if circ == False:
        line1_x = [-x/2-x*y/4, 0]
        line1_y = [y/2+e, y/2+e]
        line2_x = [-x/2-x*y/4, 0]
        line2_y = [-y/2+e, -y/2+e]
        line3_x = [-x/2, -x/2]
        line3_y = [-y/2-x*y/4+e, -2*e]
        line4_x = [x/2, x/2]
        line4_y = [-y/2-x*y/4+e, -2*e]

        ax.arrow(line1_x[0]+x/32, line2_y[0], 0, y, head_width=hw, head_length=hl, fc=color, ec=color,length_includes_head = True)
        ax.arrow(line1_x[0]+x/32, line2_y[0], 0, y, head_width=hw, head_length=hl, fc=color, ec=color,length_includes_head = True)
        ax.arrow(line1_x[0]+x/32, line1_y[0], 0, -y, head_width=hw, head_length=hl, fc=color, ec=color,length_includes_head = True)
        ax.arrow(line3_x[0], line3_y[0]+x/32, x, 0, head_width=hw, head_length=hl, fc=color, ec=color,length_includes_head = True)
        ax.arrow(line4_x[0], line3_y[0]+x/32, -x, 0, head_width=hw, head_length=hl, fc=color, ec=color,length_includes_head = True)
        ax.plot(line1_x, line1_y, color,zorder=0)
        ax.plot(line2_x, line2_y, color,zorder=0)
        ax.plot(line3_x, line3_y, color,zorder=0)
        ax.plot(line4_x, line4_y, color,zorder=0)

        ax.text(
            0, -y/2-x*y/16*5+e,
            t1,
            horizontalalignment='center',
            verticalalignment='center',
            size='large',
            color = color,
            alpha=transparency)
        ax.text(
            -x/2-x*y/16*5, e,
            t2,
            horizontalalignment='center',
            verticalalignment='center',
            size='large',
            color = color,
            alpha=transparency)
    elif circ == True:
        line1_x = [-1, 1]
        line1_y = [1.732, -1.732]

        ax.plot(line1_x, line1_y, color,zorder=3)
        ax.arrow(line1_x[0], line1_y[0], 0.5, -0.866, head_width=hw, head_length=hl, fc=color, ec=color,length_includes_head = True)
        ax.arrow(line1_x[1], line1_y[1], -0.5, 0.866, head_width=hw, head_length=hl, fc=color, ec=color,length_includes_head = True)

        ax.text(
            1.1, -1.4,
            "Ød",
            horizontalalignment='center',
            verticalalignment='center',
            size='large',
            color = color,
            alpha=transparency)
def coordinate_system(x, y, ax, e, colors):
    color = colors['draw_secondary']
    transparency = 1
    hw = 0.015*x*y
    hl = 2*hw
    ax.arrow(
        -x/2-x*y/8, 0, x+x*y/3, 0,
        head_width=hw,
        head_length=hl,
        fc=color, ec=color,
        length_includes_head = True,
        alpha=transparency,
        zorder=3)
    ax.arrow(
        0, -y/2-x*y/8+e, 0, y+x*y/3,
        head_width=hw,
        head_length=hl,
        fc=color, ec=color,
        length_includes_head = True,
        alpha=transparency,
        zorder=3)
    ax.text(
        x/2+x*y/5, -x*y/20,
        r"$x$",
        horizontalalignment='center',
        verticalalignment='center',
        size='large',
        color = color,
        alpha=transparency)
    ax.text(
        -x*y/20, y/2+x*y/5+e,
        r"$y$",
        horizontalalignment='center',
        verticalalignment='center',
        size='large',
        color = color,
        alpha=transparency)

def transformed_coordinate_system(x, y, ax, phi, colors):
    color = colors['draw_tertiary']
    hw = 0.015*x*y
    hl = 2*hw
    phi = phi/180*np.pi
    ar1_x = (-x*3/4)*np.cos(phi)+x/5
    ar1_y = -x*3/4*np.sin(phi)+y/5
    ar1_dx = (x*3/2)*np.cos(phi)
    ar1_dy = x*3/2*np.sin(phi)
    ar2_x = y*3/4*np.sin(phi)+x/5
    ar2_y = -y*3/4*np.cos(phi)+y/5
    ar2_dx = (-y*3/2)*np.sin(phi)
    ar2_dy = y*3/2*np.cos(phi)

    ax.arrow(ar1_x, ar1_y, ar1_dx, ar1_dy,
                         head_width=hw, head_length=hl, fc=color, ec=color,length_includes_head = True, zorder=3)
    ax.arrow(ar2_x, ar2_y, ar2_dx, ar2_dy,
                         head_width=hw, head_length=hl, fc=color, ec=color,length_includes_head = True, zorder=3)
    ax.text(ar1_x+ar1_dx+x/20, ar1_y+ar1_dy+y/20,  r"$\xi$", horizontalalignment='center', color = color,
                        verticalalignment='center', size='large')
    ax.text(ar2_x+ar2_dx+x/20, ar2_y+ar2_dy+y/20, r"$\eta$", horizontalalignment='center', color = color,
                        verticalalignment='center', size='large')

def transformation_dimensions(x, y, ax, colors):
    color = colors['draw_tertiary']
    transparency = 1 #0.7
    hw = 0.015*x*y
    hl = 2*hw
    y_disp_x = [x/5, x]
    y_disp_y = [y/5, y/5]
    ax.plot(y_disp_x, y_disp_y, color, lw=1, zorder=5, alpha=transparency)
    ax.arrow(x/2+x/8, 0, 0, y/5,
                         head_width=hw, head_length=hl, fc=color, ec=color,length_includes_head = True, alpha=transparency)
    ax.arrow(x/2+x/8, y/5, 0, -y/5,
                         head_width=hw, head_length=hl, fc=color, ec=color,length_includes_head = True, alpha=transparency)
    ax.text(x/2+x/6, y/8, r"$y$", horizontalalignment='center', color = color,
                        verticalalignment='center', alpha=transparency)
    x_disp_x = [x/5, x/5]
    x_disp_y = [y/5, -y/5]
    ax.plot(x_disp_x, x_disp_y, color, lw=1, zorder=5, alpha=transparency)
    ax.arrow(0, -y/8, x/5, 0,
                        head_width=hw, head_length=hl, fc=color, ec=color,length_includes_head = True, alpha=transparency)
    ax.arrow(x/5, -y/8, -x/5, 0,
                        head_width=hw, head_length=hl, fc=color, ec=color,length_includes_head = True, alpha=transparency)
    ax.text(x/8, -y/12, r"$x$", horizontalalignment='center', color = color,
                    verticalalignment='center', alpha=transparency)
    style = "Simple, tail_width=0.2, head_width=4, head_length=8"
    kw = dict(arrowstyle=style, color=color)
    a3 = patches.FancyArrowPatch((x/2+x/3, y/5), (x/2+x/5+x/20, y/5+x*3/20),
                            connectionstyle="arc3,rad=.2", **kw, alpha=transparency)
    ax.add_patch(a3)
    ax.text(x/2+x/4+x/8, y/4+y/12, r"$\varphi$", horizontalalignment='center', color = color,
                    verticalalignment='center', alpha=transparency)
def sign_evaluation(alpha, angle_unit, beta = False):
    if angle_unit == "deg":
        alpha = alpha/180*np.pi
        if beta == True:
            alpha = alpha+np.pi/2
            print('deg')
    else:
        if beta == True:
            alpha = alpha+np.pi/2
            print('rad')
    if alpha >= 0 and alpha < np.pi/2:
        signx = 1
        signy = 1
    elif alpha >= np.pi/2 and alpha < np.pi:
        signx = -1
        signy = 1
    elif alpha >= np.pi and alpha < np.pi*3/2:
        signx = -1
        signy = -1
    elif alpha >= np.pi*3/2 and alpha < np.pi*2:
        signx = 1
        signy = -1
    else:
        signx = 1
        signy = 1
    return signx, signy, alpha
def plot_principal_axes(parent, colors, ax, alpha, angle_unit, transformed_coordinate_on):
    try:
        parent.principal_axis1.remove()
        parent.principal_axis2.remove()
    except:
        None
    if transformed_coordinate_on == False:
        color = colors['draw_principal']
        x = 2
        y = 1
        hw = 0.015*x*y
        hl = 2*hw
        
        # evaluate orientation signs of the principal axis
        signx1, signy1, alpha = sign_evaluation(alpha, angle_unit)
        signx2, signy2, beta = sign_evaluation(alpha, angle_unit, True)


        x = 1.2
        y = 0.7
        arrow_length = (x**2+y**2)**0.5
        # first principal axis
        x_val1 = arrow_length*np.cos(alpha)
        y_val1 = arrow_length*np.sin(alpha)
        if x_val1 >= x:
            x_val1 = x
            y_val1 = x_val1*np.tan(alpha)
        elif y_val1 >= y:
            y_val1 = y
            x_val1 = y_val1/np.tan(alpha)

        ar1_x1 = -signx1*x_val1
        ar1_y1 = -signy1*y_val1
        ar1_x2 = signx1*x_val1
        ar1_y2 = signy1*y_val1
        ar1_dx = ar1_x2-ar1_x1
        ar1_dy = ar1_y2-ar1_y1
        # second principal axis
        x_val2 = arrow_length*np.cos(beta)
        y_val2 = arrow_length*np.sin(beta)
        if x_val2 >= x:
            x_val2 = x
            y_val2 = x_val2*np.tan(beta)
            print('x_val')
        elif y_val2 >= y:
            y_val2 = y
            x_val2 = y_val2/np.tan(beta)
            print('y_val')

        ar2_x1 = -signx2*x_val2
        ar2_y1 = -signy2*y_val2
        ar2_x2 = signx2*x_val2
        ar2_y2 = signy2*y_val2
        ar2_dx = ar2_x2-ar2_x1
        ar2_dy = ar2_y2-ar2_y1

        parent.principal_axis1 = ax.arrow(ar1_x1, ar1_y1, ar1_dx, ar1_dy,
                            head_width=hw, head_length=hl, fc=color, ec=color,length_includes_head = True, zorder=5)
        parent.principal_axis2 = ax.arrow(ar2_x1, ar2_y1, ar2_dx, ar2_dy,
                            head_width=hw, head_length=hl, fc=color, ec=color,length_includes_head = True, zorder=5)
        parent.canvas.draw()