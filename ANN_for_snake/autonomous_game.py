import time
from food import Food
from snake import Snake
from field import Field
import random
import pygame


# initialize the field
field = Field(630, 630, 30)

# define evolution PARAMS
pop_size = 4000
mutation_rate = 0.05
generations = 50
last_gen = 0


def create_snake():
    snake = Snake(field, 29, 10)
    snake.head.prev_loc = [snake.head.loc[0]-1, snake.head.loc[1]]
    snake.grow()
    snake.tail.prev_loc = [snake.head.loc[0] - 1, snake.head.loc[1]]
    snake.grow()
    return snake


# create initial population of snakes
population = []
for i in range(pop_size):
    population.append(create_snake())


##################
# Start training #
##################
while(1):
    total_fitness = 0
    total_time = 0
    total_score = 0
    # print('Running Generation -> {}'.format(era))
    # for each snake in the population
    for i in range(pop_size):
        food = Food(field, population[i])
        print('Running {}'.format(i))
        population[i].play_game(food)
        total_fitness += population[i].fitness
        total_score += population[i].score
        total_time += population[i].time

    # order population by highest ranking fitness
    population.sort(key=lambda snake: snake.fitness, reverse=True)
    top_scorer = sorted(population, key=lambda x: x.score, reverse=True)
    top_timer = sorted(population, key=lambda x: x.time, reverse=True)

    print('----- REPORT -------')
    print('Average Time Alive: {}'.format(total_time / pop_size))
    print('Average Score: {}'.format(total_score / pop_size))
    print('Average Fitness: {}'.format(total_fitness / pop_size))
    print(' ')
    print('Top Performer Score: {}'.format(top_scorer[0].score))
    print('Top Performer Time: {}'.format(top_timer[0].time))
    print('Top Performer Fitness: {}'.format(population[0].fitness))
    print(' ')
    print('Fittest Time Alive: {}'.format(population[0].time))
    print('Fittest Score: {}'.format(population[0].score))
    print(population[0].reason_of_death)
    print('---------------------')

    # print("Playing Replay")

    field.replay(population[0].moves_list, population[0].food_locations,
                 population[0].death_loc, population[0].reason_of_death)

    # Create new population
    # transfer top performing snake
    child = create_snake()
    child.brain = population[0].brain
    new_population = [child]

    while len(new_population) < len(population):

        # select parents
        tmp = random.randint(0, 10)
        if (tmp < 8):
            mother = population[random.randint(0, int(pop_size * 0.1))]
        else:
            mother = population[random.randint(0, int(pop_size * 0.4))]

        tmp = random.randint(0, 10)
        if (tmp < 8):
            father = population[random.randint(0, int(pop_size * 0.1))]
        else:
            father = population[random.randint(0, int(pop_size * 0.4))]

        # Create child
        child = create_snake()

        for j in range(len(child.brain.layers)):
            for k in range(len(child.brain.layers[j].neurons)):
                for i in range(len(child.brain.layers[j].neurons[k].connection_weights)):
                    if i % 2 == 0:
                        child.brain.layers[j].neurons[k].connection_weights[i] = mother.brain.layers[j].neurons[k].connection_weights[i]
                    else:
                        child.brain.layers[j].neurons[k].connection_weights[i] = father.brain.layers[j].neurons[k].connection_weights[i]

                    # Mutation
                    if random.uniform(0, 1) <= mutation_rate:
                        child.brain.layers[j].neurons[k].connection_weights[i] += random.uniform(
                            -0.4, 0.4)
                        if child.brain.layers[j].neurons[k].connection_weights[i] > 1.0:
                            child.brain.layers[j].neurons[k].connection_weights[i] = 1.0
                        if child.brain.layers[j].neurons[k].connection_weights[i] < -1.0:
                            child.brain.layers[j].neurons[k].connection_weights[i] = -1.0

        new_population.append(child)

    # print('population size: {}'.format(len(population)))
    # print('new population size: {}'.format(len(new_population)))
    population = new_population
    pop_size = len(new_population)


# print('-' * 20)
# print('The Last Generation: {}'.format(last_gen))
print(' ')
