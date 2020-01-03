import pygame
import time
from field import Field
from snake import Snake
from food import Food

field_width = 30

field = Field(660, 660, field_width)
snake = Snake(field, field_width-1, 10)
food = Food(field, snake)

clock = pygame.time.Clock()

# game loop
while(1):
    pygame.time.delay(25)
    clock.tick(20)
    snake.manual_move(food)
    food.eaten(snake)
    field.update(snake, food)
