from game.settings import *
from game.support import *
from game.laser import Laser               

class Player(pygame.sprite.Sprite):
    def __init__(self, laser_groups, groups):
        super().__init__(groups)
        self.original_surf = image_importer('assets', 'images', 'ufo.png', scale_factor=0.25)
        self.image = self.original_surf
        self.rect = self.image.get_frect(center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 1.1))
        self.direction = pygame.math.Vector2(0, 0)
        self.speed = 1000
        self.laser_groups = laser_groups

        # rotation
        self.rotation = 0
        self.max_rotation = 15
        self.rotation_speed = 150
        self.recover_speed = 150

        # laser cooldown
        self.can_shoot = True
        self.laser_shoot_time = 0
        self.cooldown_duration = 250
        
    # initializing methods
    def laser_timer(self):
        if self.can_shoot == False:
            current_time = pygame.time.get_ticks()
            if current_time - self.laser_shoot_time >= self.cooldown_duration:
                self.can_shoot = True

    def update(self, dt):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])     
        # self.direction.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])
        # if self.direction:
        #     self.direction = self.direction.normalize()
        
        if self.direction.x:
            self.rotation += self.direction.x * self.rotation_speed * -1 * dt
            self.rotation = max(-1 * self.max_rotation, min(self.max_rotation, self.rotation))
        else: # make it rotate to its original angle when not moving
            if self.rotation >= 0:
                self.rotation -= self.recover_speed * dt
            elif self.rotation <= 0:
                self.rotation += self.recover_speed * dt

        self.image = pygame.transform.rotozoom(self.original_surf, self.rotation, 1)
        self.rect = self.image.get_frect(center = self.rect.center)
        
        self.rect.center += self.direction * self.speed * dt
        self.rect.centerx = max(0, min(WINDOW_WIDTH, self.rect.centerx))

        recent_keys = pygame.key.get_pressed()
        if recent_keys[pygame.K_SPACE] and self.can_shoot:
            Laser(self.rect.midtop, self.laser_groups)
            self.can_shoot = False
            self.laser_shoot_time = pygame.time.get_ticks()

        self.laser_timer()