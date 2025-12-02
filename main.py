import pygame
import json

from DataManager import Save_Manager
from Menu import Button, Button_Blocked, Checker_once, Choose_Continu, Info_area, Text_Input, Valume
from Informations import Info_Game, Info_Spells, Links, Stats
from Levels import LVL1, LVL2, LVL_BONUS
from Map_Editor import Editor, Admin_Room
from Sound_Controller import FX

pygame.init()
window = pygame.display.set_mode((1920, 1080))
pygame.display.set_icon(pygame.image.load('graph/menu/logo.png'))
pygame.display.set_caption('TrashGame')
########################################################################################################################


class Start_Menu:
    def __init__(self):
        self.arial_24 = pygame.font.SysFont("arial", 24)
        self.arial_16 = pygame.font.SysFont("arial", 16)
        self.arial_12 = pygame.font.SysFont("arial", 12)

        '''-----Game-----'''
        self.fx = FX()
        self.FX_active = True
        self.wand_id = 0
        self.links = Links()
        self.wands_set = self.links.wands_set
        self.standard_icon_set = self.links.standard_icon_set
        self.global_set = self.links.global_set_icon
        self.run = True
        self.clock = 0
        self.bg = pygame.image.load("graph/menu/start_menu.png")


        self.NICKNAME = ''
        self.MAX_SCORE = 0
        self.LEVEL = 0          #admin = 0
        self.LOGED = False
        self.COINS = 0
        if self.LEVEL == 0:
            self.COINS = 100

        '''-----Map_Editor-----'''
        '''
            With Admin Mode can you easily Create your own Map 4b756261
        '''
        self.editor = Editor()
        self.A_room = Admin_Room()

        '''-----LOGIN-----'''
        # submit_button = Button(270, 450, "graph/menu/buttons/button_SUBMIT")
        self.pre_admin_state = False                                                                # if u try to log as admin -> True
        self.data_manag = Save_Manager('G:\python_worksapce\Platform_Game\data\data.json')
        self.nick_input = Text_Input(270, 350, 150, 40, 20, 'nickname', True, 270, 450)
        self.pass_input = Text_Input(270, 400, 150, 40, 20, 'password')
        # max_score = pygame.font.Font.render(self.arial_24, f'', True, (0, 0, 0))
        # current_level = pygame.font.Font.render(self.arial_24, '', True, (0, 0, 0))

        '''-----LVL-----'''
        self.current_lvl = 0

        self.info_icon = pygame.image.load('graph/menu/info_icon.png')
        self.i_game = Info_Game()
        self.info_box = Info_area(1580, 291, 24, 24, True)
        self.info_box.dis_between_text = 24

        self.lvl1_button = Button_Blocked(300, 600, "graph/menu/lvl_1_icon", 'graph/menu/lvl_blocked_icon')
        self.lvl1_info_top = pygame.font.Font.render(self.arial_16, "Undeads Cementery", True, (0, 0, 0))
        self.lvl1_info_bot = pygame.font.Font.render(self.arial_16, "LVL 1", True, (0, 0, 0))

        self.lvl_2_activ = False
        self.lvl2_button = Button_Blocked(450, 600, "graph/menu/lvl_2_icon", 'graph/menu/lvl_blocked_icon')
        self.lvl2_info_top = pygame.font.Font.render(self.arial_16, "Olimp Mountain", True, (0, 0, 0))
        self.lvl2_info_bot = pygame.font.Font.render(self.arial_16, "LVL 2", True, (0, 0, 0))

        self.lvl_3_activ = False
        self.lvl3_button = Button_Blocked(600, 600, "graph/menu/lvl_3_icon", 'graph/menu/lvl_blocked_icon')
        self.lvl3_info_top = pygame.font.Font.render(self.arial_16, "Hell", True, (0, 0, 0))
        self.lvl3_info_bot = pygame.font.Font.render(self.arial_16, "LVL 3", True, (0, 0, 0))

        self.lvl_4_activ = False
        self.lvl4_button = Button_Blocked(750, 600, "graph/menu/lvl_4_icon", 'graph/menu/lvl_blocked_icon')
        self.lvl4_info_top = pygame.font.Font.render(self.arial_16, "Jungle", True, (0, 0, 0))
        self.lvl4_info_bot = pygame.font.Font.render(self.arial_16, "LVL 4", True, (0, 0, 0))

        self.lvl_5_activ = False
        self.lvl5_button = Button_Blocked(900, 600, "graph/menu/lvl_5_icon", 'graph/menu/lvl_blocked_icon')
        self.lvl5_info_top = pygame.font.Font.render(self.arial_16, "Ice Age", True, (0, 0, 0))
        self.lvl5_info_bot = pygame.font.Font.render(self.arial_16, "LVL 5", True, (0, 0, 0))

        self.lvl_6_activ = False
        self.lvl6_button = Button_Blocked(1050, 600, "graph/menu/lvl_6_icon", 'graph/menu/lvl_blocked_icon')
        self.lvl6_info_top = pygame.font.Font.render(self.arial_16, "Wulkan", True, (0, 0, 0))
        self.lvl6_info_bot = pygame.font.Font.render(self.arial_16, "LVL 6", True, (0, 0, 0))

        self.lvl_7_activ = False
        self.lvl7_button = pygame.image.load('graph/menu/lvl_blocked_icon.png')
        self.lvl7_info_top = pygame.font.Font.render(self.arial_16, "---", True, (0, 0, 0))
        self.lvl7_info_bot = pygame.font.Font.render(self.arial_16, "LVL 7", True, (0, 0, 0))

##############################################################################################################################

        self.m_editor_activ = False
        self.m_editor_button = Button_Blocked(750, 760, "graph/menu/map_editor_icon", 'graph/menu/lvl_blocked_icon')
        self.m_info_top = pygame.font.Font.render(self.arial_16, "MAP EDITOR", True, (0, 0, 0))
        self.m_info_bot = pygame.font.Font.render(self.arial_16, "", True, (0, 0, 0))

        self.A_activ = False
        self.A_button = Button_Blocked(900, 760, "graph/menu/admin_room_icon", 'graph/menu/lvl_blocked_icon')
        self.A_info_top = pygame.font.Font.render(self.arial_16, "???", True, (0, 0, 0))
        self.A_info_bot = pygame.font.Font.render(self.arial_16, "", True, (0, 0, 0))

        self.lvl_B_activ = False
        self.lvl_BONUS_button = Button_Blocked(1050, 760, "graph/menu/lvl_bonus_icon", 'graph/menu/lvl_blocked_icon')
        self.lvl_BONUS_info_top = pygame.font.Font.render(self.arial_16, "Glitch World", True, (0, 0, 0))
        self.lvl_BONUS_info_bot = pygame.font.Font.render(self.arial_16, "BONUS", True, (0, 0, 0))

        '''----SETUP----'''
        self.exit_button = Button(1400, 870, "graph/menu/buttons/button_EXIT")

        self.checker_easy = Checker_once(1400, 350, True)
        self.checker_med = Checker_once(1400, 390)
        self.checker_hard = Checker_once(1400, 430)
        self.checker_res = Checker_once(1400, 500, True)
        self.checker_fx = Checker_once(1400, 570, True)
        self.checker_musik = Checker_once(1400, 610, True)

        self.FX_volume = Valume(1500, 570)

        self.s_info = Info_Spells()

        '''-----Wand-----'''
        self.choose_wand_set = Choose_Continu(990, 330, 870, 330, self.wands_set)
        self.choose_wand_iter = 0
        self.wand_info = Info_area(910, 320, 50, 50)

        '''-----Standard_Spells-----'''
        '''
            It doesn't Working right now but i hope someday i have a clu why.
            
            It should work like: 
            You can choose three from 3 (for now) of spells like Heal, Dmg_Burst etc.
            It can be for example Heal, Heal, Heal or Heal, Heal, Flash dosen't care.
            
            You can choose the 1st setup and it work but for other setups it dosent work corretly
            
            If u want u can fix it, Have Fun !
        '''
        self.choose_standard_spell_1 = Choose_Continu(900, 470, 870, 470, self.standard_icon_set)
        self.info_1 = Info_area(865, 415, 50, 50)
        self.choose_standard_spell_2 = Choose_Continu(975, 470, 945, 470, self.standard_icon_set, 1)
        self.info_2 = Info_area(940, 415, 50, 50)
        self.choose_standard_spell_3 = Choose_Continu(1050, 470, 1020, 470, self.standard_icon_set, 2)
        self.info_3 = Info_area(1015, 415, 50, 50)
        self.standard_spells = [0, 1, 2]

        '''-----Coins/Upgrades-----'''
        self.coins_req_upgrade = 10
        self.upgrade_buttons = []
        ub_y = 350

        for b in range(0, 5):
            self.upgrade_buttons.append(Button(720, ub_y, "graph/menu/upgrade"))
            ub_y += 25

        '''-----Stats-----'''
        self.first_y = 350
        self.char_labels = []
        self.char_list = []
        char_y = self.first_y
        for ch in range(0, 5):
            self.char_list.append(Button(450, char_y, 'graph/menu/buttons/button_CHAR'))
            self.char_labels.append(pygame.font.Font.render(self.arial_16, self.s_info.char_list_name[ch], True, (0, 0, 0)))
            char_y += 23

        self.stats = Stats()
        self.player_img = pygame.image.load('graph/player/player_stand.png')
        self.player_stats_labels = []
        self.player_info_labels = []
        for ch in range(0, 5):
            self.player_info_labels.append(pygame.font.Font.render(self.arial_16, self.s_info.player_info_labels[ch], True, (0, 0, 0)))
        for ch in range(0, 5):
            self.player_stats_labels.append(pygame.font.Font.render(self.arial_16, f'{self.stats.player[self.LEVEL][ch+2]}', True, (0, 0, 0)))

    def start(self):
        while self.run:
            '''-----GAME-----'''
            delta = pygame.time.Clock().tick(60) / 1000  # maksymalnie 60 fps
            self.clock += delta
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:  # jeśli gracz zamknie okienko
                    self.run = False

            window.blit(self.bg, (0, 0))

            if self.exit_button.tick(delta):
                self.run = False
            self.exit_button.draw(window)

            '''-----LOGIN-----'''
            self.NICKNAME = self.nick_input.tick(self.clock, events, delta)
            if self.NICKNAME != '':
                if self.NICKNAME == 'admin':
                    self.pre_admin_state = True
                print(self.NICKNAME)
                if not self.data_manag.get_player(self.NICKNAME):
                    self.data_manag.add_player(self.NICKNAME, '')
                else:
                    if data_manag.login(NICKNAME, ''):
                        self.LOGED = True
                        self.MAX_SCORE = data_manag.get_value(NICKNAME, "score")
                        self.LEVEL = data_manag.get_value(NICKNAME, "level")
                        print(f'score: {self.MAX_SCORE}')
                        print(f'level: {self.LEVEL}')
            self.nick_input.draw(window)

            if self.pre_admin_state:
                passw = self.pass_input.tick(self.clock, events, delta)
                self.pass_input.draw(window)

            '''-----CHAR_CHOOSE-----'''
            '''
                You can create 4 saves and then chose one of 5.
            '''
            char_labels_iter = 350
            for ch in range(0, 5):
                if self.char_list[ch].tick(delta):
                    if ch == 0:
                        pass
                self.char_list[ch].draw(window)
                window.blit(self.char_labels[ch], (455, char_labels_iter))
                char_labels_iter += 23

            '''-----PLAYER_STATS-----'''
            window.blit(self.player_img, (630, 370))
            window.blit(pygame.font.Font.render(self.arial_16, f'COINS: {self.COINS}', True, (0, 0, 0)), (750, 320))
            for ch in range(0, 5):
                self.player_stats_labels[ch] = pygame.font.Font.render(self.arial_16, f'{self.stats.player[self.LEVEL][ch + 2] + self.stats.player_stats_bonus[ch]}', True, (0, 0, 0))
            player_labels_iter = 350
            for ch in range(0, 5):
                window.blit(self.player_info_labels[ch], (750, player_labels_iter))
                window.blit(self.player_stats_labels[ch], (795, player_labels_iter))
                player_labels_iter += 25
            if self.COINS >= self.coins_req_upgrade:
                for u in range(0, 5):
                    if self.upgrade_buttons[0].tick(delta):
                        self.COINS -= self.coins_req_upgrade
                        self.stats.player_stats_bonus[0] += 10
                    elif self.upgrade_buttons[1].tick(delta):
                        self.COINS -= self.coins_req_upgrade
                        self.stats.player_stats_bonus[1] += 5
                    elif self.upgrade_buttons[2].tick(delta):
                        self.COINS -= self.coins_req_upgrade
                        self.stats.player_stats_bonus[2] += 0.1
                    elif self.upgrade_buttons[3].tick(delta):
                        self.COINS -= self.coins_req_upgrade
                        self.stats.player_stats_bonus[3] += 2
                    elif self.upgrade_buttons[4].tick(delta):
                        self.COINS -= self.coins_req_upgrade
                        self.stats.player_stats_bonus[4] += 0.2
                    self.upgrade_buttons[u].draw(window)


#############################################################################################
            '''-----LVL-----'''
            if self.LEVEL >= 2 or self.LEVEL == 0:
                self.lvl_2_activ = True
            if self.LEVEL >= 3 or self.LEVEL == 0:
                self.lvl_3_activ = True
            if self.LEVEL >= 4 or self.LEVEL == 0:
                self.lvl_4_activ = True
            if self.LEVEL >= 5 or self.LEVEL == 0:
                self.lvl_5_activ = True
            if self.LEVEL >= 6 or self.LEVEL == 0:
                self.lvl_6_activ = True
            if self.LEVEL >= 7 or self.LEVEL == 0:
                self.lvl_7_activ = True

            if self.LEVEL == 0:
                self.lvl_B_activ = True
                self.A_activ = True
                self.m_editor_activ = True

            if self.lvl1_button.tick():
                if self.choose_wand_iter <= self.LEVEL or self.LEVEL == 0:
                    lvl = LVL1(self.wand_id, self.FX_active, [0, 1, 2], self.LEVEL)      #self.wand_id, self.FX_active, self.standard_spells
                    lvl.pause = False
                    lvl.run = True
                    lvl.start()
                    self.COINS += lvl.player.coins
                    if self.LEVEL == 1 and lvl.get_win():
                        self.LEVEL += 1
                else:
                    self.fx.error_sound(0.4)
            self.lvl1_button.draw(window)
            window.blit(self.lvl1_info_top, (295, 575))
            window.blit(self.lvl1_info_bot, (335, 705))

            if self.lvl2_button.tick(not self.lvl_2_activ):
                if self.choose_wand_iter + 1 <= self.LEVEL or self.LEVEL == 0:
                    lvl = LVL2(self.wand_id, self.FX_active, [0, 1, 2], self.LEVEL)
                    lvl.pause = False
                    lvl.run = True
                    lvl.start()
                    if self.LEVEL == 2 and lvl.get_win():
                        self.LEVEL += 1
                else:
                    self.fx.error_sound(0.3)
            self.lvl2_button.draw(window)
            window.blit(self.lvl2_info_top, (453, 575))
            window.blit(self.lvl2_info_bot, (483, 705))

            if self.lvl3_button.tick(not self.lvl_3_activ):
                if self.choose_wand_iter + 1 <= self.LEVEL:
                    pass
                else:
                    self.fx.error_sound(0.3)
            self.lvl3_button.draw(window)
            window.blit(self.lvl3_info_top, (630, 575))
            window.blit(self.lvl3_info_bot, (633, 705))

            if self.lvl4_button.tick(not self.lvl_4_activ):
                if self.choose_wand_iter + 1 <= self.LEVEL or self.LEVEL == 0:
                    pass
                else:
                    self.fx.error_sound(0.3)
            self.lvl4_button.draw(window)
            window.blit(self.lvl4_info_top, (780, 575))
            window.blit(self.lvl4_info_bot, (783, 705))

            if self.lvl5_button.tick(not self.lvl_5_activ):
                if self.choose_wand_iter + 1 <= self.LEVEL or self.LEVEL == 0:
                    pass
                else:
                    self.fx.error_sound(0.3)
            self.lvl5_button.draw(window)
            window.blit(self.lvl5_info_top, (930, 575))
            window.blit(self.lvl5_info_bot, (933, 705))

            if self.lvl6_button.tick(not self.lvl_6_activ):
                if self.choose_wand_iter + 1 <= self.LEVEL or self.LEVEL == 0:
                    pass
                else:
                    self.fx.error_sound(0.3)
            self.lvl6_button.draw(window)
            window.blit(self.lvl6_info_top, (1080, 575))
            window.blit(self.lvl6_info_bot, (1083, 705))

            window.blit(self.lvl7_button, (300, 760))

#############################################################################################
            if self.m_editor_button.tick(not self.m_editor_activ):
                self.editor.run = True
                self.editor.start()
            self.m_editor_button.draw(window)
            #window.blit(self.lvl2_info_top, (453, 575))
            #window.blit(self.lvl2_info_bot, (483, 705))

            if self.A_button.tick(not self.A_activ):
                self.A_room.run = True
                self.A_room.start()
            self.A_button.draw(window)
            #window.blit(self.lvl1_info_top, (295, 575))
            #window.blit(self.lvl1_info_bot, (335, 705))

            if self.lvl_BONUS_button.tick(not self.lvl_B_activ):
                lvl = LVL_BONUS(self.wand_id, self.FX_active, [0, 1, 2], self.LEVEL)
                lvl.pause = False
                lvl.run = True
                lvl.start()
            self.lvl_BONUS_button.draw(window)
            window.blit(self.lvl_BONUS_info_top, (1060, 735))
            window.blit(self.lvl_BONUS_info_bot, (1075, 865))

#############################################################################################


            '''-----OPTIONS-----'''
            self.checker_easy.tick(delta)
            self.checker_easy.draw(window)
            self.checker_easy.draw_text(window, "EASY", 120, 222, 18)

            self.checker_med.tick(delta)
            self.checker_med.draw(window)
            self.checker_med.draw_text(window, "MEDIUM", 204, 199, 57)

            self.checker_hard.tick(delta)
            self.checker_hard.draw(window)
            self.checker_hard.draw_text(window, "HARD", 173, 19, 19)

            self.checker_res.tick(delta)
            self.checker_res.draw(window)
            self.checker_res.draw_text(window, "1920 x 1080", 70, 70, 70)

            self.FX_active = self.checker_fx.tick(delta)
            self.checker_fx.draw(window)
            self.checker_fx.draw_text(window, "FX", 70, 70, 70)

            self.checker_musik.tick(delta)
            self.checker_musik.draw(window)
            self.checker_musik.draw_text(window, "MUSIK", 70, 70, 70)

            self.FX_volume.draw(window)

            '''-----WAND-----'''
            self.choose_wand_iter = self.choose_wand_set.tick(delta)
            self.choose_wand_set.draw(window)
            if self.choose_wand_iter + 1 <= self.LEVEL or self.LEVEL == 0:
                window.blit(pygame.image.load(f"{self.global_set[self.choose_wand_iter]}.png"), (910, 320))
                window.blit(pygame.image.load(f"{self.wands_set[self.choose_wand_iter]}.png"), (905, 300))
                self.wand_id = self.choose_wand_iter
                self.wand_info.tick(window, self.s_info.global_spells_info[self.wand_id])
            else:
                window.blit(pygame.image.load(f"{self.global_set[0]}.png"), (910, 320))
                window.blit(pygame.image.load(f"{self.wands_set[self.choose_wand_iter]}.png"), (905, 300))
            '''-----SPELLS-----'''
            choose_standard_iter_1 = self.choose_standard_spell_1.tick(delta)
            window.blit(pygame.image.load(f"{self.standard_icon_set[choose_standard_iter_1]}.png"), (865, 415))
            self.choose_standard_spell_1.draw(window)
            self.info_1.tick(window, self.s_info.standard_spells_info[choose_standard_iter_1])
            self.standard_spells[0] = choose_standard_iter_1

            choose_standard_iter_2 = self.choose_standard_spell_2.tick(delta)
            window.blit(pygame.image.load(f"{self.standard_icon_set[choose_standard_iter_2]}.png"), (940, 415))
            self.choose_standard_spell_2.draw(window)
            self.info_2.tick(window, self.s_info.standard_spells_info[choose_standard_iter_2])
            self.standard_spells[1] = choose_standard_iter_2

            choose_standard_iter_3 = self.choose_standard_spell_3.tick(delta)
            window.blit(pygame.image.load(f"{self.standard_icon_set[choose_standard_iter_3]}.png"), (1015, 415))
            self.choose_standard_spell_3.draw(window)
            self.info_3.tick(window, self.s_info.standard_spells_info[choose_standard_iter_3])
            self.standard_spells[2] = choose_standard_iter_3

            '''-----INFO-----'''
            window.blit(self.info_icon, (1580, 291))
            self.info_box.tick(window, self.i_game.game)

            pygame.display.update()


def main():
    Start_Menu().start()


if __name__ == "__main__":
    main()
