import numpy as np
import matplotlib.pyplot as plt


def sigmoid(a, b, x):
    return 1. / (1 + np.exp(b * (x - a)))


class Rule:

    def __init__(self):
        params = np.random.uniform(-1, 1, size=7)
        self.a = params[0]
        self.b = params[1]
        self.c = params[2]
        self.d = params[3]
        self.p = params[4]
        self.q = params[5]
        self.r = params[6]
        self.set_init_derivatives()

    def set_init_derivatives(self):
        self.da = self.db = self.dc = self.dd = self.dp = self.dq = self.dr = 0

    def get_function_value(self, x, y):
        return self.p * x + self.q * y + self.r

    def get_w(self, x, y):
        return sigmoid(self.a, self.b, x) * sigmoid(self.c, self.d, y)

    def update_derivatives(self, sample, output, sum_w, sum_wz):
        w = self.get_w(sample.x, sample.y)
        alpha = sigmoid(self.a, self.b, sample.x)
        beta = sigmoid(self.c, self.d, sample.y)

        self.dp += (sample.z - output) * w / sum_w * sample.x
        self.dq += (sample.z - output) * w / sum_w * sample.y
        self.dr += (sample.z - output) * w / sum_w

        self.da += (sample.z - output) * sum_wz / sum_w**2 * beta * self.b * alpha * (1 - alpha)
        self.db += (sample.z - output) * sum_wz / sum_w**2 * beta * (self.a - sample.x) * alpha * (1 - alpha)
        self.dc += (sample.z - output) * sum_wz / sum_w**2 * alpha * self.d * beta * (1 - beta)
        self.dd += (sample.z - output) * sum_wz / sum_w**2 * alpha * (self.c - sample.y) * beta * (1 - beta)

    def update(self, learning_rate):
        self.p += learning_rate * self.dp
        self.q += learning_rate * self.dq
        self.r += learning_rate * self.dr

        self.a += learning_rate * self.da
        self.b += learning_rate * self.db
        self.c += learning_rate * self.dc
        self.d += learning_rate * self.dd

        self.set_init_derivatives()

    def plot(self):
        X = np.linspace(-4, 4)
        plt.figure()
        plt.ylim(top=1)
        plt.title("Sigmoid (a, b, X)")
        plt.plot(X, sigmoid(self.a, self.b, X))

        plt.figure()
        plt.ylim(top=1)
        plt.title("Sigmoid (c, d, X)")
        plt.plot(X, sigmoid(self.c, self.d, X))
        plt.show()


class SampleDataFunction:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.z = ((x - 1)**2 + (y + 2)**2 - 5*x*y + 3) * np.cos(x / 5)**2
