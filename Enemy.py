import pygame
from math import floor
from Sound_Controller import FX
from random import randint
from Physic import Physic
from Health import Health
from Attack import Magic


class Enemy(Physic, Health):
    def __init__(self, x, y, hp, cd, dmg, acc, max_vel, file, spell_file='', is_range=False, collision=True):
        self.fx = FX()
        self.image = pygame.image.load(f"{file}.png")
        self.max_speed = 0
        width, hight = self.image.get_size()
        Physic.__init__(self, x, y, width, hight, acc, max_vel, collision)
        Health.__init__(self, hp)
        self.spell_file = spell_file

        self.distance = 0
        self.min_dis = True
        self.clock = 0
        self.bullets = []
        self.range = is_range

        self.jump_height = 15

        self.speed = 15
        self.dmg = dmg
        self.cd = cd
        self.clock_ult = 0
        self.ult_activ = False

    def attack_mele(self, player, bonus_dmg=0):
        if self.hitbox.colliderect(player.hitbox) and self.clock > self.cd:  # attack
            player.dealt_dmg(self.dmg + bonus_dmg)
            self.clock = 0

    def attack_dist(self, player, bonus_dmg=0):
        if self.clock > self.cd:
            self.fx.wand_shot_sound(0, 0.3)
            self.clock = 0
            x_side = player.x_cord - self.x_cord
            y_side = player.y_cord - self.y_cord
            self.bullets.append(Magic(self, self.speed, self.dmg + bonus_dmg, x_side, y_side, self.spell_file))

    def ult_cd_counter(self, delta, cd):
        state = False
        self.clock_ult += delta
        if self.clock_ult >= cd:
            state = True
            if self.ult_activ == False:
                self.clock_ult = 0
        else:
            state = False
        return state

    def set_max_vel(self, state, val):
        if state:
            self.max_vel = val
        else:
            self.max_vel = self.max_speed

    def go_left(self):
        if -self.hor_velocity < self.max_vel:
            self.hor_velocity -= self.acc

    def go_right(self):
        if self.hor_velocity < self.max_vel:
            self.hor_velocity += self.acc

    def go_up(self):
        if -self.ver_velocity < self.max_vel:
            self.ver_velocity -= self.gravity + self.acc

    def jump(self):
        if not self.jumping:
            self.ver_velocity -= self.jump_height
            self.jumping = True

    def tick_mele(self, delta):
        self.clock += delta

    def tick_shot(self, walls, slf, delta, enemies):        #slf = self
        self.clock += delta
        #self.x_cord = slf.x_cord
        #self.y_cord = slf.y_cord
        for bullet in self.bullets:
            bullet.tick(walls, delta, enemies, False)
            if not bullet.exists:
                self.bullets.remove(bullet)

    def draw(self, window):
        window.blit(self.image, (int(self.x_cord), int(self.y_cord)))
        self.draw_hp(window, self.x_cord, self.y_cord - 15, self.width, 8)
        if range:
            for bullet in self.bullets:
                bullet.draw(window)


class Boss(Enemy):
    def __init__(self, win, hp, cd, dmg, acc, walk_speed, enemy_img, spell_img, shooter, coll):
        self.window = win
        self.middle = 1920 / 2 - 45

        Enemy.__init__(self, self.middle, 100, hp, cd, dmg, acc, walk_speed, enemy_img, spell_img, shooter, coll)
        self.clock_phase = 0
        self.ult_dmg = dmg * 2
        self.all_summons_alive = False

    def phase_timer(self, delta):
        self.clock_phase += delta

    def summon(self, player, obj, how_much):
        for t in range(how_much):
            player.enemies.append(obj)

    def ult_pos(self):
        self.take_dmg = False
        if self.x_cord > self.middle:
            self.go_left()
        elif self.x_cord < self.middle:
            self.go_right()
        if self.y_cord >= 100:
            self.go_up()

####################################################################################################################
# Undeads


class Ghost(Enemy):
    def __init__(self, hp, cd, dmg, max_speed, x_self=0, y_self=0):
        x = randint(100, 1800)
        y = randint(100, 200)
        self.max_speed = randint(2, max_speed)
        Enemy.__init__(self, x, y, hp, cd, dmg, 0.5, self.max_speed, 'graph/enemy/lvl1/ghost', 'graph/spels/none_icon.png', False, False)
        self.gravity = 0.15

    def tick(self, walls, player, delta):
        self.physic_tick(walls)
        self.health_tick(delta)
        self.tick_mele(delta)
        self.attack_mele(player)  # attacl
        self.fx.ghost_sound(delta)

        if not self.hitbox.colliderect(player.hitbox):
            if self.y_cord > player.y_cord + 15:
                self.go_up()
            if self.x_cord > player.x_cord:
                self.go_left()
            elif self.x_cord < player.x_cord:
                self.go_right()


class Ghost_Shooter(Enemy):
    def __init__(self, hp, cd, dmg, max_speed, x_self=0, y_self=0):
        x = randint(100, 1800)
        y = randint(100, 200)
        self.max_speed = randint(2, max_speed)
        Enemy.__init__(self, x, y, hp, cd, dmg, 1, self.max_speed, 'graph/enemy/lvl1/shooter', 'graph/spels/spel_ghost', True, False)
        self.distance = 200
        self.min_dis = False
        self.gravity = 0.15


    def tick(self, walls, player, delta):
        self.physic_tick(walls)
        self.health_tick(delta)
        self.tick_shot(walls, self, delta, player)
        self.attack_dist(player)
        self.fx.ghost_sound(delta)

        if not self.hitbox.colliderect(player.hitbox):
            if self.y_cord + self.distance > player.y_cord + 15 and self.y_cord > 100:
                self.go_up()
            if self.x_cord + self.distance > player.x_cord:
                self.go_left()
            elif self.x_cord + self.distance < player.x_cord:
                self.go_right()


class Zombie_Tank(Enemy):
    def __init__(self, hp, cd, dmg, max_speed):
        self.zombie_image = 'graph/enemy/lvl1/zombie/zombie_stand'
        self.stand_right_img = pygame.image.load(f'{self.zombie_image}.png')  # normalna grafika
        self.stand_left_img = pygame.transform.flip(pygame.image.load(f'{self.zombie_image}.png'), True, False)
        self.walk_right_img = [pygame.image.load(f'graph/enemy/lvl1/zombie/zombie_walk_{x}.png') for x in range(1, 4)]  # animacja chodzenia
        self.walk_left_img = [pygame.transform.flip(pygame.image.load(f'graph/enemy/lvl1/zombie/zombie_walk_{x}.png'), True, False) for x in range(1, 4)]
        self.walk_index = 0
        self.direction = 0
        x = randint(100, 1800)
        self.max_speed = randint(1, max_speed)
        Enemy.__init__(self, x, 700, hp, cd, dmg, 0.6, self.max_speed, self.zombie_image)

    def tick(self, walls, player, delta):
        self.physic_tick(walls)
        self.health_tick(delta)
        self.tick_mele(delta)
        self.attack_mele(player)
        self.fx.zombie_sound(delta)

        if self.hor_velocity > 0:
            self.direction = 1
        elif self.hor_velocity < 0:
            self.direction = 0

        if not self.hitbox.colliderect(player.hitbox):
            if self.x_cord + self.distance > player.x_cord:
                self.go_left()
            elif self.x_cord + self.distance < player.x_cord:
                self.go_right()

    def draw(self, window):
        self.draw_hp(window, self.x_cord, self.y_cord - 15, self.width, 8)
        if self.hor_velocity != 0:
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


class Skeleton_Shooter(Enemy):
    def __init__(self, hp, cd, dmg, max_speed):
        self.skeleton_image = 'graph/enemy/lvl1/skeleton/skeleton_shooter_stand'
        self.stand_right_img = pygame.image.load(f'{self.skeleton_image}.png')  # normalna grafika
        self.stand_left_img = pygame.transform.flip(pygame.image.load(f'{self.skeleton_image}.png'), True, False)
        self.walk_right_img = [pygame.image.load(f'graph/enemy/lvl1/skeleton/skeleton_shooter_walk_{x}.png') for x in range(1, 4)]  # animacja chodzenia
        self.walk_left_img = [pygame.transform.flip(pygame.image.load(f'graph/enemy/lvl1/skeleton/skeleton_shooter_walk_{x}.png'), True, False) for x in range(1, 4)]
        self.walk_index = 0
        self.direction = 0
        self.distance = 400
        x = randint(100, 1800)
        y = randint(100, 200)
        self.max_speed = randint(4, max_speed)
        Enemy.__init__(self, x, y, hp, cd, dmg, 1, self.max_speed, self.skeleton_image, 'graph/spels/arrow', True)

    def tick(self, walls, player, delta):
        self.physic_tick(walls)
        self.health_tick(delta)
        self.tick_shot(walls, self, delta, player)
        self.attack_dist(player)
        self.fx.skeleton_sound(delta)

        if self.hor_velocity > 0:
            self.direction = 1
        elif self.hor_velocity < 0:
            self.direction = 0

        if not self.hitbox.colliderect(player.hitbox):
            if self.x_cord + self.distance > player.x_cord:
                self.go_left()
            elif self.x_cord + self.distance < player.x_cord:
                self.go_right()

            if self.y_cord > player.y_cord:
                self.jump()

    def draw(self, window):
        self.draw_hp(window, self.x_cord, self.y_cord - 15, self.width, 8)
        if self.hor_velocity != 0:
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

        for bullet in self.bullets:
            bullet.draw(window)


class Skeleton_Turrets(Enemy):
    def __init__(self, hp, cd, dmg):
        self.plant_image = 'graph/enemy/lvl1/skeleton_turret'
        self.stand_right_img = pygame.image.load(f'{self.plant_image}.png')
        self.stand_left_img = pygame.transform.flip(pygame.image.load(f'{self.plant_image}.png'), True, False)
        self.min_dis = False
        x = randint(100, 1800)
        y = randint(100, 200)

        Enemy.__init__(self, x, y, hp, cd, dmg, 1, 1, self.plant_image, 'graph/spels/arrow', True)

    def tick(self, walls, player, delta):
        self.physic_tick(walls)
        self.health_tick(delta)
        self.tick_shot(walls, self, delta, player)
        self.attack_dist(player)
        self.fx.skeleton_sound(delta)


class Lich(Boss):
    def __init__(self, hp, cd, dmg, max_speed, win):
        lich_image ='graph/enemy/lvl1/lich'
        # self, win, hp, cd, ult_dmg, acc, walk_speed, enemy_img, spell_img, shooter, coll
        Boss.__init__(self, win, hp, cd, dmg, 1, max_speed, lich_image, 'graph/spels/spel_lich', True, False)
        self.right_img = pygame.image.load(f'{lich_image}.png')  # normalna grafika
        self.left_img = pygame.transform.flip(pygame.image.load(f'{lich_image}.png'), True, False)
        self.distance = 0
        self.min_dis = False
        self.gravity = 0.05
        self.direction = 0
        self.phase_counter = 1
        self.pahase_pos = False



    def tick(self, walls, player, delta):

        self.physic_tick(walls)
        self.health_tick(delta)
        self.phase_timer(delta)
        self.tick_mele(delta)
        self.tick_shot(walls, self, delta, player)

#############################################################################################
        if self.phase_counter == 1 or self.phase_counter == 3 or self.phase_counter == 5:
            self.fx.lich_sound(delta)

            if abs(self.x_cord - player.x_cord) > 50 or abs(self.y_cord - player.y_cord) > 100:
                self.attack_dist(player)
            else:
                self.attack_mele(player, 10)

            if not self.hitbox.colliderect(player.hitbox):
                if self.y_cord + self.distance > player.y_cord + 15 and self.y_cord > 100:
                    self.go_up()
                if self.x_cord + self.distance > player.x_cord:
                    self.go_left()
                elif self.x_cord + self.distance < player.x_cord:
                    self.go_right()
#############################################################################################
        elif self.phase_counter == 2 or self.phase_counter == 4:
            self.ult_pos()

###############################################
            if self.y_cord <= 100 and not self.pahase_pos:
                #self.summon(player, Ghost_Shooter(50, 1.5, 10, 6), 3)
                for t in range(3):
                    player.enemies.append(Ghost_Shooter(50, 1.5, 10, 6))
                for e in player.enemies:
                    if not e == 0:
                        self.all_summons_alive = False
                        self.phase_counter = 3
                        self.take_dmg = True
                self.pahase_pos = True

                #self.summon(Ghost_Shooter, 2)
                #self.take_dmg = True
#############################################################################################
        if self.hp < self.max_hp * 0.7 and self.phase_counter == 1:
            print("hp 70")
            self.phase_counter = 2


#############################################################################################
        if self.hor_velocity > 0:
            self.direction = 1
        elif self.hor_velocity < 0:
            self.direction = 0


    def draw(self, window):
        self.draw_hp(window, self.x_cord, self.y_cord - 15, self.width, 8)
        if self.direction == 1:
            window.blit(self.right_img, (self.x_cord, self.y_cord))
        elif self.direction == 0:
            window.blit(self.left_img, (self.x_cord, self.y_cord))
        for bullet in self.bullets:
            bullet.draw(window)

####################################################################################################################
# Olimp


class Soldier_Ghost(Enemy):
    def __init__(self, hp, cd, dmg, max_speed, x_self=0, y_self=0):
        x = randint(100, 1800)
        y = randint(100, 200)
        self.max_speed = randint(2, max_speed)
        Enemy.__init__(self, x, y, hp, cd, dmg, 0.5, self.max_speed, 'graph/enemy/lvl2/soldier_ghost', 'graph/spels/none_icon', False, False)
        self.gravity = 0.1

    def tick(self, walls, player, delta):
        self.physic_tick(walls)
        self.health_tick(delta)
        self.attack_mele(player)  # attacl

        if not self.hitbox.colliderect(player.hitbox):
            if self.y_cord > player.y_cord + 15 or self.y_cord > 855 - self.height:
                self.go_up()
            if self.x_cord > player.x_cord:
                self.go_left()
            elif self.x_cord < player.x_cord:
                self.go_right()


class Soldier_Tank(Enemy):
    def __init__(self, hp, cd, dmg, max_speed):
        self.tank_image = 'graph/enemy/lvl2/soldier_anima/soldier_tank'
        self.stand_right_img = pygame.image.load(f'{self.tank_image}.png')  # normalna grafika
        self.stand_left_img = pygame.transform.flip(pygame.image.load(f'{self.tank_image}.png'), True, False)
        self.walk_right_img = [pygame.image.load(f'graph/enemy/lvl2/soldier_anima/soldier_tank_walk_{x}.png') for x in range(1, 4)]  # animacja chodzenia
        self.walk_left_img = [pygame.transform.flip(pygame.image.load(f'graph/enemy/lvl2/soldier_anima/soldier_tank_walk_{x}.png'), True, False) for x in range(1, 4)]


        self.walk_index = 0
        self.direction = 0
        x = randint(100, 1800)
        self.max_speed = randint(1, max_speed)
        Enemy.__init__(self, x, 700, hp, cd, dmg, 0.6, self.max_speed, self.tank_image)

    def tick(self, walls, player, delta):
        self.physic_tick(walls)
        self.health_tick(delta)
        self.attack_mele(player)

        if self.hor_velocity > 0:
            self.direction = 1
        elif self.hor_velocity < 0:
            self.direction = 0

        if not self.hitbox.colliderect(player.hitbox):
            if self.x_cord + self.distance > player.x_cord:
                self.go_left()
            elif self.x_cord + self.distance < player.x_cord:
                self.go_right()

    def draw(self, window):
        self.draw_hp(window, self.x_cord, self.y_cord - 15, self.width, 8)
        if self.hor_velocity != 0:
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


class Roman_Shaman(Enemy):
    def __init__(self, win, hp, cd, dmg, max_speed):
        self.win = win
        x = randint(100, 1800)
        y = randint(100, 200)
        self.max_speed = randint(2, max_speed)
        Enemy.__init__(self, x, y, hp, cd, dmg, 1, self.max_speed, 'graph/enemy/lvl2/roman_shaman/roman_shaman_1', 'graph/spels/spel_thunder', True)
        self.img = [pygame.image.load(f'graph/enemy/lvl2/roman_shaman/roman_shaman_{x}.png') for x in range(1, 7)]
        self.distance = 200
        self.min_dis = False
        self.walk_index = 0



    def tick(self, walls, player, delta):
        self.physic_tick(walls)
        self.health_tick(delta)
        self.tick_shot(walls, self, delta, player)
        self.attack_dist(player)
        #self.fx.ghost_sound(delta)

        if not self.hitbox.colliderect(player.hitbox):
            if self.x_cord + self.distance > player.x_cord:
                self.go_left()
            elif self.x_cord + self.distance < player.x_cord:
                self.go_right()

    def draw(self, window):
        self.draw_hp(window, self.x_cord, self.y_cord - 15, self.width, 8)
        window.blit(self.img[floor(self.walk_index)], (self.x_cord, self.y_cord))
        self.walk_index += 0.4
        if self.walk_index >= 6:
            self.walk_index = 0

        for bullet in self.bullets:
            bullet.draw(window)


class Zeus(Boss):
    def __init__(self, win, hp, cd, dmg, max_speed):
        self.win = win
        self.max_speed = randint(2, max_speed)
        Boss.__init__(self, win, hp, cd, dmg, 1, self.max_speed, 'graph/enemy/lvl2/zeus/zeus_1', 'graph/spels/spel_thunder', True, True)
        self.zeus_img = [pygame.image.load(f'graph/enemy/lvl2/zeus/zeus_{x}.png') for x in range(1, 6)]
        self.distance = 600
        self.min_dis = False
        self.gravity = 0.15
        self.walk_index = 0
        self.x_cord_u = 0
        self.clock_active = 0

    def ult_spell(self, player, delta, win, dmg):
        self.clock_active += delta
        if self.ult_activ and self.clock_active > 0.4:
            self.x_cord_u += 100
            win.blit(pygame.image.load('graph/spels/thunder_drop_down.png'), (self.x_cord_u, 0))
            if player.hitbox.colliderect(self.hitbox):
                player.dealt_dmg(dmg, 0)

            if self.x_cord_u >= 1920:
                self.ult_activ = False


    def tick(self, walls, player, delta):
        self.physic_tick(walls)
        self.health_tick(delta)
        self.tick_shot(walls, self, delta, player)
        self.attack_dist(player)
        if self.ult_cd_counter(delta, 5):
            self.ult_spell(player, delta, self.win, 50)
        self.fx.ghost_sound(delta)

        if not self.hitbox.colliderect(player.hitbox):
            if self.y_cord + self.distance > player.y_cord + 15 and self.y_cord > 100:
                self.go_up()
            if self.x_cord + self.distance > player.x_cord:
                self.go_left()
            elif self.x_cord + self.distance < player.x_cord:
                self.go_right()

    def draw(self, window):
        self.draw_hp(window, self.x_cord, self.y_cord - 15, self.width, 8)
        window.blit(self.zeus_img[floor(self.walk_index)], (self.x_cord, self.y_cord))
        self.walk_index += 0.4
        if self.walk_index >= 5:
            self.walk_index = 0

        for bullet in self.bullets:
            bullet.draw(window)

####################################################################################################################
# Hell

class Fire_Bug(Enemy):
    def __init__(self, hp, cd, dmg, max_speed):
        self.image = 'graph/enemy/lvl3/floor_bug/floor_bug'
        self.stand_img = pygame.image.load(f'{self.image}.png')  # normalna grafika
        self.walk_img = [pygame.image.load(f'graph/enemy/lvl3/floor_bug/floor_bug_{x}.png') for x in range(1, 5)]  # animacja chodzenia
        self.stand_angry_img = [pygame.image.load(f'graph/enemy/lvl3/floor_bug/floor_bug_angry_{x}.png') for x in range(1, 6)]
        self.shot_img = [pygame.image.load(f'graph/enemy/lvl3/floor_bug/shot/floor_bug_shot_{x}.png') for x in range(1, 6)]

        self.spell_lengh = 2
        self.burst = 1.5

        self.angry = False
        self.ult = False
        self.clock_angry = 0
        self.angry_cd = 5
        self.index = 0

        self.walk_index = 0
        self.direction = 0
        x = randint(100, 1800)
        self.max_speed = randint(1, max_speed)
        Enemy.__init__(self, x, 700, hp, cd, dmg, 0.6, self.max_speed, self.image)

    def tick(self, walls, player, delta):
        self.clock_angry += delta
        self.clock += delta

        self.physic_tick(walls)
        self.health_tick(delta)
        self.tick_mele(delta)
        self.attack_mele(player)

        if self.hor_velocity > 0:
            self.direction = 1
        elif self.hor_velocity < 0:
            self.direction = 0

        if not self.hitbox.colliderect(player.hitbox):
            if self.x_cord + self.distance > player.x_cord - 20:
                self.go_left()
            elif self.x_cord + self.distance < player.x_cord - 20:
                self.go_right()

        if self.y_cord + self.height > player.y_cord + player.height and self.x_cord + 30 >= player.x_cord >= self.x_cord - 10:
            if self.clock_angry >= self.angry_cd and not self.angry:
                self.angry = True
                self.clock_angry = 0
        else:
            self.angry = False

        if self.angry:
            if self.clock_angry > 3:
                self.ult = True
                if pygame.Rect(self.x_cord, self.y_cord - self.shot_img[0].get_height() + 20, self.shot_img[0].get_width(), self.shot_img[0].get_height()).colliderect(player.hitbox):
                    if self.clock >= 0.5:
                        player.dealt_dmg(floor(self.dmg * self.burst))
                        self.clock = 0
                if self.clock_angry - 3 >= self.spell_lengh or not player.alive:
                    self.angry = False
                    self.ult = False
                    self.clock_angry = 0

    def draw(self, window):
        self.draw_hp(window, self.x_cord, self.y_cord - 15, self.width, 8)
        if not self.angry:
            self.walk_index += 0.4
            if self.walk_index > 4:
                self.walk_index = 0
            if self.hor_velocity != 0:
                window.blit(self.walk_img[floor(self.walk_index)], (self.x_cord, self.y_cord))
            else:
                window.blit(self.stand_img, (self.x_cord, self.y_cord))
        else:
            self.index += 0.4
            if self.index > 5:
                self.index = 0
            window.blit(self.stand_angry_img[floor(self.index)], (self.x_cord, self.y_cord))
            if self.ult:
                window.blit(self.shot_img[floor(self.index)], (self.x_cord + 30, self.y_cord - self.shot_img[0].get_height() + 20))


class Fire_Bee(Enemy):
    def __init__(self, hp, cd, dmg, max_speed):
        self.fly_right_img = [pygame.image.load(f'graph/enemy/lvl3/bee/bee_{x}.png') for x in range(1, 4)]  # animacja chodzenia
        self.fly_left_img = [pygame.transform.flip(pygame.image.load(f'graph/enemy/lvl3/bee/bee_{x}.png'), True, False) for x in range(1, 4)]
        self.angry_right = pygame.image.load('graph/enemy/lvl3/bee/bee_angry.png')
        self.angry_left = pygame.transform.flip(pygame.image.load('graph/enemy/lvl3/bee/bee_angry.png'), True, False)

        x = randint(100, 1800)
        y = randint(700, 750)

        Enemy.__init__(self, x, y, hp, cd, dmg, 0.5, max_speed, 'graph/enemy/lvl3/bee/bee_1')
        self.gravity = 0.15

        self.move_side = 0
        self.clock_move = 0
        self.angry = False
        self.direction = 0
        self.index = 0

        self.change_move_time = 5

    def tick(self, walls, player, delta):
        self.clock_move += delta
        self.physic_tick(walls)
        self.health_tick(delta)

        if self.clock_move >= self.change_move_time:
            self.move_side = randint(0, 3)

        if self.hor_velocity > 0:
            self.direction = 1
        elif self.hor_velocity < 0:
            self.direction = 0

        if self.move_side == 0:
            if self.y_cord >= 750:
                self.move_side = 1
                #self.clock_move = 0
        elif self.move_side == 1:
            self.go_up()
            if self.y_cord <= 10:
                self.move_side = 0
                #self.clock_move = 0
        elif self.move_side == 2:
            self.go_left()
            if self.x_cord < 10:
                self.move_side = 3
                #self.clock_move = 0
        elif self.move_side == 3:
            self.go_right()
            if self.x_cord >= 1880:
                self.move_side = 2
                #self.clock_move = 0

        if self.hp < self.max_hp:
            self.angry = True

    def draw(self, window):
        if self.hor_velocity != 0:
            if self.direction == 1:
                window.blit(self.fly_right_img[floor(self.index)], (self.x_cord, self.y_cord))
            elif self.direction == 0:
                window.blit(self.fly_left_img[floor(self.index)], (self.x_cord, self.y_cord))
            self.index += 0.4
            if self.index > 3:
                self.index = 0

####################################################################################################################
# Plants


class Plant_Turrets(Enemy):
    def __init__(self, floors, hp, cd, dmg):
        self.plant_image = 'graph/enemy/plant_turret'
        self.stand_right_img = pygame.image.load(f'{self.plant_image}.png')
        self.stand_left_img = pygame.transform.flip(pygame.image.load(f'{self.plant_image}.png'), True, False)
        self.min_dis = False
        self.floors = floors
        x = randint(100, 1800)
        floors_random = randint(1, len(floors)-1)

        Enemy.__init__(self, x, floors[floors_random] + 50, hp, cd, dmg, 1, 1, self.plant_image, 'graph/spels/spel_plant', True)

    def tick(self, walls, player, delta):
        self.physic_tick(walls)
        self.health_tick(delta)
        self.tick_shot(walls, self, delta, player)
        self.attack_dist(player)
