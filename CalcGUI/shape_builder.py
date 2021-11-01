import tkinter as tk
from math import cos, sin, sqrt, atan, pi
from tkinter.constants import ANCHOR, CENTER, FALSE, NO, TRUE
from PIL import ImageTk,Image
import keyboard
WIDTH = 30
EPSILON = 10
STICKY = True

#! Selection_error: Rectangle not found...

#self.root.sb_ha_vis = False
#self.root.calc_for_orig_axis = False
#self.root.show_orig_axis = True
#self.root.orig_axis_dissapier = False

class shapeBuilder(tk.Canvas):
    def __init__(self, root, sb_sm):
        super().__init__(root, bd=0, bg=root.colors["secondary_color"],highlightthickness=0)
        self.root=root
        self.sb_sm = sb_sm #own side menu
        self.scale = 10 #scale between drawing and given value
        self.rectangles = []
        self.Xcenter = 400
        self.Ycenter = 300
        self.canvas_width = 800
        self.canvas_height = 600

        #########* Basic constants #########
        self.current = None
        self.isMoving=False
        self.width = WIDTH
        self.heigth = WIDTH
        self.last_click_pos = None
        self.starting_pos = None #selecting multiple objects
        self.selecting_area = self.create_rectangle(0,0,0,0)
        self.selected = []

        #############* Creating objects for side menu ##############
        self.label = tk.Label(self.sb_sm,text="", bg=self.sb_sm["background"], fg=root.colors["text_color"])
        self.l_width = tk.Label(self.sb_sm,text="Szélesség", bg=self.sb_sm["background"], fg=root.colors["text_color"])
        self.l_heigth = tk.Label(self.sb_sm,text="Magasság", bg=self.sb_sm["background"], fg=root.colors["text_color"])
        self.l_unit1 = tk.Label(self.sb_sm,text=root.unit, bg=self.sb_sm["background"], fg=root.colors["text_color"])
        self.l_unit2 = tk.Label(self.sb_sm,text=f"{self.root.unit}", bg=self.sb_sm["background"], fg=root.colors["text_color"])
        self.button = tk.Button(self.sb_sm, text="Számolás", command=self.calculate)
        self.e1 = tk.Entry(self.sb_sm,bg=root.colors["entry_color"], fg=root.colors["text_color"])
        self.e2 = tk.Entry(self.sb_sm,bg=root.colors["entry_color"], fg=root.colors["text_color"])
        self.button2 = tk.Button(self.sb_sm, text="Értékadás", command=self.overwrite)
        self.cls = tk.Button(self.sb_sm,text="Minden törlése", command=self.clear_all)
        #self.pos_lbl = tk.Label(self,text="", bg=self.sb_sm["background"], fg=root.colors["text_color"])
        self.pos_lbl = self.create_text(15 ,15,text="",fill= "white") # position label

        self.controls = []
        self.controls.append({"unit":self.l_unit1, "unit_type": "length"})
        self.controls.append({"unit":self.l_unit2, "unit_type": "length"})

        #############* Creating + and - buttons ##############
        self.img= (Image.open("plus.png"))
        resized_image= self.img.resize((30,30), Image.ANTIALIAS)
        self.plus_img= ImageTk.PhotoImage(resized_image)
        self.img= (Image.open("minus.png"))
        resized_image= self.img.resize((30,30), Image.ANTIALIAS)
        self.minus_img= ImageTk.PhotoImage(resized_image)
        self.minus= self.create_image(self.root.winfo_width()-310, self.root.winfo_height()-50, anchor=tk.NW,image=self.minus_img, tags=("plus_minus"))
        self.plus= self.create_image(self.root.winfo_width()-275, self.root.winfo_height()-50, anchor=tk.NW,image=self.plus_img, tags=("plus_minus"))
        self.tag_bind(self.plus, '<Button-1>', lambda e: self.rescale(2))
        self.tag_bind(self.minus, '<Button-1>', lambda e: self.rescale(0.5))
        
        ###########* Creating the basic, green rectangle #############
        self.alap = self.create_rectangle(10,10,10+WIDTH,10+WIDTH,fill="green")
        self.alap_negyzet = Rectangle(self,10,10,10+WIDTH,10+WIDTH, self.alap)
        self.width_label = self.create_text(20+self.width,10+ self.heigth/2,text=str(self.width/10))
        self.height_label = self.create_text(10+self.width/2,self.heigth+ 20,text=str(self.heigth/10))

        ##########* Creating axis #############
        self.x_axis = self.create_line(10,self.Ycenter,self.Xcenter*2,self.Ycenter, arrow=tk.LAST, fill= "gray", tags=("orig_axes")) #Drawing X-axis
        self.x_label = self.create_text(2*self.Xcenter-5,self.Ycenter+ 20,text="X",fill= "gray",tags=("orig_axes")) # X lavel
        self.y_axis = self.create_line(self.Xcenter,10,self.Xcenter,self.Ycenter*2, arrow=tk.FIRST,fill= "gray",tags=("orig_axes")) #Drawing Y-axis
        self.y_label = self.create_text(self.Xcenter +20 ,15,text="Y",fill= "gray",tags=("orig_axes")) # Y label
        if not self.root.show_orig_axis: self.itemconfigure("orig_axes",state="hidden")
        #########* Evensts and other stuff ############
        self.sticky = tk.BooleanVar(value=True)
        self.is_sticky = tk.Checkbutton(self.sb_sm, text="Automatikus igazítás", variable=self.sticky, onvalue=True, offvalue=False,bg = self.sb_sm["background"], fg=root.colors["text_color"], selectcolor=root.colors['secondary_color'])
        self.bind('<B1-Motion>',self.move) #"drag-and-drop" action
        self.bind('<ButtonRelease-1>',self.release) #when you relase the left mose button
        self.popup_menu = tk.Menu(self, tearoff=0) #right click menu
        self.popup_menu.add_command(label="Delete",command=self.delete_rectangle)
        self.popup_menu.add_command(label="Resize",command=self.resize_rectangle)
        self.popup_menu.add_command(label="Info",command=self.rectangle_info)
        self.bind("<Button-3>", self.popup) # right-click event
        self.bind("<Configure>", self.resize_canvas)
        #self.tag_bind("rect",'<Double-Button-1>',self.select)
        self.tag_bind("rect",'<Button-1>',self.select)
        self.bind("<Button-1>", self.deselect)
        self.bind("<Motion>", lambda e: self.itemconfig(self.pos_lbl, text=f"x: {(e.x-self.Xcenter)/self.scale} y: {(self.Ycenter-e.y)/self.scale}"))
        self.root.bind("<Delete>", self.delete_rectangle)
        self.root.bind("<Control-i>", self.rectangle_info)
        self.root.bind("<Control-r>", self.resize_rectangle)

        ##############* Packing objects ###############
        self.l_width.grid(row=1,column=0)
        self.e1.grid(row=1,column=1,columnspan=3)
        self.l_unit1.grid(row=1,column=4)
        self.l_heigth.grid(row=2,column=0)
        self.e2.grid(row=2,column=1,columnspan=3)
        self.l_unit2.grid(row=2,column=4)
        self.is_sticky.grid(row=3,columnspan=5)
        self.button.grid(row=4,column=3)
        self.button2.grid(row=4, column=1)
        self.label.grid(row=5,columnspan=5, pady= 50)
        self.cls.grid(row=6, column=1,columnspan=3)

    def popup(self, e): #right cklick menu shows up
        if not self.isMoving:
            for i in self.rectangles:
                pos = self.coords(i.canvas_repr)
                if e.x>=pos[0] and e.x<=pos[2] and e.y>=pos[1] and e.y <=pos[3]:
                    self.select(e)
                    try:
                        self.popup_menu.tk_popup(e.x_root, e.y_root, 0)
                    finally:
                        self.popup_menu.grab_release()
                    break
    def delete_rectangle(self, e=None):
        print("deleteing rectangle")
        for i in self.selected:
            self.delete(i.canvas_repr)
            self.rectangles.remove(i)
            self.selected = []
        for k in self.rectangles:
            k.is_overlapping()
    def resize_rectangle(self,e=None):
        for i in self.selected:
            i.refresh(i.x1, i.y1, i.x1 + self.width, i.y1 + self.heigth)
            i = None
        for k in self.rectangles:
            k.is_overlapping()
    def rectangle_info(self,e=None):
        if len(self.selected)>1:
            self.label.config(text="Hiba: Túl sok objektum van kijelölve!")
            return -1
        if len(self.selected)>0: self.label.config(text=f"Szélesség = {self.selected[0].width/self.scale}\nMagasság = {self.selected[0].heigth/self.scale}\nKözéppont = ({(self.selected[0].center[0]-self.Xcenter)/self.scale},{(self.Ycenter-self.selected[0].center[1])/self.scale})" )
        
    def select(self,e, object=None):
        #self.deselect()
        if e is None and object is not None:
            self.selected.append(object)
            for i in self.selected:
                self.itemconfig(i.canvas_repr, fill='pink')
            return 0
        tmp = self.find_closest(e.x,e.y)[0]
        for i in self.rectangles:
            if i.canvas_repr == tmp and i not in self.selected:
                self.selected.append(i)
                break
        else:
            print("Selection_Error: Rectangle not found...")
            return -1  
        for i in self.selected:
            self.itemconfig(i.canvas_repr, fill='pink')
        print("Selecting rectangle")
    def deselect(self,e=None):
        if e is not None:
            for i in self.rectangles:
                if e.x < i.x2 and e.x> i.x1 and i.y1 < e.y and i.y2 > e.y:
                    return 0
        try:
            for i in self.selected:
                print("deselect")
                self.itemconfig(i.canvas_repr, fill='blue')
            self.selected = []
        except:
            pass
        for k in self.rectangles:
            k.is_overlapping()
    def move(self,e):
        if keyboard.is_pressed("Ctrl"):
            if self.last_click_pos is None:
                self.last_click_pos = (e.x, e.y)
            else:
                self.translation(e.x-self.last_click_pos[0],e.y-self.last_click_pos[1])
                self.last_click_pos = (e.x, e.y)
            return 0
        self.itemconfig(self.pos_lbl, text=f"x: {(e.x-self.Xcenter)/self.scale} y: {(self.Ycenter-e.y)/self.scale}")
        self.deselect()
        self.label.config(text=f"")
        #choosing object
        for i in self.rectangles:
            pos = self.coords(i.canvas_repr)
            if self.current is None and e.x>=pos[0] and e.x<=pos[2] and e.y>=pos[1] and e.y <=pos[3] and self.starting_pos is None:
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
            ############### Selecting multiple objects ##############
            if self.starting_pos is None: 
                print("test")
                self.starting_pos = (e.x,e.y)
                self.itemconfigure(self.selecting_area,state="normal")
            else:
                try:
                    self.coords(self.selecting_area,self.starting_pos[0],self.starting_pos[1],e.x,e.y)
                except:
                    print("Can not show selection area")
            return -1
        pos = self.coords(self.current.canvas_repr)
        if self.isMoving or e.x>=pos[0] and e.x<=pos[2] and e.y>=pos[1] and e.y <=pos[3]:
            self.current.refresh(e.x-self.current.width/2,e.y-self.current.heigth/2,e.x+self.current.width/2,e.y+self.current.heigth/2)
            self.isMoving = True
            return 0
        
    def release(self,e):
        self.delete("hauptachse")
        self.delete("s_axis")
        if self.root.show_orig_axis:self.itemconfigure("orig_axes",state="normal")
        self.itemconfig(self.pos_lbl, text="")
        #choosing object
        if self.sticky.get() and self.current:
            pos = self.coords(self.current.canvas_repr)
            #? prioritási sorrend???    
            # sticking to another rectangles    
            for i in self.rectangles:
                i_pos = self.coords(i.canvas_repr)
                if abs(pos[0] - i_pos[0]) < EPSILON and abs(pos[1] - i_pos[3]) < EPSILON: # current rect goes under the another 
                    self.current.refresh(i_pos[0],i_pos[3],i_pos[0]+self.current.width,i_pos[3]+self.current.heigth)
                    break
                elif abs(pos[0] - i_pos[0]) < EPSILON and abs(pos[3] - i_pos[1]) < EPSILON: # TOP
                    self.current.refresh(i_pos[0],i_pos[1]-self.current.heigth,i_pos[0]+self.current.width,i_pos[1])
                    break
                elif abs(pos[1] - i_pos[1]) < EPSILON and abs(pos[0] - i_pos[2]) < EPSILON: # RIGHT
                    self.current.refresh(i_pos[2],i_pos[1],i_pos[2]+self.current.width,i_pos[1]+self.current.heigth)
                    break
                elif abs(pos[1] - i_pos[1]) < EPSILON and abs(pos[2] - i_pos[0]) < EPSILON: # LEFT
                    self.current.refresh(i_pos[0]-self.current.width,i_pos[1],i_pos[0],i_pos[1]+self.current.heigth)
                    break
                elif abs(pos[2] - i_pos[2]) < EPSILON and abs(pos[3] - i_pos[1]) < EPSILON: # ??
                    self.current.refresh(i_pos[2]-self.current.width,i_pos[1]-self.current.heigth,i_pos[2],i_pos[1])
                    break
                elif abs(pos[2] - i_pos[0]) < EPSILON and abs(pos[3] - i_pos[3]) < EPSILON: # ??
                    self.current.refresh(i_pos[0]-self.current.width,i_pos[3]-self.current.heigth,i_pos[0],i_pos[3])
                    break
                elif abs(pos[0] - i_pos[2]) < EPSILON and abs(pos[3] - i_pos[3]) < EPSILON: # !
                    self.current.refresh(i_pos[2],i_pos[3]-self.current.heigth,i_pos[2]+self.current.width,i_pos[3])
                    break
                elif abs(pos[2] - i_pos[2]) < EPSILON and abs(pos[1] - i_pos[3]) < EPSILON: # !
                    self.current.refresh(i_pos[2]-self.current.width,i_pos[3],i_pos[2],i_pos[3]+self.current.heigth)
                    break
            else: #sicking to the coordinate system
                if self.root.show_orig_axis:
                    if abs(pos[0]-self.Xcenter) < EPSILON: #left side sticks to the coordinatsystem
                        self.current.refresh(self.Xcenter,pos[1],self.Xcenter+self.current.width,pos[3])
                        pos = self.coords(self.current.canvas_repr)
                    elif abs(pos[2]-self.Xcenter) < EPSILON: #right side sticks to the coordinatsystem
                        self.current.refresh(self.Xcenter-self.current.width,pos[1],self.Xcenter,pos[3])
                        pos = self.coords(self.current.canvas_repr)
                    if abs(pos[1]-self.Ycenter) < EPSILON: #top side sticks to the coordinatsystem
                        self.current.refresh(pos[0],self.Ycenter,pos[2],self.Ycenter+self.current.heigth)
                        pos = self.coords(self.current.canvas_repr)
                    elif abs(pos[3]-self.Ycenter) < EPSILON: #bottomí side sticks to the coordinatsystem
                        self.current.refresh(pos[0],self.Ycenter-self.current.heigth,pos[2],self.Ycenter)
                        pos = self.coords(self.current.canvas_repr)
                    #* Sticking with the center of the rectangle to the coordinate system
                    if abs(self.current.center[0]-self.Xcenter)<EPSILON:
                        self.current.refresh(self.Xcenter-self.current.width/2,self.current.y1,self.Xcenter+self.current.width/2,self.current.y2)
                    if abs(self.current.center[1]-self.Ycenter)<EPSILON:
                        self.current.refresh(self.current.x1,self.Ycenter-self.current.heigth/2,self.current.x2,self.Ycenter+self.current.heigth/2)
        if self.isMoving and self.current is not None:
            #self.itemconfig(self.current.canvas_repr, fill='blue')
            self.rectangles.append(self.current)
            for k in self.rectangles:
                k.is_overlapping()
            #self.current.is_overlapping()
        if self.starting_pos is not None:
            mwc = min(self.starting_pos[0],e.x)
            mec = max(self.starting_pos[0],e.x)
            mnc = min(self.starting_pos[1],e.y)
            msc = max(self.starting_pos[1],e.y)
            for i in self.rectangles:    
                if i.center[0] > mwc and i.center[0]< mec and i.center[1] > mnc and i.center[1] < msc:
                    self.select(None, i)
            self.coords(self.selecting_area,mwc,mnc,mec,msc)
            self.starting_pos = None
        else:
            self.itemconfigure(self.selecting_area,state="hidden")
            
            
        self.isMoving = False
        self.current=None
        self.label.config(text="")
        self.itemconfig(self.pos_lbl, text=f"x: {(e.x-self.Xcenter)/self.scale} y: {(self.Ycenter-e.y)/self.scale}")
        self.tag_raise("plus_minus")
        self.tag_raise(self.pos_lbl)
        self.last_click_pos = None
    def calculate(self):
        if len(self.rectangles) == 0:
            self.label.config(text=f"A: 0 mm\nIx: 0 mm\nIy: 0 mm\nIxy: 0")
            return -1
        Ix = 0
        Iy = 0
        Ixy = 0
        A = 0
        out_str = ""
        if not self.root.calc_for_orig_axis:
            Sx=0
            Sy=0
            for i in self.rectangles:
                A += i.area
                Sx += (i.center[0]-self.Xcenter)*i.area
                Sy += (self.Ycenter-i.center[1])*i.area
            Sx /= A
            Sy /= A
            Sx += self.Xcenter
            Sy = self.Ycenter- Sy
            a_length = min(min(Sx,Sy),self.canvas_height-Sy,self.canvas_width-Sx)
            self.sx_axis = self.create_line(Sx+10-a_length,Sy,Sx+a_length-10,Sy, arrow=tk.LAST, tags=("s_axis")) #Drawing X-axis
            self.sx_label = self.create_text(Sx+a_length-20,Sy+ 20,text="Xs",tags=("s_axis")) # X lavel
            self.sy_axis = self.create_line(Sx,Sy-a_length+10,Sx,Sy+a_length-10, arrow=tk.FIRST,tags=("s_axis")) #Drawing Y-axis
            self.sy_label = self.create_text(Sx +20 ,Sy-a_length+20 ,text="Ys",tags=("s_axis")) # Y label
            if self.root.orig_axis_dissapier: self.itemconfigure("orig_axes",state="hidden")
            print(Sx/self.scale,Sy/self.scale)
            out_str += f"Sx: {Sx/self.scale}\nSy: {Sy/self.scale}\n"
        else:
            out_str += "Számítások fix tengelyre:\n"
            Sx = self.Xcenter
            Sy = self.Ycenter
            a_length = min(min(Sx,Sy),self.canvas_height-Sy,self.canvas_width-Sx)
        A = 0
        for i in self.rectangles:
            pos = self.coords(i.canvas_repr)
            A_current = (pos[2]-pos[0]) * (pos[3]-pos[1])
            A += A_current
            Ix += ((pos[2]-pos[0]) * (pos[3]-pos[1])**3 )/12+ A_current*(Sy-pos[1]-(pos[3]-pos[1])/2)**2
            Iy += (pos[2]-pos[0])**3 * (pos[3]-pos[1]) /12+ A_current*(pos[0]+(pos[2]-pos[0])/2-Sx)**2
              
            Ixy += A_current*(pos[0]+(pos[2]-pos[0])/2-Sx)*(Sy-pos[1]-(pos[3]-pos[1])/2) 
        out_str += f"A: {A/self.scale**2} mm\nIx: {Ix/self.scale**4} mm\nIy: {Iy/self.scale**4} mm\nIxy: {Ixy/self.scale**4}\n"
        i1, i2, alpha = self.hauptachsen(Ix/self.scale**4,Iy/self.scale**4,Ixy/self.scale**4, Sx,Sy,a_length)
        out_str += f"I_1 = {i1}\nI_2 = {i2}\nalpa = {alpha}"
        self.label.config(text=out_str)
        
    def overwrite(self):
        ok = True
        try:
            w=float(self.e1.get().replace(',','.'))*self.scale
            if w <=0:
                raise ValueError
            #self.width = w
            self.e1.config({"background": self.root.colors['secondary_color']})
        except:
            print("Hiba, az egyik mező nem olvashó be")
            self.e1.config({"background": "#eb4034"})
            ok = False
        try:
            h = float(self.e2.get().replace(',','.'))*self.scale
            if h <=0:
                raise ValueError
            #self.heigth = h
            self.e2.config({"background": self.root.colors['secondary_color']})
        except:
            print("Hiba, az egyik mező nem olvashó be")
            self.e2.config({"background": "#eb4034"})
            ok=False
        if not ok: return -1
        self.width = w
        self.heigth = h
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
    def hauptachsen(self, Ix, Iy, Ixy, Sx, Sy, a_length):
        I1 = (Ix+Iy)/2 + 0.5*sqrt((Ix-Iy)**2 + 4* Ixy**2)
        I2 = (Ix+Iy)/2 - 0.5*sqrt((Ix-Iy)**2 + 4* Ixy**2)
        if Ix != Iy and Ixy !=0:
            alfa = atan((Ix-I1)/Ixy)
        else:
            alfa = 0
        if self.root.sb_ha_vis:
            self.h1 = self.create_line(Sx-a_length*cos(alfa),Sy-a_length*sin(alfa),Sx+a_length*cos(alfa),Sy+a_length*sin(alfa), arrow=tk.LAST, fill=self.root.colors['draw_main'],tags=("hauptachse"))
            self.h2 = self.create_line(Sx-a_length*cos(alfa+pi/2),Sy-a_length*sin(alfa+pi/2),Sx+a_length*cos(alfa+pi/2),Sy+a_length*sin(alfa+pi/2), arrow=tk.FIRST, fill=self.root.colors['draw_main'],tags=("hauptachse"))
        return I1, I2, alfa
    def rescale(self,scale):
        self.scale *= scale
        self.alap_negyzet.refresh(10,10,10+self.width*scale,10+self.heigth*scale)
        self.width *= scale
        self.heigth *= scale
        self.coords(self.width_label,25+self.width,10+ self.heigth/2)
        self.coords(self.height_label,10+self.width/2,self.heigth+ 25)
        for i in self.rectangles:
            i.refresh(self.Xcenter-(self.Xcenter-i.x1)*scale, self.Ycenter-(self.Ycenter-i.y1)*scale, self.Xcenter-(self.Xcenter - i.x2)*scale, self.Ycenter-(self.Ycenter-i.y2)*scale)
    def resize_canvas(self,e):
        self.coords(self.minus, e.width-45, e.height-50)
        self.coords(self.plus, e.width-80, e.height-50)
        self.coords(self.pos_lbl, e.width-50, 30)
        self.canvas_width = e.width
        self.canvas_height = e.height
        self.translation(e.width/2-self.Xcenter, e.height/2-self.Ycenter)
        self.delete("s_axis")
        self.delete("hauptachse")
    def translation(self, dx, dy):
        self.Xcenter += dx
        self.Ycenter += dy
        # Basic coord system
        """
        self.coords(self.x_axis,10,self.Ycenter,self.Xcenter*2,self.Ycenter)
        self.coords(self.y_axis,self.Xcenter,10,self.Xcenter,self.Ycenter*2)
        self.coords(self.x_label,2*self.Xcenter-5,self.Ycenter+ 20)
        self.coords(self.y_label,self.Xcenter +20 ,15)
        """
        self.coords(self.x_axis,10,self.Ycenter,self.canvas_width-10,self.Ycenter)
        self.coords(self.y_axis,self.Xcenter,10,self.Xcenter,self.canvas_height-10)
        self.coords(self.x_label,2*self.Xcenter-5,self.Ycenter+ 20)
        self.coords(self.y_label,self.Xcenter +20 ,15)
        #Rectangles
        for i in self.rectangles:
            i.refresh(i.x1+dx,i.y1+dy,i.x2+dx,i.y2+dy)
    def place_objekt(self,x,y,object):
        object.refresh(x,y,x+object.width,y+object.heigth) #rectangle

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
        in_overlapping = False
        for i in self.canvas.rectangles:
            if i.canvas_repr in a:
                if len({self.x1,self.x2}.intersection({i.x1,i.x2}))==0 and len({self.y1,self.y2}.intersection({i.y1,i.y2}))==0:
                    self.canvas.itemconfig(self.canvas_repr, fill='red')
                    in_overlapping = True
        if not in_overlapping and self not in self.canvas.selected:
            print(self, self.canvas.selected)
            self.canvas.itemconfig(self.canvas_repr, fill='blue')
            
class sb_side_menu(tk.Frame):
    def __init__(self,root):
        super().__init__(root,width=30, bg=root.colors['secondary_color'])
        self.root = root
