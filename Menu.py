import pygame

from Sound_Controller import FX


''' 
    Just a button: 
        - if hitbox.collidepoint(get_pos()) -> draw '{name}_covered.png'
        - if pressed                        -> tick = True
'''
class Button:
    def __init__(self, x_cord, y_cord, file_name):
        self.fx = FX()
        self.clock = 0
        self.x_cord = x_cord
        self.y_cord = y_cord

        self.delay = 0.2
        self.button_image = pygame.image.load(f"{file_name}.png")
        try:
            self.button_image_on = pygame.image.load(f"{file_name}_covered.png")
        except FileNotFoundError:
            self.button_image_on = pygame.image.load(f"{file_name}.png")

        self.hitbox = pygame.Rect(self.x_cord, self.y_cord, self.button_image.get_width(), self.button_image.get_height())

    def tick(self, delta):
        self.clock += delta
        if self.hitbox.collidepoint(pygame.mouse.get_pos()):
           if pygame.mouse.get_pressed()[0] and self.clock > self.delay:
               self.clock = 0.0
               self.fx.accept_sound(0.4)
               return True

    def draw(self, window):
        if self.hitbox.collidepoint(pygame.mouse.get_pos()):
            window.blit(self.button_image_on, (self.x_cord, self.y_cord))
        else:
            window.blit(self.button_image, (self.x_cord, self.y_cord))


'''
    Just a button with block:
         - if tick(False)                   -> draw file_name
         - else                             -> blocked_file_name
'''
class Button_Blocked:
    def __init__(self, x_cord, y_cord, file_name, blocked_file_name):
        self.fx = FX()
        self.x_cord = x_cord
        self.y_cord = y_cord
        try:
            self.blocked_img = pygame.image.load(f"{blocked_file_name}.png")
            self.button_image = pygame.image.load(f"{file_name}.png")
            self.button_image_on = pygame.image.load(f"{file_name}_covered.png")
        except FileNotFoundError:
            name1 = file_name.replace('.png', '')
            name2 = blocked_file_name.replace('.png', '')
            if not name1 == file_name:
                print(f'LOG: menu/Button_Blocked -> file_name: Replaced ( {file_name} ) with ( {name1} )')
                self.button_image = pygame.image.load(f"{name1}.png")
                self.button_image_on = pygame.image.load(f"{name1}_covered.png")
            else:
                print(f'LOG: menu/Button_Blocked -> file_name: Name not found( {blocked_file_name} )')
            if not name2 == blocked_file_name:
                print(f'LOG: menu/Button_Blocked -> file_name: Replaced ( {blocked_file_name} ) with ( {name2} )')
                self.button_image = pygame.image.load(f"{name2}.png")
                self.button_image_on = pygame.image.load(f"{name2}_covered.png")
            else:
                print(f'LOG: menu/Button_Blocked -> file_name: Name not found ( {file_name} )')
        self.hitbox = pygame.Rect(self.x_cord, self.y_cord, self.button_image.get_width(), self.button_image.get_height())
        self.blocked = False

    def tick(self, blocked=False):
        self.blocked = blocked
        if self.hitbox.collidepoint(pygame.mouse.get_pos()) and not self.blocked:
           if pygame.mouse.get_pressed()[0]:
               self.fx.accept_sound(0.4)
               return True

    def draw(self, window):
        if not self.blocked:
            if self.hitbox.collidepoint(pygame.mouse.get_pos()):
                window.blit(self.button_image_on, (self.x_cord, self.y_cord))
            else:
                window.blit(self.button_image, (self.x_cord, self.y_cord))
        else:
            window.blit(self.blocked_img, (self.x_cord, self.y_cord))


'''
    For check list or options, example: musik = False 
        - if state = True                    -> tick = True
'''
class Checker_once:
    def __init__(self, x_cord, y_cord, state=False):
        self.x_cord = x_cord
        self.y_cord = y_cord
        self.field_image_false = pygame.image.load("graph/menu/checkbox_false.png")
        self.field_image_true = pygame.image.load("graph/menu/checkbox_true.png")
        self.hitbox = pygame.Rect(self.x_cord, self.y_cord, self.field_image_false.get_width(), self.field_image_false.get_height())
        self.field_state = state
        self.clock = 0

    def tick(self, delta):
        self.clock += delta
        if self.hitbox.collidepoint(pygame.mouse.get_pos()):
            if pygame.mouse.get_pressed()[0] and self.clock > 0.1:
                self.field_state = not self.field_state
                self.clock = 0

        return self.field_state

    def draw(self, window):
        if self.field_state:
            window.blit(self.field_image_true, (self.x_cord, self.y_cord))
        else:
            window.blit(self.field_image_false, (self.x_cord, self.y_cord))

    def draw_text(self, window, text, r, g, b):
        text_field = pygame.font.Font.render(pygame.font.SysFont("arial", 16), f"{text}", True, (r, g, b))
        window.blit(text_field, (self.x_cord + 40, self.y_cord + 7))


'''
    someday i'll write it but now it doesn't work
    it's checker but if u draw it more time in colum, u can keep state in just one True 
'''
class Checker_multi:
    def __init__(self, x_cord, y_cord, dis, nr):
        self.x_cord = x_cord
        self.y_cord = y_cord
        self.nr = nr
        self.dis = dis
        self.dis_iter = 0
        self.checker_list = []
        self.field_image_false = pygame.image.load("graph/menu/checkbox_false.png")
        self.field_image_true = pygame.image.load("graph/menu/checkbox_true.png")
        self.hitbox = pygame.Rect(self.x_cord, self.y_cord, self.field_image_false.get_width(), self.field_image_false.get_height())
        self.clock = 0

        for check in range(0, self.nr-1):
            if check == 0:
                self.checker_list.append(Checker_once(self.x_cord, self.y_cord + self.dis_iter, True))
            else:
                self.checker_list.append(Checker_once(self.x_cord, self.y_cord + self.dis_iter))

            self.dis_iter += self.dis

    def tick(self, delta):
        for check in self.checker_list:
            check.tick(delta)

    def draw(self, win):
        for check in self.checker_list:
            check.draw(win)


'''
    The arrow u can see it for example with wand choose in menu
        - u give the cords, list which one u want iter and if u don't want start with 1st pos, give other pos
'''
class Choose_Continu():
    def __init__(self, x_cord_R, y_cord_R, x_cord_L, y_cord_L, list, start=0):
        self.button_R = Button(x_cord_R, y_cord_R, 'graph/menu/arrow_right')
        self.button_L = Button(x_cord_L, y_cord_L, 'graph/menu/arrow_left')
        self.lenght = len(list)
        self.iterator = start
        self.clock = 0
        self.val = 0

    def tick(self, delta):
        if self.iterator < self.lenght:
            self.val = self.iterator
        if self.button_R.tick(delta):
            if self.iterator >= self.lenght - 1:
                self.iterator = 0
            else:
                self.iterator += 1
            self.clock = 0
        if self.button_L.tick(delta):
            if self.iterator <= 0:
                self.iterator = self.lenght - 1
            else:
                self.iterator -= 1
            self.clock = 0

        return self.val

    def draw(self, window):
        self.button_R.draw(window)
        self.button_L.draw(window)


'''
    !!! Stealed Code !!! it work but not perfect 
        - len=-1                                -> Infinity 
        - placeholder                           -> pass, login etc
        - submit_butt = True                    -> draw and tick submit_butt
        - it ENTER or submit_butt               -> tick = text
'''
class Text_Input:
    def __init__(self, x, y, width, height, len=-1, placeholder="", submit_butt=False, submit_butt_x=0, submit_butt_y=0):
        self.x_cord = x
        self.y_cord = y
        self.width = width
        self.height = height

        self.submit_butt = submit_butt
        self.submit = Button(submit_butt_x, submit_butt_y, 'graph/menu/buttons/button_SUBMIT')

        self.font = pygame.font.SysFont("Calibri", 20)
        self.text = ""
        self.font_image = pygame.font.Font.render(self.font, self.text, True, (0, 0, 0))
        self.placeholder = placeholder
        self.placeholder_img = pygame.font.Font.render(self.font, placeholder, True, (130, 130, 130))
        self.max_len = len
        self.active = False
        self.cursor = pygame.rect.Rect(self.x_cord + 5, self.y_cord + 5, 2, 30)
        self.cursor_vis = True

    def tick(self, clock, events, delta=0):
        text = ''
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    text = self.text
                elif event.key == pygame.K_BACKSPACE and self.active:
                    self.text = self.text[:-1]
                elif len(self.text) < self.max_len or self.max_len == -1: # max ilosc znakow, -1 = infinity
                    if self.active:
                        self.text += event.unicode
                self.font_image = pygame.font.Font.render(self.font, self.text, True, (0, 0, 0))
                text_x = self.font_image.get_width()
                self.cursor = pygame.rect.Rect(self.x_cord + 5 + text_x, self.y_cord + 5, 2, 30)
        if self.submit.tick(delta):
            text = self.text
        if pygame.mouse.get_pressed(3)[0]:
            if pygame.rect.Rect(self.x_cord, self.y_cord, self.width, self.height).collidepoint(pygame.mouse.get_pos()):
                self.active = True
            else:
                self.active = False
        if round(clock) % 2 == 0:
            self.cursor_vis = True
        else:
            self.cursor_vis = False

        return text

    def draw(self, window):
        pygame.draw.rect(window, (100, 100, 100), (self.x_cord, self.y_cord, self.width, self.height))
        if self.submit_butt:
            self.submit.draw(window)
        if self.text:
            window.blit(self.font_image, (self.x_cord + 5, self.y_cord + 10))
        else:
            window.blit(self.placeholder_img, (self.x_cord + 5, self.y_cord + 10))
        if self.cursor_vis and self.active:
            pygame.draw.rect(window, (0, 0, 0), self.cursor)


'''
    It good tool for all info boxes
        - fist 4 parameter are just hitbox 
        - there are reigt now only too sizes
'''
class Info_area:
    def __init__(self, x, y, width, height, big_box=False):
        self.text = []
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)
        self.big_box = big_box

        self.bonus_x = 100
        self.bonus_y = 200
        self.dis_between_text = 15


    def tick(self, win, text):
        self.text = text
        if self.hitbox.collidepoint(pygame.mouse.get_pos()):
            self.draw(win)

    def draw(self, win):
        if self.big_box:
            win.blit(pygame.image.load('graph/menu/info_big_box.png'), (self.x - 710, self.y + 30))
            for i in range(len(self.text)):
                text = pygame.font.Font.render(pygame.font.SysFont("arial", 20), self.text[i], True, (0, 0, 0))
                win.blit(text, (self.x - 650, self.y + 50 + i*self.dis_between_text))
        else:
            win.blit(pygame.image.load('graph/menu/info_box.png'), (self.x - self.bonus_x, self.y - self.bonus_y))
            if len(self.text) > 1:
                for i in range(len(self.text)):
                    text = pygame.font.Font.render(pygame.font.SysFont("arial", 16), self.text[i], True, (0, 0, 0))
                    win.blit(text, (self.x - self.bonus_x + 20, self.y - self.bonus_y + 30 + i*self.dis_between_text))

            elif len(self.text) == 1:
                text = pygame.font.Font.render(pygame.font.SysFont("arial", 16), self.text[0], True, (0, 0, 0))
                win.blit(text, (self.x - self.bonus_x + 20, self.y - self.bonus_y + 30))
            else:
                pass


'''
    Someday it will be Volume 
'''
class Valume:
    def __init__(self, x, y, max=100, start=0):
        self.x = x
        self.y = y
        self.max = max
        self.start = start
        self.hitbox = pygame.Rect(self.x-5, self.y-5, 110, 15)

    def tick(self):
        pass

    def draw(self, win):
        pygame.draw.rect(win, (100, 100, 100), (self.x-5, self.y-5, 110, 15))
        pygame.draw.rect(win, (70, 70, 70), (self.x, self.y, 100, 5))
        pygame.draw.circle(win, (255, 50, 50), (self.x+3, self.y+3), 8)
        pygame.draw.circle(win, (100, 100, 100), (self.x + 3, self.y + 3), 5)



