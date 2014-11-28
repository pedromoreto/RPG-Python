import random, pygame, sys
from pygame.locals import *

FPS = 30
LARGURA = 640
ALTURA = 480
VELOCIDADE_REVELAR = 8
TAMANHO_CAIXA = 40
TAMANHO_ESPACO = 10
TABULEIRO_HORIZONTAL = 5
TABULEIRO_VERTICAL = 4

assert (TABULEIRO_HORIZONTAL * TABULEIRO_VERTICAL) % 2 == 0, 'Tabuleiro precisa ter mais um par de caixas para ser um numero par'

MARGEN_X = int((LARGURA - (TABULEIRO_HORIZONTAL * (TAMANHO_CAIXA + TAMANHO_ESPACO)))/2 )
MARGEN_Y = int((ALTURA - (TABULEIRO_VERTICAL * (TAMANHO_CAIXA + TAMANHO_ESPACO)))/2 )

#Cores
CINZA = (100, 100, 100)
AZUL_NAV = (60, 60, 100)
BRANCO = (255, 255, 255)
VERMELHO = (255, 0, 0)
VERDE = (0, 255, 0)
AZUL = (0, 0, 255)
AMARELO = (255, 255, 0)
LARANJA = (255, 128, 0)
ROXO = (255, 0, 255)
CIANETO = (0, 255, 255)

COR_FUNDO = AZUL_NAV
COR_FUNDO_CLARA = CINZA
COR_CAIXA = BRANCO
COR_CLARA = AZUL

DONUT = 'donut'
SQUARE = 'square'
DIAMOND = 'diamond'
LINES = 'lines'
OVAL = 'oval'

TODAS_CORES = ( BRANCO, VERMELHO, VERDE, AZUL, AMARELO, LARANJA, ROXO, CIANETO)
TODAS_FORMAS = (DONUT, SQUARE, DIAMOND, LINES, OVAL)

assert len(TODAS_CORES) * len(TODAS_FORMAS) * 2 >= TABULEIRO_HORIZONTAL * TABULEIRO_VERTICAL, "Tabuleiro é muito grande para a quantidade de formas"

def main():
    global FPS_CLOCK, TELA
    pygame.init()
    FPS_CLOCK = pygame.time.Clock()
    TELA = pygame.display.set_mode((LARGURA, ALTURA))

    mouseX = 0
    mouseY = 0

    pygame.display.set_caption("Jogo da Memória")

    tabuleiro = getTabuleiroAleatorio()
    caixasReveladas = getCaixasReveladasData(False)

    primeiraSelecao = None

    TELA.fill(COR_FUNDO)

    while True:
        mouseClicou = False

        TELA.fill(COR_FUNDO)
        desenhaTabuleiro(tabuleiro, caixasReveladas)

        for event in pygame.event.get():
            if(event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE ) ):
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEMOTION:
                mouseX, mouseY = event.pos
            elif event.type == MOUSEBUTTONUP:
                mouseX, mouseY = event.pos
                mouseClicou = True

        caixaX, caixaY = buscarCaixaNoPixel(mouseX, mouseY)
        print( "\n X: %s Y: %s \n"%(caixaX, caixaY))
        if caixaX != None and caixaY != None:
            if not caixasReveladas[caixaX][caixaY]:
                desenhaBordaCaixa(caixaX, caixaY)
            if not caixasReveladas[caixaX][caixaY] and mouseClicou:
                animacaoRevelarCaixa(tabuleiro, [(caixaX, caixaY)])
                caixasReveladas[caixaX][caixaY] = True
                if primeiraSelecao == None:
                    primeiraSelecao = (caixaX, caixaY)
                else:
                    icon1Shape, icon1Color = buscarFormaECor(tabuleiro, primeiraSelecao[0], primeiraSelecao[1])
                    icon2Shape, icon2Color = buscarFormaECor(tabuleiro, caixaX, caixaY)
                    if icon1Shape != icon2Shape or icon1Color != icon2Color:
                        #Valores diferentes
                        pygame.time.wait(1000)
                        animacaoCobrirCaixas(tabuleiro, [(primeiraSelecao[0], primeiraSelecao[1]), (caixaX, caixaY)])
                        caixasReveladas[primeiraSelecao[0]][primeiraSelecao[1]] = False
                        caixasReveladas[caixaX][caixaY] = False

                    elif ganhouJogo(caixasReveladas):
                        animacaoVenceuJogo(tabuleiro)
                        pygame.time.wait(2000)

                        #Resetar o jogo
                        tabuleiro = getTabuleiroAleatorio()
                        caixasReveladas = getCaixasReveladasData(False)

                        #Mostrar todas as caixas por um segundo
                        desenhaTabuleiro(tabuleiro, caixasReveladas)
                        pygame.display.update()
                        pygame.time.wait(1000)

                        #Replay
                        animacaoInicioJogo(tabuleiro)
                    primeiraSelecao = None

        pygame.display.update()
        FPS_CLOCK.tick(FPS)
def getCaixasReveladasData(valor):
    caixasReveladas = []
    for i in range(TABULEIRO_HORIZONTAL):
        caixasReveladas.append([valor]*TABULEIRO_VERTICAL)
    return caixasReveladas

def getTabuleiroAleatorio():
    icones = []
    for cor in TODAS_CORES:
        for forma in TODAS_FORMAS:
            icones.append((forma, cor))

    random.shuffle(icones)
    numeroIconesUsados = int(TABULEIRO_HORIZONTAL * TABULEIRO_VERTICAL / 2)
    icones = icones[:numeroIconesUsados] * 2
    random.shuffle(icones)

    tabuleiro = []

    for x in range(TABULEIRO_HORIZONTAL):
        coluna = []
        for y in range(TABULEIRO_VERTICAL):
            coluna.append(icones[0])
            del icones[0]
        tabuleiro.append(coluna)
    return tabuleiro

def dividirEntreOsGruposDe(tamanhoGrupo, theList):
    resultado = []
    for i in range(0, len(theList), tamanhoGrupo):
        resultado.append((theList[i:i+tamanhoGrupo]))
    return resultado

def coordenadasCaixaEsquerdaETopo(caixaX, caixaY):
    esquerda = caixaX * (TAMANHO_CAIXA + TAMANHO_ESPACO) + MARGEN_X
    topo = caixaY * (TAMANHO_CAIXA + TAMANHO_ESPACO) + MARGEN_Y
    return (esquerda, topo)

def buscarCaixaNoPixel(x, y):
    for caixaX in range(TABULEIRO_HORIZONTAL):
        for caixaY in range(TABULEIRO_VERTICAL):
            esquerda, topo = coordenadasCaixaEsquerdaETopo(caixaX, caixaY)
            caixaQuadrada = pygame.Rect(esquerda, topo, TAMANHO_CAIXA, TAMANHO_CAIXA)
            if caixaQuadrada.collidepoint(x, y):
                return (caixaX, caixaY)
    return (None, None)

def desenharIcone(forma, cor, caixaX, caixaY):
    quarto = int(TAMANHO_CAIXA * 0.25)
    metade = int(TAMANHO_CAIXA * 0.5)

    esquerda, topo = coordenadasCaixaEsquerdaETopo(caixaX, caixaY)
    if forma == DONUT:
        pygame.draw.circle(TELA, cor, (esquerda + metade, topo + metade), metade - 5)
        pygame.draw.circle(TELA, COR_FUNDO, (esquerda + metade, topo + metade), quarto - 5)
    elif forma == SQUARE:
        pygame.draw.rect(TELA, cor, (esquerda + quarto, topo + quarto, TAMANHO_CAIXA - metade, TAMANHO_CAIXA - metade))
    elif forma == DIAMOND:
        pygame.draw.polygon(TELA, cor, ((esquerda + metade, topo), (esquerda+TAMANHO_CAIXA - 1, topo + metade), (esquerda + metade, topo + TAMANHO_CAIXA -1), (esquerda, topo + metade)) )
    elif forma == LINES:
        for i in range(0, TAMANHO_CAIXA, 4):
            pygame.draw.line(TELA, cor, (esquerda, topo + i), (esquerda + i, topo))
            pygame.draw.line(TELA, cor, (esquerda + i, topo + TAMANHO_CAIXA -1), (esquerda + TAMANHO_CAIXA -1, topo + i))
    elif forma == OVAL:
        pygame.draw.ellipse(TELA, cor, (esquerda, topo + quarto, TAMANHO_CAIXA, metade))

def buscarFormaECor(tabuleiro, caixaX, caixaY):
    return tabuleiro[caixaX][caixaY][0], tabuleiro[caixaX][caixaY][1]

def desenhaCaixasCobertas(tabuleiro, caixas, cobertas):
    for caixa in caixas:
        esquerda, topo = coordenadasCaixaEsquerdaETopo(caixa[0], caixa[1])
        pygame.draw.rect(TELA, COR_FUNDO, (esquerda, topo, TAMANHO_CAIXA, TAMANHO_CAIXA))
        forma, cor = buscarFormaECor(tabuleiro, caixa[0], caixa[1])
        desenharIcone(forma, cor, caixa[0], caixa[1])
        if cobertas > 0:
            pygame.draw.rect(TELA, COR_CAIXA, (esquerda, topo, cobertas, TAMANHO_CAIXA))

    pygame.display.update()
    FPS_CLOCK.tick(FPS)

def animacaoRevelarCaixa(tabuleiro, caixasRevelar):
    #            Inicio               Fim      Incremento/Decremento
    for cobertura in range(TAMANHO_CAIXA, (-VELOCIDADE_REVELAR) - 1, -VELOCIDADE_REVELAR):
        desenhaCaixasCobertas(tabuleiro, caixasRevelar, cobertura)

def animacaoCobrirCaixas(tabuleiro, caixaCobrir):
    for cobertura in range(0, TAMANHO_CAIXA + VELOCIDADE_REVELAR, VELOCIDADE_REVELAR):
        desenhaCaixasCobertas(tabuleiro, caixaCobrir, cobertura)

def desenhaTabuleiro(tabuleiro, revelados):
    for caixaX in range(TABULEIRO_HORIZONTAL):
        for caixaY in range(TABULEIRO_VERTICAL):
            esquerda, topo = coordenadasCaixaEsquerdaETopo(caixaX,caixaY)
            if not revelados[caixaX][caixaY]:
                pygame.draw.rect(TELA, COR_CAIXA, (esquerda, topo, TAMANHO_CAIXA, TAMANHO_CAIXA))
            else:
                forma, cor = buscarFormaECor(tabuleiro, caixaX, caixaY)
                desenharIcone(forma, cor, caixaX, caixaY)

def desenhaBordaCaixa(caixaX, caixaY):
    esquerda, topo = coordenadasCaixaEsquerdaETopo(caixaX, caixaY)
    pygame.draw.rect(TELA, COR_CLARA, (esquerda - 5, topo - 5, TAMANHO_CAIXA + 10, TAMANHO_CAIXA + 10), 4)

def animacaoInicioJogo(tabuleiro):
    caixasCobertas = getCaixasReveladasData(False)
    caixas = []
    for x in range(TABULEIRO_HORIZONTAL):
        for y in range(TABULEIRO_VERTICAL):
            caixas.append( (x,y))
    random.shuffle(caixas)
    gruposCaixas = dividirEntreOsGruposDe(8, caixas)

    desenhaTabuleiro(tabuleiro, caixasCobertas)
    for grupoCaixa in gruposCaixas:
        animacaoRevelarCaixa(tabuleiro, grupoCaixa)
        animacaoCobrirCaixas(tabuleiro, grupoCaixa)

def animacaoVenceuJogo(tabuleiro):
    caixasCobertas = getCaixasReveladasData(True)
    cor1 = COR_FUNDO_CLARA
    cor2 = COR_FUNDO

    for i in range(13):
        cor1, cor2 = cor2, cor1
        TELA.fill(cor1)
        desenhaTabuleiro(tabuleiro, caixasCobertas)
        pygame.display.update()
        pygame.time.wait(300)

def ganhouJogo(caixasReveladas):
    for i in caixasReveladas:
        if False in i:
            return False
    return True

if __name__ == '__main__':
    main()