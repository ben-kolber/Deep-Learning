import pygame
import time
import math
import random


class Field:

    def __init__(self, height, width, grid_w):
        self.h = height
        self.grid_w = grid_w
        self.w = width
        pygame.init()
        self.win = pygame.display.set_mode((self.h, self.w))
        pygame.display.set_caption("Snake")
        self.win.fill((0, 0, 0))  # black
        pygame.display.update()

    def coordinate_to_pixel(self, coordinates):
        x = coordinates[0] * self.grid_w + 1
        y = coordinates[1] * self.grid_w + 1
        return([x, y])

    def distance_to_closest_wall(self, coordinates):
        top = coordinates[1]
        bottom = self.h - coordinates[1]
        left = coordinates[0]
        right = self.w - coordinates[0]
        val = min(top, bottom, left, right)

        # return coordinates of closest wall point and distance to it
        if val == top:
            return [coordinates[0], 0, coordinates[1]]
        if val == bottom:
            return [coordinates[0], self.h, self.h - coordinates[1]]
        if val == left:
            return [0, coordinates[1], coordinates[0]]
        if val == right:
            return [self.w, coordinates[1], self.w - coordinates[0]]

    def drawGrid(self):
        rows = self.w // self.grid_w
        x = 0
        y = 0
        for l in range(rows):
            x = x + self.grid_w
            y = y + self.grid_w
            pygame.draw.line(self.win, (255, 255, 255), (x, 0), (x, self.w))
            pygame.draw.line(self.win, (255, 255, 255), (0, y), (self.h, y))
        pygame.display.update()

    # replay the best performing snake for the AI gameplay
    def replay(self, moves_list, food_locations, death_loc, msg):
        game_exit = False
        replay_complete = False
        i = 0
        MAX_ITER = len(moves_list)
        print('MAX_ITER: {}'.format(MAX_ITER))

        while not game_exit and not replay_complete:
            pygame.time.delay(25)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_exit = True

            self.win.fill((0, 0, 0))  # black

            for j in range(len(moves_list[i])):
                loc = self.coordinate_to_pixel(moves_list[i][j])
                pygame.draw.rect(self.win, (0, 255, 0), (loc[0], loc[1], 29, 29))

            # print('LOC of Food: {}'.format(food_loc))
            pygame.draw.circle(self.win, (255, 255, 0),
                               (food_locations[i][0] + 29//4, food_locations[i][1] + 29//4), 12)
            if i == (MAX_ITER - 2):
                loc = self.coordinate_to_pixel(moves_list[i][0])
                pygame.draw.rect(self.win, (255, 0, 0), (loc[0], loc[1], 29, 29))

            pygame.display.update()
            i += 1

            if (i == MAX_ITER):
                death_loc = self.coordinate_to_pixel(death_loc)
                self.end_game_for_AI(death_loc)
                replay_complete = True

    def update(self, snake, food):
        self.win.fill((0, 0, 0))  # black
        # self.drawGrid()
        # snake location
        for ligament in snake.body:
            pygame.draw.rect(self.win, (0, 255, 0), (ligament.x, ligament.y, snake.w, snake.h))

        future = snake.get_future_locations()

        for location in future:
            coordinates = self.coordinate_to_pixel(location)

            # future possible locations
            pygame.draw.rect(self.win, (185, 210, 225),
                             (coordinates[0] + snake.w//4, coordinates[1] + snake.h//4, snake.w//2, snake.h//2))

            # distance to food from future locations
            pygame.draw.line(
                self.win, (255, 165, 0), (coordinates[0] + snake.w//4, coordinates[1] + snake.h//4), (food.x, food.y))

            # closest wall to a future point
            cor = self.distance_to_closest_wall(coordinates)
            pygame.draw.line(
                self.win, (255, 165, 0), (coordinates[0] + snake.w//4, coordinates[1] + snake.h//4), (cor[0] + snake.w//4, cor[1] + snake.w//4))
        '''
        radar = snake.get_radar()

        for location in radar:
            coordinates = self.coordinate_to_pixel(location)
            pygame.draw.rect(self.win, (211, 211, 211),
                             (coordinates[0] + snake.w//4, coordinates[1] + snake.h//4, snake.w//2, snake.h//2))
        '''
        pygame.draw.circle(self.win, (255, 255, 0), (food.x, food.y), 12)
        pygame.display.update()

    # death screen manual gameplay
    def end_game(self, snake):
        pygame.draw.rect(self.win, (255, 0, 0), (snake.head.x, snake.head.y, snake.w, snake.h))
        pygame.display.update()
        font = pygame.font.Font('freesansbold.ttf', 64)
        time.sleep(0.5)
        losing_text = font.render('GAME OVER...', True, (255, 0, 0), (255, 255, 255))
        textRect = losing_text.get_rect()
        textRect.center = (self.h/2, self.w/2)
        self.win.blit(losing_text, textRect)
        pygame.display.update()
        pygame.quit()
        time.sleep(1)
        quit()
    # death screen AI gameplay

    def end_game_for_AI(self, loc):
        pygame.draw.rect(self.win, (255, 0, 0), (loc[0], loc[1], 29, 29))
        pygame.display.update()
