import tkinter as tk
from PIL import ImageTk,Image
import numpy as np

global img # kép változó a betöltésekhez

LARGE_FONT = ("Verdana", 12) #betűtípus

class calcGUI(tk.Tk):

	def __init__(self, *args, **kwargs):

		tk.Tk.__init__(self, *args, **kwargs)

		self.geometry("1280x720") #ablak mérete, minimum mérete, neve
		self.minsize(500,500)
		self.title("Számoló GUI")

		container = tk.Frame(self)
		container.pack(side="top", fill="both", expand=True)

		container.grid_rowconfigure(0, weight=1) #grid beállítása
		container.grid_columnconfigure(0, weight=1)

		self.frames = {}

		for F in (StartPage, Teglalap_oldal, Kor_oldal): #kapcsolható oldalak

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


	def show_frame(self, cont): #ablak előhozó fvg.

		frame = self.frames[cont]
		frame.tkraise()

class StartPage(tk.Frame): #kezdőoldal csoporja

	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)

		label1 = tk.Label(self, text="Start Page", font=LARGE_FONT)
		label1.grid(row=0, column=0)

class Teglalap_oldal(tk.Frame): #téglalap oldal csoportja

	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)

		label1 = tk.Label(self, text="Geometria:", font=LARGE_FONT)
		label1.grid(row=0, column=0, sticky="W", padx=10, pady=5) #geometria kiírás

		canvas = tk.Canvas(self, width=350, height=225, bg="pink")
		canvas.grid(row=1, column=0) #vászon betöltése

		img = Image.open("img/teglalap.png") #kép ráhelyezése a vászonra
		img_w = 1312
		img_h = 789
		ratio = img_w / img_h
		img = img.resize((325,int(325/ratio)), Image.ANTIALIAS) #kép átméretzezése
		self.img = ImageTk.PhotoImage(img) #kép konvertálása
		canvas.create_image(190, 125, anchor='center', image=self.img) #kép rajzolása
		canvas.image = self.img

		label_a = tk.Label(self, text="a = ", font=LARGE_FONT)
		label_a.grid(row=3, column=0, sticky="W", padx=20) # "a" adat szöveg

		global textbox1
		textbox1 = tk.Text(self, width=10, height=1) 
		textbox1.grid(row=3, column=0, sticky="W", padx=60, pady=10) # "a" adat textbox

		label_me1 = tk.Label(self, text="mm", font=LARGE_FONT) 
		label_me1.grid(row=3, column=0, sticky="W", padx=150) # mértékegység
		
		label_b = tk.Label(self, text="b = ", font=LARGE_FONT)
		label_b.grid(row=4, column=0, sticky="W", padx=20) # "b" adat szöveg

		global textbox2
		textbox2 = tk.Text(self, width=10, height=1)
		textbox2.grid(row=4, column=0, sticky="W", padx=60, pady=10) # "b" adat textbox

		label_me2 = tk.Label(self, text="mm", font=LARGE_FONT)
		label_me2.grid(row=4, column=0, sticky="W", padx=150) # mértékegység

		button1 = tk.Button(self, text="Számolás", font=LARGE_FONT, command= szamolas_teglalap)
		button1.grid(row=5, column=0, sticky="NW", pady=10, padx=175) #számolás gomb

		global label_hiba
		label_hiba = tk.Label(self, text="", font=LARGE_FONT)
		label_hiba.grid(row=6, column=0, sticky="NWSE", padx=160, pady=10) #hibás adatok szöveg

		global label2
		label2 = tk.Label(self, text="", font=LARGE_FONT)
		label2.grid(row=6, column=2) # "I_x" eredmény szöveg

		global label3
		label3 = tk.Label(self, text="", font=LARGE_FONT)
		label3.grid(row=7, column=2) # "I_y" eredmény szöveg


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

		global label4
		label4 = tk.Label(self, text="", font=LARGE_FONT)
		label4.grid(row=7, column=0)


from teglalap_masodrendu import teglalap_szamitas_x
from teglalap_masodrendu import teglalap_szamitas_y #számító függvények importálása

def szamolas_teglalap():

	if textbox1.compare("end-1c", "==", "1.0"):
		label_hiba.config(text="Hibás adatok!") #ha üres a textbox akkor hibát írjon ki

	elif textbox2.compare("end-1c", "==", "1.0"):
		label_hiba.config(text="Hibás adatok!") #ha üres a textbox akkor hibát írjon ki

	else: #ha nem üres akkor számoljon
		x = float(textbox1.get("1.0","end"))
		y = float(textbox2.get("1.0","end"))

		I_x = teglalap_szamitas_x(x,y)
		I_y = teglalap_szamitas_y(x,y)

		label2.config(text= "I_x = " + I_x)
		label3.config(text= "I_y = " + I_y) #eredmények kiiratása

		label_hiba.config(text="") #hiba eltüntetése ha előtte volt


from kor_masodrendu import kor_szamitas

def szamolas_kor():

	d = float(textbox3.get("1.0","end"))

	I = kor_szamitas(d)

	label4.config(text= 'I_x = I_y = ' + I)

app = calcGUI()
app.mainloop()