AI for Snake
@Ben Kolber 


# Introduction
A custom-built snake game using Python3 and the Pygame library. 
The game can be played by both a Human in manual mode, or by the AI in autonomous mode. The AI is a genetic algorithm and artificial neural network-based agent, learning to play the game from scratch with no prior knowledge of the rules or objectives.  

## Requirements
pygame 
python 3.6 
numpy


# Human Game
Simply run the program human_game.py for a snake game. control the snake using the arrows. Touching the walls or the snake itself will result in a loss. 


# AI Game
Using a genetic algorithm and neural networks the agent learns how to play snake with no prior knowledge of the game, the rules, and the objective. 

a population of snakes is created, with each snake having a randomly initialized neural network that dictates the action the snake will take (up, down, left, right).

The ANN (brain) of the snake is a 4 layered neural network, with a 24 node input layer, two 16 neuron hidden layers and a 4 neuron output layer. The rectifier function is applied at each of the hidden layers, and the softmax function on the output layer.

The vector fed into the ANN is a 24 value vector. The snake looks in 8 directions for distance to food, the wall and itself. The values are normalized and fed into the snake's brain. An additional 4 values can be added to the vector that indicates the direction of the head, represented as 1's and 0's. If added, please change the input layer of the ANN to 28 neurons in snake.py. 

The top-performing snakes, based on the amount of food eaten, time being alive and exploration, will be used to create children. The children are created by mixing the weight values of two top-performing snakes brains. The new brain is then assigned to a new snake (the child) who is added to the new population. a mutation rate is also applied to the weight values of the child's brain.

Once the new population is created, the process runs again. The process will loop as many times as defined in 'generations'.

A replay of the top-performing snake in the population is run after each generation to visualize the improvement.


## File Overview
Neural Network: 
network.py - created the ANN. 
layer.py - an object representing each layer in the ANN. You may add as many layers as needed to the network, specified in network.py.
neuron.py - the neuron object in the layer, which holds a list of connection values. 

Snake Game:
snake.py - the agent, which can be played autonomously or manually.
field.py - the field, visualized, on which the agent moves around. 
body.py - the structure of the snake.
food.py - the food placed on the field for the snake to eat and grow. 

Gameplay:
human_game.py - manually play the snake game. 
AI_game.py - AI plays snake, while learning the game with no prior knowledge. The population, mutation rate, and generations can all be edited on the top of the file. 
