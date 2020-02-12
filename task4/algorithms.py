from abc import ABC, abstractmethod
from support import Population, Chromosome


class GeneticAlgorithm(ABC):

    def __init__(self, data, pop_size, mut_prob, max_iter, elite):
        self.data = data
        self.pop_size = pop_size
        self.mut_prob = mut_prob
        self.max_iter = max_iter
        self.elite = elite

    @abstractmethod
    def run(self):
        pass

    def print_generation_fitness(self, generation, population, best):
        gen_best_chromosome = population.find_best(self.data)
        if best is None or gen_best_chromosome.fitness < best.fitness:
            best = gen_best_chromosome
            print("Generation: ", generation)
            print("New best fitness: ", best.fitness)
            print("Params: ", str(best))
            print()
        return best


class GenerationalGeneticAlgorithm(GeneticAlgorithm):

    def __init__(self, data, pop_size, mut_prob, max_iter, elite):
        super(GenerationalGeneticAlgorithm, self).__init__(data, pop_size, mut_prob, max_iter, elite)

    def run(self):
        population = Population(self.pop_size)
        best = self.print_generation_fitness(0, population, None)

        for i in range(1, self.max_iter):
            new_population = Population(0)
            j_range = self.pop_size
            if self.elite:
                new_population.add(best)
                j_range -= 1
            for j in range(j_range):
                selection = population.gen_selection(2)
                new_chromosome = Chromosome.crossover(selection[0], selection[1])
                new_chromosome.mutate(self.mut_prob)
                new_population.add(new_chromosome)
            population = new_population
            best = self.print_generation_fitness(i, population, best)

        return best


class TournamentGeneticAlgorithm(GeneticAlgorithm):

    def __init__(self, data, pop_size, mut_prob, max_iter, elite):
        super(TournamentGeneticAlgorithm, self).__init__(data, pop_size, mut_prob, max_iter, elite)

    def run(self):
        population = Population(self.pop_size)
        best = self.print_generation_fitness(0, population, None)

        for i in range(1, self.max_iter):
            tournament = population.k_selection(3)
            mother, father = tournament[0], tournament[1]
            child = Chromosome.crossover(mother, father)
            child.calc_fitness(self.data)
            child.mutate(self.mut_prob)
            child.calc_fitness(self.data)
            population.replace(tournament[2], child)

            best = self.print_generation_fitness(i, population, best)

        return best
