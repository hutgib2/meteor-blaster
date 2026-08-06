from game.settings import *
from game.space_shooter import SpaceShooter
import asyncio

class Menu:
    def __init__(self):
        self.home_screen_image = pygame.transform.scale(pygame.image.load(join('assets', 'images', 'menu.png')), (WINDOW_WIDTH, WINDOW_HEIGHT))
        self.running = True
        self.background = self.home_screen_image
        self.font = pygame.font.Font(join('assets', 'images', 'Oxanium-Bold.ttf'), 40)
        self.pending_game = None
        
        # Draw homescreen
        screen.blit(self.background, (0, 0))
        pygame.display.update()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.pending_game = SpaceShooter()
            if event.type == pygame.QUIT:
                self.running = False

    async def run(self):
        while self.running:
            self.handle_events()
            screen.blit(self.background, (0, 0))
            pygame.display.update()
            await asyncio.sleep(0)

            if self.pending_game:
                await self.pending_game.run()
                self.pending_game = None