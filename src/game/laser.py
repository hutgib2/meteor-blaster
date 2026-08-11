from game.settings import *
from game.support import *

# laser_surf = pygame.image.load(join('assets', 'images', 'double_laser.png')).convert_alpha()
laser_surf = image_importer('assets', 'images', 'double_laser.png', scale_factor=0.05)
laser_sound = pygame.mixer.Sound(join('assets', 'audio', 'damage.ogg'))
laser_sound.set_volume(0.2)

class Laser(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.image = laser_surf
        self.rect = self.image.get_frect(midbottom = pos)
        laser_sound.play()

    def update(self, dt):
        self.rect.centery -= 1000 * dt
        if self.rect.bottom < 0:
            self.kill()