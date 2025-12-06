
'''
SPOKO POMYSLY

Mana Shield → tworzy tarczę wokół gracza, która pochłania część otrzymanych obrażeń, zużywając stały procent many.
Summon Familiar → przyzywa pomocnika (np. ptaka lub małego golema), który automatycznie atakuje wrogów przez określony czas.
Gravity Well → przyciąga wszystkich przeciwników do środka i chwilowo unieruchamia ich na miejscu.
Reflective Barrier → tymczasowa bariera, która odbija część otrzymanych obrażeń w przeciwników stojących najbliżej.
Power Surge → zwiększa szybkość ataku i siłę kolejnych ataków na kilka sekund.
Leap Slam → skok w powietrze i uderzenie w ziemię w wybranym miejscu, zadające obrażenia i chwilowo powalające przeciwników. chwilowe wylaczenie kolizji
Chaos Vortex → tworzy wir, który losowo teleportuje wrogów wokół gracza i odrzuca ich w różne strony
Polymorph → zamienia jednego wroga w małe, bezbronne zwierzątko na kilka sekund.
Dimension Slash → natychmiastowa seria cięć w linii prostej, która przebija wszystkie przeszkody i wrogów.
Teleport Swap → zamienia miejscami gracza z wybranym wrogiem lub obiektem w zasięgu, zaskakując przeciwników.
'''


class Info_Game:
    def __init__(self):
        self.game = [
            'Trash Game is a platformer with action and combat elements.',
            'Your goal is to defeat all enemies and achieve the highest score.',
            'Use platforms to jump and hide behind for cover.',
            'Enemies come in waves, with the last wave always being a boss.',
            '',
            'Defeat the boss to unlock the passage to the next level.',
            '',
            'Each wand has its own element and a special global spell. Additionally',
            'you can choose from a variety of independent spells to create your own combos.',
            'In the menu, enter your character name in the login field to save your score.',
        ]


class Info_Spells:
    def __init__(self):
        self.heal_info = [
            'HEAL',
            '',
            'Restores health based on game progression,',
            'consuming a portion of mana.'
        ]
        self.flash_info = [
            'FLASH',
            '',
            'Dashes ~6 player lengths in the chosen direction,',
            'consuming mana.',
            '(A or D + spell key)'
        ]
        self.boost_info = [
            'ATACK BOOST',
            '',
            'Increases auto-attack damage for a short duration,',
            'consuming mana.'
        ]

        self.standard_spells_info = [self.heal_info, self.flash_info, self.boost_info]
########################################################################################################################
        self.none = [
            'BASIC WAND',
            '',
            'A simple wand with no special ability.'
        ]
        self.poison_hit = [
            '',
        ]
        self.thunder_bolt_info = [
            'THUNDER BOLT',
            '',
            'Global special attack from the magic wand,',
            'summoning lightning waves across the map to deal damage,',
            'consuming half of max mana.'
        ]
        self.self_explosion = [
            'SELF EXPLOSION',
            '',
            'Global special attack from the fire wand,',
            'creating an AOE explosion around the player to deal heavy damage,',
            'consuming half of max mana.',
        ]
        self.good_helper = [
            'GOOD HELPER',
            '',
            'Global special attack from the flower wand,',
            'placing a turret-like flower at the player’s position',
            'hat automatically attacks enemies and disappears after a set time.',
            'consuming half of max mana.',
        ]
        self.ice_splash = [
            'Ice_Slow',
        ]
        self.undead_curse = [
            'UNDEAD CURSE',
            '',
            'Debuff for enemies,',
            'educing the damage they can deal,',
            'consuming half of max mana.',
        ]
        self.plant_stun = [
            'PLANT STUN',
            '',
            'Global special attack from the plant wand,',
            'immobilizing all enemies on the map for a short duration,',
            'consuming half of max mana.'
        ]

        self.global_spells_info = [self.none, self.poison_hit, self.thunder_bolt_info, self.self_explosion, self.good_helper, self.ice_splash, self.undead_curse, self.plant_stun]

        self.char_list_name = [
            'ADMIN',
            '-----------------',
            '-----------------',
            '-----------------',
            '-----------------',
            '-----------------',
        ]
        #hp, mana, cd, dmg, max_speed
        self.player_info_labels = [
            'HP   :',
            'MN   :',
            'CD   :',
            'DMG :',
            'MS   :',
        ]

class Links:
    def __init__(self):
        self.standard_icon_set = [
            'graph/spels/heal',
            'graph/spels/flash',
            'graph/spels/attack_boost',
        ]
        self.wands_set = [
            'graph/weapon/wand',
            'graph/weapon/death_wand',
            'graph/weapon/thunder_wand',
            'graph/weapon/fire_wand',
            'graph/weapon/plant_wand',
            'graph/weapon/ice_wand',
            'graph/weapon/dark_wand',
            'graph/weapon/plant_wand',

        ]
        self.wand_animations = [
            'graph/weapon/wand/wand',
            'graph/weapon/death_wand/death_wand',
            'graph/weapon/thunder_wand/thunder_wand',
            'graph/weapon/fire_wand/fire_wand',
            'graph/weapon/plant_wand/plant_wand',
            'graph/weapon/ice_wand/ice_wand',
            'graph/weapon/dark_wand/dark_wand',
            'graph/weapon/plant_wand/plant_wand',

        ]
        self.global_set_icon = [
            'graph/spels/none_icon',
            'graph/spels/death_icon',
            'graph/spels/thunder_icon',
            'graph/spels/aoe_expl_icon',
            'graph/spels/flower_icon',
            'graph/spels/ice_splash_icon',
            'graph/spels/meteor_icon',
            'graph/spels/weins_stun_icon',

        ]
        self.global_set = [
            'graph/spels/None',
            'graph/spels/None',
            'graph/spels/thunder_drop_down',
            'graph/spels/explosion/exp_aoe_',
            'graph/enemy/lvl3/plant_turret',
            'graph/spels/None',
            'graph/spels/None',
            'graph/spels/None',

        ]
        self.spells = [
            'graph/spels/spel',
            'graph/spels/spel_lich',
            'graph/spels/spel_thunder',
            'graph/spels/spel_ghost',
            'graph/spels/spel_plant',
            'graph/spels/spel_ice',
            'graph/spels/spel_ghost',
            'graph/spels/spel_plant',
        ]





class Stats:
    def __init__(self):
        self.player_stats_bonus = [0, 0, 0, 0, 0]

        self.player = [  # x, y, hp, mana, cd, dmg, max_speed
            [300, 610, 900, 300, 0.3, 70, 7, 1],   # ADMIN
            [300, 610, 200, 100, 0.5, 20, 7, 1],   # lvl 1
            [300, 610, 250, 120, 0.5, 25, 7, 1],   # lvl 2
            [300, 610, 300, 140, 0.5, 30, 7, 1],   # lvl 3
            [300, 610, 350, 160, 0.4, 35, 7, 1],   # lvl 4
            [300, 610, 400, 180, 0.4, 40, 7, 1],   # lvl 5
            [300, 610, 450, 200, 0.4, 45, 7, 1],   # lvl 6
            [300, 610, 500, 250, 0.3, 50, 7, 1],   # lvl 7
        ]


class Waves_Tab:
    def __init__(self, lvl):
        self.lvl_1_mobs_stats = [
            # HP  CD  DMG walk
            [100, 0.5, 5,  4],                          # Ghost
            [50,  1.5, 10, 6],                          # Shooter
            [300, 1.5, 5,  2],                          # Zombie
            [400, 30,  1],                              # Turret
            [100, 2,   20, 5],                          # Skeleton
            [100, 100, 300, 0.5],                       # Lich
        ]

        self.lvl_2_mobs_stats = [
            # HP  CD  DMG  walk
            [100, 0.5, 5,  4],                              # Soldier Ghost
            [50,  1.5, 10, 6],                              # Soldier Tank
            [300, 1.5, 5,  2],                              # Roman Shaman
            [400, 30,  1,  10],                             # Zeus
        ]

        self.lvl_3_mobs_stats = [
            [300, 0.5, 5, 4],                           # Bug
        ]


        self.lvl_1 = [  # ghost, shooter, tank, turret, skeleton, lich
            [2, 0, 0, 0, 0, 0],
            #[1, 1, 1, 1, 1, 1],
            [1, 1, 0, 0, 0, 0],
            [2, 0, 1, 0, 0, 0],
            [0, 2, 2, 0, 0, 0],
            [2, 1, 1, 1, 0, 0],
            [1, 1, 2, 1, 1, 0],
            [0, 0, 1, 2, 2, 1],
        ]

        self.lvl_2 = [  #
            #[1, 1, 1, 1],
            [1, 0, 0, 0],
            [1, 1, 1, 1],

        ]

        self.lvl_3 = [
            [1],
        ]

        self.lvl_4 = [
            [],
        ]

        self.lvl_5 = [
            [],
        ]

        self.lvl_6 = [
            [],
        ]

        self.tab = []
        self.mob_stats = []
        if lvl == 1:
            self.tab = self.lvl_1
            self.mob_stats = self.mob_stats
        elif lvl == 2:
            self.tab = self.lvl_2
            self.mob_stats = self.lvl_2_mobs_stats
        elif lvl == 3:
            self.tab = self.lvl_3
            self.mob_stats = self.lvl_3_mobs_stats
        elif lvl == 4:
            self.tab = self.lvl_4
        elif lvl == 5:
            self.tab = self.lvl_5
        elif lvl == 6:
            self.tab = self.lvl_6


class Walls_Position:
    def __init__(self, lvl):
        self.lvl1 = [
            [0, 0, 1920, 1, 0, 0, 0, True],
            [0, 0, 1, 930, 0, 0, 0, True],
            [1920, 0, 1, 930, 0, 0, 0, True],
            [0, 890, 1920, 40, 0, 0, 0, True],
            [902, 780, 74, 8, 80, 68, 56, False],
            [902, 670, 74, 8, 80, 68, 56, False],
            [1008, 632, 60, 8, 80, 68, 56, False],
            [632, 572, 131, 9, 80, 68, 56, False],
            [739, 470, 101, 12, 80, 68, 56, False],
            [1016, 503, 125, 7, 80, 68, 56, False],
            [892, 350, 70, 11, 80, 68, 56, False],
        ]

        self.lvl2 = [
            [0, 0, 1920, 1, 0, 0, 0, True],
            [0, 0, 1, 930, 0, 0, 0, True],
            [1920, 0, 1, 930, 0, 0, 0, True],
            [0, 890, 1920, 40, 0, 0, 0, True],
        ]

        self.lvl3 = [
            [0, 0, 1920, 1, 0, 0, 0, True],
            [0, 0, 1, 930, 0, 0, 0, True],
            [1920, 0, 1, 930, 0, 0, 0, True],
            [0, 890, 1920, 40, 0, 0, 0, True],
            [902, 780, 500, 8, 80, 68, 56, False],
        ]

        self.lvl4 = [
            [0, 0, 1920, 1, 0, 0, 0, True],
            [0, 0, 1, 930, 0, 0, 0, True],
            [1920, 0, 1, 930, 0, 0, 0, True],
            [0, 890, 1920, 40, 0, 0, 0, True],
        ]

        self.lvl5 = [
            [0, 0, 1920, 1, 0, 0, 0, True],
            [0, 0, 1, 930, 0, 0, 0, True],
            [1920, 0, 1, 930, 0, 0, 0, True],
            [0, 890, 1920, 40, 0, 0, 0, True],
        ]

        self.lvl6 = [
            [0, 0, 1920, 1, 0, 0, 0, True],
            [0, 0, 1, 930, 0, 0, 0, True],
            [1920, 0, 1, 930, 0, 0, 0, True],
            [0, 890, 1920, 40, 0, 0, 0, True],
        ]

        self.tab = []
        if lvl == 1:
            self.tab = self.lvl1
        elif lvl == 2:
            self.tab = self.lvl2
        elif lvl == 3:
            self.tab = self.lvl3
        elif lvl == 4:
            self.tab = self.lvl4
        elif lvl == 5:
            self.tab = self.lvl5
        elif lvl == 6:
            self.tab = self.lvl6


class Sounds:
    def __init__(self):
        self.FX_spells = [
            'sound/FX/shots/heal',
            'sound/FX/shots/flash_spell',
            'sound/FX/shots/boost_spell',

        ]

        self.FX_wand_shot = [
            'sound/FX/shots/air_hit',
            'sound/FX/shots/air_hit',
            'sound/FX/shots/thunder_spell',
            'sound/FX/shots/fire_spell',
            'sound/FX/shots/air_hit',
            'sound/FX/shots/ice_spell',
            'sound/FX/shots/air_hit',
            'sound/FX/shots/air_hit',

        ]

        self.FX_global_spells = [
            '',
            '',
            'sound/FX/shots/thunder_drop_down',
            'sound/FX/shots/explosion',
            '',
            '',
            '',
            '',
        ]

        self.FX_other = [
            'sound/FX/shots/arrow_shot.wav',
            'sound/FX/shots/explosion',
            'sound/FX/shots/explosion_hit',
            'sound/FX/shots/light_shot',
            'sound/FX/things/error',
            'sound/FX/things/accept_sound',
        ]

