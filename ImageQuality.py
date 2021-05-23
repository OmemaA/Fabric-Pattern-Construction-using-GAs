# import cv2
from PIL import Image
import numpy as np

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
        for index, colour in enumerate(colours):
            count = counts[index]
            proportion = (100 * count) / (h * w)
            print(f"   Colour: {colour}, count: {count}, proportion: {proportion:.2f}%")

    def dullness_score(self):
        # convert image to HSV (hue, saturation, value)
        img = self.img.convert('HSV')
        n_img = np.array(img)

        # Arrange all pixels as RGB values and find unique rows to get colours
        colours = np.unique(n_img.reshape(-1,3), axis=0)
        
        total_score = 0
        # Iterate through unique colours
        for index, colour in enumerate(colours):
            total_score += sum(colour)

        return total_score/len(colours)
            
    # def color_hormonies(self):
    #     # convert image to HSV (hue, saturation, value)
    #     img = self.img.convert('HSV')
    #     n_img = np.array(img)
    #     # print(n_img)

    def global_contrast(self):
        # Convert image to grayscale to get lightness channel
        grayscale = self.img.convert('L')

        # compute global min and max intensity values
        minimum = np.min(grayscale)
        maximum = np.max(grayscale)

        # compute contrast
        return (maximum - minimum)/(maximum + minimum)


i = Image.open("Reference Images/6.jpg")
# i = Image.new('RGBA', (200,200))
IQ = ImageQuality(i).dullness_score()


# cv2.imshow("image",self.img)
# cv2.waitKey(0)

# LAB_image = cv2.cvtColor(np.array(self.img), cv2.COLOR_BGR2LAB)
# # Lightness channel
# L = cv2.split(LAB_image)[0] 

# # compute global min and max intensity values
# minimum = np.min(L)
# maximum = np.max(L)

# # compute contrast
# avg_contrast = (maximum - minimum)/(maximum + minimum)



# kernel = np.ones((5,5),np.uint8)
# min = cv2.erode(L,kernel,iterations = 1)
# max = cv2.dilate(L,kernel,iterations = 1)

# # convert min and max to floats
# min = min.astype(np.float64) 
# max = max.astype(np.float64) 

# # compute local contrast
# contrast = (max-min)/(max+min)

# # get average across whole image
# average_contrast = 100*np.mean(contrast)