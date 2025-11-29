import pygame
from math import floor
from GUI import GUI

from Sound_Controller import FX

pygame.font.init()
#############################################################################################


class Spells:
    def __init__(self, player, window, cd, value, mana_req, field):
        self.win = window
        self.player = player
        self.field = field

        self.gui = GUI(window)
        self.fx = FX()

        self.cd = cd
        self.value = value
        self.mana_req = mana_req

        self.clock = 0
        self.cd_count = True

    def tick(self, delta):
        self.clock += delta
        if not self.cd_count:
            if self.field == 1:
                self.gui.cd_counter_spell_1(floor(self.cd - self.clock + 1))
            elif self.field == 2:
                self.gui.cd_counter_spell_2(floor(self.cd - self.clock + 1))
            elif self.field == 3:
                self.gui.cd_counter_spell_3(floor(self.cd - self.clock + 1))
            if self.clock > self.cd:
                self.cd_count = True


#############################################################################################
'''PASSIVE SPELLS'''


class Mana_Regen:
    def __init__(self, window,  cd, max_mana, value):
        self.cd = cd
        self.max_mana = max_mana
        self.value = value
        self.clock = 0
        self.win = window

    def spell_it(self, delta_tm, current_mana):
        self.clock += delta_tm
        text = pygame.font.Font.render(pygame.font.SysFont("arial", 48), str(floor(self.cd - self.clock + 1)), True, (0, 0, 0))
        self.win.blit(text, (1531, 981))
        val = 0
        if self.clock > self.cd:
            self.clock = 0
            if current_mana < self.max_mana and current_mana + self.value < self.max_mana:
                val = self.value
            else:
                val = 0

        return val


#############################################################################################
'''ACTIVE SPELLS'''


class HP_regen(Spells):
    def __init__(self, player, window, cd, mana_req, value, field):
        Spells.__init__(self, player, window, cd, value, mana_req, field)

    def spell_it(self):
        if self.player.hp < self.player.max_hp:
            if self.player.current_mana >= self.mana_req:
                if self.cd_count and self.player.hp + self.value < self.player.max_hp:
                    self.fx.spell_sound(0, 0.5)
                    self.player.get_hp(self.value)
                    self.player.current_mana -= self.mana_req
                    self.clock = 0
                    self.cd_count = False
                elif self.cd_count and self.player.hp + self.value > self.player.max_hp:
                    self.fx.spell_sound(0, 0.5)
                    self.player.get_hp(self.player.max_hp - self.player.hp)
                    self.player.current_mana -= self.mana_req
                    self.clock = 0
                    self.cd_count = False
            else:
                self.fx.error_sound(0.5)
        elif self.player.hp >= self.player.max_hp:
            self.fx.error_sound(0.5)


class Damage_Boost(Spells):
    def __init__(self, player, window, cd, mana_req, spell_lenght, value, field):
        Spells.__init__(self, player, window, cd, value, mana_req, field)

        self.dmg_boost_activ_img = pygame.image.load('graph/spels/attack_boost_activ.png')
        self.lenght = spell_lenght

        self.clock_2 = 0
        self.boost_activ = False

    def tick(self, delta):
        self.clock_2 += delta
        self.clock += delta

        if self.boost_activ:
            self.win.blit(self.dmg_boost_activ_img, (490, 980))
            self.player.boost = self.value
            if self.clock_2 > self.lenght:
                if self.field == 1:
                    self.gui.cd_counter_spell_1(floor(self.lenght - self.clock_2 + 1))
                elif self.field == 2:
                    self.gui.cd_counter_spell_2(floor(self.lenght - self.clock_2 + 1))
                elif self.field == 3:
                    self.gui.cd_counter_spell_3(floor(self.lenght - self.clock_2 + 1))
                self.boost_activ = False
                self.cd_count = False
        else:
            self.player.boost = 1

        if not self.cd_count:
            if self.field == 1:
                self.gui.cd_counter_spell_1(floor(self.cd - self.clock + 1))
            elif self.field == 2:
                self.gui.cd_counter_spell_2(floor(self.cd - self.clock + 1))
            elif self.field == 3:
                self.gui.cd_counter_spell_3(floor(self.cd - self.clock + 1))

            if self.clock > self.cd:
                self.cd_count = True

    def spell_it(self):
        if self.player.current_mana >= self.mana_req:
            if self.cd_count:
                self.fx.spell_sound(2, 0.5)
                self.clock = 0
                self.clock_2 = 0
                self.player.current_mana -= self.mana_req
                self.boost_activ = True
        else:
            self.fx.error_sound(0.5)


class Flash(Spells):
    def __init__(self, player, window, cd, value, mana_req, field):
        Spells.__init__(self, player, window, cd, value, mana_req, field)

    def spell_it(self, side):   #side:   1 -> right    2 -> left
        if self.player.current_mana >= self.mana_req:
            if self.cd_count:
                self.fx.spell_sound(1, 0.5)
                self.player.current_mana -= self.mana_req
                self.clock = 0
                self.cd_count = False
                if side == 2 and self.player.x_cord + self.value <= 1500:
                   self.player.x_cord = self.player.x_cord + self.value
                elif side == 1 and self.player.x_cord - self.value >= 0:
                   self.player.x_cord = self.player.x_cord - self.value
        else:
            self.fx.error_sound(0.5)


#############################################################################################
