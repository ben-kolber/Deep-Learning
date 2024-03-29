

class Body():

    def __init__(self, X, Y, move, snake):
        self.exectued_move = move
        self.prev_move = 'null'
        self.loc = snake.get_location(X, Y)
        self.prev_loc = []
        self.x = X
        self.y = Y

    # action movements
    def move_right(self, snake,  ligament):
        ligament.x += snake.w + 1.0

    def move_left(self, snake,  ligament):
        ligament.x -= snake.w + 1.0

    def move_up(self, snake, ligament):
        ligament.y -= snake.h + 1.0

    def move_down(self, snake, ligament):
        ligament.y += snake.h + 1.0

    def update(self, snake, legiment, move, loc):
        self.prev_loc = loc
        self.prev_move = self.exectued_move
        if move == 'left':
            self.move_left(snake, legiment)

        if move == 'right':
            self.move_right(snake, legiment)

        if move == 'up':
            self.move_up(snake, legiment)

        if move == 'down':
            self.move_down(snake, legiment)

        self.loc = snake.get_location(self.x, self.y)
        self.exectued_move = move
