import random
from neuron import Neuron


class Layer:

    def __init__(self, neurons, thresh):
        self.neurons = []
        for i in range(neurons):
            self.neurons.append(Neuron(1))  # PARAM: threshold

    def init_weights(self, connect_to):
        # for each neuron in the layer
        for neuron in self.neurons:
            # generate a weight list for each connection in next layer
            for j in range(connect_to):
                neuron.connection_weights.append(random.uniform(-1.0, 1.0))
