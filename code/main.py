import pygame
from os.path import join
from random import randint

pygame.init()

# create a screen and set the caption
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Space Shooter") 

#player icon surface
player_surf = pygame.image.load(join('..', 'images', 'player.png')).convert_alpha()
player_rect = player_surf.get_frect(center = (randint(10, WINDOW_WIDTH - 10), randint(10, WINDOW_HEIGHT - 10)))

# loading star image and generating 20 random coordinates
star_surf = pygame.image.load(join('..', 'images', 'star.png')).convert_alpha()
star_positions = [(randint(0, WINDOW_WIDTH), randint(0, WINDOW_HEIGHT)) for i in range(20)]

meteor_surf = pygame.image.load(join('..', 'images', 'meteor.png')).convert_alpha()
meteor_rect = meteor_surf.get_frect(center = (640, 360))

laser_surf = pygame.image.load(join('..', 'images', 'laser.png')).convert_alpha()
laser_rect = laser_surf.get_frect(bottomleft = (20, 700))

running = True
clock = pygame.time.Clock()
speed = 0.5
x_direction = 1
y_direction = -1
while running:
    clock.tick(0)
    #event tracker
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # when x clicked , exit loop
            running = False

    #colours the background and draws the stars
    display_surface.fill('navajowhite4')
    for coord in star_positions:
        display_surface.blit(star_surf, coord)

    # Makes player bounce around the screen
    player_rect.x += x_direction * speed
    if player_rect.right > WINDOW_WIDTH or player_rect.left < 0:
        x_direction *= -1
    player_rect.y += y_direction * speed
    if player_rect.bottom > WINDOW_HEIGHT or player_rect.top < 0:
        y_direction *= -1

    #stop player moving if he touches corner perfectly
    if player_rect.left <= 0 and player_rect.top <= 0:
        speed = 0
    if player_rect.right >= WINDOW_WIDTH and player_rect.bottom >= WINDOW_HEIGHT:
        speed = 0
    if player_rect.left <= 0 and player_rect.bottom >= WINDOW_HEIGHT:
        speed = 0
    if player_rect.right >= WINDOW_WIDTH and player_rect.top <= 0:
        speed = 0
    
 
    # draws the player, metoer and laser
    display_surface.blit(meteor_surf, meteor_rect)
    display_surface.blit(laser_surf, laser_rect)
    display_surface.blit(player_surf, player_rect)
    pygame.display.update()


pygame.quit()
