# import cv2
from PIL import Image
import numpy as np
import statistics

class ImageQuality():
    def __init__(self, img):
        self.img = img
    
    def get_fitness(self):
        return (self.dullness_score())

    def area_occupied(self):
        img = self.img.convert('RGB')
        n_img = np.array(img)
        h, w = n_img.shape[:2]

        # Arrange all pixels as RGB values and find unique rows to get colours
        colours, counts = np.unique(n_img.reshape(-1,3), axis=0, return_counts=1)

        # Iterate through unique colours
        # proportion = [20,20,19,18,20]
        proportion =[]
        for index, colour in enumerate(colours):
            count = counts[index]
            proportion.append((100 * count) / (h * w))
        std = statistics.stdev(proportion)
        # p_max, p_min = max(proportion), min(proportion)
        new = []
        mean = 100/len(colours)
        for i in proportion:
            new.append((i-mean)/std)
        # normalized_std = (statistics.stdev(new)) / (100/len(colours))
        return new
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
            score = colour[0] + colour[1] + colour[2]*self.global_contrast()
            # total_score += sum(colour)
            total_score += score
        return total_score/len(colours)

    def global_contrast(self):
        # Convert image to grayscale to get lightness channel
        grayscale = self.img.convert('L')

        # compute global min and max intensity values
        minimum = np.min(grayscale)
        maximum = np.max(grayscale)

        # compute contrast
        return (maximum - minimum)/(maximum + minimum)


# i = Image.open("Patterns Generated/Palette 1/Final_1.png")
# IQ = ImageQuality(i).area_occupied()
# print(IQ)