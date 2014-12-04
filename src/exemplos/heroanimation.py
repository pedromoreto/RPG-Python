import pygame, sys
from pygame.locals import *

pygame.init()

FPS = 30
fpsClock = pygame.time.Clock()

SURFACE = pygame.display.set_mode((400,300), 0, 32)

pygame.display.set_caption("Animation")

WHITE = (255, 255, 255)

RIGHT = 'right'
LEFT = 'left'
DOWN = 'down'
UP = 'up'
MOVE = 5

heroImg = pygame.image.load("../../resources/sprite.png")
heroImg = pygame.transform.scale(heroImg, (64,64))


heroX = 10
heroY = 10
heroDirection = RIGHT
SURFACE.convert_alpha()
while True:
    SURFACE.fill(WHITE)
    
    if heroDirection == RIGHT:
        heroX += MOVE
        if heroX == 280:
            heroDirection = DOWN
    elif heroDirection == DOWN:
        heroY += MOVE
        if heroY == 220:
            heroDirection = LEFT
    elif heroDirection == LEFT:
        heroX -= MOVE
        if heroX == 10:
            heroDirection = UP
    elif heroDirection == UP:
        heroY -= MOVE
        if heroY == 10:
            heroDirection = RIGHT
    
    SURFACE.blit(heroImg, (heroX, heroY) )
    
    for event in pygame.event.get() :
        if event.type == QUIT :
            pygame.quit()
            sys.exit()
    pygame.display.update()
    fpsClock.tick(FPS)           