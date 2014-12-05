import sys, pygame
from pygame.locals import *

class Jogo():
    _animacaoIntroducao = None
    _menuInicio = None #Cenario com o menu início do jogo
    _estadoJogo = None #Variáveis referentes ao personagem
    _cenarioAtual = None #Cenário onde o loop do jogo vai rodar
    _proximoCenario = None #Usado para mudar o cenario
    _menuJogo = None #Menu quando o Pause é apertado
    _menuHUD = None #Menu interativo onde pode se alterar itens etc
    _TELA = None
    _FPSCLOCK = None
    _FPS = 15
    _irParaProximoCenario = False #Boolean usado para controlar a troca de cenários

    def __init__(self):
        pygame.init()
        self._FPSCLOCK = pygame.time.Clock()
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
            if type(self._cenarioAtual) == Cenario:
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
            self._jogo.getMenuHUD().eventos(evento)
        self.logica()
        self._jogo.getMenuHUD().logica()
        self.desenha()
        self._jogo.getMenuHUD().desenha()

if __name__ == '__main__':
    print("Testando a classe do Jogo")