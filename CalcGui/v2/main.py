import tkinter as tk
from PIL import ImageTk,Image
import numpy as np

global img

LARGE_FONT = ("Verdana", 12)


def teglalap(meret):
	print("teglalap:", meret)

def kor():
	print("kor")


class calcGUI(tk.Tk):

	def __init__(self, *args, **kwargs):

		tk.Tk.__init__(self, *args, **kwargs)

		self.geometry("500x500")
		self.minsize(500,500)
		self.title("Számoló GUI")

		container = tk.Frame(self)
		container.pack(side="top", fill="both", expand=True)

		container.grid_rowconfigure(0, weight=1)
		container.grid_columnconfigure(0, weight=1)

		self.frames = {}

		for F in (StartPage, Teglalap_oldal, Kor_oldal):

			frame = F(container, self)

			self.frames[F] = frame

			frame.grid(row=0, column=0, sticky="nsew")

		self.show_frame(StartPage)


		#menüszerkezet

		menubar = tk.Menu(self)
		self.config(menu=menubar)

		keresztmetszet = tk.Menu(self, menubar, tearoff=0)
		menubar.add_cascade(label="Keresztmetszet", menu=keresztmetszet)

		keresztmetszet.add_command(label="Téglalap",
									command = lambda: calcGUI.show_frame(self, Teglalap_oldal))
		keresztmetszet.add_command(label="Kör", 
									command = lambda: calcGUI.show_frame(self, Kor_oldal))

		menubar.add_command(label="Kilépés", command=self.destroy)


	def show_frame(self, cont):

		frame = self.frames[cont]
		frame.tkraise()

class StartPage(tk.Frame):

	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)

		label1 = tk.Label(self, text="Start Page", font=LARGE_FONT)
		label1.grid(row=0, column=0)

class Teglalap_oldal(tk.Frame):

	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)

		label1 = tk.Label(self, text="Téglalap oldal", font=LARGE_FONT)
		label1.grid(row=0, column=0)

		canvas = tk.Canvas(self, width=350, height=250, bg="pink")
		canvas.grid(row=1, column=0)

		img = Image.open("img/teglalap.png")
		img_w = 1312
		img_h = 789
		ratio = img_w / img_h
		img = img.resize((325,int(325/ratio)), Image.ANTIALIAS) #kép átméretzezése
		self.img = ImageTk.PhotoImage(img) #kép konvertálása
		canvas.create_image(190, 125, anchor='center', image=self.img) #kép rajzolása
		canvas.image = self.img

		global textbox1
		textbox1 = tk.Text(self, width=10, height=1)
		textbox1.grid(row=3, column=0)
		
		global textbox2
		textbox2 = tk.Text(self, width=10, height=1)
		textbox2.grid(row=4, column=0)
		

		button1 = tk.Button(self, text="Számolás", font=LARGE_FONT, command=szamolas_teglalap)
		button1.grid(row=5, column=0)

class Kor_oldal(tk.Frame):

	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)

		label1 = tk.Label(self, text="Kör oldal", font=LARGE_FONT)
		label1.grid(row=0, column=0)

		canvas = tk.Canvas(self, width=350, height=250, bg="pink")
		canvas.grid(row=1, column=0)

		img = Image.open("img/kor.png")
		img_w = 961
		img_h = 820
		ratio = img_w / img_h
		img = img.resize((200,int(200/ratio)), Image.ANTIALIAS) #kép átméretzezése
		self.img = ImageTk.PhotoImage(img) #kép konvertálása
		canvas.create_image(190, 125, anchor='center', image=self.img) #kép rajzolása
		canvas.image = self.img

		global textbox3
		textbox3 = tk.Text(self, width=10, height=1)
		textbox3.grid(row=3, column=0)
		
		button2 = tk.Button(self, text="Számolás", font=LARGE_FONT, command=szamolas_kor)
		button2.grid(row=5, column=0)


def szamolas_teglalap():
	adat1 = float(textbox1.get("1.0","end"))
	adat2 = float(textbox2.get("1.0","end"))

	eredmeny = adat1 * adat2**3 / 12

	print(eredmeny)

def szamolas_kor():
	adat3 = float(textbox3.get("1.0","end"))

	eredmeny = adat3**4 * np.pi / 64

	print(eredmeny)

app = calcGUI()
app.mainloop()