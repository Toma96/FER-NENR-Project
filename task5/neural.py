import numpy as np


def sigmoid(x):
    return 1. / (1. + np.exp(-x))


class Neuron:

    def __init__(self, weights_size, layer_index):
        self.layer_index = layer_index
        self.weights = np.random.uniform(-1, 1, size=weights_size)
        self.delta_weights = np.zeros(weights_size)
        self.y = 0.
        self.delta = 0.

    def update_delta_weights(self, previous_layer):
        for i, neuron in enumerate(previous_layer.neurons):
            self.delta_weights[i] += self.delta * neuron.y

    def update_weights(self, learning_rate):
        for i in range(len(self.weights)):
            self.weights[i] += learning_rate * self.delta_weights[i]
            self.delta_weights[i] = 0

    def calc_delta(self, next_layer):
        self.delta = 0.
        for neuron in next_layer.neurons:
            self.delta += self.y * (1 - self.y) * neuron.weights[self.layer_index] * neuron.delta

    def calc_y(self, layer):
        net = 0.
        for i, neuron in enumerate(layer.neurons):
            net += neuron.y * self.weights[i]
        self.y = sigmoid(net)


class Layer:

    def __init__(self, size, previous_size):
        self.neurons = [Neuron(previous_size, i) for i in range(size)]

    def forward_pass(self, input_layer):
        for neuron in self.neurons:
            neuron.calc_y(input_layer)

    def update_weights(self, learning_rate):
        for neuron in self.neurons:
            neuron.update_weights(learning_rate)

    def update_delta_ws(self, previous_layer):
        for neuron in self.neurons:
            neuron.update_delta_weights(previous_layer)

    def update_deltas(self, next_layer):
        for neuron in self.neurons:
            neuron.calc_delta(next_layer)


class NeuralNet:

    def __init__(self, filepath, layer_arch, algorithm, max_iter, learning_rate):
        self.layer_arch = layer_arch
        self.algorithm = algorithm
        self.max_iter = max_iter
        self.learning_rate = learning_rate
        self.layers = [Layer(layer_arch[0], 0)]
        self.layers.extend([Layer(layer_arch[i], layer_arch[i - 1]) for i in range(1, len(layer_arch))])
        self.inputs = []
        self.outputs = []
        self.evaluation_n = 0
        self.no_inputs = 0
        with open(filepath, "r") as f:
            for line in f.readlines():
                numbers = [float(i) for i in line.split()]
                # self.inputs.append(numbers[:1])
                # self.outputs.append(numbers[1:])
                self.inputs.append(numbers[:len(numbers)-5])
                self.outputs.append(numbers[len(numbers)-5:])
                self.no_inputs += 1

    def evaluate(self, sample):
        for i, neuron in enumerate(self.layers[0].neurons):
            neuron.y = sample[i]

        for i in range(1, len(self.layers)):
            self.layers[i].forward_pass(self.layers[i - 1])

    def get_value(self):
        last_layer = self.layers[-1]
        return [neuron.y for neuron in last_layer.neurons]

    def get_class(self, inputs):
        self.evaluate(inputs)
        classes = ["Alpha", "Beta", "Gamma", "Delta", "Epsilon"]
        last_layer = self.layers[-1]
        max_index = 0
        print([neuron.y for neuron in last_layer.neurons])
        for i in range(1, 5):
            if last_layer.neurons[i].y > last_layer.neurons[max_index].y:
                max_index = i
        return max_index, classes[max_index]

    def get_error(self):
        total_error = 0
        for i in range(len(self.inputs)):
            self.evaluate(self.inputs[i])
            for j in range(len(self.layers[-1].neurons)):
                difference = self.outputs[i][j] - self.layers[-1].neurons[j].y
                total_error += difference**2
        return total_error / self.no_inputs

    def update_weights(self, batch_size):
        last_layer_index = len(self.layers) - 1

        for i in range(batch_size):
            self.evaluate(self.inputs[self.evaluation_n % self.no_inputs])
            expected = self.outputs[self.evaluation_n % self.no_inputs]
            self.evaluation_n += 1
            for j, neuron in enumerate(self.layers[-1].neurons):
                y = neuron.y
                out_delta = y * (1 - y) * (expected[j] - y)
                neuron.delta = out_delta

            for j in range(last_layer_index - 1, 0, -1):
                self.layers[j].update_deltas(self.layers[j + 1])

            for j in range(last_layer_index, 0, -1):
                self.layers[j].update_delta_ws(self.layers[j - 1])

        for layer in self.layers:
            layer.update_weights(self.learning_rate)

    def learn(self):
        for i in range(self.max_iter):
            if i % 100 == 0:
                print("Iteration {0}\tError: {1}".format(i, self.get_error()))
            if self.algorithm == "Backpropagation":
                self.update_weights(len(self.inputs))
            elif self.algorithm == "Stochastic backpropagation":
                self.update_weights(1)
            else:
                self.update_weights(len(self.inputs) // 10)


if __name__ == '__main__':
    net = NeuralNet("kvadratna.txt", [1, 6, 6, 1], algorithm="Backpropagation",
                    learning_rate=0.2, max_iter=10000)
    net.learn()

    sample = [1.0]
    net.evaluate(sample)

    print(net.get_value())
