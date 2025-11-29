import pygame
from Informations import Links

pygame.font.init()


class GUI:
    def __init__(self, window):
        self.arial_16 = pygame.font.SysFont("arial", 16)
        self.arial_48 = pygame.font.SysFont("arial", 48)

        self.links_class = Links()
        self.links = self.links_class.standard_icon_set

        self.GUI_img = pygame.image.load('graph/background/GUI_image.png')

        self.spell_gui_1 = pygame.image.load('graph/spels/none_icon.png')
        self.spell_gui_2 = pygame.image.load('graph/spels/none_icon.png')
        self.spell_gui_3 = pygame.image.load('graph/spels/none_icon.png')

        self.mana_reg_img = pygame.image.load('graph/spels/man_regen.png')

        #self.aoe_img = pygame.image.load('graph/spels/aoe_expl_icon.png')

        self.player_mana = 0
        self.player_hp = 0
        self.window = window

    def GUI_tick(self, mana, hp):
        self.player_mana = mana
        self.player_hp = hp
        #self.score = pygame.font.Font.render(pygame.font.SysFont("arial", 48), f"scrore: {score}", True, (0, 0, 0))

    def draw_GUI(self):
        self.window.blit(self.GUI_img, (0, 930))
        self.window.blit(self.mana_reg_img, (1530, 980))

    def draw_on_GUI(self, max_mana, max_hp):
        all_width = 170
        all_hight = 10
        percent_width_mana = self.player_mana / max_mana
        width = round(all_width * percent_width_mana)
        pygame.draw.rect(self.window, (30, 30, 30), (40, 970, all_width, all_hight))
        pygame.draw.rect(self.window, (30, 30, 255), (40, 970, width, all_hight))
        mana_num = pygame.font.Font.render(self.arial_16, f"{self.player_mana}", True, (0, 0, 0))
        self.window.blit(mana_num, (50 + all_width, 967))
        self.window.blit(pygame.font.Font.render(self.arial_16, "MN:", True, (0, 0, 0)), (15, 965))

        color = (30, 255, 30)
        percent_width_hp = self.player_hp / max_hp
        width_hp = round(all_width * percent_width_hp)
        pygame.draw.rect(self.window, (30, 30, 30), (40, 950, all_width, all_hight))
        pygame.draw.rect(self.window, color, (40, 950, width_hp, all_hight))
        hp_num = pygame.font.Font.render(self.arial_16, f"{self.player_hp}", True, (0, 0, 0))
        self.window.blit(hp_num, (50 + all_width, 947))
        self.window.blit(pygame.font.Font.render(self.arial_16, "HP:", True, (0, 0, 0)), (15, 945))

    def draw_standards_spell(self, spells):
        self.window.blit(pygame.image.load(f'{self.links[spells[0]]}.png'), (350, 980))
        self.window.blit(pygame.image.load(f'{self.links[spells[1]]}.png'), (420, 980))
        self.window.blit(pygame.image.load(f'{self.links[spells[2]]}.png'), (490, 980))

    def cd_counter_spell_1(self, counter):
        self.window.blit(pygame.font.Font.render(self.arial_48, str(counter), True, (0, 0, 0)), (355, 981))

    def cd_counter_spell_2(self, counter):
        self.window.blit(pygame.font.Font.render(self.arial_48, str(counter), True, (0, 0, 0)), (425, 981))

    def cd_counter_spell_3(self, counter):
        self.window.blit(pygame.font.Font.render(self.arial_48, str(counter), True, (0, 0, 0)), (490, 981))

    def draw_cd_1(self, win, what):
        win.blit(what, (355, 981))

    def draw_cd_2(self, win, what):
        win.blit(what, (425, 981))

    def draw_cd_3(self, win, what):
        win.blit(what, (495, 981))

    def draw_Global_Spell(self, window, image):
        window.blit(pygame.image.load(f'{image}.png'), (1050, 980))
    def draw_global_cd(self, t):
        time = pygame.font.Font.render(self.arial_48, f"{t}", True, (0, 0, 0))
        self.window.blit(time, (1055, 930))



