from support import Dataset
from neural import NeuralNetwork
from genetic import TournamentGeneticAlgorithm

MAX_ITER = 10000
POPULATION_SIZE = 30
K = 3


if __name__ == '__main__':
    data = Dataset("zad7-dataset.txt")
    layer_arch = [2, 8, 4, 3]
    network = NeuralNetwork(layer_arch)
    ga = TournamentGeneticAlgorithm(network, data, K, POPULATION_SIZE, MAX_ITER)

    best_params = ga.run()

    network.classify(data, best_params)
