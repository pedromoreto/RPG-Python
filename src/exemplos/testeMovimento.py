import sys, pygame
from pygame.locals import *

pygame.init()
FPS = 30
LARGURA = 800
ALTURA = 600

TELA = pygame.display.set_mode((LARGURA, ALTURA),0,0)
pygame.display.set_caption("Teste Sprite")
TELA.convert_alpha()
fpsClock = pygame.time.Clock()

x = int(LARGURA /2)
y = int(ALTURA /2)

isStop = False
frameCounter = 0
frameUsing = 0

heroImg = []

heroImg.append(pygame.image.load("../../resources/sprites/sprite_1.png"))
heroImg.append(pygame.image.load("../../resources/sprites/sprite_2.png"))
heroImg.append(pygame.image.load("../../resources/sprites/sprite_3.png"))
heroImg.append(pygame.image.load("../../resources/sprites/sprite_4.png"))
heroImg.append(pygame.image.load("../../resources/sprites/sprite_5.png"))

DIMENSAO_HEROI = 64

heroImg[0] = pygame.transform.scale(heroImg[0], (DIMENSAO_HEROI, DIMENSAO_HEROI))
heroImg[1] = pygame.transform.scale(heroImg[1], (DIMENSAO_HEROI, DIMENSAO_HEROI))
heroImg[2] = pygame.transform.scale(heroImg[2], (DIMENSAO_HEROI, DIMENSAO_HEROI))
heroImg[3] = pygame.transform.scale(heroImg[3], (DIMENSAO_HEROI, DIMENSAO_HEROI))
heroImg[4] = pygame.transform.scale(heroImg[4], (DIMENSAO_HEROI, DIMENSAO_HEROI))


incrementoAndar = 4
animation = True
contadorFrame = 20
# 'left' or 'right'
direction = 'right'
RED = (255, 0, 0, 128)
BRANCO = (255, 255, 255)

showColision = False

pygame.key.set_repeat(1, 10)

while True:

    direcaoAtual = direction
    animation = False
    TELA.fill(BRANCO)
    for event in pygame.event.get():
        if event.type == QUIT or ( event.type == KEYDOWN and event.key == K_ESCAPE ):
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            keys = pygame.key.get_pressed()
            if keys[K_LSHIFT]:
                showColision = not showColision
            #Quando uma tecla de movimento for acionada a animação irá começar
            if keys[K_RIGHT]:
                x += incrementoAndar
                print("Right!!!")
                if direction == 'left':
                    direction = 'right'
                animation = True
            if keys[K_LEFT]:
                x -= incrementoAndar
                print("Left!!!")
                if direction == 'right':
                    direction = 'left'
                animation = True
            if keys[K_UP]:
                y -= incrementoAndar
                print("Up!!!")
                animation = True
            if keys[K_DOWN]:
                y += incrementoAndar
                print("Down!!!")
                animation = True
        elif event.type == pygame.KEYUP:
            keys = pygame.key.get_pressed()
            #Quando uma tecla de movimento for acionada a animação irá começar
            if keys[K_RIGHT]:
                animation = False
            if keys[K_LEFT]:
                animation = False
            if keys[K_UP]:
                animation = False
            if keys[K_DOWN]:
                animation = False

    if x > LARGURA:
        x = -100
    if x < -100:
        x = LARGURA
    if y > ALTURA:
        y = -100
    if y < -100:
        y = ALTURA

    if direcaoAtual != direction:
        heroImg[0] = pygame.transform.flip(heroImg[0], True, False)
        heroImg[1] = pygame.transform.flip(heroImg[1], True, False)
        heroImg[2] = pygame.transform.flip(heroImg[2], True, False)
        heroImg[3] = pygame.transform.flip(heroImg[3], True, False)
        heroImg[4] = pygame.transform.flip(heroImg[4], True, False)

    TELA.blit(heroImg[frameUsing], (x, y) )

    if showColision:
        quadrado = pygame.Surface((DIMENSAO_HEROI-20,DIMENSAO_HEROI -5), pygame.SRCALPHA)
        quadrado.fill(RED)
        TELA.blit(quadrado, (x+10, y+5) )

    if animation:
        frameCounter += contadorFrame
        if frameCounter > 100:
            frameCounter = 0
            frameUsing += 1

        if frameUsing > 4:
            frameUsing = 0
            animation = False

    pygame.display.update()
    fpsClock.tick(FPS)
#     Loop do Jogo

