import pygame, sys
from pygame.locals import *

pygame.init()

SURFACE = pygame.display.set_mode((500,400),True,32)
pygame.display.set_caption("Drawning")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0 , 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0, 128)

SURFACE.fill(WHITE)

#Parâmetros (superficie, cor, coordenadas (x,y)... )
#O argumento referente a espessura pode ser omitido ficando 0
pygame.draw.polygon(SURFACE, GREEN,((146, 0),(291, 306), (236, 277), (56, 277), (0, 106) ), 0)

#Parâmetros (superficie, cor, coordenadas (x1,y1),(x2,y2), espessura linha )
#O argumento referente a espessura pode ser omitido ficando 1
pygame.draw.line(SURFACE, BLUE, (60,60), (120, 60), 4 )
pygame.draw.line(SURFACE, BLUE, (120,60), (60, 120) )
pygame.draw.line(SURFACE, BLUE, (60,120), (120, 120), 4 )

#Parâmetros (superficie, cor, coordenadas (x1,y1),largura, espessura )
#O argumento referente a espessura pode ser omitido ficando 0
pygame.draw.circle(SURFACE, BLUE, (300, 100), 20, 0) 

#Parâmetros (superficie, cor, coordenadas (x1,y1),(x2,y2),largura, espessura )
#O argumento referente a espessura pode ser omitido ficando 0
pygame.draw.ellipse(SURFACE, RED, (300, 250, 40, 80),1)

#Parâmetros (superficie, cor, coordenadas (x1,y1, largura, altura), espessura )
#O argumento referente a espessura pode ser omitido ficando 0
pygame.draw.rect(SURFACE, RED, (200, 150, 100, 50),2)

pixObj = pygame.PixelArray(SURFACE)
pixObj[480][380] = BLACK
pixObj[482][382] = BLACK
pixObj[484][384] = BLACK
pixObj[486][386] = BLACK
pixObj[488][388] = BLACK
del pixObj

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()