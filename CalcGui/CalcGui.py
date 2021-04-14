import tkinter as tk
import Function as f
#----------------------------------------------------------------
# Fuctions
#-------------------------------
def handle_click():
    x = float(ent_num.get())
    y = f.poly(x)
    ent_num.delete(0, tk.END)
    lbl_result["text"] = y
    print(y)
#----------------------------------------------------------------
# Call the window
#-------------------------------
window = tk.Tk() 
window.title("CalcGUI")  # Window title
#----------------------------------------------------------------
# Commands
#-------------------------------
## Frame
frm_base = tk.Frame(master = window)
ent_num = tk.Entry(master = frm_base, width = 10)
lbl_result = tk.Label(master=frm_base)
lbl_poly = tk.Label(master = window, text = "x^2+2x")
btn_calc = tk.Button(
    master=window,
    text="Calculate",
    command=handle_click
)
lbl_poly.grid(row = 0, column = 0)
frm_base.grid(row=1, column=0)
ent_num.grid(row=1, column=1)
btn_calc.grid(row=1, column=2)
lbl_result.grid(row=1, column=3, sticky="w")
#----------------------------------------------------------------
# Loop
#-------------------------------
window.mainloop()

