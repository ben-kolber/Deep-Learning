import pygame
import time
import random
import math

from field import Field
from snake import Snake
from food import Food

field_width = 30

field = Field(600, 600, field_width)  # field size
snake = Snake(field_width-1, field_width-1, 10)  # needs to math grid size
food = Food(field, snake)

clock = pygame.time.Clock()
# game loop
while(1):
    pygame.time.delay(50)
    clock.tick(10)
    snake.move(field)
    food.eaten(field, snake)
    field.update(snake, food)
