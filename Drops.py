import pygame
#randint(0, 1500)


class Drop:
    def __init__(self, window, x, y, drop_type, image):
        self.win = window
        self.image = pygame.image.load(f"graph/drops/{image}.png")
        self.x_cord = x
        self.y_cord = y
        self.width, self.height = self.image.get_size()

        self.item = pygame.rect.Rect(self.x_cord, self.y_cord, self.width, self.height)
        self.hitbox = pygame.rect.Rect(self.x_cord, self.y_cord, self.width, self.height)

    def tick(self, player):
        self.hitbox = pygame.rect.Rect(self.x_cord, self.y_cord, self.width, self.height)
        if self.hitbox.colliderect(player.hitbox):
            pass

    def draw(self):
        self.win.blit(self.image, (self.x_cord, self.y_cord))



def get(player, score):
    banknotes = []
    for banknote in banknotes:
        banknote.tick()

    for banknote in banknotes:
        if player.hitbox.colliderect(banknote.hitbox):
            banknotes.remove(banknote)
            score += 1

    for banknote in banknotes:
        banknote.draw()