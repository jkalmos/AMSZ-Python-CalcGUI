import tkinter as tk

window = tk.Tk()
window.title("Calculator")
window.geometry("1024x720")

window.columnconfigure(0, minsize=500)
window.rowconfigure([0, 1], minsize=100)

label1 = tk.Label(text="CalcGUI test")
label1.grid(row=0, column=0)

listbox_select = tk.Listbox()
listbox_select.insert(1, "Option 1")
listbox_select.insert(2, "Option 2")
listbox_select.insert(3, "Option 3")
listbox_select.grid(row=1, column=0)

button_select = tk.Button(text="Select")
button_select.grid(row=2, column=0)

window.mainloop()