from game.settings import *
from game.meteor_blaster import MeteorBlaster
import asyncio

class Menu:
    def __init__(self):
        self.home_screen_image = pygame.transform.scale(pygame.image.load(join('assets', 'images', 'space_background.jpg')), (WINDOW_WIDTH, WINDOW_HEIGHT))
        self.background = self.home_screen_image
        self.pending_game = None
        self.running = True
        
        self.font = pygame.font.Font(join('assets', 'fonts', 'Oxanium-Bold.ttf'), 40)
        self.text_surf = self.font.render("Press enter to play", True, '#F0F0F0')
        self.text_rect = self.text_surf.get_frect(center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
        
        self.title_font = pygame.font.Font(join('assets', 'fonts', 'Oxanium-Bold.ttf'), 100)
        self.title_surf = self.title_font.render("Meteor Blaster", True, "#00FFFF")
        self.title_rect = self.title_surf.get_frect(center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 6))
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.pending_game = MeteorBlaster()
            if event.type == pygame.QUIT:
                self.running = False

    async def run(self):
        while self.running:
            self.handle_events()
            screen.blit(self.background, (0, 0))
            screen.blit(self.text_surf, self.text_rect)
            screen.blit(self.title_surf, self.title_rect)
            
            pygame.display.update()
            await asyncio.sleep(0)

            if self.pending_game:
                await self.pending_game.run()
                self.pending_game = None