import random


class Food:

    def __init__(self, field, snake):
        self.rows = field.w // field.grid_w - 1

        self.x = random.randint(0, self.rows) * field.grid_w + field.grid_w // 2
        self.y = random.randint(0, self.rows) * field.grid_w + field.grid_w // 2

    def eaten(self, field, snake):
        if snake.x + snake.w//2 == self.x and snake.y + snake.h // 2 == self.y:
            self.x = random.randint(0, self.rows) * field.grid_w + field.grid_w // 2
            self.y = random.randint(0, self.rows) * field.grid_w + field.grid_w // 2
