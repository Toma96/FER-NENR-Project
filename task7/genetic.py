import random
import numpy as np


PM1 = 0.11
PM2 = 0.11
SIGM1 = 0.1
SIGM2 = 0.3
DES1 = 1
DES2 = 1
DES3 = 1


class TournamentGeneticAlgorithm:

    def __init__(self, neural_net, dataset, k, pop_size, max_iter, e=1e-6):
        self.neural_net = neural_net
        self.dataset = dataset
        self.max_iter = max_iter
        self.e = e
        self.k = k
        self.errors = np.zeros(pop_size)
        self.generation = np.random.normal(0, 1, size=(pop_size, neural_net.get_num_of_params()))
        self.best, self.best_index = self.calc_best()
        print("Starting best fitness (least error): ", self.best)

    def calc_best(self):
        best_err = np.inf
        best_index = 0
        for i, ch in enumerate(self.generation):
            if i > 0:
                self.neural_net.calc_output(ch)
            self.errors[i] = self.neural_net.calc_error(self.dataset, ch)
            if self.errors[i] < best_err:
                best_err = self.errors[i]
                best_index = i
        return best_err, best_index

    def get_opt_params(self):
        return self.generation[self.best_index]

    def run(self):

        for i in range(1, self.max_iter):
            if self.e > self.best:
                print("The best fitness is better than precision e!")
                print("Algorithm has stopped now.")
                break

            sample = random.sample(range(len(self.generation)), self.k)
            tournament = sorted([[self.errors[k], self.generation[k], k] for k in sample])
            mother, father = tournament[0][1], tournament[1][1]
            crossover = np.random.choice([cross1, cross2, cross3])
            child = crossover(mother, father)
            mutation = np.random.choice([mutate1, mutate2, mutate3],
                                        p=[DES1 / (DES1 + DES2 + DES3),
                                           DES2 / (DES1 + DES2 + DES3),
                                           DES3 / (DES1 + DES2 + DES3)])
            mutation(child)
            child_error = self.neural_net.calc_error(self.dataset, child)
            worst_index = tournament[-1][2]
            if child_error < tournament[-1][0]:
                self.generation[worst_index] = child

            if child_error < self.best:
                self.best = child_error
                print("Generation: ", i)
                print("New best fitness: ", self.best)
                self.best_index = worst_index
                # print("Params: ", child)

        return self.get_opt_params()


def cross1(mother, father):
    return (mother + father) / 2


def cross2(mother, father):
    return np.array([np.random.choice((m, f)) for m, f in zip(mother, father)])


def cross3(mother, father):
    cross_point = random.randint(0, len(mother))
    return np.append(mother[:cross_point], father[cross_point:])


def mutate1(gen):
    for i in range(len(gen)):
        if np.random.random() < PM1:
            gen[i] += np.random.normal(0, SIGM1)


def mutate2(gen):
    for i in range(len(gen)):
        if np.random.random() < PM1:
            gen[i] += np.random.normal(0, SIGM2)


def mutate3(gen):
    for i in range(len(gen)):
        if np.random.random() < PM2:
            gen[i] = np.random.normal(0, SIGM2)

