from types import TracebackType
from ImageQuality import ImageQuality
from Shapes import Shapes

class GA:
    def __init__(self):
        self.popSize = 30
        self.generations = 500
        self.fitness = None
        self.offsprings = 10
        self.mutationRate = 0.5

    def initial_population(self):
        population = [Shapes() for _ in range(self.popSize)]
        return population

    def compute_fitness(self, img):
        quality = ImageQuality(img)
        return quality.get_fitness()

    def mutation(self, population):
        # change color, add two parents
        pass

    # def cycle(self):
    #     iters = []
    #     for _ in range(self.iterations):
    #         generations = 0
    #         chromosomes = self.initial_population() 
    #         # compute fitness of each individual in population
    #         self.fitness = [self.compute_fitness(indv) for indv in chromosomes]
    #         while generations < self.generations:
    #             # Saving image after every 250 generations
    #             # if generations % 250 == 0:
    #             #     print('Generation', generations+1)
    #             #     for x in chromosomes:
    #             #         fit = min([self.computeFitness(i) for i in chromosomes])
    #             #         if self.computeFitness(x) == fit:
    #             #             x.img.save('MonaLisa'+str(generations)+'.png', 'PNG')
    #             #             print("Fitness:", fit)
    #             #             break
    #             for _ in range(self.offsprings//2):
    #                 # parent selection
    #                 parents = self.random(chromosomes, 2)
    #                 parent1, parent2 = parents[0], parents[1]
    #                 # cross over
    #                 offspring1, offspring2  = self.crossover(parent1, parent2)
    #                 # add new offsprings to population
    #                 chromosomes.append(offspring1)
    #                 chromosomes.append(offspring2)
    #                 # compute fitness of new offsprings
    #                 self.fitness.append(self.computeFitness(offspring1))
    #                 self.fitness.append(self.computeFitness(offspring2))
    #                 # mutation
    #                 if random.random() < self.mutationRate:
    #                     chromosomes = self.mutation(chromosomes)
    #             # survivor selection
    #             chromosomes = self.truncation(chromosomes,maximise,self.popSize)
   


# i = Image.open("Reference Images/6.jpg")
# x = Image.open("test.jpg")
# print(GA().fitness_function(i))
# print(GA().fitness_function(x))