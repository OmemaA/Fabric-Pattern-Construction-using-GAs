from types import TracebackType
from Colors import ColorPalette
from PIL import Image
from PIL import ImageDraw
import numpy as np
from random import randint
from random import random
from random import choice

class Shapes:
    def __init__(self):
        self.colors = ColorPalette("Reference Images/5.jpg", 10).createPalette()
        self.block = Image.new('RGBA', (200,200))
        # self.iters = int(randint(3,10))
        self.iters = 1
        self.lines = []
        self.polygons = []
        limits= (0,0), (200,0), (0,200), (200,200)
        self.division(limits)

        # Attempt to draw polygons with colors filled in
        # print(m_fill)
        ImageDraw.Draw(self.block).rectangle((0, 0, 200, 200), fill='pink')
        for i in range(len(self.polygons)):
            m_fill = choice(self.colors)
            m_fill = tuple([int(x*255) for x in m_fill])
            ImageDraw.Draw(self.block).polygon(self.polygons[i], fill=m_fill)
            
        # for i in range(len(self.lines)):
        #     ImageDraw.Draw(self.block).line(self.lines[i], fill='black')
        # self.block.show()
        self.form_tile(np.array(self.block))
    
        
    def generate_random_point(self, p1, p2):
        u = random()
        pt_x, pt_y= int((1-u)*p1[0] + u*p2[0]), int((1-u)*p1[1] + u*p2[1])
        return (pt_x, pt_y)

    def new_limits(self, limits, pt1, pt2, option, segment=None):
        first_half, second_half = [], []
        if option == 0:  # slant and vertical
            first_half = [(limits[0]), (pt1), (limits[2]), (pt2)] # x1, y1, x2, y2
            second_half = [(pt1), (limits[1]), (pt2), (limits[3])]
        elif option == 1: # slant and horizontal
            first_half = [(limits[0]), (limits[1]), (pt1), (pt2)]
            second_half = [(pt1), (pt2), (limits[2]), (limits[3])]
        elif option == 2:
            if segment == "TL":
                first_half = [(limits[0]), (pt1), (pt2)]
                second_half = [(pt1), (limits[1]), (pt2), (limits[2]), (limits[3])]
            elif segment == "TR":
                first_half = [(limits[0]), (pt1), (limits[1]), (limits[2], (pt2))]
                second_half = [(pt1), (limits[1]), (pt2)]
            elif segment == "BL":
                first_half = [(pt1), (limits[2]), (pt2)]
                second_half = [(limits[0]), (limits[1]), (pt1), (pt2), (limits[3])]
            elif segment == "BR":
                first_half = [(limits[0]), (limits[1]), (limits[2]), (pt1), (pt2)]
                second_half = [(pt1), (pt2), (limits[3])]

        return first_half, second_half

    def form_tile(self,chromosomes):
        hor=np.flip(chromosomes,0)
        vert=np.flip(chromosomes,1)
        left=np.flip(hor,1)
        a=np.hstack((hor,chromosomes))
        b=np.hstack((left,vert))
        array_tuple = (a,b)
        f=np.vstack(array_tuple)
        img = Image.fromarray(f)
        img.show()


    def generate_pattern(self):
        limits = []

        self.division(0,0, limits)
        for i in range(len(self.polygons)):
            ImageDraw.Draw(self.block).line(self.polygons[i])
        self.block.show()
        

    def division(self, limits, iterx=0, itery=0):

        # print("iterx", iterx, "itery", itery)
        if(iterx == self.iters):
            # print("HEREE")
            iterx = 0
            return
        if(itery == self.iters):
            itery = 0
            return
        pt1, pt2 = (0,0), (0,0)
        option = randint(0,1)
        segment = None
        if option == 0: # top and bottom 
            pt1, pt2 = self.generate_random_point(limits[0], limits[1]), self.generate_random_point(limits[2], limits[3])  
        elif option == 1: # left and right
            pt1, pt2 = self.generate_random_point(limits[0], limits[2]), self.generate_random_point(limits[1], limits[3])  
        elif option == 2: # vertical and horizontal
            v_side, h_side = randint(0,1), randint(0,1)
            if v_side == 0: # top 
                pt1 = self.generate_random_point(limits[0], limits[1])
                segment = "T"
            elif v_side == 1: # bottom
                pt1 = self.generate_random_point(limits[2], limits[3])
                segment = "B"

            if h_side == 0: # left
                pt2 = self.generate_random_point(limits[0], limits[2])
                segment += "L"
            elif h_side == 1: # right
                pt2 = self.generate_random_point(limits[1], limits[3])
                segment += "R"

        self.lines.append([pt1, pt2])

        new_limits = self.new_limits(limits, pt1, pt2, option, segment)
        self.polygons.extend(new_limits)
        # print(new_limits)
        self.division(new_limits[0], iterx+1, itery)
        self.division(new_limits[1], iterx, itery+1)


s = Shapes()


