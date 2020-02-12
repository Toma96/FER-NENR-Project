import numpy as np


def n1_out(net):
    return 1 / (1 + net)


def n2_out(net):
    return 1 / (1 + np.exp(-net))


class NeuralNetwork:

    """param layers is like [2, 5, 3]"""
    def __init__(self, layers):
        self.layers = layers
        self.neurons = np.zeros(sum([n for n in layers]))

    def set_inputs(self, x, y):
        self.neurons[0] = x
        self.neurons[1] = y

    def get_num_of_params(self):
        params = self.layers[0] * self.layers[1] * 2
        for i in range(2, len(self.layers)):
            params += self.layers[i] * (self.layers[i - 1] + 1)
        return params

    def calc_output(self, params):
        start = 0
        end = 2
        param_index = 0

        for i in range(1, len(self.layers)):
            for j in range(self.layers[i]):
                net = 0
                for k in range(start, end):
                    x = self.neurons[k]
                    if i == 1:
                        w = params[param_index]
                        param_index += 1
                        s = params[param_index]
                        param_index += 1
                        net += (abs(x - w) / abs(s))
                    else:
                        w = params[param_index]
                        param_index += 1
                        net += (x * w)

                if i == 1:
                    self.neurons[end + j] = n1_out(net)
                else:
                    self.neurons[end + j] = n2_out(net)
                # self.neurons[end + j] = n1_out(net) if i == 1 else n2_out(net)

            start = end
            end += self.layers[i]

    def calc_error(self, data, params):
        n = len(self.neurons)
        error = 0

        for sample in data.samples:
            self.set_inputs(sample.x, sample.y)
            self.calc_output(params)
            error += (self.neurons[n - 3] - sample.a) ** 2
            error += (self.neurons[n - 2] - sample.b) ** 2
            error += (self.neurons[n - 1] - sample.c) ** 2

        return error / len(data.samples)

    def classify(self, data, params):
        n = len(self.neurons)
        correct = 0
        wrong = 0
        for sample in data.samples:
            self.set_inputs(sample.x, sample.y)
            self.calc_output(params)

            outer_neurons = self.neurons[n - 3:]
            for i, neuron in enumerate(outer_neurons):
                self.neurons[n - i - 1] = round(self.neurons[n - i - 1])
            if self.neurons[n - 3] == sample.a and self.neurons[n - 2] == sample.b and self.neurons[n - 1] == sample.c:
                correct += 1
            else:
                wrong += 1

        print("Correctly classified: ", correct)
        print("Wrongly classified: ", wrong)


