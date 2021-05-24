from Colors import ColorPalette
from PIL import Image
from PIL import ImageDraw
import numpy as np
import random 

class Shapes:
    def __init__(self, child=False):
        self.block = Image.new('RGBA', (200,200))
        self.iters = 1
        self.lines = []
        self.polygons = []
        self.colors = []
        self.colorPalette = ColorPalette("Reference Images/1.jpg", 10).createPalette()
        if not child:
            limits= [(0,0), (200,0), (0,200), (200,200)]
            # Generating random polygons to contruct pattern
            self.division(limits)
            # Storing color for each polygon 
            for _ in range(len(self.polygons)):
                m_fill = random.choice(self.colorPalette)
                m_fill = tuple([int(x*255) for x in m_fill])
                self.colors.append(m_fill)
            self.generate_pattern()

    def generate_random_point(self, p1, p2):
        u = random.random()
        pt_x, pt_y= int((1-u)*p1[0] + u*p2[0]), int((1-u)*p1[1] + u*p2[1])
        return (pt_x, pt_y)

    def new_limits(self, limits, pt1, pt2, option, segment=None):
        first_half, second_half = [], []
        if option == 0:  # slant and vertical
            first_half = [(limits[0]), (pt1), (pt2), (limits[2]) ] # x1, y1, x2, y2
            second_half = [(pt1), (limits[1]), (limits[3]), (pt2)]
        elif option == 1: # slant and horizontal
            first_half = [(limits[0]), (limits[1]), (pt2), (pt1)]
            second_half = [(pt1), (pt2), (limits[3]), (limits[2])]
        elif option == 2:
            if segment == "TL":
                first_half = [(limits[0]), (pt1), (pt2)]
                second_half = [(pt1), (pt2), (limits[1]), (limits[3]), (limits[2])]
            elif segment == "TR":
                first_half = [(limits[0]), (pt1), pt2, (limits[3]), (limits[2])]
                second_half = [(pt1), (limits[1]), (pt2)]
            elif segment == "BL":
                first_half = [(pt1), (limits[2]), (pt2)]
                second_half = [(limits[0]), (limits[1]), (limits[3]), (pt1), pt2]
            elif segment == "BR":
                first_half = [(limits[0]), (limits[1]), (pt2), (pt1), (limits[2])]
                second_half = [(pt1), (pt2), (limits[3])]

        return first_half, second_half

    def form_tile(self,chromosomes, name,tile_size):
        array =  np.empty((tile_size, tile_size), dtype=object)
        for columns in range(tile_size):
            for rows in range(tile_size):
                trans=random.randint(0,3)
                if trans==0:
                    trans_ch=np.fliplr(chromosomes)
                elif trans==1:
                    trans_ch=np.flipud(chromosomes)
                elif trans==2:
                    horiz=np.fliplr(chromosomes)
                    trans_ch=np.flipud(horiz)
                else:
                     trans_ch=chromosomes
                array[rows][columns]=trans_ch
        hstack=[]
        for row in array:
            r=np.hstack(tuple(row))
            hstack.append(r)
        hstack=np.array(hstack)
        vstack=np.vstack(tuple(hstack))
        img = Image.fromarray(vstack)
        # img.show()
        img.save('Pattern'+str(name)+'.png', 'PNG')

    def generate_pattern(self):
        self.block = Image.new('RGBA', (200,200))
        ImageDraw.Draw(self.block).rectangle((0, 0, 200, 200), fill='white')
        for i in range(len(self.polygons)):
            ImageDraw.Draw(self.block).polygon(self.polygons[i], fill=self.colors[i])
            
        # self.form_tile(np.array(self.block), name)
 
    def division(self, limits, iterx=0, itery=0):
        if(iterx == self.iters):
            iterx = 0
            return
        if(itery == self.iters):
            itery = 0
            return
        pt1, pt2 = (0,0), (0,0)
        option = random.randint(0,2)
        segment = None
        if option == 0: # top and bottom 
            pt1, pt2 = self.generate_random_point(limits[0], limits[1]), self.generate_random_point(limits[2], limits[3])  
        elif option == 1: # left and right
            pt1, pt2 = self.generate_random_point(limits[0], limits[2]), self.generate_random_point(limits[1], limits[3])  
        elif option == 2: # vertical and horizontal
            v_side, h_side = random.randint(0,1), random.randint(0,1)
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
        
        # for _ in range(2):
        #     m_fill = random.choice(self.colorPalette)
        #     m_fill = tuple([int(x*255) for x in m_fill])
        #     self.colors.append(m_fill)

        # self.generate_pattern()
        self.division(new_limits[0], iterx+1, itery)
        self.division(new_limits[1], iterx, itery+1)

# s = Shapes()
# s.generate_pattern()
