import sys, pygame
from pygame.locals import *

_000000 = (0, 0, 0)
_FFFFFF = (255, 255, 255)

def sairJogo():
    pygame.quit()
    sys.exit()

class Jogo():
    _animacaoIntroducao = None
    _menuInicio = None #Cenario com o menu início do jogo
    _estadoJogo = None #Variáveis referentes ao personagem
    _cenarioAtual = None #Cenário onde o loop do jogo vai rodar
    _proximoCenario = None #Usado para mudar o cenario
    _menuJogo = None #Menu quando o Pause é apertado
    _menuHUD = None #Menu interativo onde pode se alterar itens etc
    _TELA = None
    _TELA_NOME_JOGO = "Nome do Jogo"
    _TELA_LARGURA= 800
    _TELA_ALTURA = 400
    _COR_FUNDO = _000000
    _FONTE_MENU = None
    _FPSCLOCK = None
    _FPS = 15
    _irParaProximoCenario = False #Boolean usado para controlar a troca de cenários

    def __init__(self):
        pygame.init()
        self._FPSCLOCK = pygame.time.Clock()
        self._TELA = pygame.display.set_mode((self._TELA_LARGURA, self._TELA_ALTURA),0,0)
        pygame.display.set_caption(self._TELA_NOME_JOGO)
        self._FONTE_MENU = pygame.font.Font('freesansbold.ttf', 18)
        self._menuJogo = MenuJogo(self, self._estadoJogo)
        #Inicializar Variaveis

    def getTela(self):
        return self._TELA

    def getMenuHUD(self):
        return self._menuHUD

    def getMenuJogo(self):
        return self._menuJogo

    def _teste(self):
        '''Método de Teste'''

    def trocarCenario(self, proximoCenario):
        self._proximoCenario = proximoCenario
        self._irParaProximoCenario = True

    def main(self):
        if type(self._animacaoIntroducao) == type(self._teste):
            self._animacaoIntroducao(self)
        self._cenarioAtual = self._menuJogo
        while True:
            self._TELA.fill(self._COR_FUNDO)
            if issubclass(Cenario, type(self._cenarioAtual) ):
                self._cenarioAtual.main()
            if self._irParaProximoCenario:
                aux = self._cenarioAtual
                self._cenarioAtual = self._proximoCenario
                del aux
            pygame.display.update()
            self._FPSCLOCK.tick(self._FPS)

class CenarioGenerico():
    _estadoJogo = None
    _jogo = None

    def __init__(self, jogo, estadoJogo):
        self._estadoJogo = estadoJogo
        self._jogo = jogo

    def eventos(self, evento):
        raise NotImplementedError()

    def logica(self):
        raise NotImplementedError()

    def desenha(self):
        raise NotImplementedError()

    def main(self):
        raise NotImplementedError()

class Cenario(CenarioGenerico):

    def main(self):
        for evento in pygame.event.get():
            self.eventos(evento)
            if self._jogo.getMenuHUD() != None:
                self._jogo.getMenuHUD().eventos(evento)
        self.logica()
        if self._jogo.getMenuHUD() != None:
            self._jogo.getMenuHUD().logica()
        self.desenha()
        if self._jogo.getMenuHUD() != None:
            self._jogo.getMenuHUD().desenha()

class MenuJogo(Cenario):
    def eventos(self, evento):
        if evento.type == QUIT:
            sairJogo()
        elif evento.type == KEYDOWN:
            if evento.key == K_ESCAPE:
                sairJogo()
if __name__ == '__main__':
    print("Testando a classe do Jogo")