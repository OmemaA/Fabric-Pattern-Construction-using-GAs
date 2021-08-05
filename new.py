from Colors import ColorPalette
from PIL import Image
from PIL import ImageDraw
from Lsystem import Lsystem
import numpy as np
import random 
from PIL import Image, ImageFilter

rules = [
    {
        "F":"F+F--F+F", "S":"F",
        "direct":180,
        "angle":60,
        "iter":5,
        "title":"Koch"
    },
    {
        "X":"X+YF+", "Y":"-FX-Y", "S":"FX",
        "direct":0,
        "angle":90,
        "iter":13,
        "title":"Dragon"
    },
    {
        "f":"F-f-F", "F":"f+F+f", "S":"f",
        "direct":0,
        "angle":60,
        "iter":7,
        "title":"Triangle"
    },
    {
        "X":"F-[[X]+X]+F[+FX]-X", "F":"FF", "S":"X",
        "direct":-45,
        "angle":25,
        "iter":6,
        "title":"Plant"
    },
    {
        "S":"X", "X":"-YF+XFX+FY-", "Y":"+XF-YFY-FX+",
        "direct":0,
        "angle":90,
        "iter":6,
        "title":"Hilbert"
    },
    {
        "S":"L--F--L--F", "L":"+R-F-R+", "R":"-L+F+L-",
        "direct":0,
        "angle":45,
        "iter":10,
        "title":"Sierpinski"
    },
]

class Shapes:
    def __init__(self, child=False):
        self.block = Image.new('RGBA', (200,200))
        self.iters = 1
        self.lines = []
        self.polygons = []
        self.colors = []
        self.fracColor = []
        self.colorPalette = ColorPalette("Reference Images/10.jpg", 5).createPalette()
        self.child = child
        # Creating fractals 
        # rule = random.choice([0,1,3,4,5])
        rule = 1
        self.design = Lsystem(rules[rule]).get_lines()
        for _ in range(len(self.design)):
            m_fill = random.choice(self.colorPalette)
            m_fill = tuple([int(x*255) for x in m_fill]) 
            self.fracColor.append(m_fill)
        # Storing color for each polygon 
        if not self.child:
            limits= [(0,0), (200,0), (0,200), (200,200)]
            # Generating random polygons to contruct pattern
            self.__division(limits)
            for _ in range(len(self.polygons)):
                m_fill = random.choice(self.colorPalette)
                m_fill = tuple([int(x*255) for x in m_fill]) 
                self.colors.append(m_fill)
            self.generate_pattern()

    def __generate_random_point(self, p1, p2):
        u = random.random()
        pt_x, pt_y= int((1-u)*p1[0] + u*p2[0]), int((1-u)*p1[1] + u*p2[1])
        return (pt_x, pt_y)

    def __new_limits(self, limits, pt1, pt2, option, segment=None):
        first_half, second_half = [], []
        if option == 0:  # slant and vertical
            first_half = [(limits[0]), (pt1), (pt2), (limits[2]) ] # x1, y1, x2, y2
            second_half = [(pt1), (limits[1]), (limits[3]), (pt2)]
        elif option == 1: # slant and horizontal
            first_half = [(limits[0]), (limits[1]), (pt2), (pt1)]
            second_half = [(pt1), (pt2), (limits[3]), (limits[2])]
        elif option == 2: # vertical and horizontal
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

    def form_tile(self, chromosomes, name, tile_size):
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
                array[rows][columns]= trans_ch
        hstack=[]
        for row in array:
            r=np.hstack(tuple(row))
            hstack.append(r)
        hstack=np.array(hstack)
        vstack=np.vstack(tuple(hstack))
        img = Image.fromarray(vstack)
        img = self.generate_LTree(img)
        # img = Image.fromarray(vstack)
        img.save('Pattern'+str(name)+'.png', 'PNG')
        # image=img.filter(ImageFilter.ModeFilter(size=25))
        # final=image.filter(ImageFilter.SMOOTH_MORE)
    
        # final.save('Pattern'+str(name)+'.png', 'PNG')
        # img.show()

    def generate_pattern(self):
        self.block = Image.new('RGBA', (200,200))
        m_fill = random.choice(self.colorPalette)
        m_fill = tuple([int(x*255) for x in m_fill])
        ImageDraw.Draw(self.block).rectangle((0, 0, 200, 200), fill=m_fill)
        for i in range(len(self.polygons)):
            ImageDraw.Draw(self.block).polygon(self.polygons[i], fill=self.colors[i])
        # for i in range(len(self.design)):
        #     ImageDraw.Draw(self.block).line(self.design[i], fill=self.fracColor[i])
        # tmp_image = self.block
        # 50% chance to apply smoothing 
        if random.choice([1,2]) == 0:
            self.block = self.block.filter(ImageFilter.ModeFilter(size=25))
            self.block = self.block.filter(ImageFilter.SMOOTH_MORE)
        self.form_tile(np.array(self.block), " lsystem", 2)

    def generate_LTree(self, img):
        for i in range(len(self.design)):
            ImageDraw.Draw(img).line(self.design[i], fill=self.fracColor[i])
        return img


    def __division(self, limits, iterx=0, itery=0):
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
            pt1, pt2 = self.__generate_random_point(limits[0], limits[1]), self.__generate_random_point(limits[2], limits[3])  
        elif option == 1: # left and right
            pt1, pt2 = self.__generate_random_point(limits[0], limits[2]), self.__generate_random_point(limits[1], limits[3])  
        elif option == 2: # vertical and horizontal
            v_side, h_side = random.randint(0,1), random.randint(0,1)
            if v_side == 0: # top 
                pt1 = self.__generate_random_point(limits[0], limits[1])
                segment = "T"
            elif v_side == 1: # bottom
                pt1 = self.__generate_random_point(limits[2], limits[3])
                segment = "B"

            if h_side == 0: # left
                pt2 = self.__generate_random_point(limits[0], limits[2])
                segment += "L"
            elif h_side == 1: # right
                pt2 = self.__generate_random_point(limits[1], limits[3])
                segment += "R"

        self.lines.append([pt1, pt2])
        new_limits = self.__new_limits(limits, pt1, pt2, option, segment)
        self.polygons.extend(new_limits)
        
        self.__division(new_limits[0], iterx+1, itery)
        self.__division(new_limits[1], iterx, itery+1)

s = Shapes()
s.generate_pattern()