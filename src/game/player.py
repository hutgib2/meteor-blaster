from game.settings import *

class Player(pygame.sprite.Sprite): # defining a player class and inheriting from sprite class
    # initializing attributes
    def __init__(self, groups):             # initializing player class
        super().__init__(groups)          # initializing parent class
        self.image = pygame.image.load(join('src', 'images', 'player.png')).convert_alpha()
        self.rect = self.image.get_frect(center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 1.1))
        self.direction = pygame.math.Vector2(0, 0)
        self.speed = 1000

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
        self.direction.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])
        if self.direction:
            self.direction = self.direction.normalize()
        self.rect.center += self.direction * self.speed * dt

        recent_keys = pygame.key.get_just_pressed()
        if recent_keys[pygame.K_SPACE] and self.can_shoot:
            Laser(laser_surf, self.rect.midtop, (all_sprites, laser_sprites))
            self.can_shoot = False
            self.laser_shoot_time = pygame.time.get_ticks()

        self.laser_timer()