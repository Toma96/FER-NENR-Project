from rules import Rule, SampleDataFunction
import random


class Anfis:

    def __init__(self, learning_rate, no_rules, max_iter):
        self.learning_rate = learning_rate
        self.max_iter = max_iter
        self.rules = [Rule() for _ in range(no_rules)]
        self.samples = [SampleDataFunction(x, y) for x in range(-4, 4) for y in range(-4, 4)]
        self.sum_w = self.sum_wz = 0

    def evaluate(self, x, y):
        self.sum_w = sum([r.get_w(x, y) for r in self.rules])
        self.sum_wz = sum([r.get_w(x, y) * r.get_function_value(x, y) for r in self.rules])
        return self.sum_wz / self.sum_w

    def get_errors(self):
        return [abs(self.samples[i].z - self.evaluate(self.samples[i].x, self.samples[i].y)) for i in range(len(self.samples))]

    def mse(self):
        return sum([(self.evaluate(sample.x, sample.y) - sample.z)**2 for sample in self.samples]) / len(self.samples)

    def batch(self):
        for i in range(self.max_iter):
            for sample in self.samples:
                o = self.evaluate(sample.x, sample.y)
                for rule in self.rules:
                    z = rule.get_function_value(sample.x, sample.y)
                    rule.update_derivatives(sample, o, self.sum_w, self.sum_w*z - self.sum_wz)

            for rule in self.rules:
                rule.update(self.learning_rate)

            mse = self.mse()
            if i % 100 == 0:
                print("Iteration {0}: MSE = {1}".format(i, mse))

    def stochastic(self):
        for i in range(self.max_iter):

            if i % len(self.samples) == 0:
                random.shuffle(self.samples)

            current_sample = self.samples[i % len(self.samples)]
            o = self.evaluate(current_sample.x, current_sample.y)

            for rule in self.rules:
                z = rule.get_function_value(current_sample.x, current_sample.y)
                rule.update_derivatives(current_sample, o, self.sum_w, self.sum_w*z - self.sum_wz)
                rule.update(self.learning_rate)

            mse = self.mse()
            if i % 100 == 0:
                print("Iteration {0}: MSE = {1}".format(i, mse))

    def batch_with_trace(self):
        errors = []
        for i in range(self.max_iter):
            for sample in self.samples:
                o = self.evaluate(sample.x, sample.y)
                for rule in self.rules:
                    z = rule.get_function_value(sample.x, sample.y)
                    rule.update_derivatives(sample, o, self.sum_w, self.sum_w*z - self.sum_wz)

            for rule in self.rules:
                rule.update(self.learning_rate)

            mse = self.mse()
            errors.append(mse)

            if i % 100 == 0:
                print("Iteration {0}: MSE = {1}".format(i, mse))

        return errors

    def stochastic_with_trace(self):
        errors = []
        for i in range(self.max_iter):

            if i % len(self.samples) == 0:
                random.shuffle(self.samples)

            current_sample = self.samples[i % len(self.samples)]
            o = self.evaluate(current_sample.x, current_sample.y)

            for rule in self.rules:
                z = rule.get_function_value(current_sample.x, current_sample.y)
                rule.update_derivatives(current_sample, o, self.sum_w, self.sum_w*z - self.sum_wz)
                rule.update(self.learning_rate)

            mse = self.mse()
            errors.append(mse)

            if i % 100 == 0:
                print("Iteration {0}: MSE = {1}".format(i, mse))

        return errors
