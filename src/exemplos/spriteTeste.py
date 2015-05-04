# *-* coding: utf-8 *-*
import  pygame, sys
from pygame.locals import *
from requests.api import head


pygame.init()

TELA = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Teste Sprite")

def desenhaTile():

    tileset = pygame.image.load("../../resources/map/basis.png").convert()
    largura = 16
    altura = 16
    #Criar a superfície onde irá ficar o tile
    tile = pygame.Surface([largura, altura]).convert()
    # Copiar o sprite da imagem na posição X e Y com largura e altura
    x = 16 * 19
    y = 16 * 8
    tile.blit(tileset, (0, 0), (x, y, largura, altura))

    # Assundo que o Preto é a cor transparente
    BLACK    = (0,   0,   0, 255)
    tile.set_colorkey(BLACK)
    tile = tile.convert()
    tile = pygame.transform.scale(tile, (64, 64))
    return tile

class Tile(pygame.sprite.Sprite):
    _tileset = None

    def __init__(self, imagem, x, y, largura, altura, opacidade = 255):
        pygame.sprite.Sprite.__init__(self)
        self._tileset = pygame.image.load(imagem).convert()
        tile = pygame.Surface([largura, altura],pygame.SRCALPHA).convert()
        # Copiar o sprite da imagem na posição X e Y com largura e altura
        tile.blit(self._tileset, (0, 0), (x, y, largura, altura))
        COR_TRANSPARENCIA = (0, 0, 0)
        tile.set_colorkey(COR_TRANSPARENCIA)
        tile.set_alpha(opacidade)
        self.image = tile.convert()
        self.image = pygame.transform.scale(self.image, (64, 64))
        self.rect = self.image.get_rect()
        

    def setPosition(self, x, y):
        self.rect.x = x
        self.rect.y = y

class Heroi(pygame.sprite.Sprite):
    _estadoJogo = None
    frames = []
    _frameAtual = 0
    _contadorFrames = 0
    _lado = 'direita'
    _ladoMudou = False

    def lado(self, lado):
        if self._lado != lado:
            self._lado = lado
            self._ladoMudou = True

    #Quando houver mais frames criar uma lista de frames para cada lado da animacao
    #E somente trocar a listaAtual para apontar para a lista com as imagens do outro lado
    def atualizaLado(self):
        self.frames[0] = pygame.transform.flip(self.frames[0], True, False)
        self.frames[1] = pygame.transform.flip(self.frames[1], True, False)
        self.frames[2] = pygame.transform.flip(self.frames[2], True, False)
        self.frames[3] = pygame.transform.flip(self.frames[3], True, False)
        self.frames[4] = pygame.transform.flip(self.frames[4], True, False)

    def set_position(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def __init__(self):

        pygame.sprite.Sprite.__init__(self)

        self.frames.append(pygame.image.load("../../resources/sprites/sprite_1.png"))
        self.frames.append(pygame.image.load("../../resources/sprites/sprite_2.png"))
        self.frames.append(pygame.image.load("../../resources/sprites/sprite_3.png"))
        self.frames.append(pygame.image.load("../../resources/sprites/sprite_4.png"))
        self.frames.append(pygame.image.load("../../resources/sprites/sprite_5.png"))

        self.frames[0] = pygame.transform.scale(self.frames[0], (64, 64))
        self.frames[1] = pygame.transform.scale(self.frames[1], (64, 64))
        self.frames[2] = pygame.transform.scale(self.frames[2], (64, 64))
        self.frames[3] = pygame.transform.scale(self.frames[3], (64, 64))
        self.frames[4] = pygame.transform.scale(self.frames[4], (64, 64))

        self.image = self.frames[0]

        self.rect = self.image.get_rect()
        self.rect.width = 30
        self.rect.height = 60
        self.rect.x = 100 + 20

    def update(self):
        print("Update Hero")
        self._contadorFrames += 20
        if self._contadorFrames >= 100:
            self._contadorFrames = 0
            self._frameAtual += 1

        if self._frameAtual >= len(self.frames):
            self._frameAtual = 0
        if self._ladoMudou:
            self.atualizaLado(self)
        self.image = self.frames[self._frameAtual]

        # Teste para ver se embaixo de um telhado ou arvore é mais bacana aplicar transparência no herói ou no tile
        # Ideal seria pintar o herói sem transparencia primeiro, e depois de desenhar os tiles redesenhar ele com uma transparência
        #COR_TRANSPARENCIA = (0, 0, 0)
        #self.image.set_colorkey(COR_TRANSPARENCIA)
        #self.image.set_alpha(100)
        #self.image = self.image.convert()

RED = (255, 0, 0)

WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

FPS = 30
fpsClock = pygame.time.Clock()

heroi = Heroi()
heroi.set_position(150, 0)
grupoHeroi = pygame.sprite.Group(heroi)

x = 16 * 19
y = 16 * 9
largura = 16
altura = largura
tile1 = Tile("../../resources/map/basis.png", x, y, largura, largura )
tile2 = Tile("../../resources/map/tiled01.png", (16*0), (16* 15), largura, largura)
tile3 = Tile("../../resources/map/tiled01.png", (16*0), (16* 14), largura, largura, 200)

tile4 = Tile("../../resources/map/tiled01.png", (16*0), (16* 14), largura, largura)
tile5 = Tile("../../resources/map/tiled01.png", (16*0), (16* 15), largura, largura )

tile4.setPosition(200,0)
tile5.setPosition(200,64)



tile2.setPosition(100,64)
tile3.setPosition(100,0)
grupoTile = pygame.sprite.Group()
grupoTile.add(tile1)
grupoTile.add(tile2)
grupoTile.add(tile3)
grupoTile.add(tile4)
grupoTile.add(tile5)

grupoTile2 = pygame.sprite.Group()
grupoTile2.add(tile2)
grupoTile2.add(tile3)
pygame.key.set_repeat(1, 10)

while True:

    TELA.fill(BLUE)
    for evento in pygame.event.get():
        if evento.type == QUIT or (evento.type == KEYDOWN and evento.key == K_ESCAPE):
            pygame.quit()
            sys.exit()

    grupoHeroi.update()

    grupoTile.draw(TELA)
    grupoHeroi.draw(TELA)
    pygame.draw.rect(TELA, RED, tile3.rect,1)

    if pygame.sprite.groupcollide(grupoHeroi, grupoTile2, False, False):
        pygame.draw.rect(TELA, RED, heroi.rect,1)
        print("Colisao entre os grupos: grupoHeroi + grupoTile2")



    pygame.display.update()
    fpsClock.tick(FPS)
    # TELA.blit()