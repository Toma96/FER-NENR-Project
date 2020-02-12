import matplotlib.pyplot as plt
import numpy as np


def neuron_out(x, w, s):
    return 1 / (1 + abs(x - w) / abs(s))


def task1():
    w = 2
    x = np.linspace(-8, 10)
    for s in [1, 0.25, 4, 10]:
        plt.plot(x, neuron_out(x, w, s), label='s={0}'.format(s))
    plt.legend()
    plt.show()


def task2():
    class_a_x = []
    class_a_y = []
    class_b_x = []
    class_b_y = []
    class_c_x = []
    class_c_y = []
    with open("zad7-dataset.txt", "r") as f:
        for line in f.readlines():
            values = [float(v) for v in line.split()]
            if values[2]:
                class_a_x.append(values[0])
                class_a_y.append(values[1])
            elif values[3]:
                class_b_x.append(values[0])
                class_b_y.append(values[1])
            else:
                class_c_x.append(values[0])
                class_c_y.append(values[1])

    plt.scatter(class_a_x, class_a_y, marker='o')
    plt.scatter(class_b_x, class_b_y, marker='s')
    plt.scatter(class_c_x, class_c_y, marker='v')
    plt.show()


if __name__ == '__main__':
    task1()
    task2()

