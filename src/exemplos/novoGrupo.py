import pygame, sys
from pygame.locals import *

pygame.init()

class TileSprite(pygame.sprite.Sprite):
    #utilizar o self.rect para colisões
    _tileset = None
    posicao_tile = None
    frames = []
    animation = False
    
    def __init__(self, *args, **kwargs):
        super(TileSprite, self).__init__()
        if len(args) == 3:    
            imagem, quadrado, opacidade = args
        elif len(args) == 2:
            imagem, quadrado= args
            opacidade = 255
        self._tileset = pygame.image.load(imagem).convert()
        tile = pygame.Surface([quadrado.width, quadrado.height],pygame.SRCALPHA).convert()
        tile.blit(self._tileset, (0, 0), (quadrado.x, quadrado.y, quadrado.width, quadrado.height))
         
        COR_TRANSPARENCIA = (0, 0, 0)
         
        tile.set_colorkey(COR_TRANSPARENCIA)
        tile.set_alpha(opacidade)
         
        self.image = tile.convert()
        self.image = pygame.transform.scale(self.image, (64, 64))
        self.rect = self.image.get_rect()
        self.posicao_tile = self.image.get_rect()
    
    def posicao(self,  *args, **kwargs):
        if type(args[0]) == pygame.Rect:
            self.posicao_tile = args[0]
        elif len(args) == 2:
            self.posicao_tile.x = args[0]
            self.posicao_tile.y = args[1]
            
    def set_mask(self, color, opacity = 255):
        cor_final = color[0],color[1],color[2], opacity
        self.image.set_masks((1000,1000,1000,255))
#         self.image.fill(cor_final)
        self.image.convert()
        print("setting a Mask")
    
    def appendAnimation(self, animation):
        print("Appending an animation")

class GrupoSprites(pygame.sprite.Group):
    def __init__(self, *args, **kwargs):
        pygame.sprite.Group.__init__(self, *args, **kwargs)
    
    def draw(self, *args, **kwargs):
        superficie = args[0]
        for tile in self.sprites():
            superficie.blit(tile.image, tile.posicao_tile)


def executaTeste():
    FPS = 30
    fpsClock = pygame.time.Clock()
#     BLACK = (0, 0, 0)
#     WHITE = (255, 255, 255)
    BLUE = (0, 0, 255)
    RED = (0, 110, 0, 100)
    ALTURA = 600
    LARGURA = 800
    TELA = pygame.display.set_mode((LARGURA, ALTURA),)
    
    x = 16 * 19
    y = 16 * 9
    largura = 16
    altura = largura
    tile1 = TileSprite("../../resources/map/basis.png", pygame.Rect(x, y, largura, altura) )
    grupo_tile = GrupoSprites(tile1)
    tile1.set_mask(RED)
    contador = 0
    while True:
        TELA.fill(BLUE)
        for evento in pygame.event.get():
            if evento.type == QUIT or (evento.type == KEYDOWN and evento.key == K_ESCAPE):
                pygame.quit()
                sys.exit()    
        print(contador)
        tile1.posicao(contador,y)
        contador += 5
        if contador > LARGURA:
            contador = -50
        grupo_tile.update()
        grupo_tile.draw(TELA)

        pygame.display.update()
        fpsClock.tick(FPS)


if __name__ == '__main__':
    executaTeste()