"""
This class implements the namespace of turtle-art functions.

It can be overriden in order to create a different set of functions, either by
inclusion of exclusion of items. 
"""

import io
import sys
from collections import MutableMapping
from .mathutil import Vec
from functools import wraps as _wraps
from .mathutil import Vec as _Vec

COLOR_TRANSLATIONS = {
    'azul': 'blue',
    'amarelo': 'yellow',
    'vermelho': 'red',
    'preto': 'black',
    'branco': 'white',
}


def _vecargsmethod(func):
    """
    Decorates a function of a vec object to accept the following signatures:

        func(vec, **kwds)
        func(x, y, **kwds)

    A Vec object is always passed to the given implementation.
    """
    @_wraps(func)
    def decorated(self, x, y=None, **kwds):
        if y is None:
            try:
                x, y = x
            except ValueError:
                raise ValueError('expected 2 elements, got %s' % len(x))

            return func(self, _Vec(x, y), **kwds)
        else:
            return func(self, _Vec(x, y), **kwds)
    return decorated


def alias(*args):
    """Set a list of function aliases for TurtleFunction methods. 
    
    The aliases are automatically included in the resulting namespace."""
    
    def decorator(func):
        func.alias_list = args
        return func
    return decorator


class TurtleNamespaceEnglish(MutableMapping):
    """
    Defines the namespace of turtle functions. 
    
    The TurtleFunction namespace behaves like a dictionary and requires a 
    TurtleScene as a first argument. Additional keyword arguments are
    inserted into the dictionary. 
    """
    
    _BLACKLIST = ['items', 'keys', 'values', 'get', 'blacklist', 
                  'update', 'setdefault', 'pop', 'popitem']
    
    def __init__(self, scene, D={}, **kwds):
        self._scene = scene
        self._data = {}
        self._data.update(**kwds)
        self._blacklist = set(self._BLACKLIST)
        self.__inspect()
        self._delay = 0.05
    
    def __delitem__(self, key):
        del self._data[key]
        
    def __getitem__(self, key):
        return self._data[key]
    
    def __setitem__(self, key, value):
        self._data[key] = value
    
    def __iter__(self):
        return iter(self._data)
    
    def __len__(self):
        return len(self._data)
    
    def __inspect(self):
        D = {}
        blacklist = self._blacklist
        
        for name in dir(self):
            if name.startswith('_') or name in blacklist:
                continue
            
            # Add to dictionary
            func = getattr(self, name)
            D[name] = func
            for alias in getattr(func, 'alias_list', ()):
                D[alias] = func

        self._data.update(D)

    @classmethod
    def _getaliases(cls):
        D = {}
        blacklist = set(cls._BLACKLIST)

        for name in dir(cls):
            # Add to dictionary
            func = getattr(cls, name)
            for alias in getattr(func, 'alias_list', ()):
                D[alias] = name
        return D

    def _getstate(self, name):
        """Get the current (tip) value of the state of the current turtle."""
        
        return self._scene.turtleState(name)
        
    def _setstate(self, name, value, **kwds):
        """Modify the state of the current turtle."""
        
        self._scene.setTurtleState(name, value, **kwds)
        
    def _getturtle(self):
        """Return the current turtle"""
        
        return self._scene.turtle()
        
    def blacklist(self, name):
        """Adds given name to blacklist of function names"""
        
        self._blacklist.add(name)
        
    def _threaded_factory(self, func):
        """Return a threaded factory function"""
        
    #
    # Speed control
    #
    def speed(self, n):
        """Set the simulation speed: its a number between 1 and 10, where
        0 is the slowest and 10 is the fastest"""
        
        self._delay = max(0.05/n**2 - 0.0005, 0)
        
    #
    # Direct state control
    #
    def getpos(self):
        """Return a vector (x, y) with turtle's position (in pixels)"""
        
        return self._getstate('pos')
    
    @_vecargsmethod
    def setpos(self, value):
        """Modifies turtle's position (in pixels)
        
        User can pass the x, y coordinates of the new position or a tuple of 
        (x, y) values."""

        self._setstate('pos', value, draw=False, delay=0)
    
    def getheading(self):
        """Return current heading of the turtle (in degrees)"""
        
        return self._getstate('heading')
    
    def setheading(self, value):
        """Modifies turtle's heading (in degrees)"""

        self._setstate('heading', value, delay=0)

    def getwidth(self):
        """Return the pen width (in pixels)"""
        
        return self._getstate('width')
    
    def setwidth(self, value):
        """Modifies the pen width heading (in pixels)"""

        self._setstate('width', value)
    
    def getcolor(self):
        """Return a tuple of (R, G, B) with the current pen color"""
        
        return self._getstate('color')
    
    def setcolor(self, color):
        """Modifies the pen color.
        
        Color can be specified as an (R, G, B) tuple or as a hex string or by
        name."""

        self._setstate('color', color)
    
    def getfill(self):
        """Return a tuple of (R, G, B) with the current fill color"""
        
        return self._getstate('fill')
    
    def setfill(self, color):
        """Modifies the fill color.
        
        Color can be specified as an (R, G, B) tuple or as a hex string or by
        name."""
        self._setstate('fill', color)
    
    @alias('pu')
    def penup(self):
        """Raises the turtle pen so it stops drawing"""

        self._setstate('isdown', False)
    
    @alias('pd')
    def pendown(self):
        """Lower the turtle pen so it can draw in the screen"""

        self._setstate('isdown', True)
    
    def isdown(self):
        """Return True if the pen is down or False otherwise"""
        
        return self._getstate('isdown')

    #
    # Movement functions
    #
    @_vecargsmethod
    def goto(self, pos):
        """Goes to the given position.

        If the pen is down, it draws a line."""

        will_draw = self._getstate('isdown')
        self._setstate('pos', pos, draw=will_draw, delay=self._delay)

    @_vecargsmethod
    def jumpto(self, pos):
        """Goes to the given position without drawing."""

        self._setstate('pos', pos, draw=False, delay=self._delay)

    @alias('fd')
    def forward(self, step):
        """Move the turtle forward by the given step size (in pixels).

        Return a vector with final position after the movement."""
        
        delta = Vec.from_angle(self.getheading()) * step
        finalpos = delta + self.getpos()
        self.goto(finalpos)

    @alias('bk', 'back')
    def backward(self, step):
        """Move the turtle backward by the given step size (in pixels).

        Return a vector with final position after the movement."""

        self.forward(-step)
    
    @alias('lt')
    def left(self, angle):
        """Rotate the turtle counter-clockwise by the given angle.
        
        Negative angles produces clockwise rotation. Return final heading."""
        
        heading = (self.getheading() + angle) % 360
        self._setstate('heading', heading, delay=self._delay)

    @alias('rt')
    def right(self, angle):
        """Rotate the turtle clockwise by the given angle.
        
        Negative angles produces counter-clockwise rotation. Return final
        heading."""

        self.left(-angle)
    
    def restart(self):
        """Restart the scene.
        
        Clear all elements on the screen and put turtle black to the 
        default position"""

        self._scene.restart_screen_signal.emit()

    def clear(self):
        """Clear elements preserving turtle.
        
        Clear all elements on the screen, but preserves turtle state."""

        self._scene.clear_screen_signal.emit()

    def turtlehelp(self):
        """Display a help message of all turtle functions"""
        
        L = ["List of supported turtle functions.\n"]
        for func in sorted(self._data):
            try:
                method = getattr(self, func)
                if callable(method):
                    L.append(function_description(method))
            except AttributeError:
                pass
        print('\n\n'.join(L))


#
# Pytuguês -- default temporário
#
# TODO: split Python from Pytuguês versions of tugalinhas
#       The python version can be called "Turtle" or "Logo"
#
class TurtleNamespace(TurtleNamespaceEnglish):
    """Quick hack around english namespace"""

    def frente(self, passo):
        """Move o Tuga para frente pelo passo especificado em pixels.

        Se a caneta estiver abaixada, desenha uma linha. Passos negativos
        correspondem a um movimento para trás.
        """

        return self.forward(passo)

    @alias('tras')
    def trás(self, passo):
        """Move o Tuga para trás pelo passo especificado em pixels.

        Se a caneta estiver abaixada, desenha uma linha. Passos negativos
        correspondem a um movimento para frente.
        """

        return self.backward(passo)

    def esquerda(self, ângulo):
        """Gira o Tuga para a esquerda pelo ângulo fornecido em graus."""

        return self.left(ângulo)

    def direita(self, ângulo):
        """Gira o Tuga para a direita pelo ângulo fornecido em graus."""

        return self.right(ângulo)

    @_vecargsmethod
    @alias('vá_para', 'va_para')
    def ir_para(self, posição):
        """Desloca o Tuga para o ponto dado.

        Se a caneta estiver abaixada, desenha uma linha."""

        self.goto(posição)

    @_vecargsmethod
    @alias('teletransporte', 'teletransportar', 'pule_para')
    def pular_para(self, posição):
        """Desloca o Tuga para o ponto dado sem desenhar.

        Não altera o estado da caneta após o deslocamento."""

        self.jumpto(posição)

    @alias('levante', 'subir_caneta', 'suba_caneta',
           'levantar_caneta', 'levante_caneta')
    def levantar(self):
        """Levanta a caneta do Tuga.

        Deslocamentos na tela não produzirão nenhum desenho."""

        self.penup()

    @alias('abaixe', 'baixe_caneta', 'baixar_caneta',
           'abaixar_caneta', 'abaixe_caneta')
    def abaixar(self):
        """Abaixa a caneta do Tuga.

        Deslocamentos na tela produzirão desenho."""

        self.pendown()

    def desenhando(self):
        """Retorna verdadeiro se a caneta estiver abaixada e falso, caso
        contrário."""

        return self.isdown()

    @alias('limpe')
    def limpar(self):
        """Limpa todos os desenhos na tela"""

        self.clear()

    @alias('reinicie')
    def reiniciar(self):
        """Limpa os desenhos na tela e retorna o Tuga para a orientação
        orignal"""

        self.restart()

    @alias('posicao')
    def posição(self):
        """Retorna um vetor de duas coordenada com a posição do Tuga"""

        return self.getpos()

    @alias('defina_posição', 'defina_posicao')
    def definir_posição(self, *args):
        """Define as novas coordenadas do Tuga.

        Pode receber dois argumentos com a nova posição x e y ou um argumento
        com um vetor ou tupla de duas coordenadas."""

        self.setpos(*args)

    @alias('direcao')
    def direção(self):
        """Retorna a orientação do Tuga em graus.

        Medimos a orientação a partir da posição horizontal com o Tuga olhando
        para a direita."""

        return self.getheading()

    @alias('defina_direção', 'defina_direcao')
    def definir_direção(self, direção):
        """Gira o Tuga para a orientação fornecida.

        Medimos a orientação a partir da posição horizontal com o Tuga olhando
        para a direita."""

        return self.setheading(direção)

    def cor_da_linha(self):
        """Retorna a cor da linha"""

        return self.getcolor()

    def cor_do_fundo(self):
        """Retorna a cor do fundo"""

        return self.getfill()

    @alias('defina_cor_da_linha')
    def definir_cor_da_linha(self, cor):
        """Define a cor da linha do desenho.

        A cor pode ser especificada pelas coordenadas (R, G, B), por uma string
        hex ou pelo seu nome em inglês ou português."""

        if isinstance(cor, str):
            cor = cor.lower()
            cor = COLOR_TRANSLATIONS.get(cor, cor)
        self.setcolor(cor)

    @alias('defina_cor_do_fundo')
    def definir_cor_do_fundo(self, cor):
        """Define a cor do preenchimento.

        A cor pode ser especificada pelas coordenadas (R, G, B), por uma string
        hex ou pelo seu nome em inglês ou português."""

        if isinstance(cor, str):
            cor = cor.lower()
            cor = COLOR_TRANSLATIONS.get(cor, cor)
        self.setfill(cor)

    def espessura(self):
        """Retorna a espessura da linha em pixels."""

        return self.getwidth()

    @alias('defina_espessura')
    def definir_espessura(self, px):
        """Define a espessura da linha em pixels."""

        self.setwidth(px)

    @alias('definir_velocidade', 'defina_velocidade')
    def velocidade(self, valor):
        """Modifica a velocidade de desenho do Tuga.

        A velocidade corresponde a um número de 1 até 10, onde 1 corresponde
        ao desenho mais lento e 10 ao desenho mais rápido."""

        self.speed(valor)

    def ajuda(self):
        """Mostra uma ajuda com os principais comandos disponíveis em inglês."""

        self.turtlehelp()


def helpstr(*args):
    """Returns the output of the help() function as a string"""
    
    stdout, sys.stdout = sys.stdout, io.StringIO()
    try:
        help(*args)
        data = sys.stdout.getvalue()
    finally:
        sys.stdout = stdout
    return data


def function_description(method):
    """Format function description to show in turtlefunc() help"""
    
    data = helpstr(method).partition('\n\n')[2]
    head, _, descr = data.partition('\n')
    head = head.partition(' method')[0].rjust(20)
    descr = descr.partition('\n')[0].lstrip()
    data = '%s -- %s' % (head, descr)
    alias = getattr(method, 'alias_list', None)
    if alias:
        data += '\n' + (', '.join(alias)).rjust(20)
    return data
