import tkinter as tk
import Function1 as f1
from tkinter import ttk
#----------------------------------------------------------------


## Fuctions
#-------------------------------
def callbackFunc(event):
    combo = event.widget.get()
    print(combo)

def handle_click():
    x = float(ent_x.get())
    y = 0
    if combo == poly_list[0]:
        y = f1.poly(x)
    elif combo == poly_list[1]:
        y = f2.poly(x)
    ent_x.delete(0, tk.END)
    lbl_result["text"] = y
    print(y)


#----------------------------------------------------------------


## Call the window
#-------------------------------
window = tk.Tk() 
window.title("CalcGUI")  # window title
window.geometry("1280x720") # window size
#----------------------------------------------------------------


## Widgets
#-------------------------------
# Frame
frm_base = tk.Frame(master = window)
frm_base.grid(row=0, column=0)

# combobox
stringvar = tk.StringVar()
poly_list = ["y = x^2 + 2*x", "y = x^3 + 3*x"]
combo = ttk.Combobox(frm_base, textvariable = stringvar)
combo['values'] = poly_list
combo['state'] = 'readonly'
combo.bind("<<ComboboxSelected>>", callbackFunc)
combo.grid(row=0, column=1, padx = 5, pady = 5)

# Entry for x values
ent_x = tk.Entry(master = frm_base, width = 10)
ent_x.grid(row=0, column=2)

# Label to print results
lbl_result = tk.Label(master=frm_base)
lbl_result.grid(row=0, column=4, sticky="w")

# Calculate button
btn_calc = tk.Button(
    master=window,
    text="Calculate",
    command=handle_click
)
btn_calc.grid(row=0, column=3)
#----------------------------------------------------------------


## Loop
#-------------------------------
window.mainloop()

