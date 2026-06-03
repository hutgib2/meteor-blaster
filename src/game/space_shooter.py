from game.settings import *
from random import randint, uniform
from game.star import Star
from game.player import Player
from game.meteor import Meteor
from game.laser import Laser
from game.explosion import Explosion

class SpaceShooter():
	def __init__(self):
		self.running = True
		self.game_paused = False
		self.clock = pygame.time.Clock()
		self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

		# import
		
		self.meteor_surf = pygame.image.load(join('src', 'images', 'meteor.png')).convert_alpha()
		self.star_surf = pygame.image.load(join('src', 'images', 'star.png')).convert_alpha()
		self.font = pygame.font.Font(join('src', 'images', 'Oxanium-Bold.ttf'), 40)
		self.explosion_frames = [pygame.image.load(join('src', 'images', 'explosion', f'{i}.png')).convert_alpha() for i in range(21)]
		self.game_music = pygame.mixer.Sound(join('src', 'audio', 'Glorious Morning.ogg'))
		self.game_music.set_volume(0.25)
		self.game_music.play(loops= -1)

		# sprites
		self.all_sprites = pygame.sprite.Group()
		self.meteor_sprites = pygame.sprite.Group()
		self.laser_sprites = pygame.sprite.Group()
		
		for i in range(20):
			Star(self.all_sprites, self.star_surf)
		self.player = Player((self.all_sprites, self.laser_sprites), self.all_sprites)

		#custom meteor event
		self.meteor_event = pygame.event.custom_type()
		pygame.time.set_timer(self.meteor_event, 400)
		
	def collisions(self):
		collision_sprites = pygame.sprite.spritecollide(self.player, self.meteor_sprites, True, pygame.sprite.collide_mask)
		if collision_sprites:
			self.running = False

		for laser in self.laser_sprites:
			collision = pygame.sprite.spritecollide(laser, self.meteor_sprites, True)
			if collision:
				laser.kill()
				Explosion(self.explosion_frames, laser.rect.midtop, self.all_sprites)

	def display_score(self):
		current_time = int(pygame.time.get_ticks() / 1000)
		self.text_surf = self.font.render(str(current_time), True, '#F0F0F0')
		self.text_rect = self.text_surf.get_frect(midbottom = (WINDOW_WIDTH / 2, 100))
		self.display_surface.blit(self.text_surf, self.text_rect)
		pygame.draw.rect(self.display_surface, '#F0F0F0', self.text_rect.inflate(20, 10).move(0, -6), 5, 10)

	async def run(self):
		while self.running:
			dt = self.clock.tick() / 1000 # getting the delta time in seconds
			await asyncio.sleep(0)
			
			#event tracker
			for event in pygame.event.get():
				if event.type == pygame.KEYDOWN and event.key == pygame.K_p:  
					self.game_paused = not self.game_paused
				if event.type == pygame.QUIT: # when x clicked , exit loop
					self.running = False
				if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
					self.running = False
				if event.type == self.meteor_event and not self.game_paused:
					Meteor((self.all_sprites, self.meteor_sprites), self.meteor_surf)

			if self.game_paused:
				continue

			self.all_sprites.update(dt)  
			self.collisions()

			#colours the background and draws the stars
			self.display_surface.fill('#3a2e3f')
			self.all_sprites.draw(self.display_surface)
			self.display_score()
			
			pygame.display.update()