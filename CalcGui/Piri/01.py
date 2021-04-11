from tkinter import *
from PIL import ImageTk,Image

window = Tk() #ablak létrehozása
window.geometry("1280x720") #ablak mérete
window.minsize(800,600) #minimális ablakméret
window.title("TKinter gui") #ablak címe

global img #kép változó definiálása
global label_a
global label_b

canvas = Canvas(window, width = 400, height = 500) #vászon létrehozása a képekhez


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

	canvas.create_text(110, 340, anchor=SE, text="a =", font=("Courier", 14)) # `a` adat szöveg

	entry1 = Entry(window)
	canvas.create_window(130, 340, anchor=SW, window=entry1, height=20, width=80) # `a` adat textbox

	canvas.create_text(110, 400, anchor=SE, text="b =", font=("Courier", 14)) # `b` adat szöveg

	entry2 = Entry(window)
	canvas.create_window(130, 400, anchor=SW, window=entry2, height=20, width=80) # `b` adat textbox

	

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

	canvas.create_text(110, 340, anchor=SE, text="d =", font=("Courier", 14)) # `d` adat szöveg

	entry1 = Entry(window)
	canvas.create_window(130, 340, anchor=SW, window=entry1, height=20, width=80) # `d` adat textbox

	window.mainloop() #minden frissít


#Menüszerkezet létrehozása

menubar = Menu(window) #menüsáv létrehozása
window.config(menu=menubar) #menüsáv hozzáadása az ablakhoz

keresztmetszet = Menu(menubar, tearoff=0) #keresztmetszet menü létrehozása
menubar.add_cascade(label="Keresztmetszet", menu=keresztmetszet) #keresztmetszet menü neve

keresztmetszet.add_command(label="Téglalap", command=teglalap) #keresztmetszet 1. almenüje
keresztmetszet.add_command(label="Kör", command=kor) #keresztmetszet 2. almenüje

menubar.add_command(label="Kilépés", command=window.quit) #kilépés menü létrehozása

window.mainloop() #minden frissít