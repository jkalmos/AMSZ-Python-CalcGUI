import tkinter as tk

class mainWindow(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.root = root
        self.root.geometry("600x500")
        self.canvas = tk.Canvas(self,bg="white", width=400, height=400)
        self.canvas.pack()
        self.my_menu = tk.Menu(self.root)
        self.object_choosing_menu = tk.Menu(self.my_menu)
        self.my_menu.add_cascade(label= "Shapes", menu = self.object_choosing_menu)
        self.object_choosing_menu.add_command(label="Teglalap", command = self.add_telalap)
        self.object_choosing_menu.add_command(label="Kör", command= self.add_circle)

        self.root.config(menu=self.my_menu)
    def add_telalap(self):
        self.canvas.delete('all')
        self.canvas.create_rectangle(100,100,300,300,fill="blue")
    def add_circle(self):
        self.canvas.delete('all')
        self.canvas.create_oval(100,100,300,300,fill="blue")

if __name__ == '__main__':
    root = tk.Tk()
    app = mainWindow(root)
    app.pack()
    root.mainloop()