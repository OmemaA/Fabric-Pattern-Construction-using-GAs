from ImageQuality import ImageQuality
from Shapes import Shapes
import random
import numpy as np
import math

class GA:
    def __init__(self):
        self.popSize = 10
        self.generations = 50
        self.fitness = None
        self.offsprings = 5
        self.mutationRate = 0.5

    def initial_population(self):
        population = [Shapes() for _ in range(self.popSize)]
        return population

    def compute_fitness(self, img):
        quality = ImageQuality(img.block)
        return quality.get_fitness()

    def mutation(self, population):
        # randomly assign a color from color palette
        for i in population:
            chance = random.randint(1,10)
            if chance < 5:
                index = random.randint(0, (len(i.polygons)-1))
                m_fill = random.choice(i.colorPalette)
                m_fill = tuple([int(x*255) for x in m_fill])
                i.colors[index] = m_fill
                i.generate_pattern()

    def crossover(self, parent1, parent2):
        line = [(0,100) , (200,100)]
        # top and bottom parents
        top, bottom = [], []
        t_colors, b_colors = [], []

        # Top half
        for iter, i in enumerate(parent1.polygons):
            v1 = (line[1][0]-line[0][0], line[1][1]- line[0][1]) # x2-x1, y2-y1
            accepted, discarded = [], []
            for x in i:
                v2 = (line[1][0]-x[0], line[1][1]-x[1]) #x2 - xA, y2-yA
                dot = v1[0]*v2[1] - v1[1]*v2[0]  # Cross product
                if dot >= 0: # top or on the line 
                    accepted.append(x)
                else:
                    discarded.append(x)
            if len(accepted) > 2:
                top.append(accepted)
                t_colors.append(parent1.colors[iter])
            elif len(accepted) > 1: # adjust coordinates
                min = math.inf
                index = discarded[0]
                for coord in discarded:
                    p1, p2, p3 = np.asarray(line[0]), np.asarray(line[1]), np.asarray(x)
                    d = np.linalg.norm(np.cross(p2-p1, p1-p3))/np.linalg.norm(p2-p1)
                    if d < min: 
                        min = d
                        index = coord
                accepted.append((index[0], line[0][1]))
                top.append(accepted)
                t_colors.append(parent1.colors[iter])

        # Bottom half
        for iter, i in enumerate(parent2.polygons):
            v1 = (line[1][0]-line[0][0], line[1][1]- line[0][1]) # x2-x1, y2-y1
            accepted, discarded = [], []
            for x in i:
                v2 = (line[1][0]-x[0], line[1][1]-x[1]) #x2 - xA, y2-yA
                dot = v1[0]*v2[1] - v1[1]*v2[0]  # Cross product
                if dot <= 0: # top or on the line 
                    accepted.append(x)
                else:
                    discarded.append(x)
            if len(accepted) > 2:
                bottom.append(accepted)
                b_colors.append(parent2.colors[iter])
            elif len(accepted) > 1: # adjust coordinates
                min = math.inf
                index = discarded[0]
                for coord in discarded:
                    p1, p2, p3 = np.asarray(line[0]), np.asarray(line[1]), np.asarray(x)
                    d = np.linalg.norm(np.cross(p2-p1, p1-p3))/np.linalg.norm(p2-p1)
                    if d < min: 
                        min = d
                        index = coord
                accepted.append((index[0], line[0][1]))
                bottom.append(accepted)
                b_colors.append(parent1.colors[iter])

        offspring = Shapes(True)
        offspring.polygons.extend(top)
        offspring.polygons.extend(bottom)
        offspring.colors.extend(t_colors)
        offspring.colors.extend(b_colors)
        offspring.generate_pattern()

        return offspring

    def cycle(self):
        generations = 0
        chromosomes = self.initial_population() 
        # compute fitness of each individual in population
        self.fitness = [self.compute_fitness(indv) for indv in chromosomes]
        while generations < self.generations:
            # print("Generation: ", generations)
            # Saving image after every 250 generations
            if generations % 10 == 0:
                print('Generation', generations+1)
                for x in chromosomes:
                    fit = min([self.compute_fitness(i) for i in chromosomes])
                    if self.compute_fitness(x) == fit:
                        x.form_tile(np.array(x.block), str(generations))
                        print("Fitness:", fit)
                        break
            for _ in range(self.offsprings):
                # parent selection
                parent1, parent2 = self.random(chromosomes)[:2]
                # cross over
                offspring  = self.crossover(parent1, parent2)
                # add new offspring to population
                chromosomes.append(offspring)
                # compute fitness of new offspring
                self.fitness.append(self.compute_fitness(offspring))
                # mutation
                if random.random() < self.mutationRate:
                    self.mutation(chromosomes)
            # survivor selection
            chromosomes = self.truncation(chromosomes,self.popSize)
            # compute fitness of each individual in population
            self.fitness = [self.compute_fitness(indv) for indv in chromosomes]
            generations +=1

    def truncation(self, chromosomes, size):
        indexes = [(self.fitness[i], i) for i in range(len(self.fitness))]
        # sorts list accoridng to fitness
        indexes.sort(key = lambda x: x[0], reverse=True)
        indexes = indexes[:size]
        # selects top N elements
        top_N = [chromosomes[i[1]] for i in indexes]
        return top_N
    
    def random(self, chromosomes):
        # randomly selects 2 chromosomes from population
        return random.sample(chromosomes, 2)
   


# i = Image.open("Reference Images/6.jpg")
# x = Image.open("test.jpg")
# print(GA().fitness_function(i))
# print(GA().fitness_function(x))

ga = GA()
ga.cycle()