from anfis import Anfis
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np


def task4():
    # neuro_fuzzy = Anfis(0.001, 1, 100000)
    # neuro_fuzzy.stochastic()

    # neuro_fuzzy = Anfis(0.001, 2, 100000)
    # neuro_fuzzy.stochastic()

    neuro_fuzzy = Anfis(0.001, 7, 100000)
    neuro_fuzzy.stochastic()


def task5():
    neuro_fuzzy = Anfis(0.001, 7, 100000)
    neuro_fuzzy.stochastic()
    for rule in neuro_fuzzy.rules:
        rule.plot()


def task6():
    neuro_fuzzy = Anfis(0.001, 7, 100000)
    neuro_fuzzy.stochastic()

    errors = np.array(neuro_fuzzy.get_errors())
    errors = errors.reshape(-1, 8)

    X = np.linspace(-4, 4, 9)
    Y = np.linspace(-4, 4, 9)
    fig = plt.figure(figsize=(16, 16))
    ax = fig.add_subplot(111, projection='3d', title='error')
    ax.plot_wireframe(X, Y, errors)


def task7():
    neuro_fuzzy_sto = Anfis(0.001, 3, 10000)
    errors_sto = neuro_fuzzy_sto.stochastic_with_trace()

    neuro_fuzzy_batch = Anfis(0.001, 3, 10000)
    errors_batch = neuro_fuzzy_batch.batch_with_trace()

    plt.figure()
    plt.plot(errors_batch, label='Gradient')
    plt.plot(errors_sto, label='Stochastic')
    plt.yscale('log')
    plt.legend()
    plt.show()


def task8():
    for eta in [0.01, 0.001, 0.00001]:
        neuro_fuzzy_sto = Anfis(eta, 3, 10000)
        errors_sto = neuro_fuzzy_sto.stochastic_with_trace()

        # neuro_fuzzy_batch = Anfis(eta, 3, 10000)
        # errors_batch = neuro_fuzzy_batch.batch_with_trace()

        plt.figure(1)
        plt.plot(errors_sto, label='Eta={0}'.format(eta))
        plt.yscale('log')
        plt.legend()

        # plt.figure(2)
        # plt.plot(errors_batch, label='Eta={0}'.format(eta))
        # plt.yscale('log')
        # plt.legend()
    plt.show()


if __name__ == '__main__':
    # task4()
    # task5()
    # # task6()
    task7()
    task8()
