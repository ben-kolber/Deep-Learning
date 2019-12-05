import pygame

from field import Field
from snake import Snake
from food import Food

field_width = 30

field = Field(600, 600, field_width)  # field size
snake = Snake(field, field_width-1, field_width-1, 10)  # needs to math grid size
food = Food(field, snake)


clock = pygame.time.Clock()
# game loop
while(1):
    pygame.time.delay(25)
    clock.tick(20)
    snake.move()
    food.eaten(snake)
    field.update(snake, food)
