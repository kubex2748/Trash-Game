import pygame
from math import floor
from Sound_Controller import FX
class Health:
    def __init__(self, max_hp, player=False):
        self.fx = FX()
        self.hp = max_hp
        self.max_hp = max_hp
        self.alive = True
        self.last_dmg = 0
        self.player = player
        self.take_dmg = True

    def health_tick(self, delta_tm):
        self.last_dmg += delta_tm

    def dealt_dmg(self, dmg):
        if self.take_dmg:
            self.fx.mele_hit_sound(0.3)
            if self.hp > dmg:
                self.hp -= dmg
            elif self.hp <= dmg:
                self.hp = 0
                self.alive = False


    def get_hp(self, hp):
        if self.hp < self.max_hp:
            self.hp += hp

    def draw_hp(self, window, x, y, max_width, height):
        percent_width = self.hp / self.max_hp
        width = round(max_width * percent_width)
        #width_player = round(100 * percent_width)
        if self.hp > floor(self.max_hp * 0.3):
            color = (30, 255, 30)
        else:
            color = (255, 30, 30)

        pygame.draw.rect(window, (30, 30, 30), (x, y, max_width, height))
        pygame.draw.rect(window, color, (x, y, width, height))

