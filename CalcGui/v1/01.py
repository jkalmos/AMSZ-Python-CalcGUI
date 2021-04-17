from tkinter import *
from PIL import ImageTk,Image

window = Tk() #ablak létrehozása
window.geometry("1280x720") #ablak mérete
window.minsize(800,600) #minimális ablakméret
window.title("TKinter gui") #ablak címe

canvas = Canvas(window, width = 400, height = 300, bg="pink") #vászon létrehozása a képekhez

def szamolas():
	adat1 = float(textbox1.get("1.0","end"))
	adat2 = float(textbox2.get("1.0","end"))

	eredmeny = adat1 * adat2**3 / 12

	print(eredmeny)

button1 = Button(window, height=2, width=8, text="Számolás", command=szamolas) #.place(x=400, y=100)
button1.pack()

textbox1 = Text(window, height=1, width=10) #.place(x=130, y=340)
textbox1.pack()

textbox2 = Text(window, height=1, width=10) #.place(x=130, y=400)
textbox2.pack()

#Függvény, ami csinál valamit, most épp betölti a képeket

def teglalap():
	canvas.delete('all') #rajztábla törlése
	canvas.place(x=20, y=20) #rajztábla elhelyezése az ablakban
	img = Image.open("img/teglalap.png") #kép betöltése
	img_w = 1312
	img_h = 789
	ratio = img_w / img_h
	img = img.resize((325,int(325/ratio)), Image.ANTIALIAS) #kép átméretzezése
	img = ImageTk.PhotoImage(img) #kép konvertálása
	canvas.create_image(50, 50, anchor=NW, image=img) #kép rajzolása

	canvas.create_text(40, 280, anchor=SW, text="Geometriai adatok:", font=("Courier", 14)) #geometriai adatok szöveg

	window.mainloop() #minden frissít

def kor():
	canvas.delete('all') #rajztábla törlése
	canvas.place(x=20, y=20) #rajztábla elhelyezése az ablakban
	img = Image.open("img/kor.png") #kép betöltése
	img_w = 961
	img_h = 820
	ratio = img_w / img_h
	img = img.resize((200,int(200/ratio)), Image.ANTIALIAS) #kép átméretzezése
	img = ImageTk.PhotoImage(img) #kép konvertálása
	canvas.create_image(93, 35, anchor=NW, image=img) #kép rajzolása

	canvas.create_text(40, 280, anchor=SW, text="Geometriai adatok:", font=("Courier", 14)) # `geometriai adatok` szöveg

	window.mainloop() #minden frissít


#Menüszerkezet létrehozása

menubar = Menu(window) #menüsáv létrehozása
window.config(menu=menubar) #menüsáv hozzáadása az ablakhoz

keresztmetszet = Menu(menubar, tearoff=0) #keresztmetszet menü létrehozása
menubar.add_cascade(label="Keresztmetszet", menu=keresztmetszet) #keresztmetszet menü neve

keresztmetszet.add_command(label="Téglalap", command=teglalap) #keresztmetszet 1. almenüje
keresztmetszet.add_command(label="Kör", command=kor) #keresztmetszet 2. almenüje

menubar.add_command(label="Kilépés", command=window.destroy) #kilépés menü létrehozása

window.mainloop() #minden frissít