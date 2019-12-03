import pygame


class Snake:

    def __init__(self, height, width, velocity):
        self.w = width
        self.h = height
        self.v = velocity
        self.x = 151
        self.y = 151
        self.up = False
        self.down = False
        self.right = False
        self.left = False

    def move(self, field):
        print('MOVE')
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                field.end_game(self)

            # arrow key movement
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.left = True
                self.right = False
                self.up = False
                self.down = False
            if keys[pygame.K_RIGHT]:
                self.left = False
                self.right = True
                self.up = False
                self.down = False
            if keys[pygame.K_UP]:
                self.left = False
                self.right = False
                self.up = True
                self.down = False
            if keys[pygame.K_DOWN]:
                self.left = False
                self.right = False
                self.up = False
                self.down = True

        # continuous movement
        if self.left:
            print('going left')
            self.x -= self.w + 1

        if self.right:
            print('going left')
            self.x += self.w + 1

        if self.up:
            print('going left')
            self.y -= self.h + 1

        if self.down:
            print('going left')
            self.y += self.h + 1

        if self.x > field.w:
            self.x -= field.grid_w
            field.end_game(self)
        if self.x < 0:
            self.x += field.grid_w
            field.end_game(self)
        if self.y > field.h:
            self.y -= field.grid_w
            field.end_game(self)
        if self.y < 0:
            self.y += field.grid_w
            field.end_game(self)
