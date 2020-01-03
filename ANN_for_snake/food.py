import random
import math

from body import Body


class Food:

    def __init__(self, field, snake):
        self.rows = field.w // field.grid_w - 1
        self.snake = snake
        self.field = field
        self.x = 0
        self.y = 0
        self.loc = []
        self.generate_food()

    # create food randomly within field params
    def generate_food(self):
        searching = True
        while searching:
            self.x = self.snake.food_x = random.randint(
                0, self.rows) * self.field.grid_w + self.field.grid_w // 2
            self.y = self.snake.food_y = random.randint(
                0, self.rows) * self.field.grid_w + self.field.grid_w // 2
            for ligament in self.snake.body:
                if ligament.loc == [self.x, self.y]:
                    searching = True
                    break
                else:
                    searching = False
        self.loc = self.snake.get_location(self.x, self.y)

    # check if food was eaten
    def eaten(self, snake):
        if snake.head.x + snake.w//2 == self.x and snake.head.y + snake.h // 2 == self.y:
            self.generate_food()
            snake.score += 1
            # add 100 moves to snake, with a max of 500 moves
            snake.moves += 100

            snake.grow()

    def distance_to_food(self, coordinates):
        return math.sqrt((coordinates[0] - self.x)**2 + (coordinates[1] - self.y)**2)
