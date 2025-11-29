import pygame
from math import sqrt, degrees, asin, floor

from Sound_Controller import FX
from Physic import Physic
from GUI import GUI
from Informations import Links



class Magic(Physic):
    def __init__(self, magic, speed, damage, x_side, y_side, image):
        self.spell_img = pygame.image.load(f"{image}.png")
        self.width, self.height = self.spell_img.get_size()
        self.acc = 0
        super().__init__(magic.x_cord, magic.y_cord, self.width, self.height, 0, speed)
        self.gravity = 0
        c_side = sqrt(x_side ** 2 + y_side ** 2)
        step = c_side / speed
        x_speed = x_side / step
        y_speed = y_side / step
        self.hor_velocity = x_speed
        self.ver_velocity = y_speed
        self.damage = damage
        self.clock = 0
        self.exists = True

    def tick(self, walls, delta, enemies, is_player=True):
        self.physic_tick(walls)

        for wall in walls:
            if wall.hitbox.colliderect(self.hitbox):
                self.exists = False

        self.clock += delta
        if self.clock > 3:
            self.exists = False
        if is_player:
            for enemy in enemies:
                if enemy.hitbox.colliderect(self.hitbox):
                    enemy.dealt_dmg(self.damage)
                    self.exists = False
        else:
            if enemies.hitbox.colliderect(self.hitbox):
                enemies.dealt_dmg(self.damage)
                self.exists = False

    def draw(self, window):
        window.blit(self.spell_img, (self.x_cord, self.y_cord))


def degree(x_screen, y_screen, x_mouse, y_mouse):
    x_side = x_screen - x_mouse
    y_side = y_screen - y_mouse
    triangle_long = sqrt(x_side**2 + y_side**2)
    dg = degrees(asin(y_side / triangle_long))
    if x_side > 0:
        dg = -dg
    return dg


def centered_rotate(image, x, y, angle):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center=image.get_rect(center=(x, y)).center)
    return rotated_image, new_rect


class Weapon:
    def __init__(self, win, speed, damage, cooldown, wand_id=0):
        self.fx = FX()
        links = Links()
        self.spells = links.spells
        self.global_spels = links.global_set_icon

        self.wand_id = wand_id
        self.win = win
        self.x_cord = int(0)
        self.y_cord = int(0)
        self.speed = speed
        self.damage = damage
        self.cd = cooldown
        self.bullets = []
        self.image = [pygame.image.load(f'{links.wand_animations[wand_id]}_{x}.png') for x in range(1, 11)]
        self.image_index = 0
        self.clock = 0




    def shoot(self, boost):
        if self.clock > self.cd:
            self.fx.wand_shot_sound(self.wand_id, 0.6)
            self.clock = 0
            x_mouse, y_mouse = pygame.mouse.get_pos()
            x_side = x_mouse - self.x_screen
            y_side = y_mouse - self.y_cord
            self.bullets.append(Magic(self, self.speed, self.damage * boost, x_side, y_side, self.spells[self.wand_id]))

    # experimental
    def shoot_shotgun(self):
        shots_y = [0, 0, 0]
        if self.clock > self.cd:
            self.clock = 0
            x_mouse, y_mouse = pygame.mouse.get_pos()
            x_side = x_mouse - self.x_screen
            for i in range(0, 3):
                shots_y[i] = y_mouse - (self.y_cord - 75) + i*75
            self.bullets.append(Magic(self, self.speed, self.damage * 2, x_side, shots_y[0], self.spells[self.wand_id]))
            self.bullets.append(Magic(self, self.speed, self.damage * 2, x_side, shots_y[1], self.spells[self.wand_id]))
            self.bullets.append(Magic(self, self.speed, self.damage * 2, x_side, shots_y[2], self.spells[self.wand_id]))


    def tick(self, beams, player, delta, enemies):
        self.clock += delta
        self.x_cord = player.x_cord
        self.y_cord = player.y_cord
        for bullet in self.bullets:
            bullet.tick(beams, delta, enemies)
            if not bullet.exists:
                self.bullets.remove(bullet)

    def draw(self, win, x_screen):
        GUI.draw_Global_Spell(self, self.win, self.global_spels[self.wand_id])
        self.x_screen = x_screen
        for bullet in self.bullets:
            bullet.draw(win)
        angle = degree(x_screen, self.y_cord, *pygame.mouse.get_pos())
        if pygame.mouse.get_pos()[0] - x_screen < 0:
            image = pygame.transform.flip(self.image[floor(self.image_index)], True, False)
        else:
            image = self.image[floor(self.image_index)]
        to_blit = centered_rotate(image, x_screen + 30, self.y_cord + 35, angle)
        self.image_index += 0.5
        if self.image_index >= 10:
            self.image_index = 0
        win.blit(*to_blit)
