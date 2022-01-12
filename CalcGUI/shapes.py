from shape_builder import EPSILON
from math import atan, atan2, degrees, sin, cos, radians,pi, sqrt

def dist(p1,p2):
    return sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)

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
        self.center=(self.x1+self.width/2, self.y1+self.heigth/2)
        self.s_center = self.center
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
        self.s_center = self.center
        self.canvas.coords(self.canvas_repr,x1,y1,x2,y2)
    def is_overlapping(self):
        orig=list(self.canvas.find_overlapping(self.x1,self.y1,self.x2,self.y2))
        ############# with another Rect ##################
        a = [p for p in orig if "rect" in self.canvas.gettags(p)]
        a.remove(self.canvas_repr)
        in_overlapping = False
        for i in self.canvas.rectangles:
            if i.canvas_repr in a:
                if len({self.x1,self.x2}.intersection({i.x1,i.x2}))==0 and len({self.y1,self.y2}.intersection({i.y1,i.y2}))==0:
                    self.canvas.itemconfig(self.canvas_repr, fill='red')
                    in_overlapping = True
        ############ with Arc #################
        a = [p for p in orig if "arc" in self.canvas.gettags(p)]
        for i in self.canvas.arcs:
            if i.canvas_repr in a:
                if True: #!Ez szintén nem jó így de kezdetnek megteszi...
                    self.canvas.itemconfig(self.canvas_repr, fill='red')
                    in_overlapping = True
        if not in_overlapping and self not in self.canvas.selected:
            self.canvas.itemconfig(self.canvas_repr, fill='blue')
    def align(self):
        self.align_by_side()# sticking to another rectangles 
        self.align_by_center()
        self.align_to_axis()#sicking to the coordinate system
    def align_to_axis(self):
        if self.canvas.root.show_orig_axis:
            pos=[self.x1,self.y1,self.x2,self.y2]
            if abs(pos[0]-self.canvas.Xcenter) < EPSILON: #left side sticks to the coordinatsystem
                self.refresh(self.canvas.Xcenter,pos[1],self.canvas.Xcenter+self.width,pos[3])
                pos = self.canvas.coords(self.canvas_repr)
            elif abs(pos[2]-self.canvas.Xcenter) < EPSILON: #right side sticks to the coordinatsystem
                self.refresh(self.canvas.Xcenter-self.width,pos[1],self.canvas.Xcenter,pos[3])
                pos = self.canvas.coords(self.canvas_repr)
            if abs(pos[1]-self.canvas.Ycenter) < EPSILON: #top side sticks to the coordinatsystem
                self.refresh(pos[0],self.canvas.Ycenter,pos[2],self.canvas.Ycenter+self.heigth)
                pos = self.canvas.coords(self.canvas_repr)
            elif abs(pos[3]-self.canvas.Ycenter) < EPSILON: #bottomí side sticks to the coordinatsystem
                self.refresh(pos[0],self.canvas.Ycenter-self.heigth,pos[2],self.canvas.Ycenter)
                pos = self.canvas.coords(self.canvas_repr)
            #* Sticking with the center of the rectangle to the coordinate system
            if abs(self.center[0]-self.canvas.Xcenter)<EPSILON:
                self.refresh(self.canvas.Xcenter-self.width/2,self.y1,self.canvas.Xcenter+self.width/2,self.y2)
            if abs(self.center[1]-self.canvas.Ycenter)<EPSILON:
                self.refresh(self.x1,self.canvas.Ycenter-self.heigth/2,self.x2,self.canvas.Ycenter+self.heigth/2)
    def align_to_corners(self): #! OLD VERSION - NOT USED
        pos=[self.x1,self.y1,self.x2,self.y2]
        for i in self.canvas.rectangles:
            i_pos = self.canvas.coords(i.canvas_repr)
            if abs(pos[0] - i_pos[0]) < EPSILON and abs(pos[1] - i_pos[3]) < EPSILON: # current rect goes under the another 
                self.refresh(i_pos[0],i_pos[3],i_pos[0]+self.width,i_pos[3]+self.heigth)
                break
            elif abs(pos[0] - i_pos[0]) < EPSILON and abs(pos[3] - i_pos[1]) < EPSILON: # TOP
                self.refresh(i_pos[0],i_pos[1]-self.heigth,i_pos[0]+self.width,i_pos[1])
                break
            elif abs(pos[1] - i_pos[1]) < EPSILON and abs(pos[0] - i_pos[2]) < EPSILON: # RIGHT
                self.refresh(i_pos[2],i_pos[1],i_pos[2]+self.width,i_pos[1]+self.heigth)
                break
            elif abs(pos[1] - i_pos[1]) < EPSILON and abs(pos[2] - i_pos[0]) < EPSILON: # LEFT
                self.refresh(i_pos[0]-self.width,i_pos[1],i_pos[0],i_pos[1]+self.heigth)
                break
            elif abs(pos[2] - i_pos[2]) < EPSILON and abs(pos[3] - i_pos[1]) < EPSILON: # ??
                self.refresh(i_pos[2]-self.width,i_pos[1]-self.heigth,i_pos[2],i_pos[1])
                break
            elif abs(pos[2] - i_pos[0]) < EPSILON and abs(pos[3] - i_pos[3]) < EPSILON: # ??
                self.refresh(i_pos[0]-self.width,i_pos[3]-self.heigth,i_pos[0],i_pos[3])
                break
            elif abs(pos[0] - i_pos[2]) < EPSILON and abs(pos[3] - i_pos[3]) < EPSILON: # !
                self.refresh(i_pos[2],i_pos[3]-self.heigth,i_pos[2]+self.width,i_pos[3])
                break
            elif abs(pos[2] - i_pos[2]) < EPSILON and abs(pos[1] - i_pos[3]) < EPSILON: # !
                self.refresh(i_pos[2]-self.width,i_pos[3],i_pos[2],i_pos[3]+self.heigth)
                break
        else:
            return 0
        return 1
    def align_by_center(self):
        for i in self.canvas.rectangles:
            if abs(self.center[0]-i.center[0])<EPSILON:
                self.refresh(i.center[0]-self.width/2,self.y1,i.center[0]+self.width/2,self.y2)
                break
            if abs(self.center[1]-i.center[1])<EPSILON:
                self.refresh(self.x1,i.center[1]-self.heigth/2,self.x2,i.center[1]+self.heigth/2)
                break
    def align_by_side(self):
        for i in self.canvas.rectangles:
            if abs(self.x1-i.x1)<EPSILON: self.refresh(i.x1,self.y1,i.x1+self.width,self.y2) # sticking by left-left          
            if abs(self.x1-i.x2)<EPSILON: self.refresh(i.x2,self.y1,i.x2+self.width,self.y2) #sicking by left-right
            if abs(self.x2-i.x1)<EPSILON: self.refresh(i.x1-self.width,self.y1,i.x1,self.y2) #sticking by right-left
            if abs(self.x2-i.x2)<EPSILON: self.refresh(i.x2-self.width,self.y1,i.x2,self.y2) #sticking by right-right
            if abs(self.y1-i.y1)<EPSILON: self.refresh(self.x1,i.y1,self.x2,i.y1+self.heigth) # sticking by top-top
            if abs(self.y1-i.y2)<EPSILON: self.refresh(self.x1,i.y2,self.x2,i.y2+self.heigth) # sticking by top-bottom
            if abs(self.y2-i.y1)<EPSILON: self.refresh(self.x1,i.y1-self.heigth,self.x2,i.y1) # sticking by bottom-top
            if abs(self.y2-i.y2)<EPSILON: self.refresh(self.x1,i.y2-self.heigth,self.x2,i.y2) # sticking by top-top
    def translate(self, dx,dy):
        self.refresh(self.x1+dx,self.y1+dy,self.x2+dx,self.y2+dy)
    def is_inside(self,point):
        if point[0]>self.x1 and point[0]<self.x2 and point[1]>self.y1 and point[1]<self.y2:
            return True
        else:
            return False
    def get_info(self):
        text=f"Szélesség = {self.width/self.canvas.scale}\nMagasság = {self.heigth/self.canvas.scale}\nKözéppont = ({(self.center[0]-self.canvas.Xcenter)/self.canvas.scale},{(self.canvas.Ycenter-self.center[1])/self.canvas.scale})"
        return text
class Arc():
    def __init__(self,canvas, center_x, center_y, r, angle=180, start=0):
        self.canvas = canvas
        self.center = (center_x,center_y)
        self.r = r
        self.d = 2*r
        self.start = start
        self.angle = min (360,angle)
        self.area = r**2*pi*(self.angle/360)
        self.s_center = (center_x+ (2/3*r*sin(radians(angle))/radians(angle))*cos(radians(start)),center_y+ (2/3*r*sin(radians(angle))/radians(angle))*sin(radians(start)))
        self.canvas_repr = self.canvas.create_arc(center_x-r,center_y-r,center_x+r,center_y+r,extent=self.angle, start = self.start, fill="blue", tags=("arc","shape"))
    def refresh(self, center_x, center_y,r,angle=180, start=0):
        self.center = (center_x,center_y)
        self.r = r
        self.d = 2*r
        self.start = start
        self.angle = min(360,angle)
        self.area = r**2*pi*(self.angle/360)
        self.s_center = (center_x + (4/3*r*sin(radians(angle/2))/radians(angle))*cos(radians(start+angle/2)),center_y - (4/3*r*sin(radians(angle/2))/radians(angle))*sin(radians(start+angle/2)))
        self.canvas.coords(self.canvas_repr,center_x-r,center_y-r,center_x+r,center_y+r)
    def align(self):
        self.align_to_axis()
    def align_to_axis(self):
        if self.canvas.root.show_orig_axis:
            #* Sticking with the center of the rectangle to the coordinate system
            if abs(self.center[0]-self.canvas.Xcenter)<EPSILON:
                self.refresh(self.canvas.Xcenter,self.center[1],self.r,self.angle,self.start)
            if abs(self.center[1]-self.canvas.Ycenter)<EPSILON:
                self.refresh(self.center[0],self.canvas.Ycenter,self.r,self.angle,self.start)
    def get_bounding_box(self):
        # Karnaugh - tábla alapján
        C = bool(self.start == 90) or (self.start == 270)
        B = 180 <= self.start
        #B = cos(radians(self.angle)) == 0
        A = self.angle == 180
        
        #print(self.angle, self.start,A,B,C)

        l = self.center[0] - self.r*((A and not C) or (B and not C) or (C and not B))
        r = self.center[0] + self.r*((A and B) or (not (C or B) or (C and B)))
        t = self.center[1] - self.r*((C and A) or not B)
        b = self.center[1] + self.r*(B or (A and C))
        #print((l-self.canvas.Xcenter)/self.canvas.scale,(self.canvas.Ycenter-t)/self.canvas.scale,(r-self.canvas.Xcenter)/self.canvas.scale,(self.canvas.Ycenter-b)/self.canvas.scale)
        return l,r,t,b

    def is_overlapping(self):
        l,r,t,b = self.get_bounding_box()
        orig=list(self.canvas.find_overlapping(l,t,r,b))
        ############# with another Arc ##################
        a = [p for p in orig if "arc" in self.canvas.gettags(p)]
        a.remove(self.canvas_repr)
        in_overlapping = False
        for i in self.canvas.arcs:
            if i.canvas_repr in a:
                if True: #! Ezt javitani kell, de jobb mint a semmi...
                    self.canvas.itemconfig(self.canvas_repr, fill='red')
                    in_overlapping = True
        ############### with Rectangle ###################
        a = [p for p in orig if "rect" in self.canvas.gettags(p)]
        for i in self.canvas.rectangles:
            if i.canvas_repr in a:
                if True: #! Ezt is ki kéne számolni, de legalább valamit csinál
                    self.canvas.itemconfig(self.canvas_repr, fill='red')
                    in_overlapping = True
        if not in_overlapping and self not in self.canvas.selected:
            self.canvas.itemconfig(self.canvas_repr, fill='blue')
    def is_inside(self,point):
        dy = point[1]-self.center[1]
        dx = point[0]-self.center[0]
        szog = degrees(atan2(-dy,dx))
        if szog <0: szog = 360+szog
        if dist(point,self.center)<=self.r and  szog>self.start and szog<self.start+self.angle: return True
        return False
    def translate(self,dx,dy):
        self.refresh(self.center[0]+dx,self.center[1]+dy,self.r,self.angle,self.start)
    def get_info(self):
        text=f"Sugár = {self.r/self.canvas.scale}\nKözéppont = ({(self.center[0]-self.canvas.Xcenter)/self.canvas.scale},{(self.canvas.Ycenter-self.center[1])/self.canvas.scale})"
        return text
class Shapes():
    def __init__(self, canvas, rectangles, arcs):
        self.canvas = canvas
        self.container = []
        self.rectangles = rectangles
        self.arcs = arcs
        self.container.append(self.rectangles)
        self.container.append(self.arcs)
    def __iter__(self):
        self.n = 0
        self.max =0 
        for i in self.container: self.max+=len(i)
        return self
    def __getitem__(self, key):
        return self.__getelement_by_index(key)
    def __next__(self):
        if self.n < self.max:
            x = self.n
            self.n += 1
            return self.__getelement_by_index(x)
        else:
            raise StopIteration
    def __len__(self):
        l = 0
        for i in self.container: l+=len(i)
        return l
    def __getelement_by_index(self,index):
        tmp = []
        for i in self.container:
            for k in i:
                tmp.append(k)
        return tmp[index]
    def append(self, obj):
        if type(obj)==Rectangle:
            self.rectangles.append(obj)
        elif type(obj==Arc):
            self.arcs.append(obj)
        else:
            print("Hiba: A formatum nem megfelelo!")
    def remove(self, obj):
        if type(obj)==Rectangle:
            self.rectangles.remove(obj)
        elif type(obj==Arc):
            self.arcs.remove(obj)
        else:
            print("Hiba: A formatum nem megfelelo!")
