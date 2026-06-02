from game.settings import *

class Laser(pygame.sprite.Sprite):
    def __init__(self,surf,pos,groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(midbottom = pos)
        laser_sound.play()

    def update(self, dt):
        self.rect.centery -= 1000 * dt
        if self.rect.bottom < 0:
            self.kill()