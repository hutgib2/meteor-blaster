import asyncio
import pygame

from game.settings import *
from random import choice
from game.player import Player
from game.meteor import Meteor
from game.explosion import Explosion

from utils.timer import Timer
from utils.file_importer import load_images
from utils.async_clock import AsyncClock


class MeteorBlaster:
    def __init__(self):
        self.running = True
        self.game_paused = False
        self.clock = AsyncClock()
        self.start_time = pygame.time.get_ticks()
        self.score = 0
        self.spawn_rate = 500

        # import
        self.background_surf = pygame.image.load(
            join("assets", "images", "space_background.jpg")
        )
        self.background_rect = self.background_surf.get_frect(
            center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
        )

        self.font = pygame.font.Font(join("assets", "fonts", "Oxanium-Bold.ttf"), 40)
        self.explosion_frames = load_images(
            "assets", "animations", "explosion", scale=0.3
        )
        self.meteor_surfs = load_images("assets", "images", "meteors")

        # audio
        self.game_music = pygame.mixer.Sound(
            join("assets", "audio", "Glorious Morning.ogg")
        )
        self.game_music.set_volume(0.25)
        self.game_music.play(loops=-1)

        # sprites
        self.all_sprites = pygame.sprite.Group()
        self.meteor_sprites = pygame.sprite.Group()
        self.laser_sprites = pygame.sprite.Group()
        self.player = Player((self.all_sprites, self.laser_sprites), self.all_sprites)

        # create meteor timer
        self.meteor_timer = Timer(
            self.spawn_rate,
            lambda: Meteor(
                choice(self.meteor_surfs), (self.all_sprites, self.meteor_sprites)
            ),
            repeat=True,
            autostart=True,
        )
        self.spawn_rate_timer = Timer(
            1000,
            lambda: self.decrement_spawn_rate_timer(1),
            repeat=True,
            autostart=True,
        )

    # create a new timer with an updated spawn rate
    def decrement_spawn_rate_timer(self, decrement):
        if self.spawn_rate > 100:
            self.spawn_rate -= decrement
            self.meteor_timer = Timer(
                self.spawn_rate,
                lambda: Meteor(
                    choice(self.meteor_surfs), (self.all_sprites, self.meteor_sprites)
                ),
                repeat=True,
                autostart=True,
            )

    def collisions(self):
        collision_sprites = pygame.sprite.spritecollide(
            self.player, self.meteor_sprites, True, pygame.sprite.collide_mask
        )
        if collision_sprites:
            self.running = False

        for laser in self.laser_sprites:
            collision = pygame.sprite.spritecollide(laser, self.meteor_sprites, True)
            if collision:
                laser.kill()
                Explosion(self.explosion_frames, laser.rect.midtop, self.all_sprites)
                self.score += 5
                self.decrement_spawn_rate_timer(5)

    def display_score(self):
        current_time = (pygame.time.get_ticks() - self.start_time) // 1000
        total_score = current_time + self.score
        self.text_surf = self.font.render(str(total_score), True, "#F0F0F0")
        self.text_rect = self.text_surf.get_frect(midbottom=(WINDOW_WIDTH / 2, 100))
        screen.blit(self.text_surf, self.text_rect)
        pygame.draw.rect(
            screen, "#F0F0F0", self.text_rect.inflate(20, 10).move(0, -6), 5, 10
        )

    async def run(self):
        while self.running:
            dt = await self.clock.tick() / 1000
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                    self.game_paused = not self.game_paused
                if event.type == pygame.QUIT:  # when x clicked , exit loop
                    self.running = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.running = False

            if self.game_paused:
                continue

            self.all_sprites.update(dt)
            self.meteor_timer.update()
            self.spawn_rate_timer.update()
            self.collisions()

            screen.blit(self.background_surf, self.background_rect)
            self.all_sprites.draw(screen)
            self.display_score()
            pygame.display.update()

        self.game_music.stop()
