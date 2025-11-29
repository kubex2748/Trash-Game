import pygame


class Physic:
    def __init__(self, x, y, width, height, acc, max_vel, colision=True):
        self.x_cord = x  # współrzędna x
        self.y_cord = y  # współrzędna y
        self.hor_velocity = 0  # prędkość w poziomie
        self.ver_velocity = 0  # prędkość w pionie
        self.acc = acc  # przyspieszenie
        self.is_coll = colision
        self.max_vel = max_vel  # maksymalna prędkość
        self.width = width  # szerokość
        self.height = height  # wysokość
        self.previous_x = x
        self.previous_y = y
        self.hitbox = pygame.Rect(self.x_cord, self.y_cord, self.width, self.height)
        self.gravity = 0.8
        self.jumping = False


    def physic_tick(self, walls):
        self.ver_velocity += self.gravity
        self.x_cord += self.hor_velocity
        self.y_cord += self.ver_velocity
        self.hitbox = pygame.Rect(self.x_cord, self.y_cord, self.width, self.height)  # odświeżanie hitboxa
        for wall in walls:
            if wall.is_floor or not wall.is_floor and self.is_coll:
                if wall.hitbox.colliderect(self.hitbox):  # cofanie obiektu do miejsca z poprzedniej klatki
                    if self.x_cord + self.width >= wall.x_cord + 1 > self.previous_x + self.width:  # kolizja z prawej strony
                        self.x_cord = self.previous_x
                        self.hor_velocity = 0
                    if self.x_cord <= wall.x_cord + wall.width - 1 < self.previous_x:  # kolizja z lewej strony
                        self.x_cord = self.previous_x
                        self.hor_velocity = 0
                    if self.y_cord + self.height >= wall.y_cord + 1 > self.previous_y + self.height:  # kolizja z dołu
                        self.y_cord = self.previous_y
                        self.ver_velocity = 0
                        self.jumping = False
                    if self.y_cord <= wall.x_cord + wall.width - 1 < self.previous_y:  # kolizja z góry
                        self.y_cord = self.previous_y
                        self.ver_velocity = 0

        self.previous_x = self.x_cord
        self.previous_y = self.y_cord