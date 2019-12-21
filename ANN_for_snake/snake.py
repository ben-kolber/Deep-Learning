import pygame
import random
import math

from body import Body
from network import Network
from layer import Layer


class Snake:

    def __init__(self, field, dimension, velocity):
        self.w = self.h = dimension
        self.field = field
        self.v = velocity
        self.rows = field.w // field.grid_w - 1
        self.tail = self.head = Body(151, 151, 'null', self)
        self.body = [self.head]
        self.moves = 150        # limited moves before death
        self.fitness = 0        # snake fitness score for next gen
        self.dead = False
        self.actions = ['left', 'up', 'right', 'down']
        self.score = 1
        self.moves_list = []
        self.food_locations = []
        self.death_loc = ''
        self.towards_food = 0
        self.away_from_food = 0
        self.reason_of_death = 'null'
        self.time = 0
        self.brain = self.init_brain()

    # initialize brain (ANN)

    def init_brain(self):
        # initilize neural network
        network = Network()

        # add an input layer
        # PARAMS: neurons, threshold
        network.add_input_layer(Layer(24))

        # add hidden layer
        network.add_hidden_layer(Layer(16))
        network.add_hidden_layer(Layer(16))

        # add output layer and coresponding actions
        network.add_output_layer(Layer(4))

        return network

    def get_radar(self):
        radar = []
        for i in range(3):
            radar.append([self.head.loc[0]-i, self.head.loc[1]-i])
            radar.append([self.head.loc[0], self.head.loc[1]-i])
            radar.append([self.head.loc[0]+i, self.head.loc[1]-i])
            radar.append([self.head.loc[0]+i, self.head.loc[1]])
            radar.append([self.head.loc[0]+i, self.head.loc[1]+i])
            radar.append([self.head.loc[0], self.head.loc[1]+i])
            radar.append([self.head.loc[0]-i, self.head.loc[1]+i])
            radar.append([self.head.loc[0]-i, self.head.loc[1]])

        return radar
    # a list of possible future locations
    #
    #               2 3 4
    #               1 * 5
    #               8 7 6

    def get_future_locations(self):
        future_locations = []
        # based on head direction
        if self.head.exectued_move == 'right':
            future_locations.append([self.head.loc[0]-1, self.head.loc[1]-1])
            future_locations.append([self.head.loc[0], self.head.loc[1]-1])
            future_locations.append([self.head.loc[0]+1, self.head.loc[1]-1])
            future_locations.append([self.head.loc[0]+1, self.head.loc[1]])
            future_locations.append([self.head.loc[0]+1, self.head.loc[1]+1])
            future_locations.append([self.head.loc[0], self.head.loc[1]+1])
            future_locations.append([self.head.loc[0]-1, self.head.loc[1]+1])

        if self.head.exectued_move == 'left':
            future_locations.append([self.head.loc[0]-1, self.head.loc[1]])
            future_locations.append([self.head.loc[0]-1, self.head.loc[1]-1])
            future_locations.append([self.head.loc[0], self.head.loc[1]-1])
            future_locations.append([self.head.loc[0]+1, self.head.loc[1]-1])
            future_locations.append([self.head.loc[0]+1, self.head.loc[1]+1])
            future_locations.append([self.head.loc[0], self.head.loc[1]+1])
            future_locations.append([self.head.loc[0]-1, self.head.loc[1]+1])

        if self.head.exectued_move == 'up':
            future_locations.append([self.head.loc[0]-1, self.head.loc[1]])
            future_locations.append([self.head.loc[0]-1, self.head.loc[1]-1])
            future_locations.append([self.head.loc[0], self.head.loc[1]-1])
            future_locations.append([self.head.loc[0]+1, self.head.loc[1]-1])
            future_locations.append([self.head.loc[0]+1, self.head.loc[1]])
            future_locations.append([self.head.loc[0]+1, self.head.loc[1]+1])
            future_locations.append([self.head.loc[0]-1, self.head.loc[1]+1])

        if self.head.exectued_move == 'down':
            future_locations.append([self.head.loc[0]-1, self.head.loc[1]])
            future_locations.append([self.head.loc[0]-1, self.head.loc[1]-1])
            future_locations.append([self.head.loc[0]+1, self.head.loc[1]-1])
            future_locations.append([self.head.loc[0]+1, self.head.loc[1]])
            future_locations.append([self.head.loc[0]+1, self.head.loc[1]+1])
            future_locations.append([self.head.loc[0], self.head.loc[1]+1])
            future_locations.append([self.head.loc[0]-1, self.head.loc[1]+1])

        return future_locations

    # status report of a specific snake ligament

    def report(self, ligament):
        print('Head Loc: {}'.format(ligament.loc))
        print('Previous Head Loc: {}'.format(ligament.prev_loc))
        print('Latest Move: {}'.format(ligament.exectued_move))
        print('Previous Move: {}'.format(ligament.prev_move))
        print(' ')

    # X,Y locations on the field represented as a 20X20 matrix
    def get_location(self, x, y):
        x = (x - 1.0) // self.field.grid_w
        y = (y - 1.0) // self.field.grid_w
        return([x, y])

    # X,Y locations to the equivalent pixel location (corner of square)
    def coordinate_to_pixel(self, coordinates):
        # print(coordinates)
        x = coordinates[0] * self.field.grid_w + 1
        y = coordinates[1] * self.field.grid_w + 1
        return([x, y])

    def head_mover(self, move):
        self.head.update(self, self.head, move, self.get_location(
            self.head.x, self.head.y))
        # self.report(self.head)
        if len(self.body) > 1:
            self.update_snake()

    def manual_move(self, food):
        # check if any moves left
        if self.moves == 0:
            self.field.end_game(self)

        transition = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.field.end_game(self)

            # arrow key movement -> transition state
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and self.head.exectued_move != 'left':
                self.moves -= 1
                transition = True
                self.head_mover('left')
                self.get_brain_input_vector(food)

            if keys[pygame.K_RIGHT] and not transition and self.head.exectued_move != 'right':
                self.moves -= 1
                transition = True
                self.head_mover('right')
                self.get_brain_input_vector(food)

            if keys[pygame.K_UP] and not transition and self.head.exectued_move != 'up':
                self.moves -= 1
                transition = True
                self.head_mover('up')
                self.get_brain_input_vector(food)

            if keys[pygame.K_DOWN] and not transition and self.head.exectued_move != 'down':
                self.moves -= 1
                transition = True
                self.head_mover('down')
                self.get_brain_input_vector(food)

        # touch walls ends the game
        if self.head.x >= self.field.w:
            self.head.x -= self.field.grid_w
            self.field.end_game(self)
        if self.head.x <= 0:
            self.head.x += self.field.grid_w
            self.field.end_game(self)
        if self.head.y > self.field.h:
            self.head.y -= self.field.grid_w
            self.field.end_game(self)
        if self.head.y <= 0:
            self.head.y += self.field.grid_w
            self.field.end_game(self)

    def update_snake(self):
        for i in range(len(self.body)-1):
            self.body[i+1].update(self, self.body[i+1],
                                  self.body[i].prev_move, self.body[i+1].loc)

            # snake touches it self
            if self.body[i+1].loc == self.head.loc:
                self.dead = True
                self.reason_of_death = 'ERROR: SELF COLLISION'
                self.death_loc = self.head.loc
                # self.field.end_game(self)

    def grow(self):

        # generate new body part in tail's previous location
        loc = self.coordinate_to_pixel(self.tail.prev_loc)
        if len(loc) == 0:
            loc = self.coordinate_to_pixel(self.head.prev_loc)

        # remember last move, so that it can take it at time t+1
        ligament = Body(loc[0], loc[1], self.head.exectued_move, self)
        self.body.append(ligament)
        self.tail = ligament

    def get_euclidian_dist(self, loc_1, loc_2):
        return math.sqrt((loc_1[0] - loc_2[0])**2 + (loc_1[1] - loc_2[1])**2)

    # checking range of 8 for vision
    # 1. If wall is detected, returns distance
    # 2. If food is detected, return distance
    # 3. If tail is detected, returns distance
    # 4. One hot ecoded direction
    # Vision structure:
    #
    #             v1    v2   v3
    #                 2 3 4
    #             v0  1 * 5  v4
    #                 8 7 6
    #             v7    v6   v5
    #
    # Movement sequence: L U R D

    def look_to(self, sensor, r, food):
        look = [0.0] * 3
        wall_x = self.field.w / self.field.grid_w
        wall_y = self.field.h / self.field.grid_w

        X = self.head.loc[0]
        Y = self.head.loc[1]
        food_loc = food.loc

        if (sensor == 'v0'):
            food_found = False
            body_found = False
            wall = False
            distance = 0

            while not wall:
                distance += 1
                if [X-distance, Y] == food_loc and not food_found:
                    food_found = True
                    look[0] = 1.0 / distance
                # check for body
                if not body_found:
                    for ligament in self.body:
                        if [X-distance, Y] == ligament.loc:
                            body_found = True
                            look[1] = 1.0 / distance
                if X-distance == -1:  # West Wall
                    wall = True
                    look[2] = 1.0 / distance

        if (sensor == 'v1'):
            wall = False
            food_found = False
            body_found = False
            distance = 0

            while not wall:
                distance += 1
                if [X-distance, Y-distance] == food_loc and not food_found:
                    food_found = True
                    look[0] = 1.0 / distance
                if not body_found:
                    for ligament in self.body:
                        if [X-distance, Y-distance] == ligament.loc:
                            body_found = True
                            look[1] = 1.0 / distance
                if Y-distance == -1 and not wall:  # North Wall
                    wall = True
                    look[2] = 1.0 / distance
                if X-distance == -1 and not wall:  # West Wall
                    wall = True
                    look[2] = 1.0 / distance

        if (sensor == 'v2'):
            food_found = False
            body_found = False
            wall = False
            distance = 0

            while not wall:
                distance += 1
                if [X, Y-distance] == food_loc and not food_found:
                    food_found = True
                    look[0] = 1.0 / distance
                if not body_found:
                    for ligament in self.body:
                        if [X, Y-distance] == ligament.loc:
                            body_found = True
                            look[1] = 1.0 / distance
                if Y-distance == -1:  # North Wall
                    wall = True
                    look[2] = 1.0 / distance

        if (sensor == 'v3'):
            wall = False
            food_found = False
            body_found = False
            distance = 0

            while not wall:
                distance += 1
                if [X+distance, Y-distance] == food_loc and not food_found:
                    food_found = True
                    look[0] = 1.0 / distance
                if not body_found:
                    for ligament in self.body:
                        if [X+distance, Y-distance] == ligament.loc:
                            body_found = True
                            look[1] = 1.0 / distance
                if X+distance == wall_x and not wall:  # East Wall
                    wall = True
                    look[2] = 1.0 / distance
                if Y-distance == -1 and not wall:  # North Wall
                    wall = True
                    look[2] = 1.0 / distance

        if (sensor == 'v4'):
            food_found = False
            body_found = False
            wall = False
            distance = 0

            while not wall:
                distance += 1
                if [X+distance, Y] == food_loc and not food_found:
                    food_found = True
                    look[0] = 1.0 / distance
                if not body_found:
                    for ligament in self.body:
                        if [X+distance, Y] == ligament.loc:
                            body_found = True
                            look[1] = 1.0 / distance
                if X+distance == wall_x:  # East Wall
                    wall = True
                    look[2] = 1.0 / distance

        if (sensor == 'v5'):
            wall = False
            food_found = False
            body_found = False
            distance = 0

            while not wall:
                distance += 1
                if [X+distance, Y+distance] == food_loc and not food_found:
                    food_found = True
                    look[0] = 1.0 / distance
                if not body_found:
                    for ligament in self.body:
                        if [X+distance, Y+distance] == ligament.loc:
                            body_found = True
                            look[1] = 1.0 / distance

                if X+distance == wall_x and not wall:  # East Wall
                    wall = True
                    look[2] = 1.0 / distance
                if Y+distance == wall_y and not wall:  # South Wall
                    wall = True
                    look[2] = 1.0 / distance

        if (sensor == 'v6'):
            food_found = False
            body_found = False
            wall = False
            distance = 0

            while not wall:
                distance += 1
                if [X, Y+distance] == food_loc and not food_found:
                    food_found = True
                    look[0] = 1.0 / distance
                if not body_found:
                    for ligament in self.body:
                        if [X, Y+distance] == ligament.loc:
                            body_found = True
                            look[1] = 1.0 / distance
                if Y+distance == wall_y:  # South Wall
                    look[2] = 1.0 / distance
                    wall = True

        if (sensor == 'v7'):
            wall = False
            food_found = False
            body_found = False
            distance = 0

            while not wall:
                distance += 1
                if [X-distance, Y+distance] == food_loc and not food_found:
                    food_found = True
                    look[0] = 1.0 / distance
                if not body_found:
                    for ligament in self.body:
                        if [X-distance, Y-distance] == ligament.loc:
                            body_found = True
                            look[1] = 1.0 / distance

                if Y+distance == wall_y and not wall:  # South Wall
                    wall = True
                    look[2] = 1.0 / distance
                if X-distance == -1 and not wall:  # West Wall
                    wall = True
                    look[2] = 1.0 / distance

            '''
            # get head direction as oneHotEncoded value
            if self.head.exectued_move == 'left':
                head_dir_vector[0] = 1.0
            if self.head.exectued_move == 'up':
                head_dir_vector[1] = 1.0
            if self.head.exectued_move == 'right':
                head_dir_vector[2] = 1.0
            if self.head.exectued_move == 'down':
                head_dir_vector[3] = 1.0

            # get tail direction as oneHotEncoded value
            if self.tail.exectued_move == 'left':
                tail_dir_vector[0] = 1.0
            if self.tail.exectued_move == 'up':
                tail_dir_vector[1] = 1.0
            if self.tail.exectued_move == 'right':
                tail_dir_vector[2] = 1.0
            if self.tail.exectued_move == 'down':
                tail_dir_vector[3] = 1.0

            '''
        return look

    def get_brain_input_vector(self, food):
        vector = [0.0] * 24
        r = 22

        look = self.look_to('v0', r, food)
        vector[0] = look[0]
        vector[1] = look[1]
        vector[2] = look[2]
        look = self.look_to('v1', r, food)
        vector[3] = look[0]
        vector[4] = look[1]
        vector[5] = look[2]
        look = self.look_to('v2', r, food)
        vector[6] = look[0]
        vector[7] = look[1]
        vector[8] = look[2]
        look = self.look_to('v3', r, food)
        vector[9] = look[0]
        vector[10] = look[1]
        vector[11] = look[2]
        look = self.look_to('v4', r, food)
        vector[12] = look[0]
        vector[13] = look[1]
        vector[14] = look[2]
        look = self.look_to('v5', r, food)
        vector[15] = look[0]
        vector[16] = look[1]
        vector[17] = look[2]
        look = self.look_to('v6', r, food)
        vector[18] = look[0]
        vector[19] = look[1]
        vector[20] = look[2]
        look = self.look_to('v7', r, food)
        vector[21] = look[0]
        vector[22] = look[1]
        vector[23] = look[2]

        return vector

    def autonomous_move(self, food):
        # check if any moves left
        if self.moves == 0:
            self.dead = True
            self.death_loc = self.head.loc
            self.reason_of_death = 'ERROR: OUT OF MOVES'

        self.time += 1

        # get movement vector:
        vector = self.get_brain_input_vector(food)
        #print('Moving on Vector::: {}'.format(vector))
        action = self.brain.run_network(vector, self.actions)

        if self.head.exectued_move == 'null':
            self.head.exectued_move = 'right'

        if action == 'left':
            self.moves -= 1
            self.head_mover('left')

        if action == 'up':
            self.moves -= 1
            self.head_mover('up')

        if action == 'right':
            self.moves -= 1
            self.head_mover('right')

        if action == 'down':
            self.moves -= 1
            self.head_mover('down')

        # touch walls ends the game
        if self.head.x >= self.field.w:
            self.head.x -= self.field.grid_w
            self.dead = True
            self.death_loc = self.head.loc
            self.reason_of_death = 'ERROR: WALL COLLISION'
        if self.head.x <= 0:
            self.head.x += self.field.grid_w
            self.dead = True
            self.death_loc = self.head.loc
            self.reason_of_death = 'ERROR: WALL COLLISION'
        if self.head.y > self.field.h:
            self.head.y -= self.field.grid_w
            self.dead = True
            self.death_loc = self.head.loc
            self.reason_of_death = 'ERROR: WALL COLLISION'
        if self.head.y <= 0:
            self.head.y += self.field.grid_w
            self.dead = True
            self.death_loc = self.head.loc
            self.reason_of_death = 'ERROR: WALL COLLISION'

        if (self.get_euclidian_dist(self.head.loc, food.loc) < self.get_euclidian_dist(self.head.prev_loc, food.loc)):
            self.towards_food += 1
        else:
            self.away_from_food += 1

    def play_game(self, food):
        while self.dead == False:

            # run game autonomously
            self.autonomous_move(food)
            food.eaten(self)

            # save body locations for replay
            localized = []
            for ligament in self.body:
                localized.append(ligament.loc)
            self.moves_list.append(localized)

            # save food locations
            self.food_locations.append([food.x, food.y])

        # Calculate Fitness
        if(self.score < 10):
            self.fitness = self.time ** 2 * 2 ** self.score
            #self.fitness = self.score ** 2 * (self.time // 10)
        else:
            self.fitness = (self.time ** 2) * (2 ** 10) * (self.score-9)
