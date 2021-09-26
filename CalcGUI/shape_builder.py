import tkinter as tk
from math import cos, sin, sqrt, atan, pi
from tkinter.constants import ANCHOR, FALSE, TRUE
from PIL import ImageTk,Image
WIDTH = 30
EPSILON = 10
STICKY = True
XCENTER = 400
YCENTER = 300
SHOW_HAUPACHSEN = False
FIXED_AXIS = False

#TODO: Schwerachsen -> rescale 
#TODO: Sticking with different corners
#TODO: fixed axis vs Schwerpunkt
#TODO: +,- buttons -> top level
#TODO: window resize
#TODO: scrolling
#TODO: settings
#TODO: colors
#TODO: haupachsen arrow + alfa==0

class shapeBuilder(tk.Canvas):
    def __init__(self, root, sb_sm):
        super().__init__(root, bd=0, bg=root.colors["main_color"],highlightthickness=0)
        self.root=root
        self.sb_sm = sb_sm #own side menu
        self.scale = 10 #scale between drawing and given value
        self.rectangles = []

        #########* Basic constants #########
        self.current = None
        self.isMoving=False
        self.width = WIDTH
        self.heigth = WIDTH

        #############* Creating objects for side menu ##############
        self.label = tk.Label(self.sb_sm,text="", bg=self.sb_sm["background"], fg='white')
        self.l_width = tk.Label(self.sb_sm,text="Szélesség", bg=self.sb_sm["background"], fg='white')
        self.l_heigth = tk.Label(self.sb_sm,text="Magasság", bg=self.sb_sm["background"], fg='white')
        self.l_unit1 = tk.Label(self.sb_sm,text="mm", bg=self.sb_sm["background"], fg='white')
        self.l_unit2 = tk.Label(self.sb_sm,text=f"{self.root.unit}", bg=self.sb_sm["background"], fg='white')
        self.button = tk.Button(self.sb_sm, text="Számolás", command=self.calculate)
        self.e1 = tk.Entry(self.sb_sm,bg=self.sb_sm["background"], fg='white')
        self.e2 = tk.Entry(self.sb_sm,bg=self.sb_sm["background"], fg='white')
        self.button2 = tk.Button(self.sb_sm, text="Értékadás", command=self.overwrite)
        self.cls = tk.Button(self.sb_sm,text="Minden törlése", command=self.clear_all)
        #self.pos_lbl = tk.Label(self,text="", bg=self.sb_sm["background"], fg='white')
        self.pos_lbl = self.create_text(15 ,15,text="Pos",fill= "white") # position label

        #############* Creating + and - buttons ##############
        self.img= (Image.open("plus.png"))
        resized_image= self.img.resize((30,30), Image.ANTIALIAS)
        self.plus_img= ImageTk.PhotoImage(resized_image)
        self.img= (Image.open("minus.png"))
        resized_image= self.img.resize((30,30), Image.ANTIALIAS)
        self.minus_img= ImageTk.PhotoImage(resized_image)
        self.minus= self.create_image(self.root.winfo_width()-310, self.root.winfo_height()-50, anchor=tk.NW,image=self.minus_img)
        self.plus= self.create_image(self.root.winfo_width()-275, self.root.winfo_height()-50, anchor=tk.NW,image=self.plus_img)
        self.tag_bind(self.plus, '<Button-1>', lambda e: self.rescale(2))
        self.tag_bind(self.minus, '<Button-1>', lambda e: self.rescale(0.5))
        
        ###########* Creating the basic, green rectangle #############
        self.alap = self.create_rectangle(10,10,10+WIDTH,10+WIDTH,fill="green")
        self.alap_negyzet = Rectangle(self,10,10,10+WIDTH,10+WIDTH, self.alap)
        self.width_label = self.create_text(20+self.width,10+ self.heigth/2,text=str(self.width/10))
        self.height_label = self.create_text(10+self.width/2,self.heigth+ 20,text=str(self.heigth/10))

        ##########* Creating axis #############
        self.x_axis = self.create_line(10,YCENTER,XCENTER*2,YCENTER, arrow=tk.LAST, fill= "gray", tags=("orig_axes")) #Drawing X-axis
        self.x_label = self.create_text(2*XCENTER-5,YCENTER+ 20,text="X",fill= "gray",tags=("orig_axes")) # X lavel
        self.y_axis = self.create_line(XCENTER,10,XCENTER,YCENTER*2, arrow=tk.FIRST,fill= "gray",tags=("orig_axes")) #Drawing Y-axis
        self.y_label = self.create_text(XCENTER +20 ,15,text="Y",fill= "gray",tags=("orig_axes")) # Y label

        #########* Evensts and other stuff ############
        self.sticky = tk.BooleanVar(value=True)
        self.is_sticky = tk.Checkbutton(self.sb_sm, text="Automatikus igazítás", variable=self.sticky, onvalue=True, offvalue=False,bg = self.sb_sm["background"], fg='white', selectcolor='grey')
        self.bind('<B1-Motion>',self.move) #"drag-and-drop" action
        self.bind('<ButtonRelease-1>',self.release) #when you relase the left mose button
        self.popup_menu = tk.Menu(self, tearoff=0) #right click menu
        self.popup_menu.add_command(label="Delete",command=self.delete_rectangle)
        self.popup_menu.add_command(label="Resize",command=self.resize_rectangle)
        self.popup_menu.add_command(label="Info",command=self.rectangle_info)
        self.bind("<Button-3>", self.popup) # right-click event
        self.bind("<Configure>", self.resize_canvas)

        ##############* Packing objects ###############
        self.l_width.grid(row=1,column=0)
        self.e1.grid(row=1,column=1,columnspan=3)
        self.l_unit1.grid(row=1,column=4)
        self.l_heigth.grid(row=2,column=0)
        self.e2.grid(row=2,column=1,columnspan=3)
        self.l_unit2.grid(row=2,column=4)
        self.is_sticky.grid(row=3,columnspan=5)
        self.button.grid(row=4,column=1)
        self.button2.grid(row=4, column=3)
        self.label.grid(row=5,columnspan=5, pady= 50)
        self.cls.grid(row=6)
        
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
    def rectangle_info(self):
        self.label.config(text=f"Szélesség = {self.current.width/self.scale}\nMagasság = {self.current.heigth/self.scale}\nKözéppont = ({(self.current.center[0]-XCENTER)/self.scale},{(YCENTER-self.current.center[1])/self.scale})" )
        print(self.current.width, self.current.heigth, self.current.center)
    def move(self,e):
        self.itemconfig(self.pos_lbl, text=f"x: {(e.x-XCENTER)/self.scale} y: {(YCENTER-e.y)/self.scale}")
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
                self.current = Rectangle(self,10,10,10+self.width,10+self.heigth,self.create_rectangle(10,10,10+self.width,10+self.heigth,fill="blue", tags=("rect")))
                self.itemconfig(self.current.canvas_repr, fill='light blue')
        if not self.current:
            return -1
        pos = self.coords(self.current.canvas_repr)
        if self.isMoving or e.x>=pos[0] and e.x<=pos[2] and e.y>=pos[1] and e.y <=pos[3]:
            #self.coords(self.current.canvas_repr,e.x-self.current.width/2,e.y-self.current.heigth/2,e.x+self.current.width/2,e.y+self.current.heigth/2)
            self.current.refresh(e.x-self.current.width/2,e.y-self.current.heigth/2,e.x+self.current.width/2,e.y+self.current.heigth/2)
            self.isMoving = True
        self.label.config(text=f"")
        #self.itemconfig(self.pos_lbl, text=f"x: {(e.x-XCENTER)/self.scale} y: {(YCENTER-e.y)/self.scale}")
        #self.label.config(text=f"x: {(e.x-XCENTER)/self.scale} y: {(YCENTER-e.y)/self.scale}")
    def release(self,e):
        self.delete("hauptachse")
        self.delete("s_axis")
        self.itemconfigure("orig_axes",state="normal")
        self.itemconfig(self.pos_lbl, text="")
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
                if abs(pos[0]-XCENTER) < EPSILON: #left side sticks to the coordinatsystem
                    self.current.refresh(XCENTER,pos[1],XCENTER+self.current.width,pos[3])
                    pos = self.coords(self.current.canvas_repr)
                elif abs(pos[2]-XCENTER) < EPSILON: #right side sticks to the coordinatsystem
                    self.current.refresh(XCENTER-self.current.width,pos[1],XCENTER,pos[3])
                    pos = self.coords(self.current.canvas_repr)
                if abs(pos[1]-YCENTER) < EPSILON: #top side sticks to the coordinatsystem
                    self.current.refresh(pos[0],YCENTER,pos[2],YCENTER+self.current.heigth)
                    pos = self.coords(self.current.canvas_repr)
                elif abs(pos[3]-YCENTER) < EPSILON: #bottomí side sticks to the coordinatsystem
                    self.current.refresh(pos[0],YCENTER-self.current.heigth,pos[2],YCENTER)
                    pos = self.coords(self.current.canvas_repr)
                #* Sticking with the center of the rectangle to the coordinate system
                if abs(self.current.center[0]-XCENTER)<EPSILON:
                    self.current.refresh(XCENTER-self.current.width/2,self.current.y1,XCENTER+self.current.width/2,self.current.y2)
                if abs(self.current.center[1]-YCENTER)<EPSILON:
                    self.current.refresh(self.current.x1,YCENTER-self.current.heigth/2,self.current.x2,YCENTER+self.current.heigth/2)
        if self.isMoving and self.current is not None:
            self.itemconfig(self.current.canvas_repr, fill='blue')
            self.rectangles.append(self.current)
            for k in self.rectangles:
                k.is_overlapping()
            #self.current.is_overlapping()
            
            
        self.isMoving = False
        self.current=None
        self.label.config(text="")
    def calculate(self):
        Ix = 0
        Iy = 0
        Ixy = 0
        A = 0
        if not FIXED_AXIS:
            Sx=0
            Sy=0
            for i in self.rectangles:
                A += i.area
                Sx += (i.center[0]-XCENTER)*i.area
                Sy += (YCENTER-i.center[1])*i.area
            Sx /= A
            Sy /= A
            Sx += XCENTER
            Sy = YCENTER- Sy
            self.sx_axis = self.create_line(10,Sy,Sx*2,Sy, arrow=tk.LAST, tags=("s_axis")) #Drawing X-axis
            self.sx_label = self.create_text(2*Sx-5,Sy+ 20,text="X",tags=("s_axis")) # X lavel
            self.sy_axis = self.create_line(Sx,10,Sx,Sy*2, arrow=tk.FIRST,tags=("s_axis")) #Drawing Y-axis
            self.sy_label = self.create_text(Sx +20 ,15,text="Y",tags=("s_axis")) # Y label
            self.itemconfigure("orig_axes",state="hidden")
            print(Sx/self.scale,Sy/self.scale)
        else:
            Sx = XCENTER
            Sy = YCENTER
        A = 0
        for i in self.rectangles:
            pos = self.coords(i.canvas_repr)
            A_current = (pos[2]-pos[0]) * (pos[3]-pos[1])
            A += A_current
            Ix += ((pos[2]-pos[0]) * (pos[3]-pos[1])**3 )/12+ A_current*(Sy-pos[1]-(pos[3]-pos[1])/2)**2
            Iy += (pos[2]-pos[0])**3 * (pos[3]-pos[1]) /12+ A_current*(pos[0]+(pos[2]-pos[0])/2-Sx)**2
              
            Ixy += A_current*(pos[0]+(pos[2]-pos[0])/2-Sx)*(Sy-pos[1]-(pos[3]-pos[1])/2) 
        self.label.config(text=f"A: {A/self.scale**2} mm\nIx: {Ix/self.scale**4} mm\nIy: {Iy/self.scale**4} mm\nIxy: {Ixy/self.scale**4}")
        print(self.hauptachsen(Ix/self.scale**4,Iy/self.scale**4,Ixy/self.scale**4))
    def overwrite(self):
        try:
            w=float(self.e1.get().replace(',','.'))*self.scale
            if w <=0:
                raise ValueError
            self.width = w
            self.e1.config({"background": self.root.colors['secondary_color']})
        except:
            print("Hiba, az egyik mező nem olvashó be")
            self.e1.config({"background": "#eb4034"})
            return -1
        try:
            h = float(self.e2.get().replace(',','.'))*self.scale
            if h <=0:
                raise ValueError
            self.heigth = h
            self.e2.config({"background": self.root.colors['secondary_color']})
        except:
            print("Hiba, az egyik mező nem olvashó be")
            self.e2.config({"background": "#eb4034"})
            return -1
        self.coords(self.alap_negyzet.canvas_repr, 10,10,10+self.width,10+self.heigth)
        self.coords(self.width_label,25+self.width,10+ self.heigth/2)
        self.coords(self.height_label,10+self.width/2,self.heigth+ 25)
        self.itemconfig(self.height_label, text=str(self.width/self.scale))
        self.itemconfig(self.width_label,text=str(self.heigth/self.scale))
    def clear_all(self):
        self.rectangles = []
        self.delete("rect") 
        self.delete("hauptachse")
        self.delete("s_axis")
        self.label.config(text="")   
    def hauptachsen(self, Ix, Iy, Ixy):
        I1 = (Ix+Iy)/2 + 0.5*sqrt((Ix-Iy)**2 + 4* Ixy**2)
        I2 = (Ix+Iy)/2 - 0.5*sqrt((Ix-Iy)**2 + 4* Ixy**2)
        if Ix != Iy and Ixy !=0:
            alfa = atan((Ix-I1)/Ixy)
        else:
            alfa = 0
        if SHOW_HAUPACHSEN:
            self.h1 = self.create_line(XCENTER-250*cos(alfa),YCENTER-250*sin(alfa),XCENTER+250*cos(alfa),YCENTER+250*sin(alfa), arrow=tk.LAST, fill=self.root.colors['draw_main'],tags=("hauptachse"))
            self.h2 = self.create_line(XCENTER-250*cos(alfa+pi/2),YCENTER-250*sin(alfa+pi/2),XCENTER+250*cos(alfa+pi/2),YCENTER+250*sin(alfa+pi/2), arrow=tk.LAST, fill=self.root.colors['draw_main'],tags=("hauptachse"))
            #self.lower(self.h1)
            #self.lower(self.h2)
        return I1, I2, alfa
    def rescale(self,scale):
        self.scale *= scale
        self.alap_negyzet.refresh(10,10,10+self.width*scale,10+self.heigth*scale)
        self.width *= scale
        self.heigth *= scale
        #self.itemconfig('rect', fill='white')
        self.coords(self.width_label,25+self.width,10+ self.heigth/2)
        self.coords(self.height_label,10+self.width/2,self.heigth+ 25)
        for i in self.rectangles:
            i.refresh(XCENTER-(XCENTER-i.x1)*scale, YCENTER-(YCENTER-i.y1)*scale, XCENTER-(XCENTER - i.x2)*scale, YCENTER-(YCENTER-i.y2)*scale)
    def resize_canvas(self,e):
        self.coords(self.minus, e.width-45, e.height-50)
        self.coords(self.plus, e.width-80, e.height-50)
        self.coords(self.pos_lbl, e.width-50, 30)
        


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
        self.overlapping_with = []
    def refresh(self,x1,y1,x2,y2):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.width = self.x2-self.x1
        self.heigth = self.y2-self.y1
        self.area = self.width*self.heigth
        self.center=(self.x1+self.width/2, self.y1+self.heigth/2)
        self.canvas.coords(self.canvas_repr,x1,y1,x2,y2)
    def is_overlapping(self):
        a=list(self.canvas.find_overlapping(self.x1,self.y1,self.x2,self.y2))
        a.remove(self.canvas_repr)
        #self.canvas.itemconfig(self.canvas_repr, fill='red')
        #self.overlapping_with.append(a[:])
        in_overlapping = False
        for i in self.canvas.rectangles:
            if i.canvas_repr in a:
                if len({self.x1,self.x2}.intersection({i.x1,i.x2}))==0 and len({self.y1,self.y2}.intersection({i.y1,i.y2}))==0:
                    self.canvas.itemconfig(self.canvas_repr, fill='red')
                    in_overlapping = True
        if not in_overlapping:
            self.canvas.itemconfig(self.canvas_repr, fill='blue')
                #self.overlapping_with.append(i)
                #i.overlapping_with.append(self)
                #self.canvas.itemconfig(i.canvas_repr, fill='red')
    def is_overlapping_old(self):
        #! with different-size rectangles doesm't works properly
        for i in self.canvas.rectangles:
            if self.x1 <i.x2 and self.x1> i.x1 and self.y1 > i.y1 and self.y1 < i.y2: #top left corner is in the rectangle
                self.canvas.itemconfig(self.canvas.current.canvas_repr, fill='red')
                self.overlapping_with.append(i)
                i.overlapping_with.append(self)
                self.canvas.itemconfig(i.canvas_repr, fill='red')
            elif self.x1 <i.x2 and self.x1> i.x1 and self.y2 > i.y1 and self.y2 < i.y2: #bottom left corner is in the rectangle
                self.canvas.itemconfig(self.canvas.current.canvas_repr, fill='red')
                self.overlapping_with.append(i)
                i.overlapping_with.append(self)
                self.canvas.itemconfig(i.canvas_repr, fill='red')
            elif self.x2 <i.x2 and self.x2> i.x1 and self.y2 > i.y1 and self.y2 < i.y2: #bottom right corner is in the rectangle
                self.canvas.itemconfig(self.canvas.current.canvas_repr, fill='red')
                self.overlapping_with.append(i)
                i.overlapping_with.append(self)
                self.canvas.itemconfig(i.canvas_repr, fill='red')
            elif self.x2 <i.x2 and self.x2> i.x1 and self.y1 > i.y1 and self.y1 < i.y2: #top right corner is in the rectangle
                self.canvas.itemconfig(self.canvas.current.canvas_repr, fill='red')
                self.overlapping_with.append(i)
                i.overlapping_with.append(self)
                self.canvas.itemconfig(i.canvas_repr, fill='red')
            elif i in self.overlapping_with:
                self.overlapping_with.remove(i)
                i.overlapping_with.remove(self)
                if len(i.overlapping_with)==0:
                    i.canvas.itemconfig(i.canvas_repr, fill='blue')
        if len(self.overlapping_with) == 0:
            self.canvas.itemconfig(self.canvas_repr, fill='blue')

            
class sb_side_menu(tk.Frame):
    def __init__(self,root):
        super().__init__(root,width=30, bg=root.colors['secondary_color'])
        self.root = root
