import sys, pygame
from pygame.locals import *

_000000 = (0, 0, 0)
_FFFFFF = (255, 255, 255)
_FF0000 = (255, 0, 0)


def stopBgMusic():
    pygame.mixer.music.stop()


def sairJogo():
    stopBgMusic()
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
    _TELA_ALTURA = 600
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

    def getLarguraTela(self):
        return self._TELA_LARGURA

    def getAlturaTela(self):
        return self._TELA_ALTURA

    def getFontMenu(self):
        return self._FONTE_MENU

    def getTela(self):
        return self._TELA

    def getMenuHUD(self):
        return self._menuHUD

    def getMenuJogo(self):
        return self._menuJogo

    def desenhaTextoSemAlising(self, texto, cor, x, y):
        desenhoTexto = self.getFontMenu().render(texto, False, cor)
        desenhoTextoRect = desenhoTexto.get_rect()
        desenhoTextoRect.topleft = (x, y)
        self.getTela().blit(desenhoTexto, desenhoTextoRect)

    def desenhaTexto(self, texto, cor, x, y):
        desenhoTexto = self.getFontMenu().render(texto, True, cor)
        desenhoTextoRect = desenhoTexto.get_rect()
        desenhoTextoRect.topleft = (x, y)
        self.getTela().blit(desenhoTexto, desenhoTextoRect)

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
            if isinstance(self._cenarioAtual, Cenario):
                self._cenarioAtual.main()
            if self._irParaProximoCenario and isinstance(self._proximoCenario, Cenario):
                aux = self._cenarioAtual
                self._cenarioAtual = self._proximoCenario
                del aux
            pygame.display.update()
            self._FPSCLOCK.tick(self._FPS)

class CenarioGenerico():
    _estadoJogo = None
    _jogo = None
    _mostraHUD = True

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
            if self._mostraHUD and self._jogo.getMenuHUD() != None:
                self._jogo.getMenuHUD().eventos(evento)
        self.logica()
        if self._mostraHUD and self._jogo.getMenuHUD() != None:
            self._jogo.getMenuHUD().logica()
        self.desenha()
        if self._mostraHUD and  self._jogo.getMenuHUD() != None:
            self._jogo.getMenuHUD().desenha()

class MenuJogo(Cenario):

    menu = 1

    def playBgMusic(self):
        pygame.mixer.music.load("../resources/sound/menuBg.wav")
        pygame.mixer.music.play(-1, 0.0)

    def __init__(self, jogo, estadoJogo):
        Cenario.__init__(self,jogo, estadoJogo)
        self.playBgMusic()

    def moveMenuSound(self):
        sound = pygame.mixer.Sound("../resources/sound/open01.wav")
        sound.play()

    def soundMenuSelected(self):
        sound = pygame.mixer.Sound("../resources/sound/menuSelected.wav")
        sound.play()

    def eventos(self, evento):
        if evento.type == QUIT:
            sairJogo()
        elif evento.type == KEYDOWN:
            if evento.key == K_ESCAPE:
                sairJogo()
            elif evento.key == K_UP:
                self.menu -= 1
                self.moveMenuSound()
            elif evento.key == K_DOWN:
                self.menu += 1
                self.moveMenuSound()
            elif evento.key == K_RETURN:
                if self.menu == 3:
                    sairJogo()
                elif self.menu == 2:
                    print("Evento para Carregar o Save")
                    self.soundMenuSelected()
                elif self.menu == 1:
                    print("Evento do Novo Jogo")
                    self.soundMenuSelected()
        if self.menu < 1:
            self.menu = 3
        elif self.menu > 3:
            self.menu = 1

    def desenha(self):
        self._jogo.desenhaTextoSemAlising("Novo Texto", self.getCorMenu(self.menu,1), self._jogo.getLarguraTela()/2 - 70, 500)
        self._jogo.desenhaTextoSemAlising("Carregar", self.getCorMenu(self.menu,2), self._jogo.getLarguraTela()/2 - 70, 518)
        self._jogo.desenhaTextoSemAlising("Quit", self.getCorMenu(self.menu,3), self._jogo.getLarguraTela()/2 - 70, 536)

    def logica(self):
        print("Logica")

    def getCorMenu(self, valorMenu, valorVermelho):
        if valorMenu == valorVermelho:
            return _FF0000
        else:
            return _FFFFFF

if __name__ == '__main__':
    jogo = Jogo()
    jogo.main()