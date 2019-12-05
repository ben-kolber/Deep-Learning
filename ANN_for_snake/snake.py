import pygame
import random
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

    # X,Y locations on the field represented as a matrix
    # 20 X 20

    def report(self, legiment):
        print('Current Loc: {}'.format(legiment.loc))
        print('Previous Loc: {}'.format(legiment.prev_loc))
        print('Latest Move: {}'.format(legiment.exectued_move))
        print('Previous Move: {}'.format(legiment.prev_move))
        print(' ')

    def get_location(self, x, y):
        x = (x - 1) // self.field.grid_w
        y = (y - 1) // self.field.grid_w
        return([x, y])

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
        print('Growing...')

        # generate new body part in tail's previous location
        loc = self.coordinate_to_pixel(self.tail.prev_loc)

        # remember last move, so that it can take it at time t+1
        ligement = Body(loc[0], loc[1], self.head.exectued_move)
        self.body.append(ligement)
        self.tail = ligement

        print('Structure: {}'.format(self.body))
