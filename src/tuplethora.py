"""
############################################################
Tuplethora - A 3D game as variation of tic-tac-toe
############################################################

:Author: *Carlo E. T. Oliveira*
:Contact: carlo@nce.ufrj.br
:Date: 2014/05/07
:Status: This is a "work in progress"
:Home: `Labase <http://labase.selfip.org/>`__
:Copyright: 2014, `GPL <http://is.gd/3Udt>`__.

In Tuplethora you combine the properties of blobs to win.
"""
__version__ = 0.1
from __random import shuffle
from browser import doc, timer
from math import ceil
from glow import *
VAO = 8
LADO = 4
#CASAS = range(-LADO//2, LADO//2)
CASAS = (-3, -1, 1, 3)
OESTE, NORTE, LESTE, SUL, JOGA = 37, 38, 39, 40, 13
JOGADAS = [OESTE, NORTE, LESTE, SUL, JOGA]
MUZU = (-1, 0, 1)
FOCO = I, J, K, Z, Y, X = [(x, y, z) for x in MUZU for y in MUZU for z in MUZU if sum([abs(x), abs(y), abs(z)]) == 1]
ROTATE = {I: [J, Z, Y, K], J: [Z, I, K, X], K: [J, I, Y, X],
          Z: [J, X, Y, I], Y: [Z, X, K, I], X: [J, K, Y, Z]}
RBOW = [color.red, color.orange, color.yellow, color.green, color.cyan, color.blue, color.magenta, color.white]


def vec_soma(i, j):
    x, y, z = i
    a, b, c = j
    return 2*a+x, 2*b+y, 2*c+z


class Peca:
    def __init__(self, peca, pos):
        self.tipo, self.cor = tipo, cor = peca
        self.pos = x, y, z = pos
        xyz = (VAO*x, VAO*y, VAO*z)
        self.peca = tipo(pos=xyz, size=(4, 4, 4), color= cor)
        #box(pos=xyz, size=(6, 6, 6), color= RBOW[z//VAO], opacity=0.2)

    def move(self, destino):
        self.pos = destino
        self.peca.pos = vec(destino)


class Casa:
    def __init__(self, pos):
        self.peca = None
        self.pos = x, y, z = pos
        box(pos=(VAO*x, VAO*y, VAO*z), size=(2, 2, 2), opacity=0.05)

    def joga(self):
        self.peca = Peca((box, color.red), self.pos)

    def recebe(self, peca):
        self.peca = peca
        self.peca.move(self.pos)

    def limpa(self):
        self.peca = None


class Tabuleiro:
    def __init__(self):
        def joga(peca, xyz):
            tipo, cor = peca
            x, y, z = xyz
            #tipo(pos=xyz, size=(4, 4, 4), color= cor)
            #box(pos=xyz, size=(6, 6, 6), color= RBOW[z//VAO], opacity=0.2)
        self.angle = 0
        self.jogadas = {
            OESTE: self.oeste, NORTE: self.norte,
            LESTE: self.leste, SUL: self.sul, JOGA: self.joga
        }
        doc.bind('keypress', self.teclou)

        _gs = glow('main')
        cena = self.cena = canvas()
        cena.width = 1000
        cena.height = 800
        pecas = [(box, color.blue), (sphere, color.red)] * 4 * 4 * 2
        self.casas = {
            (coluna, linha, camada):
            Casa(pos=(coluna, linha, camada))
            for linha in CASAS for coluna in CASAS
            for camada in CASAS}

        shuffle(pecas)
        jogadas = [joga(pecas.pop(), (coluna*VAO, linha*VAO, camada*VAO))
                   for linha in CASAS for coluna in CASAS
                   for camada in CASAS]
        self.joga()

    def teclou(self, ev):
        jogada = ev.keyCode
        if jogada in JOGADAS:
            ev.stopPropagation()
            ev.preventDefault()
            #print("teclou", jogada)
            self.jogadas[jogada]()

    def move(self, casa, sentido):
        destino = vec_soma(casa.pos, sentido)

        print(casa.pos, destino, sentido)
        peca = casa.peca
        while destino in self.casas.keys():
            self.casas[destino].recebe(peca)
            casa.limpa()
            destino = vec_soma(peca.pos, sentido)

            print(peca.pos, destino, sentido)

    def joga(self):
        vetor = self.cena.forward
        xyz = (vetor.x, vetor.y, vetor.z)
        queda = ROTATE[xyz][0]
        cheios = [casa for casa in self.casas.values() if casa.peca is not None]
        cheios = [self.move(casa, queda) for casa in cheios]

        vazios = [casa for casa in self.casas.values() if casa.peca is None]
        shuffle(vazios)
        vazios.pop().joga()

    def rodar(self, vetor, eixo):
        self.angle = 0

        def rodando(wait=lambda: None):
            if self.angle in range(10):
                self.cena.forward = y.rotate({'angle': self.angle*pi/20, 'axis': vec(a, b, c)._vec})
                self.angle += 1
            else:
                timer.clear_interval(_timer)
                f = self.cena.forward
                self.cena.forward = vec(int(f.x*2), int(f.y*2), int(f.z*2))._vec
                print(self.cena.forward)

        azim = (vetor.x, vetor.y, vetor.z)
        a, b, c = ROTATE[azim][eixo]
        y = self.cena.forward
        _timer = timer.set_interval(rodando, 100)

    def oeste(self):
        self.rodar(self.cena.forward, 0)
        pass

    def norte(self):
        self.rodar(self.cena.forward, 1)
        pass

    def leste(self):
        self.rodar(self.cena.forward, 2)
        pass

    def sul(self):
        pass
        self.rodar(self.cena.forward, 3)


def main():
    global TABULEIRO
    print('Tuplethora %s' % __version__, color, FOCO)
    TABULEIRO = Tabuleiro()

if __name__ == "__main__":
    main()