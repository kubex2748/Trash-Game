import pygame
from random import randint
from Informations import Sounds

pygame.mixer.init()

pygame.init()
pygame.mixer.init()
## --- Muzyka w tle (MP3) ---
#pygame.mixer.music.load("muzyka.mp3")
#pygame.mixer.music.play()


class FX:
    def __init__(self, FX_active=True):
        self.activ = FX_active
        self.sounds = Sounds()

        self.clock_G = 0
        self.clock_Z = 0
        self.clock_S = 0
        self.clock_L = 0

    def error_sound(self, volume):
        shoot_sound = pygame.mixer.Sound(f'{self.sounds.FX_other[4]}.wav')
        shoot_sound.set_volume(volume)
        shoot_sound.play()

    def accept_sound(self, volume):
        shoot_sound = pygame.mixer.Sound(f'{self.sounds.FX_other[5]}.wav')
        shoot_sound.set_volume(volume)
        shoot_sound.play()

    def spell_sound(self, spell_id, volume):
        if self.activ:
            shoot_sound = pygame.mixer.Sound(f'{self.sounds.FX_spells[spell_id]}.wav')
            shoot_sound.set_volume(volume)
            shoot_sound.play()

    def wand_shot_sound(self, wand_id, volume):
        if self.activ:
            shoot_sound = pygame.mixer.Sound(f'{self.sounds.FX_wand_shot[wand_id]}.wav')
            shoot_sound.set_volume(volume)
            shoot_sound.play()

    def mele_hit_sound(self, volume):
        if self.activ:
            sound = pygame.mixer.Sound('sound/FX/things/hit_1.wav')
            sound.set_volume(volume)
            sound.play()

    def open_wave_sound(self):
        if self.activ:
            sound = pygame.mixer.Sound('sound/FX/things/open_drums.wav')
            sound.set_volume(1)
            sound.play()

#########################################################################################################################################################

    '''
        id = wand_id
    '''

    def global_spel_sounds(self, id):
        if id > 0:
            sound = pygame.mixer.Sound(f'{self.sounds.FX_global_spells[id]}.wav')
            sound.set_volume(0.5)
            sound.play()


#########################################################################################################################################################


    def zombie_sound(self, delta):
        if self.activ:
            pause = randint(3, 7)
            sound_index = randint(1, 7)
            zombie_sound = pygame.mixer.Sound(f'sound/FX/undeads/zombie_{sound_index}.wav')
            zombie_sound.set_volume(0.4)
            self.clock_Z += delta
            if self.clock_Z > pause:
                zombie_sound.play()
                self.clock_Z = 0

    def ghost_sound(self, delta):
        if self.activ:
            pause = randint(5, 8)
            sound_index = randint(1, 3)
            ghost_sound = pygame.mixer.Sound(f'sound/FX/undeads/ghost_{sound_index}.wav')
            ghost_sound.set_volume(0.4)
            self.clock_G += delta
            if self.clock_G > pause:
                ghost_sound.play()
                self.clock_G = 0

    def skeleton_sound(self, delta):
        if self.activ:
            pause = randint(2, 4)
            sound_index = randint(1, 4)
            skeleton_sound = pygame.mixer.Sound(f'sound/FX/undeads/skeleton_{sound_index}.wav')
            skeleton_sound.set_volume(0.4)
            self.clock_S += delta
            if self.clock_S > pause:
                skeleton_sound.play()
                self.clock_S = 0

    def lich_sound(self, delta):
        if self.activ:
            pause = randint(2, 8)
            sound_index = randint(1, 4)
            lich_sound = pygame.mixer.Sound(f'sound/FX/undeads/lich_{sound_index}.wav')
            lich_sound.set_volume(0.4)
            self.clock_L += delta
            if self.clock_L > pause:
                lich_sound.play()
                self.clock_L = 0











