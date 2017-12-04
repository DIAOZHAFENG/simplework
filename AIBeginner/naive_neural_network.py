import numpy as np
from numpy.matlib import repmat


def sigmoid(x):
    return 1. / (1. + np.exp(-x))


def sigmoid_prime(x):
    return x * (1. - x)


class Layer:
    def __init__(self):
        self.val = None
        self.opt_val = None


class NeuralNetwork:
    def __init__(self, layer_counts, a, lmd):
        assert len(layer_counts) > 1
        self.W = []
        self.B = []
        for i in xrange(len(layer_counts)-1):
            self.W.append(np.zeros((layer_counts[i], layer_counts[i+1])))
            self.B.append(np.zeros((1, layer_counts[i+1])))
        self.L = []
        for i in xrange(len(layer_counts)):
            self.L.append(Layer())
        self.a = a
        self.lmd = lmd

    def feed(self, inputs):
        self.m = len(inputs)
        self.L[0].opt_val = np.array(inputs)

    def forward(self):
        for i in xrange(len(self.L)-1):
            self.L[i+1].val = np.dot(self.L[i].opt_val, self.W[i]) + repmat(self.B[i], self.m, 1)
            self.L[i+1].opt_val = sigmoid(self.L[i+1].val)

    def calc_cost(self, result):
        self.diff = result - self.L[-1].opt_val
        return np.sum(self.diff*self.diff)

    def bp(self):
        delta = []
        # delta[i] == delta(i+1) (mat[len(m*L[i+1])])
        delta.insert(0, -self.diff * sigmoid_prime(self.L[-1].opt_val))
        for i in xrange(len(self.W)-1, 0, -1):
            delta.insert(0, np.dot(delta[0], self.W[i].T) * sigmoid_prime(self.L[i].opt_val))
        for i in xrange(len(delta)):
            self.W[i] = (1 - self.lmd * self.a) * self.W[i] - self.a / self.m * np.dot(self.L[i].opt_val.T, delta[i])
            self.B[i] = self.B[i] - self.a / self.m * delta[i]

    def train(self, train_input, train_output, times):
        for i in xrange(times + 1):
            self.feed(train_input)
            self.forward()
            yield self.calc_cost(train_output), i
            self.bp()

    def test(self, test_input, test_output):
        self.feed(test_input)
        self.forward()
        return self.calc_cost(test_output)
