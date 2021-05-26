from ImageQuality import ImageQuality
from Shapes import Shapes
import random
import numpy as np
import matplotlib.pyplot as plt

class GA:
    def __init__(self):
        self.popSize = 10
        self.generations = 40
        self.fitness = None
        self.offsprings = 5
        self.mutationRate = 0.5
        self.generations_score = [[] for _ in range(self.generations)]
        self.iterations = 5
        self.tileSize = random.choice([5,10,15,20,25,30,35])

    def __initial_population(self):
        population = [Shapes() for _ in range(self.popSize)]
        return population

    def __compute_fitness(self, img):
        quality = ImageQuality(img.block)
        return quality.get_fitness()

    def __mutation(self, offspring):
        index = random.randint(0, (len(offspring.polygons)-1))
        m_fill = random.choice(offspring.colorPalette)
        m_fill = tuple([int(x*255) for x in m_fill])
        offspring.colors[index] = m_fill
        offspring.generate_pattern()
        return offspring

    def __crossover(self, parent1, parent2):
        orient = random.choice([0,1]) # 0: vertical, 1: horizontal
        line = [(100,0) , (100,200)]
        if orient:
            line = [(0, 100) , (200,100)]
        # top and bottom parents
        top, bottom = [], []
        t_colors, b_colors = [], []

        top, t_colors = self.__choose_vertices(parent1, line, top, t_colors, orient, True)
        bottom, b_colors = self.__choose_vertices(parent2, line, bottom, b_colors, orient, False)

        offspring = Shapes(True)
        offspring.polygons.extend(top)
        offspring.polygons.extend(bottom)
        offspring.colors.extend(t_colors)
        offspring.colors.extend(b_colors)
        offspring.generate_pattern()

        return offspring
    
    def __choose_vertices(self, parent, line, segment, seg_color, orient, upper):
        for iter, i in enumerate(parent.polygons):
            v1 = (line[1][0]-line[0][0], line[1][1]- line[0][1]) #line vector
            accepted, discarded = [], []
            for x in i: 
                v2 = (line[1][0]-x[0], line[1][1]-x[1]) # line and point vector
                dot = v1[0]*v2[1] - v1[1]*v2[0]
                if upper:
                    if dot >= 0: accepted.append(x)
                    else: discarded.append(x)
                else:
                    if dot <= 0: accepted.append(x)
                    else: discarded.append(x)
            if len(accepted) > 2:
                segment.append(accepted)
                seg_color.append(parent.colors[iter])
            
            elif len(accepted) > 1:
                for coord in discarded:
                    if (orient):
                        accepted.append((coord[0], line[0][1]))
                    else:
                        accepted.append((line[0][0], coord[1]))
                segment.append(accepted)
                seg_color.append(parent.colors[iter])
        return segment, seg_color

    def cycle(self):
        generations, scores = 0, []
        chromosomes = self.__initial_population() 
        # compute fitness of each individual in population
        self.fitness = [self.__compute_fitness(indv) for indv in chromosomes]
        while generations < self.generations+1:
            print("Generation: ", generations)
            if generations % self.generations == 0:
                # print('Generation', generations+1)
                for x in chromosomes:
                    fit = max([self.__compute_fitness(i) for i in chromosomes])
                    if self.__compute_fitness(x) == fit:
                        x.form_tile(np.array(x.block), str(generations),self.tileSize)
                        print("Fitness Max:", fit)
                        break
            for _ in range(self.offsprings): # 5
                # parent selection
                parent1, parent2 = self.__random(chromosomes)[:2]
                # cross over
                offspring  = self.__crossover(parent1, parent2)
                # mutation
                if random.random() < self.mutationRate:
                    offspring = self.__mutation(offspring)
                # add new offspring to population
                chromosomes.append(offspring)
                # compute fitness of new offspring
                self.fitness.append(self.__compute_fitness(offspring))
            # survivor selection
            chromosomes = self.__truncation(chromosomes,self.popSize)
            # compute fitness of each individual in population
            self.fitness = [self.__compute_fitness(indv) for indv in chromosomes]
            generations +=1
            
            scores.append((max(self.fitness), sum(self.fitness)/len(self.fitness)))
        return scores
    
    def __truncation(self, chromosomes, size):
        indexes = [(self.fitness[i], i) for i in range(len(self.fitness))]
        # sorts list accoridng to fitness
        indexes.sort(key = lambda x: x[0], reverse=True)
        indexes = indexes[:size]
        # selects top N elements
        top_N = [chromosomes[i[1]] for i in indexes]
        return top_N
    
    def __random(self, chromosomes):
        # randomly selects 2 chromosomes from population
        return random.sample(chromosomes, 2)

    def plot_graph(self):
        BFS = [i[0][0] for i in self.generations_score]
        AFS = [i[0][1] for i in self.generations_score]
        generations = [i+1 for i in range(self.generations)]
        plt.plot(generations, BFS, label="Avg best-so-far Fitness")
        plt.plot(generations, AFS, label="Avg average-so-far Fitness")
        plt.xlabel('No. of generations')
        plt.ylabel('Fitness value')
        plt.legend()
        plt.show()

    def epochs(self):
        iters = [self.cycle() for _ in range(self.iterations)]
        gen = 0
        while gen < self.generations:
            best, avg = 0, 0
            for val in iters:
                best += val[gen][0]
                avg += val[gen][1]
            best = best / len(iters)
            avg = avg / len(iters)
            self.generations_score[gen].append((best,avg))
            gen +=1 
        self.plot_graph()

ga = GA()
# ga.epochs()

ga.cycle()