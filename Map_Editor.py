import pygame
from Menu import Button, Choose_Continu
import tkinter as tk
from tkinter import filedialog, colorchooser

window = pygame.display.set_mode((1920, 1080))
pygame.init()

'''
    Yes u can just copy it and Interpreting but it is loser way to use it, search for password is not that hard
'''

class Editor:
    def __init__(self, img=''):
        self.ADD_button = Button(100, 980, "graph/menu/buttons/button_ADD")
        self.COLOR_button = Button(250, 980, "graph/menu/buttons/button_COLOR")
        self.PRINT_button = Button(400, 980, "graph/menu/buttons/button_PRINT")

        self.path = img
        self.image = pygame.image.load('graph/spels/none_icon.png')
        self.run = False
        self.editor_menu_active = False
        self.clock = 0

        self.R, self.G, self.B = 0, 0, 0
        self.walls_colors = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
        ]
        self.walls = [
            [0, 0, 1920, 1],    # roof
            [0, 0, 1, 930],     # left wall
            [1920, 0, 1, 930],   # right wall
        ]

        self.arrows = Choose_Continu(600, 980, 550, 980, self.walls)

        self.draw_prototyp = False
        self.x_start = 0
        self.y_start = 0
        self.x_stop = 0
        self.y_stop = 0

        self.wall_width = 0
        self.wall_height = 0
        self.wall_start_x = 0
        self.wall_start_y = 0

        self.x_mouse = 0
        self.y_mouse = 0

        self.add_value = 10

        self.ignore_first_up = True

    def print_tab(self):
        print('----------------------------------')
        for w in range(0, len(self.walls)):
            print(f'[{self.walls[w][0]}, {self.walls[w][1]}, {self.walls[w][2]}, {self.walls[w][3]}, {self.walls_colors[w][0]}, {self.walls_colors[w][1]}, {self.walls_colors[w][2]}]')

    def add_wall(self, x, y, w, h):
        self.walls.append([x, y, w, h])
        self.walls_colors.append([self.R, self.G, self.B])

    def set_wall_pos(self):
        if self.x_start < self.x_stop:
            self.wall_width = self.x_stop - self.x_start
            self.wall_start_x = self.x_start
        if self.x_start > self.x_stop:
            self.wall_width = self.x_start - self.x_stop
            self.wall_start_x = self.x_stop
        if self.y_start < self.y_stop:
            self.wall_height = self.y_stop - self.y_start
            self.wall_start_y = self.y_start
        if self.y_start > self.y_stop:
            self.wall_height = self.y_start - self.y_stop
            self.wall_start_y = self.y_stop

    def start(self):
        while self.run:
            if not self.path == '':
                window.blit(self.image, (0, 0))
            else:
                pygame.draw.rect(window, (130, 130, 130), pygame.Rect(0, 0, 1920, 930))
            pygame.draw.rect(window, (50, 50, 50), pygame.Rect(0, 930, 1920, 250))

            delta = pygame.time.Clock().tick(120)  # maksymalnie 120 fps
            self.clock += delta
            keys = pygame.key.get_pressed()

            mouse_pos = pygame.font.Font.render(pygame.font.SysFont("arial", 16), f"x: {self.x_mouse} | y: {self.y_mouse}", True, (45, 227, 48))
            add_value_pointer = pygame.font.Font.render(pygame.font.SysFont("arial", 16), f"value: {self.add_value}", True, (45, 227, 48))
            self.x_mouse, self.y_mouse = pygame.mouse.get_pos()

            if keys[pygame.K_w] and self.wall_start_y > 0:
                self.wall_height += self.add_value
                self.wall_start_y -= self.add_value
            if keys[pygame.K_s] and self.wall_start_y < 930:
                self.wall_height -= self.add_value
                self.wall_start_y += self.add_value
            if keys[pygame.K_d] and self.wall_start_x < 1920:
                self.wall_width += self.add_value
            if keys[pygame.K_a] and self.wall_start_x > 0:
                self.wall_width -= self.add_value

            if keys[pygame.K_UP]:
                self.wall_start_y -= self.add_value
            if keys[pygame.K_DOWN]:
                self.wall_start_y += self.add_value
            if keys[pygame.K_LEFT]:
                self.wall_start_x -= self.add_value
            if keys[pygame.K_RIGHT]:
                self.wall_start_x += self.add_value


            self.wall = pygame.Rect(
                self.wall_start_x,
                self.wall_start_y,
                self.wall_width,
                self.wall_height
            )

            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:  # jeśli gracz zamknie okienko
                    self.run = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.editor_menu_active = not self.editor_menu_active

                if not self.editor_menu_active and self.y_mouse < 930:
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        self.x_start = self.x_mouse
                        self.y_start = self.y_mouse
                        self.draw_prototyp = False
                    if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                        if self.ignore_first_up:
                            self.ignore_first_up = False
                            continue  # pomiń pierwszy UP po starcie
                        self.x_stop = self.x_mouse
                        self.y_stop = self.y_mouse
                        self.draw_prototyp = True
                        self.set_wall_pos()
                if event.type == pygame.MOUSEBUTTONDOWN and self.draw_prototyp:
                    if event.button == 4 and self.add_value < 200:  # scroll up
                        self.add_value += 1
                    elif event.button == 5 and self.add_value > 1:  # scroll down
                        self.add_value -= 1

            #self.scrol_bar.tick(events, pygame.mouse.get_pos())
            #self.scrol_bar.draw(window)

            if self.draw_prototyp:
                pygame.draw.rect(window, (self.R, self.G, self.B), self.wall)

            for wall in range(0, len(self.walls)):
                pygame.draw.rect(window, (self.walls_colors[wall][0], self.walls_colors[wall][1], self.walls_colors[wall][2]), (self.walls[wall][0], self.walls[wall][1], self.walls[wall][2], self.walls[wall][3]))

            if self.ADD_button.tick(delta) and self.draw_prototyp:
                self.draw_prototyp = False
                self.add_wall(self.wall_start_x, self.wall_start_y, self.wall_width, self.wall_height)
                self.wall_start_x = 0
                self.wall_start_y = 0
                self.wall_width = 0
                self.wall_height = 0
            self.ADD_button.draw(window)

            if self.COLOR_button.tick(delta):
                self.editor_menu_active = False
                root = tk.Tk()
                root.withdraw()
                color = colorchooser.askcolor(title="COLOR PICKER")
                if color[1] is not None:  # color[1] to kolor w HEX, np. '#ffcc00'
                    hex_color = color[1]
                    self.R, self.G, self.B = [int(hex_color[i:i + 2], 16) for i in (1, 3, 5)]
                continue
            self.COLOR_button.draw(window)

            if self.PRINT_button.tick(delta):
                self.print_tab()
            self.PRINT_button.draw(window)

            self.arrows.tick(delta)
            self.arrows.draw(window)

            if self.y_mouse < 930 and not self.editor_menu_active:
                window.blit(mouse_pos, (self.x_mouse + 20, self.y_mouse + 20))
            if self.draw_prototyp:
                window.blit(add_value_pointer, (self.x_mouse + 20, self.y_mouse + 40))

            if self.editor_menu_active:
                pause_image = pygame.image.load("graph/menu/editor_menu.png")
                START_button = Button(950, 300, "graph/menu/buttons/button_START")
                IMPORT_button = Button(950, 380, "graph/menu/buttons/button_IMPORT")
                EXTI_button = Button(950, 700, "graph/menu/buttons/button_EXIT")

                if START_button.tick(delta):
                    pass
                if IMPORT_button.tick(delta):
                    root = tk.Tk()
                    root.withdraw()

                    self.path = filedialog.askopenfilename(
                        title="Wybierz plik mapy",
                        filetypes=[("Map files", "*.json"), ("All files", "*.*")]
                    )

                    self.image = pygame.image.load(self.path)
                if EXTI_button.tick(delta):
                    self.run = False


                window.blit(pause_image, (800, 200))
                START_button.draw(window)
                IMPORT_button.draw(window)
                EXTI_button.draw(window)
                pygame.display.update()
                continue

            pygame.display.update()




