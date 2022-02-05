from re import A
import re
from shape_builder import EPSILON
from math import atan, atan2, degrees, sin, cos, radians,pi, sqrt
import numpy as np
EPSILON = 10
def dist(p1,p2):
    return sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)
def check_overlapping_of_boundig_box(ax1,ax2,ay1,ay2, x1,x2,y1,y2):
    eps = 10**(-9)
    p1 = (x1+eps,y1+eps)
    p2 = (x1+eps,y2-eps)
    p3 = (x2-eps,y1+eps)
    p4 = (x2-eps,y2-eps)
    tmp = False
    for point in [p1,p2,p3,p4]: tmp = tmp or (point[0]>ax1 and point[0]<ax2 and point[1]>ay1 and point[1]<ay2)
    
    return tmp
class Rectangle():  
    def __init__(self,canvas,root,x1,y1,x2,y2, canvas_repr, Negative = False):
        self.canvas = canvas
        self.root = root
        self.type = "Rectangle"
        self.canvas_repr = canvas_repr
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.negative = Negative
        self.width = x2-x1
        self.height = y2-y1
        self.area = self.width*self.height
        self.center=(self.x1+self.width/2, self.y1+self.height/2)
        self.s_center = self.center
        self.overlapping_with = []
        if self.negative: self.canvas.negatives.append(self)
    def refresh(self,x1,y1,x2,y2):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.width = self.x2-self.x1
        self.height = self.y2-self.y1
        self.area = self.width*self.height
        self.center=(self.x1+self.width/2, self.y1+self.height/2)
        self.s_center = self.center
        self.canvas.coords(self.canvas_repr,x1,y1,x2,y2)
    def is_overlapping(self):
        if self.negative: 
            self.canvas.itemconfig(self.canvas_repr, fill='gray')
            return 0
        orig=list(self.canvas.find_overlapping(self.x1,self.y1,self.x2,self.y2))
        ############# with another Rect ##################
        a = [p for p in orig if "rect" in self.canvas.gettags(p)]
        a.remove(self.canvas_repr)
        in_overlapping = False
        for i in self.canvas.rectangles:
            if i.negative: continue
            if i.canvas_repr in a: 
                if check_overlapping_of_boundig_box(self.x1,self.x2,self.y1,self.y2,i.x1,i.x2,i.y1,i.y2) or check_overlapping_of_boundig_box(i.x1,i.x2,i.y1,i.y2,self.x1,self.x2,self.y1,self.y2):
                    self.canvas.itemconfig(self.canvas_repr, fill='red')
                    in_overlapping = True
        ############ with Arc #################
        a = [p for p in orig if "arc" in self.canvas.gettags(p)]
        for i in self.canvas.arcs:
            if i.negative: continue
            if i.canvas_repr in a:
                l,r,t,b=i.get_bounding_box()
                if check_overlapping_of_boundig_box(self.x1,self.x2,self.y1,self.y2, l,r,t,b ) or check_overlapping_of_boundig_box(l,r,t,b, self.x1,self.x2,self.y1,self.y2): #!Ez szintén nem jó így de kezdetnek megteszi...
                    self.canvas.itemconfig(self.canvas_repr, fill='red')
                    in_overlapping = True
        if not in_overlapping and self not in self.canvas.selected:
            self.canvas.itemconfig(self.canvas_repr, fill=self.root.colors["sb_draw"])
    def align(self):
        self.align_by_side()# sticking to another rectangles 
        self.align_by_center()
        self.align_to_axis()#sicking to the coordinate system
        self.align_to_arc()
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
                self.refresh(pos[0],self.canvas.Ycenter,pos[2],self.canvas.Ycenter+self.height)
                pos = self.canvas.coords(self.canvas_repr)
            elif abs(pos[3]-self.canvas.Ycenter) < EPSILON: #bottomí side sticks to the coordinatsystem
                self.refresh(pos[0],self.canvas.Ycenter-self.height,pos[2],self.canvas.Ycenter)
                pos = self.canvas.coords(self.canvas_repr)
            #* Sticking with the center of the rectangle to the coordinate system
            if abs(self.center[0]-self.canvas.Xcenter)<EPSILON:
                self.refresh(self.canvas.Xcenter-self.width/2,self.y1,self.canvas.Xcenter+self.width/2,self.y2)
            if abs(self.center[1]-self.canvas.Ycenter)<EPSILON:
                self.refresh(self.x1,self.canvas.Ycenter-self.height/2,self.x2,self.canvas.Ycenter+self.height/2)
    def align_to_corners(self): #! OLD VERSION - NOT USED
        pos=[self.x1,self.y1,self.x2,self.y2]
        for i in self.canvas.rectangles:
            i_pos = self.canvas.coords(i.canvas_repr)
            if abs(pos[0] - i_pos[0]) < EPSILON and abs(pos[1] - i_pos[3]) < EPSILON: # current rect goes under the another 
                self.refresh(i_pos[0],i_pos[3],i_pos[0]+self.width,i_pos[3]+self.height)
                break
            elif abs(pos[0] - i_pos[0]) < EPSILON and abs(pos[3] - i_pos[1]) < EPSILON: # TOP
                self.refresh(i_pos[0],i_pos[1]-self.height,i_pos[0]+self.width,i_pos[1])
                break
            elif abs(pos[1] - i_pos[1]) < EPSILON and abs(pos[0] - i_pos[2]) < EPSILON: # RIGHT
                self.refresh(i_pos[2],i_pos[1],i_pos[2]+self.width,i_pos[1]+self.height)
                break
            elif abs(pos[1] - i_pos[1]) < EPSILON and abs(pos[2] - i_pos[0]) < EPSILON: # LEFT
                self.refresh(i_pos[0]-self.width,i_pos[1],i_pos[0],i_pos[1]+self.height)
                break
            elif abs(pos[2] - i_pos[2]) < EPSILON and abs(pos[3] - i_pos[1]) < EPSILON: # ??
                self.refresh(i_pos[2]-self.width,i_pos[1]-self.height,i_pos[2],i_pos[1])
                break
            elif abs(pos[2] - i_pos[0]) < EPSILON and abs(pos[3] - i_pos[3]) < EPSILON: # ??
                self.refresh(i_pos[0]-self.width,i_pos[3]-self.height,i_pos[0],i_pos[3])
                break
            elif abs(pos[0] - i_pos[2]) < EPSILON and abs(pos[3] - i_pos[3]) < EPSILON: # !
                self.refresh(i_pos[2],i_pos[3]-self.height,i_pos[2]+self.width,i_pos[3])
                break
            elif abs(pos[2] - i_pos[2]) < EPSILON and abs(pos[1] - i_pos[3]) < EPSILON: # !
                self.refresh(i_pos[2]-self.width,i_pos[3],i_pos[2],i_pos[3]+self.height)
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
                self.refresh(self.x1,i.center[1]-self.height/2,self.x2,i.center[1]+self.height/2)
                break
    def align_by_side(self):
        for i in self.canvas.rectangles:
            if abs(self.x1-i.x1)<EPSILON: self.refresh(i.x1,self.y1,i.x1+self.width,self.y2) # sticking by left-left          
            if abs(self.x1-i.x2)<EPSILON: self.refresh(i.x2,self.y1,i.x2+self.width,self.y2) #sicking by left-right
            if abs(self.x2-i.x1)<EPSILON: self.refresh(i.x1-self.width,self.y1,i.x1,self.y2) #sticking by right-left
            if abs(self.x2-i.x2)<EPSILON: self.refresh(i.x2-self.width,self.y1,i.x2,self.y2) #sticking by right-right
            if abs(self.y1-i.y1)<EPSILON: self.refresh(self.x1,i.y1,self.x2,i.y1+self.height) # sticking by top-top
            if abs(self.y1-i.y2)<EPSILON: self.refresh(self.x1,i.y2,self.x2,i.y2+self.height) # sticking by top-bottom
            if abs(self.y2-i.y1)<EPSILON: self.refresh(self.x1,i.y1-self.height,self.x2,i.y1) # sticking by bottom-top
            if abs(self.y2-i.y2)<EPSILON: self.refresh(self.x1,i.y2-self.height,self.x2,i.y2) # sticking by top-top
    def align_to_arc(self):
        for i in self.canvas.arcs:
            own = i.get_charachteristic_points()
            x = [p[0] for p in own]
            y = [p[1] for p in own]
            arc_x = max(set(x), key=x.count)
            arc_y = max(set(y), key=y.count)
            dx = 0
            dy = 0
            # align by x
            for j in [self.x1,self.x2,self.center[0]]:
                if abs(j-arc_x) < EPSILON:
                    dx = j- arc_x
                    break
            #align by y
            for j in [self.y1,self.y2,self.center[1]]:
                if abs(j-arc_y) < EPSILON:
                    dy = j- arc_y
                    break
            if dx != 0 or dy != 0:
                self.refresh(self.x1-dx,self.y1-dy,self.x2-dx,self.y2-dy)
                for k in own:
                    for l in [(self.x1,self.y1),(self.x1,self.y2),(self.x2,self.y1),(self.x2,self.y2)]:
                        if dist(k,l)<EPSILON:
                            dx = l[0]-k[0]
                            dy = l[1]-k[1]
                            self.refresh(self.x1-dx,self.y1-dy,self.x2-dx,self.y2-dy)
                            
    def translate(self, dx,dy):
        self.refresh(self.x1+dx,self.y1+dy,self.x2+dx,self.y2+dy)
    def is_inside(self,point):
        if point[0]>self.x1 and point[0]<self.x2 and point[1]>self.y1 and point[1]<self.y2:
            return True
        else:
            return False
    def get_info(self):
        text=f"Szélesség = {self.width/self.canvas.scale}\nMagasság = {self.height/self.canvas.scale}\nKözéppont = ({(self.center[0]-self.canvas.Xcenter)/self.canvas.scale},{(self.canvas.Ycenter-self.center[1])/self.canvas.scale})"
        return text
class Arc():
    def __init__(self,canvas,root, center_x, center_y, r, angle=180, start=0, Negative=False):
        self.canvas = canvas
        self.root = root
        self.center = (center_x,center_y)
        self.r = r
        self.d = 2*r
        self.negative = Negative
        self.start = start
        self.angle = min (360,angle)
        if self.angle == 180:
            self.type = "Semicircle"
        elif self.angle == 90:
            self.type = "quarter_circle"
        self.area = r**2*pi*(self.angle/360)
        self.s_center = (center_x+ (2/3*r*sin(radians(angle))/radians(angle))*cos(radians(start)),center_y+ (2/3*r*sin(radians(angle))/radians(angle))*sin(radians(start)))
        self.canvas_repr = self.canvas.create_arc(center_x-r,center_y-r,center_x+r,center_y+r,extent=self.angle, start = self.start, fill=self.root.colors["sb_draw"], tags=("arc","shape"))
        if self.negative: self.canvas.negatives.append(self)
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
        self.align_to_rect()
        self.align_to_arc()
    def align_to_axis(self):
        if self.canvas.root.show_orig_axis:
            #* Sticking with the center of the rectangle to the coordinate system
            if abs(self.center[0]-self.canvas.Xcenter)<EPSILON:
                self.refresh(self.canvas.Xcenter,self.center[1],self.r,self.angle,self.start)
            if abs(self.center[1]-self.canvas.Ycenter)<EPSILON:
                self.refresh(self.center[0],self.canvas.Ycenter,self.r,self.angle,self.start)
    def align_to_arc(self):
        own = self.get_charachteristic_points()
        for i in self.canvas.arcs:
            aling_score = 0 # if at least two points are near eachother, then it alignes them
            other = i.get_charachteristic_points()
            for k in own:
                for j in other:
                    if dist(k,j) <= EPSILON: 
                        aling_score+=1
                        displacement = (j[0]-k[0], j[1]-k[1])
            if aling_score >= 2:
                self.refresh(self.center[0]+displacement[0], self.center[1]+displacement[1], self.r, self.angle,self.start)
                break
    def align_to_rect(self):
        own = self.get_charachteristic_points()
        x = [p[0] for p in own]
        y = [p[1] for p in own]
        arc_x = max(set(x), key=x.count)
        arc_y = max(set(y), key=y.count)
        dx = 0
        dy = 0
        for i in self.canvas.rectangles:
            # align by x
            for j in [i.x1,i.x2,i.center[0]]:
                if abs(j-arc_x) < EPSILON:
                    dx = j- arc_x
                    break
            #align by y
            for j in [i.y1,i.y2,i.center[1]]:
                if abs(j-arc_y) < EPSILON:
                    dy = j- arc_y
                    break
            if dx != 0 or dy != 0:
                self.refresh(self.center[0]+dx,self.center[1]+dy,self.r,self.angle,self.start)
                own = self.get_charachteristic_points()
                x = [p[0] for p in own]
                y = [p[1] for p in own]
                arc_x = max(set(x), key=x.count)
                arc_y = max(set(y), key=y.count)
                dx = 0
                dy = 0
                for k in own:
                    for l in [(i.x1,i.y1),(i.x1,i.y2),(i.x2,i.y1),(i.x2,i.y2)]:
                        if dist(k,l)<EPSILON:
                            dx = l[0]-k[0]
                            dy = l[1]-k[1]
                            self.refresh(self.center[0]+dx,self.center[1]+dy,self.r,self.angle,self.start)
                            own = self.get_charachteristic_points()
                            x = [p[0] for p in own]
                            y = [p[1] for p in own]
                            arc_x = max(set(x), key=x.count)
                            arc_y = max(set(y), key=y.count)
                            dx = 0
                            dy = 0
           
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
    def get_charachteristic_points(self):
        p1 = self.center
        p2 = (p1[0]+self.r*cos(radians(self.start)), p1[1]-self.r*sin(radians(self.start)))
        p3 = (p1[0]+self.r*cos(radians(self.start+self.angle)), p1[1]-self.r*sin(radians(self.start+self.angle)))
        return p2, p1, p3
    def is_overlapping(self):
        if self.negative: 
            self.canvas.itemconfig(self.canvas_repr, fill='gray')
            return 0
        l,r,t,b = self.get_bounding_box()
        orig=list(self.canvas.find_overlapping(l,t,r,b))
        ############# with another Arc ##################
        a = [p for p in orig if "arc" in self.canvas.gettags(p)]
        a.remove(self.canvas_repr)
        in_overlapping = False
        for i in self.canvas.arcs:
            if i.negative: continue
            if i.canvas_repr in a:
                l2,r2,t2,b2 = i.get_bounding_box()
                if check_overlapping_of_boundig_box(l,r,t,b,l2,r2,t2,b2) or check_overlapping_of_boundig_box(l2,r2,t2,b2,l,r,t,b):
                    self.canvas.itemconfig(self.canvas_repr, fill='red')
                    in_overlapping = True
        ############### with Rectangle ###################
        a = [p for p in orig if "rect" in self.canvas.gettags(p)]
        for i in self.canvas.rectangles:
            if i.negative: continue
            if i.canvas_repr in a:
                if check_overlapping_of_boundig_box(l,r,b,t,i.x1,i.x2,i.y1,i.y2) or check_overlapping_of_boundig_box(i.x1,i.x2,i.y1,i.y2,l,r,t,b):
                    self.canvas.itemconfig(self.canvas_repr, fill='red')
                    in_overlapping = True
        if not in_overlapping and self not in self.canvas.selected:
            self.canvas.itemconfig(self.canvas_repr, fill=self.root.colors["sb_draw"])
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

class RightTriangle():
    def __init__(self,canvas,root,center_x,center_y,w,h, orientation=0, Negative=False):
        #   h ◣
        #     w
        self.canvas = canvas
        self.root = root
        self.center = np.array([center_x,center_y])
        self.negative = Negative
        self.w = w
        self.h = h
        self.orietation = min (360,orientation)
        self.type = "rightTriangle"
        self.area = w*h/2
        self.rotation_matrix =np.matrix([[cos(radians(orientation)),-sin(radians(orientation))] , [sin(radians(orientation)),cos(radians(orientation))]])
        self.points = [self.center, np.array(self.center+self.rotation_matrix.dot([w,0]))[0], np.array(self.center+self.rotation_matrix.dot([0,-h]))[0]] 
        self.s_center = sum(self.points)/3
        self.canvas_repr = self.canvas.create_polygon(self.points[0][0],self.points[0][1],self.points[1][0],self.points[1][1],self.points[2][0],self.points[2][1], fill=self.root.colors["sb_draw"], tags=("arc","shape"))
        if self.negative: self.canvas.negatives.append(self)
        #print(self.canvas.coords(self.canvas_repr))
    def refresh(self, center_x, center_y,w,h):
        self.center = np.array([center_x,center_y])
        self.w = w
        self.h = h
        self.area = w*h/2
        #print(self.points[0][0],self.points[0][1],self.points[1][0],self.points[1][1],self.points[2][0],self.points[2][1])
        self.points = [self.center, np.array(self.center+self.rotation_matrix.dot([w,0]))[0], np.array(self.center+self.rotation_matrix.dot([0,-h]))[0]] 
        self.s_center = sum(self.points)/3
        l,r = center_x, center_x
        t,b = center_y,center_y
        for i in self.points: l = min(l,i[0])
        for i in self.points: r = max(r,i[0]) 
        for i in self.points: t = min(t,i[1]) 
        for i in self.points: b = max(b,i[1])  
        #print(self.points[0][0],self.points[0][1],self.points[1][0],self.points[1][1],self.points[2][0],self.points[2][1])
        self.canvas.coords(self.canvas_repr, self.points[0][0],self.points[0][1],self.points[1][0],self.points[1][1],self.points[2][0],self.points[2][1])

    def align(self):
        print("Warning: align is not implemented!!")
        return 0
        self.align_to_axis()
        self.align_to_rect()
        self.align_to_arc()
    def align_to_axis(self):
        raise NotImplementedError
        if self.canvas.root.show_orig_axis:
            #* Sticking with the center of the rectangle to the coordinate system
            if abs(self.center[0]-self.canvas.Xcenter)<EPSILON:
                self.refresh(self.canvas.Xcenter,self.center[1],self.r,self.angle,self.start)
            if abs(self.center[1]-self.canvas.Ycenter)<EPSILON:
                self.refresh(self.center[0],self.canvas.Ycenter,self.r,self.angle,self.start)
    def align_to_arc(self):
        raise NotImplementedError
        own = self.get_charachteristic_points()
        for i in self.canvas.arcs:
            aling_score = 0 # if at least two points are near eachother, then it alignes them
            other = i.get_charachteristic_points()
            for k in own:
                for j in other:
                    if dist(k,j) <= EPSILON: 
                        aling_score+=1
                        displacement = (j[0]-k[0], j[1]-k[1])
            if aling_score >= 2:
                self.refresh(self.center[0]+displacement[0], self.center[1]+displacement[1], self.r, self.angle,self.start)
                break
    def align_to_rect(self):
        raise NotImplementedError
        own = self.get_charachteristic_points()
        x = [p[0] for p in own]
        y = [p[1] for p in own]
        arc_x = max(set(x), key=x.count)
        arc_y = max(set(y), key=y.count)
        dx = 0
        dy = 0
        for i in self.canvas.rectangles:
            # align by x
            for j in [i.x1,i.x2,i.center[0]]:
                if abs(j-arc_x) < EPSILON:
                    dx = j- arc_x
                    break
            #align by y
            for j in [i.y1,i.y2,i.center[1]]:
                if abs(j-arc_y) < EPSILON:
                    dy = j- arc_y
                    break
            if dx != 0 or dy != 0:
                self.refresh(self.center[0]+dx,self.center[1]+dy,self.r,self.angle,self.start)
                own = self.get_charachteristic_points()
                x = [p[0] for p in own]
                y = [p[1] for p in own]
                arc_x = max(set(x), key=x.count)
                arc_y = max(set(y), key=y.count)
                dx = 0
                dy = 0
                for k in own:
                    for l in [(i.x1,i.y1),(i.x1,i.y2),(i.x2,i.y1),(i.x2,i.y2)]:
                        if dist(k,l)<EPSILON:
                            dx = l[0]-k[0]
                            dy = l[1]-k[1]
                            self.refresh(self.center[0]+dx,self.center[1]+dy,self.r,self.angle,self.start)
                            own = self.get_charachteristic_points()
                            x = [p[0] for p in own]
                            y = [p[1] for p in own]
                            arc_x = max(set(x), key=x.count)
                            arc_y = max(set(y), key=y.count)
                            dx = 0
                            dy = 0
    def is_overlapping(self):
        if self.negative: 
            self.canvas.itemconfig(self.canvas_repr, fill='gray')
            return 0
        self.canvas.itemconfig(self.canvas_repr, fill=self.root.colors["sb_draw"])
        print("Warning: overlapping detection is not implemented")
        return -1
        l,r,t,b = self.get_bounding_box()
        orig=list(self.canvas.find_overlapping(l,t,r,b))
        ############# with another Arc ##################
        a = [p for p in orig if "arc" in self.canvas.gettags(p)]
        a.remove(self.canvas_repr)
        in_overlapping = False
        for i in self.canvas.arcs:
            if i.negative: continue
            if i.canvas_repr in a:
                l2,r2,t2,b2 = i.get_bounding_box()
                if check_overlapping_of_boundig_box(l,r,t,b,l2,r2,t2,b2) or check_overlapping_of_boundig_box(l2,r2,t2,b2,l,r,t,b):
                    self.canvas.itemconfig(self.canvas_repr, fill='red')
                    in_overlapping = True
        ############### with Rectangle ###################
        a = [p for p in orig if "rect" in self.canvas.gettags(p)]
        for i in self.canvas.rectangles:
            if i.negative: continue
            if i.canvas_repr in a:
                if check_overlapping_of_boundig_box(l,r,b,t,i.x1,i.x2,i.y1,i.y2) or check_overlapping_of_boundig_box(i.x1,i.x2,i.y1,i.y2,l,r,t,b):
                    self.canvas.itemconfig(self.canvas_repr, fill='red')
                    in_overlapping = True
        if not in_overlapping and self not in self.canvas.selected:
            self.canvas.itemconfig(self.canvas_repr, fill=self.root.colors["sb_draw"])
    def is_inside(self,point):
        #print("Warning: Is_inside not i,plemented")
        #return False
        # creating local coord system with the two orthogonal side of the triangle 
        xsi = (self.points[1] -self.center)/ self.w
        eta = (self.points[1]-self.center) / self.h
        p = ([point[0],point[1]]- self.center)

        p_transformed = [np.dot(p,xsi),np.dot(p,eta)]
        if p_transformed[0] < 0 or p_transformed[1]< 0:
            return False
        elif p[1] < -(self.h/self.w)*p[1] + self.h:
            return True 
            
        return False
    def translate(self,dx,dy):
        self.refresh(self.center[0]+dx,self.center[1]+dy, self.w,self.h)
    def get_info(self):
        text=f"Befogó 1 = {self.w/self.canvas.scale}\nBefogó 2 = {self.h/self.canvas.scale}\nKözéppont = ({(self.center[0]-self.canvas.Xcenter)/self.canvas.scale},{(self.canvas.Ycenter-self.center[1])/self.canvas.scale} Irányultság = {self.orietation})"
        return text
class Shapes():
    def __init__(self, canvas, rectangles, arcs,rightTriangles):
        self.canvas = canvas
        self.container = []
        self.rectangles = rectangles
        self.arcs = arcs
        self.rightTriangles = rightTriangles
        self.container.append(self.rectangles)
        self.container.append(self.arcs)
        self.container.append(self.rightTriangles)
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
        elif type(obj)==Arc:
            self.arcs.append(obj)
        elif type(obj==RightTriangle):
            self.rightTriangles.append(obj)
        else:
            print("Hiba: A formatum nem megfelelo!")
    def remove(self, obj):
        if type(obj)==Rectangle:
            self.rectangles.remove(obj)
        elif type(obj)==Arc:
            self.arcs.remove(obj)
        elif type(obj)==RightTriangle:
            self.rightTriangles.remove(obj)
        else:
            print("Hiba: A formatum nem megfelelo!")
