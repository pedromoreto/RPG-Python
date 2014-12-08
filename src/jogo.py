import sys, os, pygame
from pygame.locals import *

_000000 = (0, 0, 0)
_FFFFFF = (255, 255, 255)
_FF0000 = (255, 0, 0)
_0000FF = (0, 0, 255)

def lerArquivo(caminho):
    if os.path.exists(caminho):
        return caminho
    elif os.path.exists("../"+caminho):
        return "../"+caminho
    else:
        raise NotADirectoryError("Diretorio %s não encontrado "%caminho)

def pararMusicaFundoMenu():
    pygame.mixer.music.stop()

def tocarMusicaFundoMenu():
        pygame.mixer.music.load(lerArquivo("resources/sound/menuBg.wav"))
        pygame.mixer.music.play(-1, 0.0)

def sairJogo():
    pararMusicaFundoMenu()
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
    _COR_FUNDO = _0000FF
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
                for x in range(1,600,10):
                    pygame.draw.rect(self.getTela(), _000000, (0, 0, 800, 600),x)
                    pygame.display.update()
                pygame.time.wait(200)
                del aux
                self._irParaProximoCenario = False
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

    opcoesMenu = 1
    enterPressionado = False

    def __init__(self, jogo, estadoJogo):
        Cenario.__init__(self,jogo, estadoJogo)
        tocarMusicaFundoMenu()

    def somMudarOpcaoMenu(self):
        sound = pygame.mixer.Sound(lerArquivo("resources/sound/open01.wav"))
        sound.play()

    def somSelecionarMenu(self):
        sound = pygame.mixer.Sound(lerArquivo("resources/sound/menuSelected.wav"))
        sound.play()

    def eventos(self, evento):
        if evento.type == QUIT:
            sairJogo()
        elif evento.type == KEYDOWN:
            if evento.key == K_ESCAPE:
                sairJogo()
            elif evento.key == K_UP:
                self.opcoesMenu -= 1
                self.somMudarOpcaoMenu()
            elif evento.key == K_DOWN:
                self.opcoesMenu += 1
                self.somMudarOpcaoMenu()
            elif evento.key == K_RETURN:
                self.enterPressionado = True
        if self.opcoesMenu < 1:
            self.opcoesMenu = 3
        elif self.opcoesMenu > 3:
            self.opcoesMenu = 1

    def desenha(self):
        self._jogo.desenhaTextoSemAlising("Novo Texto", _000000, self._jogo.getLarguraTela()/2 - 68, 502)
        self._jogo.desenhaTextoSemAlising("Novo Texto", self.getCorMenu(self.opcoesMenu,1), self._jogo.getLarguraTela()/2 - 70, 500)
        self._jogo.desenhaTextoSemAlising("Carregar", _000000, self._jogo.getLarguraTela()/2 - 68, 520)
        self._jogo.desenhaTextoSemAlising("Carregar", self.getCorMenu(self.opcoesMenu,2), self._jogo.getLarguraTela()/2 - 70, 518)
        self._jogo.desenhaTextoSemAlising("Quit", _000000, self._jogo.getLarguraTela()/2 - 68, 538)
        self._jogo.desenhaTextoSemAlising("Quit", self.getCorMenu(self.opcoesMenu,3), self._jogo.getLarguraTela()/2 - 70, 536)

    def logica(self):
        if(self.enterPressionado):
            if self.opcoesMenu == 3:
                sairJogo()
            elif self.opcoesMenu == 2:
                print("Evento para Carregar o Save")
                self.somSelecionarMenu()
            elif self.opcoesMenu == 1:
                print("Evento do Novo Jogo")
                self.somSelecionarMenu()
                inicioJogo = Mapa(self._jogo, self._estadoJogo)
                pararMusicaFundoMenu()
                self._jogo.trocarCenario(inicioJogo)
            self.enterPressionado = False

    def getCorMenu(self, valorMenu, valorVermelho):
        if valorMenu == valorVermelho:
            return _FF0000
        else:
            return _FFFFFF

class Mapa(Cenario):

    def __init__(self, jogo, estadoJogo):
        Cenario.__init__(self,jogo, estadoJogo)

    def voltarAoMenu(self):
        menuJogo = MenuJogo(self._jogo, self._estadoJogo)
        self._jogo.trocarCenario(menuJogo)

    def eventos(self, evento):
        if evento.type == QUIT:
            self.voltarAoMenu()
        elif evento.type == KEYDOWN:
            if evento.key == K_ESCAPE:
                self.voltarAoMenu()
        print("Eventos")

    def logica(self):
        print("logica")

    def desenha(self):
        print("Desenhando")

class EstadoJogo():
    _vidaMaxima = None
    _vidaAtual = None
    _manaMaxima = None
    _manaAtual = None

    _ataque = None
    _defesa = None
    _forca = None
    _inteligencia = None

    _experiencia = None
    _level = None

    _inventario = {}
    _dinheiro = None

    _arma = None
    _escudo = None
    _armadura = None
    _calca = None
    _outros = None

    _coordenadaX = None
    _coordenadaY = None
    _direcao = None

    #Modificadores quando um baú é aberto por exemplo, não poderá ser aberto novamente
    _modificadores = {}

if __name__ == '__main__':
    jogo = Jogo()
    jogo.main()