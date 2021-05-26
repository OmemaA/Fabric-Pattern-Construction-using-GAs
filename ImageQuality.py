# import cv2
from os import popen
from PIL import Image
import numpy as np
import statistics

class ImageQuality():
    def __init__(self, img):
        self.img = img
    
    def get_fitness(self):
        return (self.dullness_score()*self.area_occupied())

    def area_occupied(self):
        img = self.img.convert('RGB')
        n_img = np.array(img)
        h, w = n_img.shape[:2]

        # Arrange all pixels as RGB values and find unique rows to get colours
        colours, counts = np.unique(n_img.reshape(-1,3), axis=0, return_counts=1)

        # Iterate through unique colours
        proportion =[]
        for index, colour in enumerate(colours):
            count = counts[index]
            proportion.append((100 * count) / (h * w))
        # if only one color present
        if len(proportion) == 1:
            proportion.append(0)
        std = statistics.stdev(proportion)
        if std == 0: 
            std = 0.5
        return 1/std
        # print(f"   Colour: {colour}, count: {count}, proportion: {proportion:.2f}%")

    def dullness_score(self):
        # convert image to HSV (hue, saturation, value)
        img = self.img.convert('HSV')
        n_img = np.array(img)

        # Arrange all pixels as RGB values and find unique rows to get colours
        colours = np.unique(n_img.reshape(-1,3), axis=0)
   
        total_score = 0
        # Iterate through unique colours
        for colour in colours:
            score = int(colour[0]) + int(colour[1]) + int(colour[2])*self.global_contrast()
            # total_score += sum(colour)
            total_score += score
        return total_score/len(colours)

    def global_contrast(self):
        # Convert image to grayscale to get lightness channel
        grayscale = self.img.convert('L')

        # compute global min and max intensity values
        minimum = int(np.min(grayscale))
        maximum = int(np.max(grayscale))

        # compute contrast
        return (maximum - minimum)/(maximum + minimum)
