import asyncio
import pygame

from game.settings import *
from game.space_shooter import SpaceShooter

async def main():
    game = SpaceShooter()
    await game.run()
    pygame.quit()

asyncio.run(main())