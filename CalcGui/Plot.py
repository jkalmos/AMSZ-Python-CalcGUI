from tkinter import * 
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, 
NavigationToolbar2Tk)
import numpy as np
  
# plot function is created for 
# plotting the graph in 
# tkinter window
def handle_click():
    x = float(ent1.get())
    y = float(ent2.get())
    plot(x,y)


def plot(x,y):
  
    # the figure that will contain the plot
    fig,ax = plt.subplots(1,1,figsize=(8,8))
    #ax.set_alpha(0.)
    fig.patch.set_facecolor('#ababab')
    ax.xaxis.set_visible(False)
    ax.yaxis.set_visible(False)
    ax.set_frame_on(False)
    

    #fig.set_alpha(0.)
    #fig.tight_layout()
    # list of squares
    # create points of the rectangle
    N = 101
    rect_x = [-x/2, -x/2, x/2, x/2, -x/2]
    rect_y = [y/2, -y/2, -y/2, y/2, y/2]
    
    # adding the subplot
    ax.plot(rect_x, rect_y)
    ax.set_aspect("equal")
    

    # creating the Tkinter canvas
    # containing the Matplotlib figure
    canvas = FigureCanvasTkAgg(fig,
                               master = window)  
    canvas.draw()
  
    # placing the canvas on the Tkinter window
    canvas.get_tk_widget().pack()
  
    # creating the Matplotlib toolbar
    toolbar = NavigationToolbar2Tk(canvas,
                                   window)
    toolbar.update()
  
    # placing the toolbar on the Tkinter window
    canvas.get_tk_widget().pack()
  
# the main Tkinter window
window = Tk()
window.configure(bg = '#ababab')
  
# setting the title 
window.title('Plotting in Tkinter')
  
# dimensions of the main window
window.geometry("500x500")
  
# button that displays the plot
plot_button = Button(master = window, 
                     command = handle_click,
                     height = 2, 
                     width = 10,
                     text = "Plot")
ent1 = Entry(master = window)
ent2 = Entry(master = window)
  
# place the button 
# in main window
plot_button.pack()
ent1.pack()
ent2.pack()
  
# run the gui
window.mainloop()