import pygame
import time


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
        # self.drawGrid()

        # snake location
        pygame.draw.rect(self.win, (0, 255, 0), (snake.x, snake.y, snake.w, snake.h))

        # food location
        pygame.draw.circle(self.win, (255, 255, 0), (food.x, food.y), 15)

        pygame.display.update()

    def end_game(self, snake):
        print(snake.x)
        print(snake.y)
        pygame.draw.rect(self.win, (255, 0, 0), (snake.x, snake.y, snake.w, snake.h))
        pygame.display.update()
        font = pygame.font.Font('freesansbold.ttf', 64)
        losing_text = font.render('GAME OVER...', True, (255, 0, 0), (255, 255, 255))
        textRect = losing_text.get_rect()
        textRect.center = (self.h/2, self.w/2)
        self.win.blit(losing_text, textRect)
        pygame.display.update()
        pygame.quit()
        time.sleep(1)
        quit()
