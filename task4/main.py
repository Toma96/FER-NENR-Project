from parameters import *
from algorithms import GenerationalGeneticAlgorithm, TournamentGeneticAlgorithm


def main():

    with open("zad4-dataset1.txt") as f:
        data = f.readlines()
    data = [line.strip() for line in data]

    print("You can change parameters easily in module 'parameters.py'.")
    while True:
        flag = input("Choose between a generational (G) or tournament selection genetic algorithm (T): ")
        if flag == "G" or flag == "g":
            algorithm = GenerationalGeneticAlgorithm(data, POPULATION_SIZE, MUTATION_PROB, MAX_ITERATIONS, ELITE)
            break
        elif flag == "T" or flag == "t":
            algorithm = TournamentGeneticAlgorithm(data, POPULATION_SIZE, MUTATION_PROB, MAX_ITERATIONS, ELITE)
            break
    result = algorithm.run()
    print("The algorithm has reached its max iterations. The result is: ", result.fitness, result)


if __name__ == '__main__':
    main()
