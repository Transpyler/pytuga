"""

Desenho
=======

Funções de desenho que utilizam a biblioteca turtle.

(This module will be deprecated)
"""

try:
    import turtle as _TURTLE_MODULE
except ImportError:
    _TURTLE_MODULE = None
from transpyler.utils import synonyms


def _turtle():
    """Return turtle module or an error"""

    if _TURTLE_MODULE is None:
        raise RuntimeError('o módulo turtle ou o módulo tk não estão '
                           'disponíveis, cheque sua instalação')
    else:
        return _TURTLE_MODULE


def frente(passo):
    """Anda para frente pelo passo especificado em pixels"""

    _turtle().fd(passo)


def trás(passo):
    """Anda para trás pelo passo especificado em pixels"""

    _turtle().bk(passo)


def direita(ângulo):
    """Gira para a direita pelo ângulo especificado (em graus)"""

    _turtle().right(ângulo)


def esquerda(ângulo):
    """Gira para a esquerda pelo ângulo especificado (em graus)"""

    _turtle().left(ângulo)


@synonyms('vá_para')
def ir_para(x, y):
    """
    Move cursor para a posição absoluta especificada em pixels.

    Se a caneta estiver abaixada, desenha uma linha até o ponto especificado"""

    _turtle().goto(x, y)


def começo():
    """Move cursor para a origem do sistema de coordenadas.

    Se a caneta estiver abaixada, desenha uma linha até o ponto especificado"""

    _turtle().home()


@synonyms('mude_x')
def mudar_x(x):
    """Define a primeira coordenada da posição para o valor x deixando a outra
    inalterada."""

    _turtle().setx(x)


@synonyms('mude_y')
def mudar_y(y):
    """Define a segunda coordenada da posição para o valor y deixando a outra
    inalterada."""

    _turtle().sety(y)


@synonyms('mude_orientação')
def mudar_orientação(ângulo):
    """Define a orientação do cursor. Um ângulo=0 aponta o cursor na
    direção do eixo x. A rotação é definida no sentido anti-horário."""

    _turtle().setheading(ângulo)


@synonyms('suba_caneta')
def subir_caneta():
    """Para de desenhar na tela na medida em que o cursor se movimenta.

    Pense que se trata de um robô e que a caneta responsável pelo desenho está
    levantada do papel."""

    _turtle().pu()


@synonyms('desca_caneta')
def descer_caneta():
    """Volta a desenhar na tela na medida em que o cursor se movimenta.

    Pense que se trata de um robô e que a caneta responsável pelo desenho está
    abaixada sobre o papel."""

    _turtle().pd()
