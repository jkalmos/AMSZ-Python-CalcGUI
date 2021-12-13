import tkinter as tk
from math import cos, radians, sin, sqrt, atan, asin, pi, degrees
from tkinter.constants import ANCHOR, CENTER, FALSE, NO, TRUE
from PIL import ImageTk,Image
import keyboard
from itertools import cycle
WIDTH = 30
EPSILON = 10
STICKY = True
from shapes import Rectangle, Arc, Shapes, dist
#* https://structx.com/Shape_Formulas_004.html
#* https://hu.wikipedia.org/wiki/K%C3%B6rcikk

#TODO: Overlapping not recognized while alignig rects
#TODO: WARNING: Kijelölö négyzet használata közben tudunk új körcikkelyeket generálni... 
#TODO: X-label elúszik a canvas mozgatásakor...

class shapeBuilder(tk.Canvas):
    def __init__(self, root, sb_sm):
        super().__init__(root, bd=0, bg=root.colors["secondary_color"],highlightthickness=0)
        self.root=root
        self.sb_sm = sb_sm #own side menu
        self.scale = 10 #scale between drawing and given value
        self.rectangles = []
        self.arcs = []
        self.shapes = Shapes(self,self.rectangles,self.arcs)
        self.clipboard = []
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
        self.active_shape = "Rectangle"
        self.possible_shape_list = ["Rectangle","Semicircle","quartrer_circle"]
        self.possible_shapes = cycle(self.possible_shape_list)
        next(self.possible_shapes)

        #############* Creating objects for side menu ##############
        # self.place_holder = tk.Label(self.sb_sm,text="",width=30, bg=self.sb_sm["background"], fg=root.colors["text_color"])
        #Gege megoldása az eredményekre: self.label = tk.Label(self.sb_sm,text="EMPTY LABEL", bg=self.sb_sm["background"], fg=root.colors["text_color"])
        # self.results_label = tk.Label(self.sb_sm,text="results label", bg=self.sb_sm["background"], fg=root.colors["text_color"])
        self.l_width = tk.Label(self.sb_sm,text="Szélesség:", bg=self.sb_sm["background"], fg=root.colors["text_color"])
        self.l_heigth = tk.Label(self.sb_sm,text="Magasság:", bg=self.sb_sm["background"], fg=root.colors["text_color"])
        self.l_unit1 = tk.Label(self.sb_sm,text=root.unit, bg=self.sb_sm["background"], fg=root.colors["text_color"])
        self.l_unit2 = tk.Label(self.sb_sm,text=f"{self.root.unit}", bg=self.sb_sm["background"], fg=root.colors["text_color"])
        self.buttonimage = tk.PhotoImage(file=f"{root.colors['path']}shape_builder/calculate_button.png")
        self.calc_button = tk.Label(self.sb_sm, image=self.buttonimage, activebackground=self["background"], border = 0, bg =self["background"])
        self.calc_button.bind('<Button-1>', func=lambda e: self.calculate())
        self.e1 = tk.Entry(self.sb_sm, width = 10,bg=root.colors["entry_color"], fg=root.colors["text_color"])
        self.e2 = tk.Entry(self.sb_sm, width = 10,bg=root.colors["entry_color"], fg=root.colors["text_color"])

        # result fonts
        self.result_font = "Roboto", 10

        ## result labels ##
        self.results = tk.Label(self.sb_sm,text="", bg=self.sb_sm["background"], fg=root.colors["text_color"], font=self.result_font)
        self.result1 =  tk.Label(self.sb_sm,text="", bg=self.sb_sm["background"], fg=root.colors["text_color"], font=self.result_font)
        self.result2 =  tk.Label(self.sb_sm,text="", bg=self.sb_sm["background"], fg=root.colors["text_color"], font=self.result_font)
        self.result3 =  tk.Label(self.sb_sm,text="", bg=self.sb_sm["background"], fg=root.colors["text_color"], font=self.result_font)
        self.result4 =  tk.Label(self.sb_sm,text="", bg=self.sb_sm["background"], fg=root.colors["text_color"], font=self.result_font)
        self.result5 =  tk.Label(self.sb_sm,text="", bg=self.sb_sm["background"], fg=root.colors["text_color"], font=self.result_font)
        self.result6 =  tk.Label(self.sb_sm,text="", bg=self.sb_sm["background"], fg=root.colors["text_color"], font=self.result_font)
        self.result7 =  tk.Label(self.sb_sm,text="", bg=self.sb_sm["background"], fg=root.colors["text_color"], font=self.result_font)
        self.result8 =  tk.Label(self.sb_sm,text="", bg=self.sb_sm["background"], fg=root.colors["text_color"], font=self.result_font)
        self.result9 =  tk.Label(self.sb_sm,text="", bg=self.sb_sm["background"], fg=root.colors["text_color"], font=self.result_font)
        self.result10 =  tk.Label(self.sb_sm,text="", bg=self.sb_sm["background"], fg=root.colors["text_color"], font=self.result_font)
        self.result11 =  tk.Label(self.sb_sm,text="", bg=self.sb_sm["background"], fg=root.colors["text_color"], font=self.result_font)
        self.result12 =  tk.Label(self.sb_sm,text="", bg=self.sb_sm["background"], fg=root.colors["text_color"], font=self.result_font)

        self.results_block = []
        self.results_block.append(self.result1)
        self.results_block.append(self.result2)
        self.results_block.append(self.result3)
        self.results_block.append(self.result4)
        self.results_block.append(self.result5)
        self.results_block.append(self.result6)
        self.results_block.append(self.result7)
        self.results_block.append(self.result8)
        self.results_block.append(self.result9)
        self.results_block.append(self.result10)
        self.results_block.append(self.result11)
        self.results_block.append(self.result12)


        # self.value_button = tk.Button(self.sb_sm, text="Értékadás", command=self.overwrite)
        self.value_buttonimage = tk.PhotoImage(file=f"{root.colors['path']}shape_builder/value_button.png")
        self.value_button = tk.Label(self.sb_sm, image=self.value_buttonimage, activebackground=self["background"], border = 0, bg =self["background"])
        self.value_button.bind('<Button-1>', func=lambda e: self.overwrite())
        # self.cls = tk.Button(self.sb_sm,text="Minden törlése", command=self.clear_all)
        #self.pos_lbl = tk.Label(self,text="", bg=self.sb_sm["background"], fg=root.colors["text_color"])
        self.pos_lbl = self.create_text(15 ,15,text="",fill= root.colors['text_color']) # position label

        self.controls = []
        self.controls.append({"unit":self.l_unit1, "unit_type": "length"})
        self.controls.append({"unit":self.l_unit2, "unit_type": "length"})

        #############* Creating + and - buttons ##############
        self.img= (Image.open(f"{self.root.colors['path']}shape_builder/plus.png"))
        resized_image= self.img.resize((30,30), Image.ANTIALIAS)
        self.plus_img= ImageTk.PhotoImage(resized_image)
        self.img= (Image.open(f"{self.root.colors['path']}shape_builder/minus.png"))
        resized_image= self.img.resize((30,30), Image.ANTIALIAS)
        self.minus_img= ImageTk.PhotoImage(resized_image)
        self.img= (Image.open(f"{root.colors['path']}shape_builder/minus_hover.png"))
        resized_image= self.img.resize((30,30), Image.ANTIALIAS)
        self.minus_hover_img = ImageTk.PhotoImage(resized_image)
        self.img= (Image.open(f"{root.colors['path']}shape_builder/plus_hover.png"))
        resized_image= self.img.resize((30,30), Image.ANTIALIAS)
        self.plus_hover_img = ImageTk.PhotoImage(resized_image)
        self.minus= self.create_image(self.root.winfo_width()-310, self.root.winfo_height()-50, anchor=tk.NW,image=self.minus_img, tags=("plus_minus"))
        self.plus= self.create_image(self.root.winfo_width()-275, self.root.winfo_height()-50, anchor=tk.NW,image=self.plus_img, tags=("plus_minus"))
        self.tag_bind(self.plus, '<Button-1>', lambda e: self.rescale(2))
        self.tag_bind(self.minus, '<Button-1>', lambda e: self.rescale(0.5))
        self.tag_bind(self.minus, '<Enter>', lambda e: self.itemconfig(self.minus,image=self.minus_hover_img))
        self.tag_bind(self.plus, '<Enter>', lambda e: self.itemconfig(self.plus,image=self.plus_hover_img))
        self.tag_bind(self.minus, '<Leave>', lambda e: self.itemconfig(self.minus,image=self.minus_img))
        self.tag_bind(self.plus, '<Leave>', lambda e: self.itemconfig(self.plus,image=self.plus_img))
        
        #############* Creating up and down button #################
        self.img= (Image.open("up.png"))
        resized_image= self.img.resize((15,30), Image.ANTIALIAS)
        self.up_img= ImageTk.PhotoImage(resized_image)
        self.img= (Image.open("down.png"))
        resized_image= self.img.resize((15,30), Image.ANTIALIAS)
        self.down_img= ImageTk.PhotoImage(resized_image)
        #self.img= (Image.open(f"{root.colors['path']}shape_builder/minus_hover.png"))
        #resized_image= self.img.resize((30,30), Image.ANTIALIAS)
        #self.minus_hover_img = ImageTk.PhotoImage(resized_image)
        #self.img= (Image.open(f"{root.colors['path']}shape_builder/plus_hover.png"))
        #resized_image= self.img.resize((30,30), Image.ANTIALIAS)
        #self.plus_hover_img = ImageTk.PhotoImage(resized_image)
        self.up= self.create_image(10, 20, anchor=tk.NW,image=self.up_img, tags=("up_down", "navigate"))
        self.down= self.create_image(10, 60, anchor=tk.NW,image=self.down_img, tags=("up_down", "navigate"))
        self.tag_bind(self.up, '<Button-1>', lambda e: self.change_active_shape())
        self.tag_bind(self.down, '<Button-1>', lambda e: self.change_active_shape("down"))
        
        #############* Creating clear button on canvas ##############
        self.clear_img = tk.PhotoImage(file=f"{root.colors['path']}shape_builder/clear.png")
        self.clear_hover_img = tk.PhotoImage(file=f"{root.colors['path']}shape_builder/clear_hover.png")
        self.clear = self.create_image(10, self.root.winfo_height()-110, anchor=tk.NW,image=self.clear_img, tags=("clear"))
        self.tag_bind(self.clear, '<Button-1>', lambda e: self.clear_all())
        self.tag_bind(self.clear, '<Enter>', lambda e: self.itemconfig(self.clear,image=self.clear_hover_img))
        self.tag_bind(self.clear, '<Leave>', lambda e: self.itemconfig(self.clear,image=self.clear_img))

        ###########* Creating the basic, green rectangle #############
        """
        self.alap = self.create_rectangle(10,10,10+WIDTH,10+WIDTH,fill="green")
        self.alap_negyzet = Rectangle(self,10,10,10+WIDTH,10+WIDTH, self.alap)
        self.width_label = self.create_text(20+self.width,10+ self.heigth/2,text=str(self.width/10))
        self.height_label = self.create_text(10+self.width/2,self.heigth+ 20,text=str(self.heigth/10))
        """
        self.alap = self.create_rectangle(30,10,30+WIDTH,10+WIDTH,fill="green", tags=("alap_rectangle"))
        self.alap_negyzet = Rectangle(self,30,10,30+WIDTH,10+WIDTH, self.alap)
        self.width_label = self.create_text(40+self.width,10+ self.heigth/2,text=str(self.width/10),tags=("alap_rectangle"))
        self.height_label = self.create_text(40+self.width/2,self.heigth+ 20,text=str(self.heigth/10),tags=("alap_rectangle"))
        

        ###########* Creating basic, green circle #############
        
        self.r=20
        self.angle=180
        self.start = 0
        """
        self.alap_circle = self.create_arc(10,60,40,90,extent=self.angle, start = self.start, fill="green")
        self.r_label = self.create_text(10+30/2,60+30,text=f"r={30/2}")
        """
        self.alap_circle = self.create_arc(50-self.r,25-self.r,50+self.r,25+self.r,extent=self.angle, start = self.start, fill="green", tags=("alap_circle"))
        self.r_label = self.create_text(30+30/2,10+30,text=f"r={30/2}",tags=("alap_circle"))
        self.itemconfigure("alap_circle",state="hidden")
        

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
        self.popup_menu.add_command(label="Delete",command=self.delete_shape)
        self.popup_menu.add_command(label="Resize",command=self.resize_rectangle)
        self.popup_menu.add_command(label="Info",command=self.rectangle_info)
        self.bind("<Button-3>", self.popup) # right-click event
        self.bind("<Configure>", self.resize_canvas)
        #self.tag_bind("rect",'<Double-Button-1>',self.select)
        self.tag_bind("shape",'<Button-1>',self.select)
        #self.tag_bind("arc",'<Button-1>',self.select)
        self.bind("<Button-1>", self.deselect)
        self.bind("<Motion>", lambda e: self.itemconfig(self.pos_lbl, text=f"x: {(e.x-self.Xcenter)/self.scale} y: {(self.Ycenter-e.y)/self.scale}"))
        self.root.bind("<Delete>", self.delete_shape)
        self.root.bind("<Control-i>", self.rectangle_info)
        self.root.bind("<Control-r>", self.resize_rectangle)

        self.root.bind("<Control-c>", self.add_to_clp)
        self.root.bind("<Control-v>", self.insert_from_clp)

        #self.root.bind("<Control-n>", lambda e: self.hc.refresh(self.Xcenter-20,self.Ycenter-100, self.hc.r))

        ##############* Packing objects ###############
        # self.place_holder.grid(row=0,column=1,columnspan=5)
        self.l_width.grid(row=1,column=1,padx=(10,0),pady=(20,0))
        self.e1.grid(row=1,column=2,pady=(20,0),padx=2)
        self.l_unit1.grid(row=1,column=3,pady=(20,0))
        self.l_heigth.grid(row=2,column=1,padx=(10,0))
        self.e2.grid(row=2,column=2,padx=2)
        self.l_unit2.grid(row=2,column=3)
        self.value_button.grid(row=1,rowspan=2, column=5,pady=(15,0),padx=(5,10))
        self.is_sticky.grid(row=3,columnspan=3)
        self.calc_button.grid(row=4,column=1,columnspan=5,padx=(20))
        self.rowcount = 7
        for i in self.results_block:
            i.grid(row=self.rowcount+1, column=1, columnspan=5, padx=30, pady=2, sticky=tk.W)
            self.rowcount += 1

        self.results_block[0].grid(padx=15)
        self.results_block[3].grid(padx=15)
        self.results_block[8].grid(padx=15)
        # self.cls.grid(row=6, column=1,columnspan=3)

    def popup(self, e): #right cklick menu shows up
        if not self.isMoving:
            for i in self.shapes:
                if i.is_inside((e.x,e.y)):
                    self.select(e)
                    try:
                        self.popup_menu.tk_popup(e.x_root, e.y_root, 0)
                    finally:
                        self.popup_menu.grab_release()
                    break
    def delete_shape(self, e=None):
        print("deleteing rectangle")
        for i in self.selected:
            self.delete(i.canvas_repr)
            self.shapes.remove(i)
            self.selected = []
        for k in self.shapes:
            k.is_overlapping()
    def resize_rectangle(self,e=None): #! Something is wrong...
        for i in self.selected:
            if type(i)==Rectangle:
                i.refresh(i.x1, i.y1, i.x1 + self.width, i.y1 + self.heigth)
            if type(i)==Arc:
                i.refresh(i.center[0],i.center[1],self.width/2,i.angle, i.start)
            else:
                print(type(i),"\n" ,i)
                raise TypeError
            i = None
        for k in self.rectangles:
            k.is_overlapping()
    def rectangle_info(self,e=None): #! Formating
        self.clear_results()
        if len(self.selected)>1:
            self.result1.config(text=f"{len(self.selected)} darab objektum van kijelölve")
            return -1
        if len(self.selected)>0: self.result1.config(text= self.selected[0].get_info())
        
    def select(self,e, object=None):
        #self.deselect()
        if e is None and object is not None:
            self.selected.append(object)
            for i in self.selected:
                self.itemconfig(i.canvas_repr, fill='pink')
            return 0
        tmp = self.find_closest(e.x,e.y)[0]
        for i in self.shapes:
            if i.canvas_repr == tmp and i not in self.selected:
                self.selected.append(i)
                break
        else:
            print("Selection_Error: Shape not found...")
            return -1  
        for i in self.selected:
            self.itemconfig(i.canvas_repr, fill='pink')
        print("Selecting shape")
    def deselect(self,e=None):
        if e is not None:
            for i in self.shapes:
                if i.is_inside((e.x,e.y)):
                    return 0
        try:
            for i in self.selected:
                print("deselect")
                self.itemconfig(i.canvas_repr, fill='blue')
            self.selected = []
        except:
            pass
        for k in self.shapes:
            k.is_overlapping()
    def move(self,e): #? could be better but works...
        if keyboard.is_pressed("Ctrl"):
            if self.last_click_pos is None:
                self.last_click_pos = (e.x, e.y)
            else:
                self.translation(e.x-self.last_click_pos[0],e.y-self.last_click_pos[1])
                self.last_click_pos = (e.x, e.y)
            return 0
        self.itemconfig(self.pos_lbl, text=f"x: {(e.x-self.Xcenter)/self.scale} y: {(self.Ycenter-e.y)/self.scale}")
        self.deselect()
        # self.label.config(text=f"")
        #choosing object
        for i in self.shapes:
            if self.current is None and i.is_inside((e.x,e.y)) and self.starting_pos is None:
                self.shapes.remove(i)
                self.current = i
                self.itemconfig(self.current.canvas_repr, fill='light blue')
                break
        else:
            pos = self.coords(self.alap_negyzet.canvas_repr)
            if self.current is None and e.x>=pos[0] and e.x<=pos[2] and e.y>=pos[1] and e.y <=pos[3] and self.starting_pos is None and self.active_shape == "Rectangle":
                self.current = Rectangle(self,pos[0],pos[1],pos[0]+self.width,pos[1]+self.heigth,self.create_rectangle(pos[0],pos[1],pos[0]+self.width,pos[1]+self.heigth,fill="blue", tags=("rect","shape")))
                self.itemconfig(self.current.canvas_repr, fill='light blue')
        if not self.current: # Circle
            pos = self.coords(self.alap_circle)
            cent = (pos[0]+self.r,pos[1]+self.r)
            if dist((e.x,e.y), (pos[0]+self.r,pos[1]+self.r))<self.r and degrees(asin(abs(e.y-(pos[1]+self.r))/dist((e.x,e.y), (pos[0]+self.r,pos[1]+self.r))))<self.angle and self.starting_pos is None and (self.active_shape == "Semicircle" or self.active_shape == "quartrer_circle"):
                print("kör")
                #! Nem mindig jó helyre kattintva aktiválódik!!
                self.current = Arc(self,e.x,e.y,self.r,self.angle,self.start)
                self.itemconfig(self.current.canvas_repr, fill='light blue')
                print(type(self.current))
        if not self.current:
            ############### Selecting multiple objects ##############
            if self.starting_pos is None: 
                self.starting_pos = (e.x,e.y)
                self.itemconfigure(self.selecting_area,state="normal")
            else:
                try:
                    self.coords(self.selecting_area,self.starting_pos[0],self.starting_pos[1],e.x,e.y)
                except:
                    print("Can not show selection area")
            return -1
        pos = self.coords(self.current.canvas_repr)
        if type(self.current)==Rectangle and (self.isMoving or e.x>=pos[0] and e.x<=pos[2] and e.y>=pos[1] and e.y <=pos[3]):
            self.current.refresh(e.x-self.current.width/2,e.y-self.current.heigth/2,e.x+self.current.width/2,e.y+self.current.heigth/2)
            self.isMoving = True
            return 0
        elif self.isMoving or type(self.current)==Arc:
            self.current.refresh(e.x,e.y,self.current.r,self.current.angle,self.current.start)
            self.isMoving = True
            return 0
        
    def release(self,e):
        self.delete("hauptachse")
        self.delete("s_axis")
        if self.root.show_orig_axis:self.itemconfigure("orig_axes",state="normal")
        self.itemconfig(self.pos_lbl, text="")
        #choosing object
        if self.sticky.get() and self.current:
            self.current.align()
            #? prioritási sorrend???    
        if self.isMoving and self.current is not None:
            #self.itemconfig(self.current.canvas_repr, fill='blue')
            self.shapes.append(self.current)
            for k in self.shapes:
                k.is_overlapping()
        if self.starting_pos is not None:
            mwc = min(self.starting_pos[0],e.x)
            mec = max(self.starting_pos[0],e.x)
            mnc = min(self.starting_pos[1],e.y)
            msc = max(self.starting_pos[1],e.y)
            for i in self.shapes:    
                if i.center[0] > mwc and i.center[0]< mec and i.center[1] > mnc and i.center[1] < msc:
                    self.select(None, i)
            self.coords(self.selecting_area,mwc,mnc,mec,msc)
            self.starting_pos = None
        self.itemconfigure(self.selecting_area,state="hidden")
            
            
        self.isMoving = False
        self.current=None
        # self.label.config(text="")
        self.itemconfig(self.pos_lbl, text=f"x: {(e.x-self.Xcenter)/self.scale} y: {(self.Ycenter-e.y)/self.scale}")
        self.tag_raise("plus_minus")
        self.tag_raise(self.pos_lbl)
        self.last_click_pos = None
    def calculate(self):
        if len(self.shapes) == 0:
            self.clear_results()
            self.result1.config(text=f"A: 0 mm\nIx: 0 mm\nIy: 0 mm\nIxy: 0") #! Formatting
            return -1
        Ix = 0
        Iy = 0
        Ixy = 0
        A = 0
        out_str = ""
        if not self.root.calc_for_orig_axis:
            Sx=0
            Sy=0
            for i in self.shapes:
                #print((i.center[0]-self.Xcenter)/self.scale)
                A += i.area
                Sx += (i.s_center[0]-self.Xcenter)*i.area
                Sy += (self.Ycenter-i.s_center[1])*i.area
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
            #TODO: Sx és Sy koordináták a canvas bal felső sarkától vannak mérve, nem a globális kordináta rendszertől, így kicsit nehéz rajta kiigazodni
            self.result1.config(text="Súlypont koordinátái:")
            self.result2.config(text="Sₓ = " + str(round((Sx - self.Xcenter)/self.scale,4)) + " " + self.root.unit)
            self.result3.config(text="Sᵧ = " + str(round((self.Ycenter - Sy)/self.scale,4)) + " " + self.root.unit)
        else:
            out_str += "Számítások fix tengelyre:\n"
            Sx = self.Xcenter
            Sy = self.Ycenter
            a_length = min(min(Sx,Sy),self.canvas_height-Sy,self.canvas_width-Sx)
        A = 0
        for i in self.shapes.rectangles:
            pos = self.coords(i.canvas_repr)
            A_current = (pos[2]-pos[0]) * (pos[3]-pos[1])
            A += A_current
            Ix += ((pos[2]-pos[0]) * (pos[3]-pos[1])**3 )/12+ A_current*(Sy-pos[1]-(pos[3]-pos[1])/2)**2
            Iy += (pos[2]-pos[0])**3 * (pos[3]-pos[1]) /12+ A_current*(pos[0]+(pos[2]-pos[0])/2-Sx)**2
              
            Ixy += A_current*(pos[0]+(pos[2]-pos[0])/2-Sx)*(Sy-pos[1]-(pos[3]-pos[1])/2)
        for i in self.shapes.arcs: #! Check rotation
            A += i.area
            Ixc = (i.r**4 / 8)*(radians(i.angle)-sin(radians(i.angle))) 
            Iyc = (i.r**4 / 8)*(radians(i.angle)+sin(radians(i.angle)))
            # rotation + translation
            Ix += ((Ixc+Iyc)/2 + (Ixc-Iyc)/2 *cos(2*radians(i.start-i.angle/2))) + i.area*(Sy-i.center[1])**2
            Iy += ((Ixc+Iyc)/2 - (Ixc-Iyc)/2 *cos(2*radians(i.start-i.angle/2))) + i.area*(Sy-i.center[1])**2
            Ixy +=  ((Ixc-Iyc)/2 *sin(2*radians(i.start-i.angle/2))) + i.area*(i.center[0]-Sx)*(Sy-i.center[1])
        out_str += f"A: {A/self.scale**2} mm\nIx: {Ix/self.scale**4} mm\nIy: {Iy/self.scale**4} mm\nIxy: {Ixy/self.scale**4}\n"
        i1, i2, alpha = self.hauptachsen(Ix/self.scale**4,Iy/self.scale**4,Ixy/self.scale**4, Sx,Sy,a_length)
        out_str += f"I_1 = {i1}\nI_2 = {i2}\nalpa = {alpha}"
        self.result4.config(text="Keresztmetszeti jellemzők:")
        self.result5.config(text="A = " + str(round(A/self.scale**2, 4)) + " " + self.root.unit + "²")
        self.result6.config(text="Iₓ = " + str(round(Ix/self.scale**4, 4)) + " " + self.root.unit + "\u2074")
        self.result7.config(text="Iᵧ = " + str(round(Iy/self.scale**4,4)) + " " + self.root.unit + "\u2074")
        self.result8.config(text="Iₓᵧ = " + str(round(Ixy/self.scale**4,4)) + " " + self.root.unit + "\u2074")

        self.result9.config(text="Főmásodrendű nyomatékok:")
        self.result10.config(text="I₁ = " + str(round(i1,4)) + " " + self.root.unit + "\u2074")
        self.result11.config(text="I₂ = " + str(round(i2,4)) + " " + self.root.unit + "\u2074")
        self.result12.config(text="\u03B1 = " + str(round(alpha,4)) + " " + self.root.angle_unit)
        
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
    def clear_all(self): #? Could be better
        self.rectangles = []
        self.arcs = []
        self.delete("shape") 
        self.delete("hauptachse")
        self.delete("s_axis")
        del self.shapes
        self.shapes = Shapes(self,self.rectangles,self.arcs)
        #self.label.config(text="")   
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
    def rescale(self,scale): #!? Could be better
        self.scale *= scale
        self.alap_negyzet.refresh(40,10,40+self.width*scale,10+self.heigth*scale)
        self.coords(self.alap_circle, 40,10,40+self.width*scale,10+self.width*scale) #? Esetleg külön sugár változó
        self.width *= scale
        self.heigth *= scale
        self.coords(self.width_label,50+self.width,10+ self.heigth/2)
        self.coords(self.height_label,30+self.width/2,self.heigth+ 25)
        self.coords(self.r_label,45+self.width/2,15+ self.heigth) #! sugár ???
        for i in self.rectangles: #?Esetleg álltalánosítani bármilyen alakzatra
            i.refresh(self.Xcenter-(self.Xcenter-i.x1)*scale, self.Ycenter-(self.Ycenter-i.y1)*scale, self.Xcenter-(self.Xcenter - i.x2)*scale, self.Ycenter-(self.Ycenter-i.y2)*scale)
        for i in self.arcs:
            i.refresh(self.Xcenter-(self.Xcenter-i.center[0])*scale,self.Ycenter-(self.Ycenter-i.center[1])*scale, i.r*scale, i.angle, i.start)
    def resize_canvas(self,e):
        self.coords(self.minus, e.width-45, e.height-50)
        self.coords(self.plus, e.width-80, e.height-50)
        self.coords(self.pos_lbl, e.width-50, 30)
        self.canvas_width = e.width
        self.canvas_height = e.height
        self.translation(e.width/2-self.Xcenter, e.height/2-self.Ycenter)
        self.delete("s_axis")
        self.delete("hauptachse")
        self.coords(self.clear, 10, e.height-50)
        
    def translation(self, dx, dy):
        self.Xcenter += dx
        self.Ycenter += dy
        # Basic coord system
        self.coords(self.x_axis,10,self.Ycenter,self.canvas_width-10,self.Ycenter)
        self.coords(self.y_axis,self.Xcenter,10,self.Xcenter,self.canvas_height-10)
        self.coords(self.x_label,2*self.Xcenter-5,self.Ycenter+ 20)
        self.coords(self.y_label,self.Xcenter +20 ,15)
        #Rectangles
        for i in self.shapes:
            i.translate(dx,dy)
    def place_objekt(self,x,y,object): #? Not implemented
        object.refresh(x,y,x+object.width,y+object.heigth) #rectangle
    def add_to_clp(self,e=None):
        self.clipboard = self.selected #! deepcopy???
    def insert_from_clp(self,e=None):
        print(f"{len(self.rectangles)=}")
        print(f"{len(self.selected)=}")
        for i in self.clipboard:
            print((i.center[0]-self.Xcenter)/self.scale)
            self.rectangles.append(Rectangle(self,i.x1+5,i.y1+5,i.x2+5,i.y2+5,self.create_rectangle(i.x1+5,i.y1+5,i.x2+5,i.y2+5,fill="blue", tags=("rect"))))
            print((self.rectangles[-1].center[0]-self.Xcenter)/self.scale)
        print(f"{len(self.rectangles)=}")
        print(f"{len(self.selected)=}")
    def clear_results(self):
        for i in self.results_block:
            i.config(text="")
    def change_active_shape(self, direction="up"):
        print(direction)
        if direction == "up":
            self.active_shape = next(self.possible_shapes)
        elif direction == "down":
            for i in range(len(self.possible_shape_list)-2): next(self.possible_shapes)
            self.active_shape = next(self.possible_shapes)
        else: 
            print("Error: Invalid command by changing shape.")
            raise ValueError
        print(self.active_shape)
        # Set icon for active_shape:
        if self.active_shape == "Rectangle":
            self.itemconfigure("alap_rectangle",state="normal")
            self.itemconfigure("alap_circle",state="hidden")
        elif self.active_shape == "Semicircle":
            self.itemconfigure("alap_rectangle",state="hidden")
            c = self.coords(self.alap_circle)
            self.delete(self.alap_circle)
            self.angle = 180
            self.alap_circle = self.create_arc(50-self.r,25-self.r,50+self.r,25+self.r,extent=180, start = 0, fill="green", tags=("alap_circle"))
        elif self.active_shape == "quartrer_circle":
            self.itemconfigure("alap_rectangle",state="hidden")
            self.delete(self.alap_circle)
            self.angle = 90
            self.alap_circle = self.create_arc(50-self.r,25-self.r,50+self.r,25+self.r,extent=90, start = 0, fill="green", tags=("alap_circle"))
        else: raise ValueError





class sb_side_menu(tk.Frame):
    def __init__(self,root):
        super().__init__(root,width=30, bg=root.colors['secondary_color'])
        self.root = root
