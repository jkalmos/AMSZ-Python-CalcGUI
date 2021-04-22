# --- Imports
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as Tk
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
# --- End of imports

fig = plt.Figure()

x = np.arange(0, 2*np.pi, 0.01)


def animate(i):
    for j in range(10000000):
        k=j
    line.set_ydata(np.sin(x + i / 10.0))
    return line

root = Tk.Tk()

label = Tk.Label(root, text="Graph")
label.grid(column=0, row=0)

canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().grid(column=0, row=1)

ax = fig.add_subplot(111)
line, = ax.plot(x, np.sin(x))

ani = animation.FuncAnimation(fig, animate, np.arange(1, 200), interval=250, blit=False)

Tk.mainloop()