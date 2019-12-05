import random
import math

from body import Body


class Food:

    def __init__(self, field, snake):
        self.rows = field.w // field.grid_w - 1
        searching = True
        while searching:
            self.x = random.randint(0, self.rows) * field.grid_w + field.grid_w // 2
            self.y = random.randint(0, self.rows) * field.grid_w + field.grid_w // 2
            for legament in snake.body:
                if legament.loc == [self.x, self.y]:
                    searching = True
                    break
                else:
                    searching = False

    def eaten(self, snake):
        # if food was eaten
        if snake.head.x + snake.w//2 == self.x and snake.head.y + snake.h // 2 == self.y:
            print("FOOD FOUND!!")
            self.x = random.randint(0, self.rows) * snake.field.grid_w + snake.field.grid_w // 2
            self.y = random.randint(0, self.rows) * snake.field.grid_w + snake.field.grid_w // 2
            snake.score += 1
            snake.grow()

    def distance_to_food(self, coordinates):
        return math.sqrt((coordinates[0] - self.x)**2 + (coordinates[1] - self.y)**2)
