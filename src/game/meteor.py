from game.settings import *
from random import randint, uniform

class Meteor(pygame.sprite.Sprite):
    def __init__(self, groups, surf):
        super().__init__(groups)
        self.scale_factor = uniform(1, 1.5)
        self.original_surf = pygame.transform.smoothscale(surf,(101*self.scale_factor,84*self.scale_factor)) 
        self.image = self.original_surf
        self.rect = (self.image.get_frect(center = (randint(0, WINDOW_WIDTH), 0)))
        self.direction = pygame.Vector2(uniform(-0.5, 0.5), 1)
        self.speed = randint(900,1000)
        self.rotation_speed = randint(100,200)
        self.rotation = 0

    def update(self, dt):
        self.rect.center += self.direction * self.speed * dt
        if self.rect.top >= WINDOW_HEIGHT:
            self.kill()
        self.rotation += self.rotation_speed * dt
        self.image = pygame.transform.rotozoom(self.original_surf, self.rotation, 1)
        self.rect = self.image.get_frect(center = self.rect.center)