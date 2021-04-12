import tkinter as tk

def doNothing():
    print("i wont")

def add_circle():
    global canvas
    canvas.create_oval(25,25,50,50,fill="blue")


root = tk.Tk()
root.title("Próba GUI")
root.geometry("1000x600")
root.minsize(width=200, height=200)
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
# ********* Toolbar **********
toolbar = tk.Frame(root, bg='#F5F5DC')

tegla = tk.Button(toolbar, text="Téglalap", command=doNothing)
tegla.pack(side=tk.LEFT, padx=2, pady=2)
kor = tk.Button(toolbar, text="Kör", command=add_circle)
kor.pack(side=tk.LEFT, padx=2, pady=2)
haromszog = tk.Button(toolbar, text="Háromszög", command=doNothing)
haromszog.pack(side=tk.LEFT, padx=2, pady=2)

calc = tk.Button(toolbar, text="Calculate", command=doNothing)
calc.pack(side=tk.RIGHT, padx=2, pady=2)

toolbar.pack(side=tk.TOP, fill=tk.X)

# *********** Status bar ********
status = tk.Label(root, text="this is a status bar", bd=1, relief=tk.SUNKEN, anchor=tk.W)
status.pack(side=tk.BOTTOM, fill=tk.X)


# ********** Side menu ***************
sm = tk.Frame(root, bg='#707070')

title = tk.Label(sm, text="TThis is a side menu")
title.grid(row=0, columnspan=2)
tk.Label(sm, text="First Name").grid(row=1)
tk.Label(sm, text="Last Name").grid(row=2)
e1 = tk.Entry(sm)
e2 = tk.Entry(sm)
e1.grid(row=1, column=1)
e2.grid(row=2, column=1)

sm.pack(side=tk.LEFT, fill=tk.Y)
# ********** Canvas *************
canvas = tk.Canvas(root, width=800, height = 500, bg="white")
canvas.pack()
#blackline  = canvas.create_line(0,0,200,50)
#redline = canvas.create_line(0,100,200,50, fill="red")
#greenBox = canvas.create_rectangle(25,25, 130, 60, fill="green")


#canvas.delete(redline)

root.mainloop()


