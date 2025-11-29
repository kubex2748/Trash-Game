import pygame


class Wall:
    def __init__(self, x, y, width, height, color, is_floor=False):
        self.x_cord = x
        self.y_cord = y
        self.width = width
        self.height = height
        self.hitbox = pygame.Rect(self.x_cord, self.y_cord, self.width, self.height)
        self.color = color
        self.is_floor = is_floor

    def draw(self, window):
        pygame.draw.rect(window, (self.color), self.hitbox)




