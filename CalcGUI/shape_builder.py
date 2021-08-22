import tkinter as tk
WIDTH = 30
EPSILON = 20
STICKY = True
#TODO: Overleaping warning with different size rectangles
#TODO: Sticking with different points
#TODO: scaling
#TODO: Coordinate system fix + sicking
class shapeBuilder(tk.Canvas):
    def __init__(self, root, sm_sm):
        super().__init__(root, bg=root.colors["main_color"])
        self.root=root
        #self.root.geometry("1000x600")
        self.sb_sm = sm_sm
        self.rectangles = []
        self.label = tk.Label(self.sb_sm,text="")
        self.label.pack()
        self.button = tk.Button(self.sb_sm, text="calculate", command=self.calculate)
        self.button.pack()
        self.e1 = tk.Entry(self.sb_sm)
        self.e1.pack()
        self.e2 = tk.Entry(self.sb_sm)
        self.e2.pack()
        self.button2 = tk.Button(self.sb_sm, text="give value", command=self.overwrite)
        self.button2.pack()
        self.alap = self.create_rectangle(10,10,10+WIDTH,10+WIDTH,fill="green")
        self.alap_negyzet = Rectangle(self,10,10,10+WIDTH,10+WIDTH, self.alap)
        self.x_axis = self.create_line(0,250,500,250)
        self.y_axis = self.create_line(250,0,250,500)
        self.current = None
        self.isMoving=False
        self.width = WIDTH
        self.heigth = WIDTH
        self.sticky = tk.BooleanVar()
        self.is_sticky = tk.Checkbutton(self.sb_sm, text="Automatikus igazítás", variable=self.sticky, onvalue=True, offvalue=False)
        self.is_sticky.pack()
        self.bind('<B1-Motion>',self.move) #"drag-and-drop" action
        self.bind('<ButtonRelease-1>',self.release) #when you relase the left mose button
        self.popup_menu = tk.Menu(self, tearoff=0) #right click menu
        self.popup_menu.add_command(label="Delete",command=self.delete_rectangle)
        self.popup_menu.add_command(label="Resize",command=self.resize_rectangle)
        self.bind("<Button-3>", self.popup) # right-click event
    def popup(self, e): #right cklick menu shows up
        if not self.isMoving:
            for i in self.rectangles:
                pos = self.coords(i.canvas_repr)
                if e.x>=pos[0] and e.x<=pos[2] and e.y>=pos[1] and e.y <=pos[3]:
                    self.current = i
                    try:
                        self.popup_menu.tk_popup(e.x_root, e.y_root, 0)
                    finally:
                        self.popup_menu.grab_release()
                    break
    def delete_rectangle(self):
        self.delete(self.current.canvas_repr)
        self.rectangles.remove(self.current)
        self.current = None
    def resize_rectangle(self):
        self.current.refresh(self.current.x1, self.current.y1, self.current.x1 + self.width, self.current.y1 + self.heigth)
        self.current = None
    def move(self,e):
        #choosing object
        for i in self.rectangles:
            pos = self.coords(i.canvas_repr)
            if self.current is None and e.x>=pos[0] and e.x<=pos[2] and e.y>=pos[1] and e.y <=pos[3]:
                self.rectangles.remove(i)
                self.current = i
                self.itemconfig(self.current.canvas_repr, fill='light blue')
                break
        else:
            pos = self.coords(self.alap_negyzet.canvas_repr)
            if self.current is None and e.x>=pos[0] and e.x<=pos[2] and e.y>=pos[1] and e.y <=pos[3]:
                self.current = Rectangle(self,10,10,10+self.width,10+self.heigth,self.create_rectangle(10,10,10+self.width,10+self.heigth,fill="blue"))
                self.itemconfig(self.current.canvas_repr, fill='light blue')
        if not self.current:
            return -1
        pos = self.coords(self.current.canvas_repr)
        if self.isMoving or e.x>=pos[0] and e.x<=pos[2] and e.y>=pos[1] and e.y <=pos[3]:
            #self.coords(self.current.canvas_repr,e.x-self.current.width/2,e.y-self.current.heigth/2,e.x+self.current.width/2,e.y+self.current.heigth/2)
            self.current.refresh(e.x-self.current.width/2,e.y-self.current.heigth/2,e.x+self.current.width/2,e.y+self.current.heigth/2)
            self.isMoving = True
        self.label.config(text=f"x: {e.x} y: {e.y}")
    def release(self,e):
        #choosing object
        if self.sticky.get() and self.current:
            pos = self.coords(self.current.canvas_repr)
            #? prioritási sorrend???    
            # sticking to another rectangles    
            for i in self.rectangles:
                i_pos = self.coords(i.canvas_repr)
                if abs(pos[0] - i_pos[0]) < EPSILON and abs(pos[1] - i_pos[3]) < EPSILON: # current rect goes under the another 
                    #self.coords(self.current.canvas_repr, i_pos[0],i_pos[3],i_pos[0]+self.current.width,i_pos[3]+self.current.heigth)
                    self.current.refresh(i_pos[0],i_pos[3],i_pos[0]+self.current.width,i_pos[3]+self.current.heigth)
                    break
                elif abs(pos[0] - i_pos[0]) < EPSILON and abs(pos[3] - i_pos[1]) < EPSILON: # TOP
                    #self.coords(self.current.canvas_repr, i_pos[0],i_pos[1]-self.current.heigth,i_pos[0]+self.current.width,i_pos[1])
                    self.current.refresh(i_pos[0],i_pos[1]-self.current.heigth,i_pos[0]+self.current.width,i_pos[1])
                    break
                elif abs(pos[1] - i_pos[1]) < EPSILON and abs(pos[0] - i_pos[2]) < EPSILON: # RIGHT
                    #self.coords(self.current.canvas_repr, i_pos[2],i_pos[1],i_pos[2]+self.current.width,i_pos[1]+self.current.heigth)
                    self.current.refresh(i_pos[2],i_pos[1],i_pos[2]+self.current.width,i_pos[1]+self.current.heigth)
                    break
                elif abs(pos[1] - i_pos[1]) < EPSILON and abs(pos[2] - i_pos[0]) < EPSILON: # LEFT
                    #self.coords(self.current.canvas_repr, i_pos[0]-self.current.width,i_pos[1],i_pos[0],i_pos[1]+self.current.heigth)
                    self.current.refresh(i_pos[0]-self.current.width,i_pos[1],i_pos[0],i_pos[1]+self.current.heigth)
                    break
            else: #sicking to the coordinate system
                pass
        if self.isMoving:
            self.itemconfig(self.current.canvas_repr, fill='blue')
            self.current.is_overleaping()
            self.rectangles.append(self.current)
            
        self.isMoving = False
        self.current=None
        self.label.config(text=f"you have {len(self.rectangles)} rectangles")
    def calculate(self):
        A = 0
        for i in self.rectangles:
            pos = self.coords(i.canvas_repr)
            A += (pos[2]-pos[0]) * (pos[3]-pos[1])
        self.label.config(text=f"area: {A}")
    def overwrite(self):
        self.width = float(self.e1.get().replace(',','.'))
        self.heigth = float(self.e2.get().replace(',','.'))
        self.coords(self.alap_negyzet.canvas_repr, 10,10,10+self.width,10+self.heigth)
class Rectangle():
    def __init__(self,canvas,x1,y1,x2,y2, canvas_repr):
        self.canvas = canvas
        self.canvas_repr = canvas_repr
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.width = x2-x1
        self.heigth = y2-y1
        self.area = self.width*self.heigth
        self.center=((x1-x2)/2, (y1-y2)/2)
    def refresh(self,x1,y1,x2,y2):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.width = self.x2-self.x1
        self.heigth = self.y2-self.y1
        self.area = self.width*self.heigth
        self.center=((self.x1-self.x2)/2, (self.y1-self.y2)/2)
        self.canvas.coords(self.canvas_repr,x1,y1,x2,y2)
    def is_overleaping(self):
        #! with different-size rectangles doesm't works properly
        for i in self.canvas.rectangles:
            if self.x1 <i.x2 and self.x1> i.x1 and self.y1 > i.y1 and self.y1 < i.y2: #top left corner is in the rectangle
                self.canvas.itemconfig(self.canvas.current.canvas_repr, fill='red')
            if self.x1 <i.x2 and self.x1> i.x1 and self.y2 > i.y1 and self.y2 < i.y2: #bottom left corner is in the rectangle
                self.canvas.itemconfig(self.canvas.current.canvas_repr, fill='red')
            if self.x2 <i.x2 and self.x2> i.x1 and self.y2 > i.y1 and self.y2 < i.y2: #bottom right corner is in the rectangle
                self.canvas.itemconfig(self.canvas.current.canvas_repr, fill='red')
            if self.x2 <i.x2 and self.x2> i.x1 and self.y1 > i.y1 and self.y1 < i.y2: #top right corner is in the rectangle
                self.canvas.itemconfig(self.canvas.current.canvas_repr, fill='red')
class sb_side_menu(tk.Frame):
    def __init__(self,root):
        super().__init__(root,width=30, bg=root.colors['secondary_color'])
        self.root = root

if __name__=="__main__":
    app = tk.Tk()
    app.minsize(width=200, height=200)
    a = shapeBuilder(app)
    a.pack(expand=tk.YES, fill=tk.BOTH)
    app.mainloop()