import pygame
import random
import math

from body import Body


class Snake:

    def __init__(self, field, height, width, velocity):
        self.w = width
        self.h = height
        self.field = field
        self.v = velocity
        self.rows = field.w // field.grid_w - 1
        self.score = 0
        self.tail = self.head = Body(151, 151, 'null')
        self.body = [self.head]

    # a list of possible future locations
    #
    #               2 3 4
    #               1 * 5
    #               8 7 6
    #
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

    # scout ahead to see if body in vicity, if so return loc of body
    #
    #             v2    v3   v4
    #                 2 3 4
    #             v1  1 * 5  v5
    #                 8 7 6
    #             v8    v7   v6
    #
    def radar(self):
        r = 5
        radar = []
        for i in range(r):
            if self.head.exectued_move == 'right' and i != 0:
                radar.append([self.head.loc[0], self.head.loc[1]-i])
                radar.append([self.head.loc[0]+i, self.head.loc[1]-i])
                radar.append([self.head.loc[0]+i, self.head.loc[1]])
                radar.append([self.head.loc[0]+i, self.head.loc[1]+i])
                radar.append([self.head.loc[0], self.head.loc[1]+i])

            if self.head.exectued_move == 'left' and i != 0:
                radar.append([self.head.loc[0]-i, self.head.loc[1]])
                radar.append([self.head.loc[0]-i, self.head.loc[1]-i])
                radar.append([self.head.loc[0], self.head.loc[1]-i])
                radar.append([self.head.loc[0], self.head.loc[1]+i])
                radar.append([self.head.loc[0]-i, self.head.loc[1]+i])

            if self.head.exectued_move == 'up' and i != 0:
                radar.append([self.head.loc[0]-i, self.head.loc[1]])
                radar.append([self.head.loc[0]-i, self.head.loc[1]-i])
                radar.append([self.head.loc[0], self.head.loc[1]-i])
                radar.append([self.head.loc[0]+i, self.head.loc[1]-i])
                radar.append([self.head.loc[0]+i, self.head.loc[1]])

            if self.head.exectued_move == 'down' and i != 0:
                radar.append([self.head.loc[0]-i, self.head.loc[1]])
                radar.append([self.head.loc[0]+i, self.head.loc[1]])
                radar.append([self.head.loc[0]+i, self.head.loc[1]+i])
                radar.append([self.head.loc[0], self.head.loc[1]+i])
                radar.append([self.head.loc[0]-i, self.head.loc[1]+i])

        collision = []
        for ligament in self.body:
            if ligament.loc in radar:
                distance = math.sqrt((self.head.loc[0] - ligament.loc[0])
                                     ** 2 + (self.head.loc[1] - ligament.loc[1])**2)
                collision.append([ligament.loc, distance])

        return collision, radar

    # status report of a specific snake ligament
    def report(self, ligament):
        print('Head Loc: {}'.format(ligament.loc))
        print('Previous Head Loc: {}'.format(ligament.prev_loc))
        print('Latest Move: {}'.format(ligament.exectued_move))
        print('Previous Move: {}'.format(ligament.prev_move))
        print(' ')

    # X,Y locations on the field represented as a 20X20 matrix
    def get_location(self, x, y):
        x = (x - 1) // self.field.grid_w
        y = (y - 1) // self.field.grid_w
        return([x, y])

    # X,Y locations to the equivalent pixel location (corner of square)
    def coordinate_to_pixel(self, coordinates):
        print(coordinates)
        x = coordinates[0] * self.field.grid_w + 1
        y = coordinates[1] * self.field.grid_w + 1
        return([x, y])

    def head_mover(self, move):
        self.head.update(self, self.head, move, self.get_location(
            self.head.x, self.head.y))
        self.report(self.head)
        if len(self.body) > 1:
            self.update_snake()

    def move(self):
        transition = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.field.end_game(self)

            # arrow key movement -> transition state
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and self.head.exectued_move != 'left':
                transition = True
                self.head_mover('left')

            if keys[pygame.K_RIGHT] and not transition and self.head.exectued_move != 'right':
                transition = True
                self.head_mover('right')

            if keys[pygame.K_UP] and not transition and self.head.exectued_move != 'up':
                transition = True
                self.head_mover('up')

            if keys[pygame.K_DOWN] and not transition and self.head.exectued_move != 'down':
                transition = True
                self.head_mover('down')

        # continous movement
        if self.head.exectued_move == 'down' and not transition:
            self.head_mover('down')

        if self.head.exectued_move == 'up' and not transition:
            self.head_mover('up')

        if self.head.exectued_move == 'left' and not transition:
            self.head_mover('left')

        if self.head.exectued_move == 'right' and not transition:
            self.head_mover('right')

        # touch walls ends the game
        if self.head.x > self.field.w:
            self.head.x -= self.field.grid_w
            self.field.end_game(self)
        if self.head.x < 0:
            self.head.x += self.field.grid_w
            self.field.end_game(self)
        if self.head.y > self.field.h:
            self.head.y -= self.field.grid_w
            self.field.end_game(self)
        if self.head.y < 0:
            self.head.y += self.field.grid_w
            self.field.end_game(self)

    def update_snake(self):
        for i in range(len(self.body)-1):
            self.body[i+1].update(self, self.body[i+1],
                                  self.body[i].prev_move, self.body[i+1].loc)

            # snake touches it self
            if self.body[i+1].loc == self.head.loc:
                self.field.end_game(self)

    def grow(self):

        # generate new body part in tail's previous location
        loc = self.coordinate_to_pixel(self.tail.prev_loc)

        # remember last move, so that it can take it at time t+1
        ligement = Body(loc[0], loc[1], self.head.exectued_move)
        self.body.append(ligement)
        self.tail = ligement
