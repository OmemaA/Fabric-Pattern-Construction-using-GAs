from Colors import ColorPalette
from PIL import Image
from PIL import ImageDraw
import numpy as np
from random import randint
# import image_slicer

class Shapes:
    def __init__(self):
        self.colors = ColorPalette("Reference Images/1.jpg", 10).createPalette()
        self.block = Image.new('RGBA', (200,200))
        # self.lines = int(randint(3,10))
        self.lines = 4
        self.polygons = [] 
        limits = [(0,200), (0,0), (0,200), (200,200)] # x1, y1, x2, y2
        self.division(0,0, limits)
        for i in range(len(self.polygons)):
            ImageDraw.Draw(self.block).line(self.polygons[i])
        self.block.show()


    def division(self, iterx, itery, limits):
        print("iterx", iterx, "itery", itery)
        if(iterx == self.lines):
            print("HEREE")
            iterx = 0
            return
        elif(itery == self.lines):
            itery = 0
            return

        coords = []
        pt1 = randint(limits[0][0], limits[0][1]), randint(limits[1][0], limits[1][1])
        pt2 = randint(limits[2][0], limits[2][1]), randint(limits[3][0], limits[3][1])
        # print("pt1", pt1)
        # print("pt2", pt2)

        coords.append((pt1[0], pt1[1]))
        coords.append((pt2[0], pt2[1]))
            
        self.polygons.append(coords)

        new_limits_left = [(limits[0][0], pt1[0]), (limits[1][0], pt1[1]), (limits[2][0], pt2[0]), (limits[3][0], pt2[1])]
        new_limits_right = [(pt1[0], limits[0][1]), (pt1[1], limits[1][1]), (pt2[0], limits[2][1]), (pt2[1], limits[3][1])]
        # print("left",new_limits_left)
        # print("right",new_limits_right)

        self.division(iterx+1, itery, new_limits_left)
        self.division(iterx, itery+1, new_limits_right)

s = Shapes()

            

# c = ColorPalette("Reference Images/1.jpg", 5)
# c.displayPalette()