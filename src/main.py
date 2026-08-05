import asyncio
import pygame
from game.space_shooter import SpaceShooter

async def main():
    # print("STARTING...")
    game = SpaceShooter()

    # print("CREATED GAME...")
    await game.run()
    # pygame.quit()

asyncio.run(main())