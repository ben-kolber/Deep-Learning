import pygame
import time
import math


class Field:

    def __init__(self, height, width, grid_w):
        pygame.init()
        self.h = height
        self.grid_w = grid_w
        self.w = width
        self.win = pygame.display.set_mode((height, width))
        pygame.display.set_caption("Snake")
        self.win.fill((0, 0, 0))  # black
        pygame.display.update()

    def coordinate_to_pixel(self, coordinates):
        x = coordinates[0] * self.grid_w + 1
        y = coordinates[1] * self.grid_w + 1
        return([x, y])

    # return distance to closest wall
    # but first computes distance to all 4 walls
    # coordinates are taking in pixels
    def distance_to_closest_wall(self, coordinates):
        # distance to top wall
        top = coordinates[1]

        # distance to bottom wall
        bottom = self.h - coordinates[1]

        # distance to left wall
        left = coordinates[0]

        # distance to right wall
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

    def update(self, snake, food):
        self.win.fill((0, 0, 0))  # black
        self.drawGrid()

        # snake location
        for ligament in snake.body:
            pygame.draw.rect(self.win, (0, 255, 0), (ligament.x, ligament.y, snake.w, snake.h))

        # future locations
        future = snake.get_future_locations()
        for location in future:
            coordinates = self.coordinate_to_pixel(location)

            # future possible locations
            pygame.draw.rect(self.win, (185, 210, 225),
                             (coordinates[0] + snake.w//4, coordinates[1] + snake.h//4, snake.w//2, snake.h//2))

            # distance to food at all times
            pygame.draw.line(
                self.win, (255, 165, 0), (coordinates[0] + snake.w//4, coordinates[1] + snake.h//4), (food.x, food.y))
            print('Location: {} ,Food dist: {}'.format(location, food.distance_to_food(
                [coordinates[0] + snake.w//4, coordinates[1] + snake.h//4])))

            # closest wall to a future point
            cor = self.distance_to_closest_wall(coordinates)
            pygame.draw.line(
                self.win, (255, 165, 0), (coordinates[0] + snake.w//4, coordinates[1] + snake.h//4), (cor[0] + snake.w//4, cor[1] + snake.w//4))
            print('Location: {} ,Wall dist: {}'.format(location, cor[2]))

        # food location
        pygame.draw.circle(self.win, (255, 255, 0), (food.x, food.y), 12)
        pygame.display.update()

    # death screen
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
