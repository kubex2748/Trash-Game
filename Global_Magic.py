import pygame
from math import floor
from Sound_Controller import FX
from math import floor
from GUI import GUI
from Informations import Links
from Attack import Magic
from Physic import Physic
from Enemy import Enemy


class Global_Magic:
    def __init__(self, player, window, cd, dmg, mana_req, spell_id):
        self.gui = GUI(window)
        self.fx = FX()

        self.ID = spell_id
        self.win = window
        self.player = player
        links = Links()

        self.img_list = links.global_set
        self.spells_s = links.spells
        self.img = pygame.image.load(f'{self.img_list[0]}.png')


        #print(f'img_list : {self.img_list[spell_id]}')
        #print(f'spell_id : {spell_id}')
        try:
            if spell_id == 0:
                pass
            elif spell_id == 3:
                self.img = pygame.image.load(f'{self.img_list[spell_id]}3.png')
            else:
                self.img = pygame.image.load(f'{self.img_list[spell_id]}.png')
        except FileNotFoundError:
            print(f'LOG: Global_Magic/Global_Magic: Grafic for : Global_Magic with ID: {spell_id} not found ')
        self.width, self.height = self.img.get_size()

        self.cd = cd
        self.dmg = dmg
        self.req = mana_req

        self.spell_activ = False
        self.clock = 0
        self.cd_count = False

    def cd_counter(self):
        if self.cd_count:
            self.gui.draw_global_cd(floor(self.cd - self.clock + 1))
            if self.clock >= self.cd:
                self.cd_count = False

class Summons_Shooter(Enemy):
    def __init__(self, x_self, y_self, hp, cd, dmg, max_speed):

        self.max_speed = max_speed
        Enemy.__init__(self, x_self, y_self, hp, cd, dmg, 0.5, self.max_speed, 'graph/enemy/lvl1/ghost', 'graph/spels/none_icon.png', False, False)
        self.gravity = 0.15

    def tick(walls, self, enemies, delta):
        self.physic_tick(walls)
        self.health_tick(delta)
        self.fx.ghost_sound(delta)

        if not self.hitbox.colliderect(player.hitbox):
            if self.y_cord > player.y_cord + 15:
                self.go_up()
            if self.x_cord > player.x_cord:
                self.go_left()
            elif self.x_cord < player.x_cord:
                self.go_right()

        for e in enemies:
            dx = e.x_cord - self.x_cord
            dy = e.y_cord - self.y_cord
            dist2 = dx*dx + dy*dy
            if dist2 < nearest_dist:
                nearest_dist = dist2
                nearest = e
                x_side, y_side = dx, dy

        self.tick_shot(walls, self, delta, nearest)
        # strzelaj co 'fire_rate' sekund
        if nearest:
            self.attack_dist(nearest)
            #self.shoot(x_side, y_side)


class Summon_Ghost(Global_Magic, Physic):
    def __init__(self, player, window, cd, dmg, mana_req, spell_id):
        Global_Magic.__init__(self, player, window, cd, dmg, mana_req, spell_id)

        self.x_cord = 0
        self.y_cord = 0

        self.nearest_x = 0
        self.nearest_y = 0

        self.bullets = []  # lista pocisków Magic
        self.spell_img = 'graph/spels/spel_plant'

        self.speed = 15             # bullets speed
        self.fire_rate = 1          # attack speed
        self.lifetime = 30          # lifetime

        self.alive_time = 0         # ile już działa
        self.cooldown = 0.0         # timer do kolejnego strzału

        self.max_dis = 5

    def spell_it(self):
        if self.player.current_mana >= self.req and not self.cd_count:
            if not self.spell_activ:
                self.x_cord = self.player.x_cord
                self.y_cord = self.player.y_cord
                self.clock = 0
                self.spell_activ = True
                self.player.current_mana -= self.req

    def tick(self, delta, enemies, walls):
        pass


    def draw(self):
        self.win.blit(self.img, (self.x_cord, self.y_cord))
        for bullet in self.bullets:
            bullet.draw(self.win)

class Poison_Hit(Global_Magic):
    def __init__(self, player, window, cd, dmg, mana_req, spell_id):
        Global_Magic.__init__(self, player, window, cd, dmg, mana_req, spell_id)
        self.poison_hit = 10
        self.pause = 1

        self.hit = 0

    def spell_it(self):
        if self.player.current_mana >= self.req and not self.cd_count:
            if not self.spell_activ:
                self.spell_activ = True
                self.clock = 0
                self.player.current_mana -= self.req

    def tick(self, delta, enemies, walls):
        self.clock += delta
        self.cd_counter()
        if self.spell_activ and self.clock >= self.pause:
            self.clock = 0
            self.hit += 1
            for e in enemies:
                e.dealt_dmg(self.dmg)
        if self.hit >= self.poison_hit:
            self.spell_activ = False
            self.clock = 0
            self.cd_count = True


class Thunder_Bolt(Global_Magic):
    def __init__(self, player, window, cd, dmg, mana_req, spell_id):
        Global_Magic.__init__(self, player, window, cd, dmg, mana_req, spell_id)
        self.x_cord = 0             # spell x start
        self.pause = 0.05            # time pause between thunders
        self.width_pause = 100      # distance between thunders

    def spell_it(self):
        if self.player.current_mana >= self.req and not self.cd_count:
            if not self.spell_activ:
                self.spell_activ = True
                self.clock = 0
                self.x_cord = 0
                self.player.current_mana -= self.req

    def tick(self, delta, enemies, walls):
        self.clock += delta
        self.cd_counter()
        if self.spell_activ:
            hitbox = pygame.Rect(self.x_cord, 0, self.width, self.height)
            if self.x_cord < 1920:
                if self.clock >= self.pause:
                    self.x_cord += self.width_pause
                    self.fx.global_spel_sounds(2)
                    self.draw()
                    for enemy in enemies:
                        if enemy.hitbox.colliderect(hitbox):
                            enemy.dealt_dmg(self.dmg)
                    self.clock = 0
            else:
                self.spell_activ = False
                self.clock = 0
                self.cd_count = True

    def draw(self):
        self.win.blit(self.img, (self.x_cord, 0))


class Explosion(Global_Magic):
    def __init__(self, player, window, cd, dmg, mana_req, spell_id):
        Global_Magic.__init__(self, player, window, cd, dmg, mana_req, spell_id)
        self.x_cord = 0
        self.y_cord = 0
        self.hitbox = pygame.Rect(0, 0, 1, 1)


    def spell_it(self):
        if self.player.current_mana >= self.req and not self.cd_count:
            if not self.spell_activ:
                self.spell_activ = True
                self.clock = 0
                self.x_cord = self.player.x_cord
                self.y_cord = self.player.y_cord
                self.player.current_mana -= self.req


    def tick(self, delta, enemies, walls):
        self.clock += delta
        self.cd_counter()
        if self.spell_activ:
            if self.clock < 0.05:
                self.draw(1)
            elif self.clock < 0.09 and self.clock > 0.05:
                self.draw(2)
            elif self.clock < 0.2 and self.clock > 0.09:
                self.draw(3)
            elif self.clock >= 0.2:
                self.spell_activ = False
                self.clock = 0
                self.cd_count = True

            for enemy in enemies:
                if enemy.hitbox.colliderect(self.hitbox):
                    enemy.dealt_dmg(self.dmg)

    def draw(self, slide):
        img = pygame.image.load(f'{self.img_list[self.ID]}{floor(slide)}.png')
        x = self.player.x_cord + self.player.width
        y = self.player.y_cord + self.player.height
        self.hitbox = pygame.Rect(x - img.get_width(), y - img.get_height(), img.get_width(), img.get_height())
        self.win.blit(img, (x - img.get_width() + 70 * slide, y - img.get_height() + 60 * slide))


class Good_Helper(Global_Magic):
    def __init__(self, player, window, cd, dmg, mana_req, spell_id):
        Global_Magic.__init__(self, player, window, cd, dmg, mana_req, spell_id)

        self.x_cord = 0
        self.y_cord = 0

        self.nearest_dx = 0
        self.nearest_dy = 0

        self.bullets = []  # lista pocisków Magic
        self.spell_img = 'graph/spels/spel_plant'

        self.speed = 15             # bullets speed
        self.fire_rate = 1          # attack speed
        self.lifetime = 30          # lifetime

        self.alive_time = 0         # ile już działa
        self.cooldown = 0.0         # timer do kolejnego strzału

    def spell_it(self):
        if self.player.current_mana >= self.req and not self.cd_count:
            if not self.spell_activ:
                self.x_cord = self.player.x_cord
                self.y_cord = self.player.y_cord
                self.clock = 0
                self.spell_activ = True
                self.player.current_mana -= self.req

    def tick(self, delta, enemies, walls):
        self.clock += delta
        self.cooldown = max(0.0, self.cooldown - delta)
        self.cd_counter()
        if self.spell_activ:
            self.draw()
            if self.clock >= self.lifetime:
                self.spell_activ = False
                self.clock = 0
                self.cd_count = True

            nearest = None
            nearest_dist = float('inf')
            x_side = y_side = 0

            for e in enemies:
                dx = e.x_cord - self.x_cord
                dy = e.y_cord - self.y_cord
                dist2 = dx*dx + dy*dy
                if dist2 < nearest_dist:
                    nearest_dist = dist2
                    nearest = e
                    x_side, y_side = dx, dy

            # strzelaj co 'fire_rate' sekund
            if nearest and self.cooldown <= 0.0:
                self.shoot(x_side, y_side)
                self.cooldown = self.fire_rate

            # aktualizuj pociski
            for bullet in self.bullets[:]:
                bullet.tick(walls, delta, enemies)
                if not bullet.exists:
                    self.bullets.remove(bullet)

    def shoot(self, x_side, y_side):
        self.bullets.append(Magic(self, self.speed, self.dmg, x_side, y_side, self.spell_img))

    def draw(self):
        self.win.blit(self.img, (self.x_cord, self.y_cord))
        for bullet in self.bullets:
            bullet.draw(self.win)


class Ice_Slow(Global_Magic):
    def __init__(self, player, window, cd, dmg, mana_req, spell_id):
        Global_Magic.__init__(self, player, window, cd, dmg, mana_req, spell_id)
        self.lenght = 5
        self.slow = 1      # 0.3 = 30 %


    def spell_it(self):
        if self.player.current_mana >= self.req and not self.cd_count:
            if not self.spell_activ:
                self.clock = 0
                self.spell_activ = True
                self.player.current_mana -= self.req

    def tick(self, delta, enemies, walls):
        self.clock += delta
        self.cd_counter()
        if self.spell_activ:
            for e in enemies:
                e.set_max_vel(True, self.slow)

            if self.clock >= self.lenght:
                for e in enemies:
                    e.set_max_vel(False, self.slow)

                self.spell_activ = False
                self.clock = 0
                self.cd_count = True

    def draw(self):
        pass


class Meteor(Global_Magic):
    def __init__(self, player, window, cd, dmg, mana_req, spell_id):
        Global_Magic.__init__(self, player, window, cd, dmg, mana_req, spell_id)

    def spell_it(self):
        pass

    def tick(self, delta, enemies, walls):
        pass


class Hammer_Jump(Global_Magic):
    def __init__(self, player, window, cd, dmg, mana_req, spell_id):
        Global_Magic.__init__(self, player, window, cd, dmg, mana_req, spell_id)
        self.player = player
        self.player_high = 0

        self.jump_speed = 15
        self.jump_stop = 10

    def spell_it(self):
        if self.player.current_mana >= self.req and not self.cd_count:
            if not self.spell_activ:
                self.spell_activ = True
                self.player_high = self.player.y_cord
                self.player.ver_velocity -= self.jump_speed
                self.player.is_coll = False

    def tick(self, delta, enemies, walls):
        self.clock += delta
        self.cd_counter()
        if self.spell_activ:
            if self.player.y_cord >= self.jump_stop:
                self.player.ver_velocity = 0
            elif self.player.y_cord <= self.player_high + 10:
                self.player.is_coll = True
                self.spell_activ = False
                self.clock = 0
                self.cd_count = True


