from copy import deepcopy
import numpy as np
from pprint import pprint
from PIL import Image


pixels = 32

class EvolutionaryAlgorithm:
    def __init__(self):
        self.offsprings = 10
        self.generations = 15000
        self.fitness = None

    def initialPopulation(self):
        values = np.random.randint(0, 255, (pixels, pixels,3))
        gray = np.dot(values[...,:3],[0.299, 0.587, 0.114])
        # img = Image.fromarray(gray)
        # img.show()
        return gray

    def computeFitness(self, path):
        pass
        

    def mutation(self, chromosomes):
        replicas = [deepcopy(chromosomes) for i in range(3)]
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
        return replicas


    # EA cycle
    def cycle(self, maximise):
        generations = 0
        chromosomes = self.initialPopulation() 
        while generations < self.generations:
            if generations % 250 == 0:
                print('Generation', generations+1)
                img = Image.fromarray(chromosomes)
                img.show()
            # Replication and mutation
            candidates = self.mutation(chromosomes)
            candidates.append(chromosomes)

            # Fitness evaluation of each individual in population
            self.fitness = [self.computeFitness(indv) for indv in chromosomes]

            # Survivor selection
            chromosomes = chromosomes[self.fitness.index(min(self.fitness))]
            generations +=1 


# ea = EvolutionaryAlgorithm()
# chromosome = ea.initialPopulation()
# pprint(ea.mutation(chromosome))
