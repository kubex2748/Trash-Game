import pygame
from math import floor

from Physic import Physic
from GUI import GUI
from Sound_Controller import FX

from Health import Health
from Attack import Weapon
from Spells import Mana_Regen, HP_regen, Damage_Boost, Flash
from Global_Magic import Thunder_Bolt, Explosion, Good_Helper, Ice_Slow, Poison_Hit, Meteor, Hammer_Jump


class Player(Physic, Health):
    def __init__(self, window, x, y, hp, mana, cd, dmg, max_speed, wand_id, spells_id):
        self.win = window
        self.fx = FX()
        self.stand_right_img = pygame.image.load('graph/player/player_stand.png')  # normalna grafika
        self.stand_left_img = pygame.transform.flip(pygame.image.load('graph/player/player_stand.png'), True, False)
        width = self.stand_right_img.get_width()  # szerokość
        height = self.stand_right_img.get_height()  # wysokość
        Health.__init__(self, hp, True)
        Physic.__init__(self, x, y, width, height, 1, max_speed)
        self.jump_right_img = pygame.image.load('graph/player/player_jump.png')  # grafika skoku
        self.jump_left_img = pygame.transform.flip(pygame.image.load('graph/player/player_jump.png'), True, False)  # grafika skoku
        self.walk_right_img = [pygame.image.load(f'graph/player/player_walk_{x}.png') for x in range(1, 4)]  # animacja chodzenia
        self.walk_left_img = [pygame.transform.flip(pygame.image.load(f'graph/player/player_walk_{x}.png'), True, False) for x in range(1, 4)]
        self.walk_index = 0
        self.direction = 0
        self.ID = wand_id
        self.controll_active = True

        self.score_sum = 1

        self.max_mana = mana
        self.cd = cd
        self.hp = hp
        self.dmg = dmg
        self.magic_speed = 20
        self.AA_mana_req = 5        # Auto Atack
        self.enemies = []
        self.summons = []

        self.current_mana = self.max_mana
        self.gui = GUI(self.win)
        self.clock_shot = 0
        self.clock_hp = 5

        self.wand = Weapon(self.win, self.magic_speed, dmg, cd, self.ID)
        self.spells_id = spells_id
        self.spells = []

        self.mana_reg = Mana_Regen(self.win, 5, self.max_mana, 10)
        self.boost = 1

        self.choose_spell()

        self.global_spell = None
        self.global_spell_choose()

        self.coins = 0

    def global_spell_choose(self):
        if self.ID == 0:
            self.fx.error_sound(0.5)
        elif self.ID == 1:
            self.global_spell = Poison_Hit(self, self.win, 40, 10, 50, self.ID)
        elif self.ID == 2:
            self.global_spell = Thunder_Bolt(self, self.win, 40, 50, 50, self.ID)
        elif self.ID == 3:
            self.global_spell = Explosion(self, self.win, 40, 50, 50, self.ID)
        elif self.ID == 4:
            self.global_spell = Good_Helper(self, self.win, 40, 50, 50, self.ID)
        elif self.ID == 5:
            self.global_spell = Ice_Slow(self, self.win, 40, 0, 50, self.ID)
        elif self.ID == 6:
            self.global_spell = Meteor(self, self.win, 40, 0, 50, self.ID)
        elif self.ID == 7:
            self.global_spell = Hammer_Jump(self, self.win, 40, 0, 50, self.ID)


    def choose_spell(self):
        for i in range(0, 3):
            if self.spells_id[i] == 0:
                self.spells.append(HP_regen(self, self.win, 10, 10, 50, i+1))
            elif self.spells_id[i] == 1:
                self.spells.append(Flash(self, self.win, 15, 250, 20, i+1))
            elif self.spells_id[i] == 2:
                self.spells.append(Damage_Boost(self, self.win, 30, 40, 7, 3, i+1))

    def tick(self, keys, walls, delta_tm, enemies):  # wykonuje się raz na powtórzenie pętli
        self.enemies = enemies
        if not self.alive:
            return

        if self.controll_active:
            '''TICK'''
            self.physic_tick(walls)
            self.health_tick(delta_tm)
            self.wand.tick(walls, self, delta_tm, self.enemies)
            self.gui.GUI_tick(self.current_mana, self.hp)

            '''PASIVES SPELLS'''
            self.current_mana += self.mana_reg.spell_it(delta_tm, self.current_mana)

            '''STANDARD SPELLS'''
            for i in range(0, 3):
                self.spells[i].tick(delta_tm)

            if keys[pygame.K_q]:                                                                    # Q
                if self.spells_id[0] == 0:                                                          # HEAL
                    self.spells[0].spell_it()
                    self.score_sum += 1

                elif self.spells_id[0] == 1:                                                        # FLASH
                    self.spells[1].spell_it(self.direction+1)
                    self.score_sum += 1

                elif self.spells_id[0] == 2:                                                        # BOOST
                    self.spells[2].spell_it()
                    self.score_sum += 1

            if keys[pygame.K_w]:                                                                    # W
                if self.spells_id[1] == 0:  # HEAL
                    self.spells[0].spell_it()
                    self.score_sum += 1

                elif self.spells_id[1] == 1:                                                        # FLASH
                    self.spells[1].spell_it(self.direction+1)
                    self.score_sum += 1

                elif self.spells_id[1] == 2:                                                        # BOOST
                    self.spells[2].spell_it()
                    self.score_sum += 1

            if keys[pygame.K_e]:                                                                    # E
                if self.spells_id[2] == 0:  # HEAL
                    self.spells[0].spell_it()
                    self.score_sum += 1

                elif self.spells_id[2] == 1:                                                            # FLASH
                    self.spells[1].spell_it(self.direction+1)
                    self.score_sum += 1

                elif self.spells_id[2] == 2:                                                            # BOOST
                    self.spells[2].spell_it()
                    self.score_sum += 1

            '''GLOBAL SPELLS'''
            if not self.ID == 0:
                if keys[pygame.K_h]:                                                        # Global magic
                    self.global_spell.spell_it()
                self.global_spell.tick(delta_tm, self.enemies, walls)
            else:
                if keys[pygame.K_h]:
                    self.fx.error_sound(0.5)


            '''AUTO ATTACK'''
            self.clock_shot += delta_tm
            if pygame.mouse.get_pressed(3)[0]:
                if self.current_mana >= self.AA_mana_req:
                    if self.clock_shot > self.wand.cd:
                        self.wand.shoot(self.boost)
                        #self.wand.shoot_shotgun()
                        self.current_mana -= self.AA_mana_req
                        self.clock_shot = 0
                else:
                    self.fx.error_sound(0.5)

            '''MOVEMENT'''
            if keys[pygame.K_a] and self.hor_velocity > self.max_vel * -1:
                self.hor_velocity -= self.acc
            if keys[pygame.K_d] and self.hor_velocity < self.max_vel:
                self.hor_velocity += self.acc
            if keys[pygame.K_SPACE] and self.jumping is False:
                self.ver_velocity -= 15
                self.jumping = True
            if keys[pygame.K_LSHIFT]:
                self.is_coll = False
            else:
                self.is_coll = True

            if self.hor_velocity > 0:
                self.direction = 1
            elif self.hor_velocity < 0:
                self.direction = 0
            if not (keys[pygame.K_d] or keys[pygame.K_a]):
                if self.hor_velocity > 0:
                    self.hor_velocity -= self.acc
                elif self.hor_velocity < 0:
                    self.hor_velocity += self.acc

    def draw(self, window):
        self.draw_hp(window, self.x_cord, self.y_cord - 15, self.width, 8)
        self.gui.draw_on_GUI(self.max_mana, self.max_hp)

        if self.jumping:
            if self.direction == 1:
                window.blit(self.jump_right_img, (self.x_cord, self.y_cord))
            elif self.direction == 0:
                window.blit(self.jump_left_img, (self.x_cord, self.y_cord))
        elif self.hor_velocity != 0:
            if self.direction == 1:
                window.blit(self.walk_right_img[floor(self.walk_index)], (self.x_cord, self.y_cord))
            elif self.direction == 0:
                window.blit(self.walk_left_img[floor(self.walk_index)], (self.x_cord, self.y_cord))
            self.walk_index += 0.4
            if self.walk_index > 3:
                self.walk_index = 0
        else:
            if self.direction == 1:
                window.blit(self.stand_right_img, (self.x_cord, self.y_cord))
            elif self.direction == 0:
                window.blit(self.stand_left_img, (self.x_cord, self.y_cord))

        self.wand.draw(window, self.x_cord)




