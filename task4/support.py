import numpy as np
import random


LOWER_BOUND = -4
UPPER_BOUND = 4
NO_ELEMENTS = 5


class Chromosome(object):

    def __init__(self, genes=None):
        self.fitness = 0
        if genes is None:
            self.genes = np.random.uniform(LOWER_BOUND, UPPER_BOUND, size=(NO_ELEMENTS,))
        elif len(genes) != NO_ELEMENTS:
            raise IncorrectGeneSizeException("Gene size must be 5!")
        else:
            self.genes = genes

    def __lt__(self, other):
        return self.fitness < other.fitness

    def __le__(self, other):
        return self.fitness <= other.fitness

    def __eq__(self, other):
        return self.fitness == other.fitness

    def __ne__(self, other):
        return self.fitness != other.fitness

    def __ge__(self, other):
        return self.fitness >= other.fitness

    def __gt__(self, other):
        return self.fitness > other.fitness

    def __str__(self):
        return "(" + ",".join([str(item) for item in self.genes]) + ")"

    def __hash__(self):
        return hash(str(self))

    @staticmethod
    def crossover(mother, father):
        genesm = mother.genes
        genesf = father.genes
        new_genes = [(genesf[i] + genesm[i]) / 2 for i in range(len(genesm))]
        return Chromosome(new_genes)

    def mutate(self, prob):
        for i in range(len(self.genes)):
            if np.random.random() <= prob:
                self.genes[i] = LOWER_BOUND + np.random.random()*(UPPER_BOUND - LOWER_BOUND)

    def calc_fitness(self, data):
        measures = np.array([])
        for line in data:
            x, y, f = line.split("\t")
            x, y, f = float(x), float(y), float(f)
            measures = np.append(measures, (f - transfer_function(x, y, self.genes))**2)
        self.fitness = np.mean(measures)
        return self.fitness


class Population(object):

    def __init__(self, size):
        self.size = size
        self.chromosomes = [Chromosome() for _ in range(size)]
        self.best = self.chromosomes[0] if size > 0 else None

    def add(self, new_chromosome):
        self.chromosomes.append(new_chromosome)
        self.size += 1

    def replace(self, old_chromosome, new_chromosome):
        self.chromosomes.remove(old_chromosome)
        self.add(new_chromosome)

    def find_best(self, data):
        self.best = self.chromosomes[0]
        for ch in self.chromosomes:
            if ch.calc_fitness(data) < self.best.calc_fitness(data):
                self.best = ch
        return self.best

    def calc_pop_fitness(self):
        return sum([ch.fitness for ch in self.chromosomes])

    def gen_selection(self, n):
        parents = []
        total_fitness = self.calc_pop_fitness()
        for parent_index in range(n):
            limit = random.uniform(0, total_fitness)
            chosen = 0
            upper_limit = 1 / self.chromosomes[chosen].fitness
            while limit >= upper_limit and chosen < self.size - 1:
                chosen += 1
                upper_limit += 1 / self.chromosomes[chosen].fitness
            parents.append(self.chromosomes[chosen])
        return parents

    def k_selection(self, n):
        selected = random.choices(self.chromosomes, k=n)
        return sorted(selected) if n > 1 else selected[0]


class IncorrectGeneSizeException(Exception):
    pass


def transfer_function(x, y, params):
    return np.sin(params[0] + params[1]*x) + params[2]*np.cos(x*(params[3] + y)) / (1 + np.e**(x - params[4])**2)

