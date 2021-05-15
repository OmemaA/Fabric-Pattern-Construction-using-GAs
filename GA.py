from copy import deepcopy
from operator import sub
import numpy as np
from pprint import pprint
from PIL import Image
import matplotlib.pyplot as plt #importing matplotlib
# import cv2
from scipy import ndimage

pixels = 32


def imhist(im):
	m, n = im.shape
	h = [0.0] * 256
	for i in range(m):
		for j in range(n):
			h[int(im[i, j])]+=1
	return np.array(h)

def cumsum(h):
	return [sum(h[:i+1]) for i in range(len(h))]

def histeq(im):
    h = imhist(im)
	# cdf = np.array(cumsum(h))
    cdf = h.cumsum()
	# sk = np.uint8(255 * cdf)
	# s1, s2 = im.shape
	# Y = np.zeros_like(im)
	# for i in range(0, s1):
	# 	for j in range(0, s2):
	# 		Y[i, j] = sk[int(im[i, j])]
	# H = imhist(Y)
    cdf_normalized = cdf * h.max()/ cdf.max()
    
    return  h, cdf_normalized

class EvolutionaryAlgorithm:
    def __init__(self):
        self.offsprings = 10
        self.generations = 5000
        self.fitness = None

    def initialPopulation(self):
        values = np.random.randint(0, 255, (pixels, pixels,3))
        gray = np.dot(values[...,:3],[0.299, 0.587, 0.114])
        # gray = np.average(values, axis=-1)
        # img = Image.fromarray(gray)
        # img.show()
        # exit(1)
        return gray


    def computeFitness(self, path):
        gx, gy = np.gradient(path)
        h, new_h= histeq(path)
        result=np.subtract(h,new_h)
        gx=sum([sum(x) for x in gx])
        gy=sum([sum(x) for x in gy])
        cost=(gx)+(gy)+sum(result)
        return cost
        
    def mutation(self, chromosomes):
        replicas = [deepcopy(chromosomes) for i in range(100)]
        for i in replicas:
            for pixel in i:
                number = np.random.randint(0,3)
                pts = np.random.randint(0, pixels, size=2)
                if number == 0:
                    pixel[pts[0]], pixel[pts[1]] = pixel[pts[1]], pixel[pts[0]]
                elif number == 1:
                    pixel[pts[0]] = pixel[pts[1]]
                elif number == 2:
                    value = np.random.randint(0,255,(1,1,3))
                    pixel[pts[0]] = float(np.dot(value[...,:3], [0.299, 0.587, 0.114]))
                    # pixel[pts[0]] = np.average(value, axis = -1)
        replicas.append(chromosomes)
        #print(len(replicas),len(chromosomes))
        return replicas


    # EA cycle
    def cycle(self, maximise):
        generations = 0
        chromosomes = self.initialPopulation() 
        #print("chromosomes",chromosomes)
        while generations < self.generations:
            if generations % 250 == 0:
                print('Generation', generations+1)
            # Replication and mutation
            candidates = self.mutation(chromosomes)
            #self.fitness=self.computeFitness(candidates)
            # Fitness evaluation of each individual in population
            self.fitness = [self.computeFitness(indv) for indv in candidates]
            # Survivor selection
            chromosomes = candidates[self.fitness.index(min(self.fitness))]
            generations +=1
        #img = Image.fromarray(chromosomes)
        #img.show()
        form_tile(chromosomes)
    


def form_tile(chromosomes):
    hor=np.flip(chromosomes,0)
    vert=np.flip(chromosomes,1)
    left=np.flip(hor,1)
    a=np.hstack((hor,chromosomes))
    b=np.hstack((left,vert))
    array_tuple = (a,b)
    f=np.vstack(array_tuple)
    img = Image.fromarray(f)
    img.show()
    
ea = EvolutionaryAlgorithm()
ea.cycle(True)
#chromosome = ea.initialPopulation()
#ea.mutation(chromosome)