import sys, os, pygame, json
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
    _animacao_introducao = None
    _menu_inicio = None #Cenario com o menu início do jogo
    _estado_jogo = None #Variáveis referentes ao personagem
    _cenario_atual = None #Cenário onde o loop do jogo vai rodar
    _proximo_cenario = None #Usado para mudar o cenario
    _menu_jogo = None #Menu quando o Pause é apertado
    _menu_HUD = None #Menu interativo onde pode se alterar itens etc
    _TELA = None
    _TELA_NOME_JOGO = "Nome do Jogo"
    _TELA_LARGURA= 800
    _TELA_ALTURA = 600
    _COR_FUNDO = _0000FF
    _FONTE_MENU = None
    _FPSCLOCK = None
    _FPS = 15
    _ir_para_proximo_cenario = False #Boolean usado para controlar a troca de cenários
    _proximo_cenario_pronto = False
    _pular_eventos_e_logica = False
    _frame_animacao_cenario = None
    _contador_animacao_cenario = None

    def __init__(self):
        pygame.init()
        self._FPSCLOCK = pygame.time.Clock()
        self._TELA = pygame.display.set_mode((self._TELA_LARGURA, self._TELA_ALTURA),0,0)
        pygame.display.set_caption(self._TELA_NOME_JOGO)
        self._FONTE_MENU = pygame.font.Font('freesansbold.ttf', 18)
        self._menu_jogo = MenuJogo(self, self._estado_jogo)
        #Inicializar Variaveis

    def get_largura_tela(self):
        return self._TELA_LARGURA

    def get_altura_tela(self):
        return self._TELA_ALTURA

    def get_font_menu(self):
        return self._FONTE_MENU

    def get_tela(self):
        return self._TELA

    def get_menu_HUD(self):
        return self._menu_HUD

    def get_menu_jogo(self):
        return self._menu_jogo

    def is_pular_eventos_e_logica(self):
        return self._pular_eventos_e_logica

    def desenha_texto_sem_alising(self, texto, cor, x, y):
        self._desenha_texto_generico( texto, _000000, x+2, y+2, False)
        self._desenha_texto_generico( texto, cor, x, y, False)

    def desenha_texto(self, texto, cor, x, y):
        self._desenha_texto_generico( texto, _000000, x+2, y+2, True)
        self._desenha_texto_generico( texto, cor, x, y, True)

    def _desenha_texto_generico(self, texto, cor, x, y, alising):
        desenhoTexto = self.get_font_menu().render(texto, alising, cor)
        desenhoTextoRect = desenhoTexto.get_rect()
        desenhoTextoRect.topleft = (x, y)
        self.get_tela().blit(desenhoTexto, desenhoTextoRect)

    def _teste(self):
        '''Método de Teste'''

    def trocar_cenario(self, proximoCenario):
        self._proximo_cenario = proximoCenario
        self._ir_para_proximo_cenario = True

    def _troca_de_cenario(self):
        if self._ir_para_proximo_cenario and isinstance(self._proximo_cenario, Cenario) and self._frame_animacao_cenario < 100:
            self._pular_eventos_e_logica = True
            tamanhoQuadrado = self._frame_animacao_cenario * int(600 / 100)
            pygame.draw.rect(self.get_tela(), _000000, (0, 0, 800, 600), tamanhoQuadrado)
            self._frame_animacao_cenario += self._contador_animacao_cenario
            if self._frame_animacao_cenario == 100:
                aux = self._cenario_atual
                self._cenario_atual = self._proximo_cenario
                del aux
                self._ir_para_proximo_cenario = False
        if not self._ir_para_proximo_cenario and isinstance(self._proximo_cenario, Cenario) and self._frame_animacao_cenario > 1:
            tamanhoQuadrado = self._frame_animacao_cenario * int(600 / 100)
            pygame.draw.rect(self.get_tela(), _000000, (0, 0, 800, 600), tamanhoQuadrado)
            self._frame_animacao_cenario -= self._contador_animacao_cenario
            if self._frame_animacao_cenario == 0:
                self._pular_eventos_e_logica = False

    def main(self):
        self._frame_animacao_cenario = 0
        self._contador_animacao_cenario = 10
        if type(self._animacao_introducao) == type(self._teste):
            self._animacao_introducao(self)
        self._cenario_atual = self._menu_jogo
        while True:
            self._TELA.fill(self._COR_FUNDO)
            if isinstance(self._cenario_atual, Cenario):
                self._cenario_atual.main()
            self._troca_de_cenario()
            pygame.display.update()
            self._FPSCLOCK.tick(self._FPS)

class CenarioGenerico():
    _estado_jogo = None
    _jogo = None
    _mostra_HUD = True

    def __init__(self, jogo, estadoJogo):
        self._estado_jogo = estadoJogo
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
        if not self._jogo.is_pular_eventos_e_logica():
            for evento in pygame.event.get():
                self.eventos(evento)
                if self._mostra_HUD and self._jogo.get_menu_HUD() != None:
                    self._jogo.get_menu_HUD().eventos(evento)
            self.logica()
            if self._mostra_HUD and self._jogo.get_menu_HUD() != None:
                self._jogo.get_menu_HUD().logica()
        self.desenha()
        if self._mostra_HUD and  self._jogo.get_menu_HUD() != None:
            self._jogo.get_menu_HUD().desenha()

class MenuJogo(Cenario):

    opcoes_menu = 1
    enter_pressionado = False

    def __init__(self, jogo, estadoJogo):
        Cenario.__init__(self,jogo, estadoJogo)
        tocarMusicaFundoMenu()

    def som_mudar_opcao_menu(self):
        sound = pygame.mixer.Sound(lerArquivo("resources/sound/open01.wav"))
        sound.play()

    def som_selecionar_menu(self):
        sound = pygame.mixer.Sound(lerArquivo("resources/sound/menuSelected.wav"))
        sound.play()

    def eventos(self, evento):
        if evento.type == QUIT:
            sairJogo()
        elif evento.type == KEYDOWN:
            if evento.key == K_ESCAPE:
                sairJogo()
            elif evento.key == K_UP:
                self.opcoes_menu -= 1
                self.som_mudar_opcao_menu()
            elif evento.key == K_DOWN:
                self.opcoes_menu += 1
                self.som_mudar_opcao_menu()
            elif evento.key == K_RETURN:
                self.enter_pressionado = True
        if self.opcoes_menu < 1:
            self.opcoes_menu = 3
        elif self.opcoes_menu > 3:
            self.opcoes_menu = 1

    def desenha(self):
        corMenuOpcao1 = self.get_cor_menu(self.opcoes_menu, 1)
        corMenuOpcao2 = self.get_cor_menu(self.opcoes_menu, 2)
        corMenuOpcao3 = self.get_cor_menu(self.opcoes_menu, 3)

        coordenadaXTexto = self._jogo.get_largura_tela() / 2 - 70
        self._jogo.desenha_texto_sem_alising("Novo Jogo", corMenuOpcao1, coordenadaXTexto, 500)
        self._jogo.desenha_texto_sem_alising("Carregar", corMenuOpcao2, coordenadaXTexto, 518)
        self._jogo.desenha_texto_sem_alising("Quit", corMenuOpcao3, coordenadaXTexto, 536)

    def logica(self):
        if(self.enter_pressionado):
            if self.opcoes_menu == 3:
                sairJogo()
            elif self.opcoes_menu == 2:
                print("Evento para Carregar o Save")
                self.som_selecionar_menu()
            elif self.opcoes_menu == 1:
                print("Evento do Novo Jogo")
                self.som_selecionar_menu()
                inicioJogo = Mapa(self._jogo, self._estado_jogo)
                pararMusicaFundoMenu()
                self._jogo.trocar_cenario(inicioJogo)
            self.enter_pressionado = False

    def get_cor_menu(self, valorMenu, valorVermelho):
        if valorMenu == valorVermelho:
            return _FF0000
        else:
            return _FFFFFF

class Mapa(Cenario):

    def __init__(self, jogo, estadoJogo):
        Cenario.__init__(self,jogo, estadoJogo)

    def voltar_ao_menu(self):
        menuJogo = MenuJogo(self._jogo, self._estado_jogo)
        self._jogo.trocar_cenario(menuJogo)

    def eventos(self, evento):
        if evento.type == QUIT:
            self.voltar_ao_menu()
        elif evento.type == KEYDOWN:
            if evento.key == K_ESCAPE:
                self.voltar_ao_menu()
        print("Eventos")

    def logica(self):
        print("logica")

    def desenha(self):
        print("Desenhando")

class EstadoJogo():
    _vida_maxima = None
    _vida_atual = None
    _mana_maxima = None
    _mana_atual = None

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

    _coordenada_x = None
    _coordenada_y = None
    _direcao = None

    #Modificadores quando um baú é aberto por exemplo, não poderá ser aberto novamente
    _modificadores = {}

if __name__ == '__main__':
    jogo = Jogo()
    jogo.main()