from random import randint

import pygame
#import json
from math import floor

from Sound_Controller import FX
from Player import Player
from Wall import Wall
from Drops import HP_Potion, Mana_Potion, Coin
from Menu import Button
from GUI import GUI
from Informations import Stats, Waves_Tab, Walls_Position

from Enemy import \
    Ghost, Ghost_Shooter, Zombie_Tank, Lich, Skeleton_Turrets, Skeleton_Shooter, \
    Soldier_Ghost, Soldier_Tank, Roman_Shaman, Zeus, \
    Fire_Bug, Fire_Bee

window = pygame.display.set_mode(
    (0, 0),
    pygame.NOFRAME
)
pygame.init()
pygame.display.set_icon(pygame.image.load('graph/menu/logo.png'))
pygame.display.set_caption('TrashGame')


class Levels:
    def __init__(self, wand_id, FX_active, maps, stand_spells, player_lvl):
        """----OBJECTS----"""
        self.gui = GUI(window)
        self.wave_tab = Waves_Tab(maps)
        self.wall_pos = Walls_Position(maps)
        self.stats = Stats()
        """----FONTS----"""
        self.arial_42 = pygame.font.SysFont("arial", 42)
        self.arial_72 = pygame.font.SysFont("arial", 72)
        self.arial_48 = pygame.font.SysFont("arial", 48)

        """----GAME----"""
        self.background = pygame.image.load("graph/spels/None.png")
        self.run = True
        self.win = False
        self.clock_obj = pygame.time.Clock()
        self.fps = 0
        self.fps_text = pygame.font.Font.render(pygame.font.SysFont("arial", 42), 'FPS: ', True, (0, 0, 0))
        self.score = 0.0
        self.enemies = []
        self.death_animation_img = [pygame.image.load(f'graph/game/death/death_{x}.png') for x in range(1, 10)]
        self.wave_itterator = 0
        self.waves = self.wave_tab.tab
        self.wand_id = wand_id
        self.walls = []
        self.bonus_mana = 20
        self.admin_mod = False
        if player_lvl == 0:
            self.admin_mod = True

        '''----DROPS----'''
        self.clock_drops = 0
        self.drop_time = 10
        self.drops = []

        '''----SPELLS----'''
        self.spells = stand_spells
        #self.spells = [0, 1, 2]

        """----PLAYER----"""
        self.player = Player(
            window,
            self.stats.player[player_lvl][0],
            self.stats.player[player_lvl][1],
            self.stats.player[player_lvl][2],
            self.stats.player[player_lvl][3],
            self.stats.player[player_lvl][4],
            self.stats.player[player_lvl][5],
            self.stats.player[player_lvl][6],
            self.wand_id,
            stand_spells
        )
        #print(f'stand_spells in Levels: {stand_spells}')

        """----TIME----"""
        self.timer_on = True
        self.clock = 0
        self.second = 0
        self.minute = 0
        self.seconds_text = pygame.font.Font.render(pygame.font.SysFont("arial", 72), '', True, (0, 0, 0))

        """----BREAK----"""
        self.gameover_img = pygame.image.load('graph/menu/win.png')
        self.pause_image = pygame.image.load("graph/menu/pause_menu.png")
        self.RESUME_button = Button(950, 300, "graph/menu/buttons/button_RESUME")
        self.EXIT_button = Button(950, 700, "graph/menu/buttons/button_EXIT")
        self.pause = False

        """----OPENING----"""
        fx = FX(FX_active)
        fx.open_wave_sound()

    """----SCORE----"""
    def game(self):
        if self.admin_mod:
            self.fps_text = pygame.font.Font.render(self.arial_42, f'FPS: {floor(self.clock_obj.get_fps())}', True, (0, 0, 0))
            window.blit(self.fps_text, (1750, 10))
        window.blit(pygame.font.Font.render(self.arial_42, f'COINS: {self.player.coins}', True, (0, 0, 0)), (10, 10))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # jeśli gracz zamknie okienko
                self.run = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.timer_on = not self.timer_on
                self.pause = not self.pause
        self.gui.draw_GUI()
        self.gui.draw_standards_spell(self.spells)

    def drop_tick(self, delta):
        self.clock_drops += delta
        if self.clock_drops >= self.drop_time:
            if randint(0, 4) == 0:
                self.drops.append(Mana_Potion(window, 30))
            else:
                self.drops.append(HP_Potion(window, 30))
            self.clock_drops = 0
        for d in self.drops:
            if d.tick(self.player, self.walls):
                self.drops.remove(d)
            d.draw()

    def enemy_tick(self, delta, enemies, player, walls):
        for enemy in enemies:
            enemy.tick(walls, player, delta)
        for enemy in enemies:
            enemy.draw(window)
        for enemy in enemies:
            if not enemy.alive:
                x, y = enemy.x_cord, enemy.y_cord - 50
                self.drops.append(Coin(window, x, y))
                if player.current_mana < player.max_mana and player.current_mana + self.bonus_mana < player.max_mana:
                    player.current_mana += self.bonus_mana
                enemies.remove(enemy)
                self.death_animation(window, x, y)
            if len(enemies) == 0:
                self.wave_itterator += 1

    def timer(self, delta):
        self.second += delta
        if self.second < 10 and self.minute <= 0:
            self.seconds_text = pygame.font.Font.render(self.arial_72, f'{self.minute}:0{floor(self.second)}', True, (0, 0, 0))
        elif self.second < 60 and self.minute <= 0:
            self.seconds_text = pygame.font.Font.render(self.arial_72, f'{self.minute}:{floor(self.second)}', True, (0, 0, 0))
        elif self.second < 10 and self.minute > 0:
            self.seconds_text = pygame.font.Font.render(self.arial_72, f'{self.minute}:0{floor(self.second)}', True, (0, 0, 0))
        elif self.second < 60 and self.minute > 0:
            self.seconds_text = pygame.font.Font.render(self.arial_72, f'{self.minute}:{floor(self.second)}', True, (0, 0, 0))
        window.blit(self.seconds_text, (945, 15))
        if self.second >= 60:
            self.second = 0
            self.minute += 1

    def def_pause(self, delta):
        self.player.controll_active = False
        self.timer_on = False

        if self.RESUME_button.tick(delta):
            self.player.controll_active = True
            self.pause = not self.pause

        if self.EXIT_button.tick(delta):
            self.run = False

        window.blit(self.pause_image, (800, 200))
        self.RESUME_button.draw(window)
        self.EXIT_button.draw(window)
        pygame.display.update()

    def game_over(self, delta, is_win):
        if is_win:
            self.win = True
        window.blit(pygame.image.load('graph/menu/win.png'), (800, 200))
        self.player.controll_active = False
        self.timer_on = False
        mobs, boss = self.calc_monsters()
        window.blit(self.gameover_img, (800, 200))
        window.blit(pygame.font.Font.render(self.arial_48, "Score:", True, (0, 0, 0)), (930, 280))
        window.blit(pygame.font.Font.render(self.arial_72, f"{self.calc_score(self.player)}", True, (0, 0, 0)), (930, 330))
        window.blit(pygame.font.Font.render(self.arial_48, f"HP       :  {floor(self.player.hp / self.player.max_hp * 100)}%", True, (0, 0, 0)), (890, 420))
        window.blit(pygame.font.Font.render(self.arial_48, f"SPELL :  {self.player.score_sum - 1}", True, (0, 0, 0)), (890, 470))
        window.blit(pygame.font.Font.render(self.arial_48, f"MOBS :  {mobs}", True, (0, 0, 0)), (890, 520))
        window.blit(pygame.font.Font.render(self.arial_48, f"BOSS  :  {boss}", True, (0, 0, 0)), (890, 570))
        self.EXIT_button.draw(window)
        if self.EXIT_button.tick(delta):
            self.run = False

    def get_win(self):
        return self.win

    def set_spell(self, which, what):
        self.spells[which] = what

    def death_animation(self, win, x, y):
        for index in range(1, 270):
            win.blit(self.death_animation_img[floor(index / 30)], (x, y))

    def calc_monsters(self):
        mobs = 0
        boss = 0
        for i in range(len(self.waves)):
            for j in range(len(self.waves[0])):
                if j == len(self.waves[0]):
                    boss += self.waves[i][j]
                else:
                    mobs += self.waves[i][j]
        return mobs, boss

    def calc_score(self, player):
        mobs, boss = self.calc_monsters()
        erg = 0
        hp_score = player.hp / player.max_hp + 1
        if player.score_sum > 0:
            erg = floor((mobs + boss * 2) / (player.score_sum) * (hp_score + 0.01) * 1000)
        else:
            erg = 0
        return erg


class LVL1(Levels):
    def __init__(self, wand_id, FX_active, spell_ids, player_lvl):

        map_lvl = 1
        ''''''
        Levels.__init__(self, wand_id, FX_active, 1, spell_ids, player_lvl)
        self.background = pygame.image.load(f'graph/background/map_{map_lvl}.png')
        for w in range(0, len(self.wall_pos.tab)):
            color = (self.wall_pos.tab[w][4], self.wall_pos.tab[w][5], self.wall_pos.tab[w][6])
            self.walls.append(Wall(
                self.wall_pos.tab[w][0],
                self.wall_pos.tab[w][1],
                self.wall_pos.tab[w][2],
                self.wall_pos.tab[w][3],
                color
            ))

    """----WAVE SPAWN----"""
    '''i will automating it someday'''
    def spawn_wave(self, wave):
        if wave < len(self.waves):
            if not self.waves[wave][0] == 0:
                if self.waves[wave][0] > 1:  # ghost
                    for enemy in range(self.waves[wave][0]):
                        self.enemies.append(Ghost(
                            self.wave_tab.mob_stats[0][0],
                            self.wave_tab.mob_stats[0][1],
                            self.wave_tab.mob_stats[0][2],
                            self.wave_tab.mob_stats[0][3],
                        ))
                else:
                    self.enemies.append(Ghost(
                        self.wave_tab.mob_stats[0][0],
                        self.wave_tab.mob_stats[0][1],
                        self.wave_tab.mob_stats[0][2],
                        self.wave_tab.mob_stats[0][3],
                    ))
            if not self.waves[wave][1] == 0:  # shooter
                if self.waves[wave][1] > 1:
                    for enemy in range(self.waves[wave][1]):
                        self.enemies.append(Ghost_Shooter(
                            self.wave_tab.mob_stats[1][0],
                            self.wave_tab.mob_stats[1][1],
                            self.wave_tab.mob_stats[1][2],
                            self.wave_tab.mob_stats[1][3],
                        ))
                else:
                    self.enemies.append(Ghost_Shooter(
                        self.wave_tab.mob_stats[1][0],
                        self.wave_tab.mob_stats[1][1],
                        self.wave_tab.mob_stats[1][2],
                        self.wave_tab.mob_stats[1][3],
                    ))
            if not self.waves[wave][2] == 0:  # tank
                if self.waves[wave][2] > 1:
                    for enemy in range(self.waves[wave][2]):
                        self.enemies.append(Zombie_Tank(
                            self.wave_tab.mob_stats[2][0],
                            self.wave_tab.mob_stats[2][1],
                            self.wave_tab.mob_stats[2][2],
                            self.wave_tab.mob_stats[2][3],
                        ))
                else:
                    self.enemies.append(Zombie_Tank(
                        self.wave_tab.mob_stats[2][0],
                        self.wave_tab.mob_stats[2][1],
                        self.wave_tab.mob_stats[2][2],
                        self.wave_tab.mob_stats[2][3],
                    ))
            if not self.waves[wave][3] == 0:  # turret
                if self.waves[wave][3] > 1:
                    for enemy in range(self.waves[wave][3]):
                        self.enemies.append(Skeleton_Turrets(
                            self.wave_tab.mob_stats[3][0],
                            self.wave_tab.mob_stats[3][1],
                            self.wave_tab.mob_stats[3][2],
                        ))
                else:
                    self.enemies.append(Skeleton_Turrets(
                        self.wave_tab.mob_stats[3][0],
                        self.wave_tab.mob_stats[3][1],
                        self.wave_tab.mob_stats[3][2],
                    ))
            if not self.waves[wave][4] == 0:  # skeleton
                if self.waves[wave][4] > 1:
                    for enemy in range(self.waves[wave][4]):
                        self.enemies.append(Skeleton_Shooter(
                            self.wave_tab.mob_stats[4][0],
                            self.wave_tab.mob_stats[4][1],
                            self.wave_tab.mob_stats[4][2],
                            self.wave_tab.mob_stats[4][3],
                        ))
                else:
                    self.enemies.append(Skeleton_Shooter(
                            self.wave_tab.mob_stats[4][0],
                            self.wave_tab.mob_stats[4][1],
                            self.wave_tab.mob_stats[4][2],
                            self.wave_tab.mob_stats[4][3],
                    ))
            if not self.waves[wave][5] == 0:
                if self.waves[wave][5] > 1:
                    for enemy in range(self.waves[wave][5]):
                        self.enemies.append(Lich(
                            self.wave_tab.mob_stats[5][0],
                            self.wave_tab.mob_stats[5][1],
                            self.wave_tab.mob_stats[5][2],
                            self.wave_tab.mob_stats[5][3],
                            window
                        ))
                else:
                    self.enemies.append(Lich(
                            self.wave_tab.mob_stats[5][0],
                            self.wave_tab.mob_stats[5][1],
                            self.wave_tab.mob_stats[5][2],
                            self.wave_tab.mob_stats[5][3],
                            window
                    ))

            for e in self.enemies:
                print(e)

    def start(self):
        while self.run:
            """----GAME----"""
            window.blit(self.background, (0, 0))        # background
            keys = pygame.key.get_pressed()             # keyboard events
            delta = self.clock_obj.tick(60) / 1000      # 120 fps
            self.clock += delta
            self.game()                                 # other game functions

            """----PAUSE----"""
            if self.pause:
                self.def_pause(delta)
                continue

            """----TIME----"""
            if self.timer_on:
                self.timer(delta)

            """----WALL SPAWN----"""
            for wall in self.walls:
                wall.draw(window)

            """----WAVE SPAWN----"""
            if len(self.enemies) == 0:
                self.spawn_wave(self.wave_itterator)

            """----ENEMIES----"""
            self.enemy_tick(delta, self.enemies, self.player, self.walls)

            """----DROPS----"""
            self.drop_tick(delta)

            """----PLAYER----"""
            self.player.tick(keys, self.walls, delta, self.enemies)
            self.player.draw(window)

            """----WIN----"""
            if self.wave_itterator >= len(self.waves):
                self.game_over(delta, True)

            """----LOSE----"""
            if not self.player.alive:
                self.game_over(delta, False)

            pygame.display.update()


class LVL2(Levels):
    def __init__(self, wand_id, FX_active, spell_ids, player_lvl):

        map_lvl = 2
        ''''''
        Levels.__init__(self, wand_id, FX_active, map_lvl, spell_ids, player_lvl)
        self.background = pygame.image.load(f'graph/background/map_{map_lvl}.png')
        for w in range(0, len(self.wall_pos.tab)):
            color = (self.wall_pos.tab[w][4], self.wall_pos.tab[w][5], self.wall_pos.tab[w][6])
            self.walls.append(Wall(
                self.wall_pos.tab[w][0],
                self.wall_pos.tab[w][1],
                self.wall_pos.tab[w][2],
                self.wall_pos.tab[w][3],
                color
            ))

    """----WAVE SPAWN----"""
    def spawn_wave(self, wave):
        if wave < len(self.waves):
            '''-----Soldier_Ghost-----'''
            if not self.waves[wave][0] == 0:
                if self.waves[wave][0] > 1:
                    for enemy in range(self.waves[wave][0]):
                        self.enemies.append(Soldier_Ghost(100, 0.5, 5, 4))
                else:
                    self.enemies.append(Soldier_Ghost(100, 0.5, 5, 4))

            '''-----Soldier_Tank-----'''
            if not self.waves[wave][1] == 0:
                if self.waves[wave][1] > 1:
                    for enemy in range(self.waves[wave][1]):
                        self.enemies.append(Soldier_Tank(300, 1.5, 5, 2))
                else:
                    self.enemies.append(Soldier_Tank(300, 1.5, 5, 2))
            '''-----Roman_Shaman-----'''
            if not self.waves[wave][2] == 0:
                if self.waves[wave][2] > 1:
                    for enemy in range(self.waves[wave][2]):
                        self.enemies.append(Roman_Shaman(window, 200, 1, 20, 2))
                else:
                    self.enemies.append(Roman_Shaman(window, 200, 1, 20, 2))

            '''-----Zeus-----'''
            if not self.waves[wave][3] == 0:
                if self.waves[wave][3] > 1:
                    for enemy in range(self.waves[wave][3]):
                        self.enemies.append(Zeus(window, 700, 1.5, 100, 2))
                else:
                    self.enemies.append(Zeus(window, 700, 1.5, 100, 2))
            for e in self.enemies:
                print(e)

    def start(self):
        while self.run:
            """----GAME----"""
            window.blit(self.background, (0, 0))  # background
            keys = pygame.key.get_pressed()  # keyboard events
            delta = self.clock_obj.tick(60) / 1000  # 120 fps
            self.clock += delta
            self.game()  # other game functions

            """----PAUSE----"""
            if self.pause:
                self.def_pause(delta)
                continue

            """----TIME----"""
            if self.timer_on:
                self.timer(delta)

            """----WALL SPAWN----"""
            for wall in self.walls:
                wall.draw(window)

            """----WAVE SPAWN----"""
            if len(self.enemies) == 0:
                self.spawn_wave(self.wave_itterator)

            """----ENEMIES----"""
            self.enemy_tick(delta, self.enemies, self.player, self.walls)

            """----DROPS----"""
            self.drop_tick(delta)

            """----PLAYER----"""
            self.player.tick(keys, self.walls, delta, self.enemies)
            self.player.draw(window)

            """----WIN----"""
            if self.wave_itterator >= len(self.waves):
                self.game_over(delta, True)

            """----LOSE----"""
            if not self.player.alive:
                self.game_over(delta, False)

            pygame.display.update()


class LVL3(Levels):
    def __init__(self, wand_id, FX_active, spell_ids, player_lvl):

        map_lvl = 3
        ''''''
        Levels.__init__(self, wand_id, FX_active, map_lvl, spell_ids, player_lvl)
        self.background = pygame.image.load(f'graph/background/map_{map_lvl}.png')
        for w in range(0, len(self.wall_pos.tab)):
            color = (self.wall_pos.tab[w][4], self.wall_pos.tab[w][5], self.wall_pos.tab[w][6])
            self.walls.append(Wall(
                self.wall_pos.tab[w][0],
                self.wall_pos.tab[w][1],
                self.wall_pos.tab[w][2],
                self.wall_pos.tab[w][3],
                color
            ))

    """----WAVE SPAWN----"""
    def spawn_wave(self, wave):
        if wave < len(self.waves):
            '''-----Fire_Bug-----'''
            if not self.waves[wave][0] == 0:
                if self.waves[wave][0] > 1:
                    for enemy in range(self.waves[wave][0]):
                        self.enemies.append(Fire_Bug(200, 5, 30, 2))
                else:
                    self.enemies.append(Fire_Bug(200, 5, 30, 2))
            '''-----Fire_Bee-----'''
            if not self.waves[wave][1] == 0:
                if self.waves[wave][1] > 1:
                    for enemy in range(self.waves[wave][0]):
                        self.enemies.append(Fire_Bee(200, 5, 30, 2))
                else:
                    self.enemies.append(Fire_Bee(200, 5, 30, 2))

            for e in self.enemies:
                print(e)

    def start(self):
        while self.run:
            """----GAME----"""
            window.blit(self.background, (0, 0))  # background
            keys = pygame.key.get_pressed()  # keyboard events
            delta = self.clock_obj.tick(60) / 1000  # 120 fps
            self.clock += delta
            self.game()  # other game functions

            """----PAUSE----"""
            if self.pause:
                self.def_pause(delta)
                continue

            """----TIME----"""
            if self.timer_on:
                self.timer(delta)

            """----WALL SPAWN----"""
            for wall in self.walls:
                wall.draw(window)

            """----WAVE SPAWN----"""
            if len(self.enemies) == 0:
                self.spawn_wave(self.wave_itterator)

            """----ENEMIES----"""
            self.enemy_tick(delta, self.enemies, self.player, self.walls)

            """----DROPS----"""
            self.drop_tick(delta)

            """----PLAYER----"""
            self.player.tick(keys, self.walls, delta, self.enemies)
            self.player.draw(window)

            """----WIN----"""
            if self.wave_itterator >= len(self.waves):
                self.game_over(delta, True)

            """----LOSE----"""
            if not self.player.alive:
                self.game_over(delta, False)

            pygame.display.update()


class LVL4(Levels):
    def __init__(self, wand_id, FX_active, spell_ids, player_lvl):

        map_lvl = 4
        ''''''
        Levels.__init__(self, wand_id, FX_active, map_lvl, spell_ids, player_lvl)
        self.background = pygame.image.load(f'graph/background/map_{map_lvl}.png')
        for w in range(0, len(self.wall_pos.tab)):
            color = (self.wall_pos.tab[w][4], self.wall_pos.tab[w][5], self.wall_pos.tab[w][6])
            self.walls.append(Wall(
                self.wall_pos.tab[w][0],
                self.wall_pos.tab[w][1],
                self.wall_pos.tab[w][2],
                self.wall_pos.tab[w][3],
                color
            ))

    """----WAVE SPAWN----"""
    def spawn_wave(self, wave):
        if wave < len(self.waves):
            '''-----Fire_Bug-----'''
            if not self.waves[wave][0] == 0:
                if self.waves[wave][0] > 1:
                    for enemy in range(self.waves[wave][0]):
                        self.enemies.append(Fire_Bug(200, 5, 30, 2))
                else:
                    self.enemies.append(Fire_Bug(200, 5, 30, 2))

            for e in self.enemies:
                print(e)

    def start(self):
        while self.run:
            """----GAME----"""
            window.blit(self.background, (0, 0))  # background
            keys = pygame.key.get_pressed()  # keyboard events
            delta = self.clock_obj.tick(60) / 1000  # 120 fps
            self.clock += delta
            self.game()  # other game functions

            """----PAUSE----"""
            if self.pause:
                self.def_pause(delta)
                continue

            """----TIME----"""
            if self.timer_on:
                self.timer(delta)

            """----WALL SPAWN----"""
            for wall in self.walls:
                wall.draw(window)

            """----WAVE SPAWN----"""
            if len(self.enemies) == 0:
                self.spawn_wave(self.wave_itterator)

            """----ENEMIES----"""
            self.enemy_tick(delta, self.enemies, self.player, self.walls)

            """----DROPS----"""
            self.drop_tick(delta)

            """----PLAYER----"""
            self.player.tick(keys, self.walls, delta, self.enemies)
            self.player.draw(window)

            """----WIN----"""
            if self.wave_itterator >= len(self.waves):
                self.game_over(delta, True)

            """----LOSE----"""
            if not self.player.alive:
                self.game_over(delta, False)

            pygame.display.update()


class LVL_BONUS(Levels):
    def __init__(self, wand_id, FX_active, spell_ids, player_lvl):
        Levels.__init__(self, wand_id, FX_active, 1, spell_ids, player_lvl)
        self.bg = [pygame.image.load(f'graph/background/glitch_map/glitch_map_{x}.png') for x in range(1, 38)]
        self.bg_index = 0
        for w in range(0, len(self.wall_pos.lvl1)):
            color = (self.wall_pos.lvl1[w][4], self.wall_pos.lvl1[w][5], self.wall_pos.lvl1[w][6])
            self.walls.append(Wall(
                self.wall_pos.lvl1[w][0],
                self.wall_pos.lvl1[w][1],
                self.wall_pos.lvl1[w][2],
                self.wall_pos.lvl1[w][3],
                color
            ))

    """----WAVE SPAWN----"""
    def spawn_wave(self, wave):
        if wave < len(self.waves):
            if not self.waves[wave][0] == 0:
                if self.waves[wave][0] > 1:  # ghost
                    for enemy in range(self.waves[wave][0]):
                        self.enemies.append(Ghost(100, 0.5, 5, 4))
                else:
                    self.enemies.append(Ghost(100, 0.5, 5, 4))
            if not self.waves[wave][1] == 0:  # shooter
                if self.waves[wave][1] > 1:
                    for enemy in range(self.waves[wave][1]):
                        self.enemies.append(Ghost_Shooter(50, 1.5, 10, 6))
                else:
                    self.enemies.append(Ghost_Shooter(50, 1.5, 10, 6))
            if not self.waves[wave][2] == 0:  # tank
                if self.waves[wave][2] > 1:
                    for enemy in range(self.waves[wave][2]):
                        self.enemies.append(Zombie_Tank(300, 1.5, 5, 2))
                else:
                    self.enemies.append(Zombie_Tank(300, 1.5, 5, 2))
            if not self.waves[wave][3] == 0:  # turret
                if self.waves[wave][3] > 1:
                    for enemy in range(self.waves[wave][3]):
                        self.enemies.append(Skeleton_Turrets(30, 1, 10))
                else:
                    self.enemies.append(Skeleton_Turrets(30, 1, 10))
            if not self.waves[wave][4] == 0:  # skeleton
                if self.waves[wave][4] > 1:
                    for enemy in range(self.waves[wave][4]):
                        self.enemies.append(Skeleton_Shooter(100, 2, 20, 5))
                else:
                    self.enemies.append(Skeleton_Shooter(100, 2, 20, 5))
            if not self.waves[wave][5] == 0:  # lich
                if self.waves[wave][5] > 1:
                    for enemy in range(self.waves[wave][5]):
                        self.enemies.append(Lich(100, 100, 300, 0.5, 40, 3))
                else:
                    self.enemies.append(Lich(100, 100, 300, 1, 40, 3))
            for e in self.enemies:
                print(e)

    def start(self):
        while self.run:
            """----GAME----"""
            window.blit(self.background, (0, 0))  # rysowanie tła
            window.blit(self.fps_text, (1750, 10))
            delta = self.clock_obj.tick(60) / 1000  # maksymalnie 120 fps
            self.clock += delta
            self.fps_text = pygame.font.Font.render(self.arial_42, f'FPS: {floor(self.clock_obj.get_fps())}', True, (0, 0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # jeśli gracz zamknie okienko
                    self.run = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.timer_on = not self.timer_on
                    self.pause = not self.pause
            keys = pygame.key.get_pressed()
            self.gui.draw_GUI()
            self.gui.draw_standards_spell(self.spells)

            """----PAUSE----"""
            if self.pause:
                self.player.controll_active = False
                self.timer_on = False

                if self.RESUME_button.tick(delta):
                    self.player.controll_active = True
                    self.pause = not self.pause

                if self.EXIT_button.tick(delta):
                    self.run = False

                window.blit(self.pause_image, (800, 200))
                self.RESUME_button.draw(window)
                self.EXIT_button.draw(window)
                pygame.display.update()
                continue

            """----TIME----"""
            if self.timer_on:
                self.second += delta
                if self.second < 10 and self.minute <= 0:
                    self.seconds_text = pygame.font.Font.render(self.arial_72, f'{self.minute}:0{floor(self.second)}', True, (0, 0, 0))
                elif self.second < 60 and self.minute <= 0:
                    self.seconds_text = pygame.font.Font.render(self.arial_72, f'{self.minute}:{floor(self.second)}', True, (0, 0, 0))
                elif self.second < 10 and self.minute > 0:
                    self.seconds_text = pygame.font.Font.render(self.arial_72, f'{self.minute}:0{floor(self.second)}', True, (0, 0, 0))
                elif self.second < 60 and self.minute > 0:
                    self.seconds_text = pygame.font.Font.render(self.arial_72, f'{self.minute}:{floor(self.second)}', True, (0, 0, 0))
            window.blit(self.seconds_text, (945, 15))
            if self.second >= 60:
                self.second = 0
                self.minute += 1

            """----WALL SPAWN----"""
            for wall in self.walls:
                wall.draw(window)

            """----WAVE SPAWN----"""
            if len(self.enemies) == 0:
                self.spawn_wave(self.wave_itterator)

            """----ENEMIES----"""
            for enemy in self.enemies:
                enemy.tick(self.walls, self.player, delta)
            for enemy in self.enemies:
                enemy.draw(window)
            for enemy in self.enemies:
                if not enemy.alive:
                    x, y = enemy.x_cord, enemy.y_cord - 50
                    if self.player.current_mana < self.player.max_mana and self.player.current_mana + self.bonus_mana < self.player.max_mana:
                        self.player.current_mana += self.bonus_mana
                    self.enemies.remove(enemy)
                    self.death_animation(window, x, y)
                if len(self.enemies) == 0:
                    self.wave_itterator += 1

            """----PLAYER----"""
            self.player.tick(keys, self.walls, delta, self.enemies)
            self.player.draw(window)

            """----WIN----"""
            if self.wave_itterator >= len(self.waves):
                self.player.controll_active = False
                self.timer_on = False
                mobs, boss = self.calc_monsters()
                window.blit(self.gameover_img, (800, 200))
                window.blit(pygame.font.Font.render(self.arial_48, "Score:", True, (0, 0, 0)), (930, 280))
                window.blit(pygame.font.Font.render(self.arial_72, f"{self.calc_score(self.player)}", True, (0, 0, 0)), (930, 330))
                window.blit(pygame.font.Font.render(self.arial_48, f"HP       :  {floor(self.player.hp / self.player.max_hp * 100)}%", True, (0, 0, 0)), (890, 420))
                window.blit(pygame.font.Font.render(self.arial_48, f"SPELL :  {self.player.score_sum - 1}", True, (0, 0, 0)), (890, 470))
                window.blit(pygame.font.Font.render(self.arial_48, f"MOBS :  {mobs}", True, (0, 0, 0)), (890, 520))
                window.blit(pygame.font.Font.render(self.arial_48, f"BOSS  :  {boss}", True, (0, 0, 0)), (890, 570))
                self.EXIT_button.draw(window)
                if self.EXIT_button.tick(delta):
                    self.run = False

            """----LOSE----"""
            if not self.player.alive:
                self.player.controll_active = False
                self.timer_on = False
                mobs, boss = self.calc_monsters()
                window.blit(pygame.image.load('graph/menu/win.png'), (800, 200))
                window.blit(pygame.font.Font.render(self.arial_48, "Score:", True, (0, 0, 0)), (930, 280))
                window.blit(pygame.font.Font.render(self.arial_72, f"{self.calc_score(self.player)}", True, (0, 0, 0)), (930, 330))
                window.blit(pygame.font.Font.render(self.arial_48, f"HP       :  {floor(self.player.hp / self.player.max_hp * 100)}%", True, (0, 0, 0)), (890, 420))
                window.blit(pygame.font.Font.render(self.arial_48, f"SPELL :  {self.player.score_sum}", True, (0, 0, 0)), (890, 470))
                window.blit(pygame.font.Font.render(self.arial_48, f"MOBS :  {mobs}", True, (0, 0, 0)), (890, 520))
                window.blit(pygame.font.Font.render(self.arial_48, f"BOSS  :  {boss}", True, (0, 0, 0)), (890, 570))
                self.EXIT_button.draw(window)
                if self.EXIT_button.tick(delta):
                    self.run = False

            pygame.display.update()
