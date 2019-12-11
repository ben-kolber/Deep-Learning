import numpy as np


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
            print('ERROR: No input layer in network')
        else:
            # check previous layer neurons
            x = len(self.layers)

            self.layers[x-1].init_weights(len(hidden_layer.neurons))

            self.layers.append(hidden_layer)

    def add_output_layer(self, output_layer):
        if not self.input_layer:
            print('ERROR: No input layer in network')
        else:
            # connect to last added layer
            self.layers[-1].init_weights(len(output_layer.neurons))
            self.layers.append(output_layer)
            self.output_layer = True

    def run_network(self, vector):
        if len(vector) != len(self.layers[0].neurons):
            print('ERROR: Vector incompatible with input layer')

        if not self.input_layer or not self.output_layer:
            print('ERROR: Missing input or output layer')

        else:
            cur_layer = 0
            next_layer = 1
            complete = False

            # each neuron in the input layer gets the value of the vector.
            # initializes the input layer
            print('Initializing input layer to vector: {}'.format(vector))
            for i in range(len(vector)):
                self.layers[0].neurons[i].value = vector[i]
                print('Loading Value: {}'.format(vector[i]))

            print('' * 20)

            # run the hidden layers
            print('Running the Network...')
            while not complete:
                print('Running Layer {} to connected Layer number {}'.format(cur_layer, next_layer))
                # for each connection to the next layer
                for connection in range(len(self.layers[next_layer].neurons)):
                    print('Running connection number {}'.format(connection))
                    # for each neuron in the current layer
                    sum = 0
                    print('Summing weight to vector -> ')
                    for neuron in self.layers[cur_layer].neurons:
                        if neuron.activate:
                            sum += neuron.value * neuron.connection_weights[connection]
                        else:
                            pass
                    print('The summation for connection {} = {}'.format(connection, sum))
                    activation = np.maximum(0, sum)
                    print('ReLu output = {}'.format(activation))
                    if activation > 0:
                        self.layers[next_layer].neurons[connection].value = activation
                        self.layers[next_layer].neurons[connection].activate = True
                    else:
                        self.layers[next_layer].neurons[connection].activate = False

                    print(self.layers[next_layer].neurons[connection].activate)
                cur_layer += 1
                next_layer += 1
                if next_layer == len(self.layers):
                    complete = True
                print('-' * 20)
                print(' '*20)

            # check the output
            max = [0, 0]
            for i in range(len(self.layers[-1].neurons)):
                if self.layers[-1].neurons[i].value > max[0]:
                    max = [self.layers[-1].neurons[i].value, i]

            print('FIRING Neuron {} with val {}'.format(max[1], max[0]))