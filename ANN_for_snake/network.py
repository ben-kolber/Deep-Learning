import numpy as np
import time


class Network:

    def __init__(self):
        self.layers = []
        self.input_layer = False
        self.output_layer = False

    def add_input_layer(self, input_layer):
        self.layers.append(input_layer)
        self.input_layer = True

    def add_hidden_layer(self, hidden_layer):
        if not self.input_layer:
            raise Exception('No input layer in network')
        else:
            # check previous layer neurons
            x = len(self.layers)
            self.layers[x-1].init_weights(len(hidden_layer.neurons))
            self.layers.append(hidden_layer)

    def add_output_layer(self, output_layer):
        if not self.input_layer:
            raise Exception('No input layer in network')
        else:
            # connect to last added layer
            self.layers[-1].init_weights(len(output_layer.neurons))
            self.layers.append(output_layer)
            self.output_layer = True

    def run_network(self, vector, actions):
        if len(vector) != len(self.layers[0].neurons):
            raise Exception('Vector incompatible with input layer')
            print('Vector: {}'.format(vector))

        if not self.input_layer or not self.output_layer:
            raise Exception('Missing input or output layer')

        else:
            cur_layer = 0
            next_layer = 1
            complete = False
            bias = 1

            # each neuron in the input layer gets the value of the vector.
            # initializes the input layer
            #print('Initializing input layer to vector: {}'.format(vector))
            for i in range(len(vector)):
                self.layers[0].neurons[i].value = vector[i]
                if vector[i] == 0:
                    self.layers[0].neurons[i].active = False
                #print('Loading Value: {}'.format(vector[i]))

            #print('' * 20)

            # run the hidden layers
            #print('Running the Network...')
            while not complete:
                #print('Running Layer {} to connected Layer number {}'.format(cur_layer, next_layer))
                # for each connection to the next layer
                for connection in range(len(self.layers[next_layer].neurons)):
                    #print('Running connection number {}'.format(connection))
                    # for each neuron in the current layer
                    sum = 0
                    #print('Summing weight to vector -> ')
                    for neuron in self.layers[cur_layer].neurons:
                        #    print('Neuron val: {}'.format(neuron.value))
                        #    print('Weight Value: {}'.format(neuron.connection_weights[connection]))
                        sum += neuron.value * neuron.connection_weights[connection]
                    #print('The summation for connection {} = {}'.format(connection, sum))
                    sum += bias
                    activation = np.maximum(0, sum)
                    #print('ReLu output = {}'.format(activation))
                    if activation > 0:
                        self.layers[next_layer].neurons[connection].value = activation
                        self.layers[next_layer].neurons[connection].activate = True
                    else:
                        self.layers[next_layer].neurons[connection].value = 0
                        self.layers[next_layer].neurons[connection].activate = False

                cur_layer += 1
                next_layer += 1
                if next_layer == len(self.layers):
                    complete = True
                #print('-' * 20)
                #print(' '*20)

            # check the output
            max = [0, 0]
            for i in range(len(self.layers[-1].neurons)):
                #print('Output Neuron {} Value -> {}'.format(i, self.layers[-1].neurons[i].value))
                if self.layers[-1].neurons[i].value > max[0]:
                    max = [self.layers[-1].neurons[i].value, i]

            # print('MAX : {}'.format(max[1]))
            # print('ACTIONS: {}'.format(actions))
            #print('FIRING Neuron {} with val {}'.format(actions[max[1]], max[0]))
            return actions[max[1]]
