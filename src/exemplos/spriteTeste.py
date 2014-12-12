import  pygame, sys
from pygame.locals import *
from requests.api import head


pygame.init()

TELA = pygame.display.set_mode((800, 600), 0, 0)
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

    def __init__(self, imagem, x, y, largura, altura):
        pygame.sprite.Sprite.__init__(self)
        self._tileset = pygame.image.load(imagem).convert()
        tile = pygame.Surface([largura, altura]).convert()
        # Copiar o sprite da imagem na posição X e Y com largura e altura
        tile.blit(self._tileset, (0, 0), (x, y, largura, altura))
        COR_TRANSPARENCIA = (0, 0, 0)
        tile.set_colorkey(COR_TRANSPARENCIA)
        self.image = tile.convert()
        self.image = pygame.transform.scale(self.image, (64, 64))
        self.rect = self.image.get_rect()

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
        self.rect.x = 100

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

WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

FPS = 30
fpsClock = pygame.time.Clock()

heroi = Heroi()
grupoHeroi = pygame.sprite.Group(heroi)

x = 16 * 19
y = 16 * 9
largura = 16
altura = largura
grupoTile = pygame.sprite.Group(Tile("../../resources/map/basis.png", x, y, largura, largura ))
pygame.key.set_repeat(1, 10)

while True:

    TELA.fill(BLUE)
    for evento in pygame.event.get():
        if evento.type == QUIT or (evento.type == KEYDOWN and evento.key == K_ESCAPE):
            pygame.quit()
            sys.exit()

    grupoHeroi.update()
    grupoHeroi.draw(TELA)
    grupoTile.draw(TELA)

    pygame.display.update()
    fpsClock.tick(FPS)
    # TELA.blit()