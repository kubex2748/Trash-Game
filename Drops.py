from random import randint
from Physic import Physic
import pygame


class Drop(Physic):
    def __init__(self, window, x, y, image):
        self.win = window
        self.image = pygame.image.load(f"graph/drops/{image}.png")
        self.x_cord = x
        self.y_cord = y
        width, height = self.image.get_size()
        Physic.__init__(self, x, y, width, height, 0.5, 2, True)

        self.clock = 0

        self.item = pygame.rect.Rect(self.x_cord, self.y_cord, self.width, self.height)
        self.hitbox = pygame.rect.Rect(self.x_cord, self.y_cord, self.width, self.height)

    def draw(self):
        self.win.blit(self.image, (self.x_cord, self.y_cord))


class Mana_Potion(Drop):
    def __init__(self, window, value):
        x = randint(100, 1800)
        y = randint(50, 100)
        Drop.__init__(self, window, x, y, 'mana_pot_img')
        self.val = value

    def tick(self, player, walls):
        self.physic_tick(walls)
        self.hitbox = pygame.rect.Rect(self.x_cord, self.y_cord, self.width, self.height)
        if self.hitbox.colliderect(player.hitbox):
            if player.current_mana + self.val <= player.max_mana:
                player.current_mana += self.val
            else:
                player.current_mana = player.max_mana
            return True
        else:
            return False


class HP_Potion(Drop):
    def __init__(self, window, value):
        x = randint(100, 1800)
        y = randint(50, 100)
        Drop.__init__(self, window, x, y, 'hp_pot_img')
        self.val = value

    def tick(self, player, walls):
        self.physic_tick(walls)
        self.hitbox = pygame.rect.Rect(self.x_cord, self.y_cord, self.width, self.height)
        if self.hitbox.colliderect(player.hitbox):
            if player.hp + self.val <= player.max_hp:
                player.hp += self.val
            else:
                player.hp = player.max_hp
            return True
        else:
            return False


class Coin(Drop):
    def __init__(self, window, x, y):
        Drop.__init__(self, window, x, y, 'coin_img')

    def tick(self, player, walls):
        self.physic_tick(walls)
        self.hitbox = pygame.rect.Rect(self.x_cord, self.y_cord, self.width, self.height)
        if self.hitbox.colliderect(player.hitbox):
            player.coins += 1
            return True
        else:
            return False
