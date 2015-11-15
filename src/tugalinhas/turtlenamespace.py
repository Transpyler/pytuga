'''
This class implements the namespace of turtle-art functions.

It can be overriden in order to create a different set of functions, either by
inclusion of exclusion of items. 
'''

import io
import sys
from collections import MutableMapping
from .mathutil import Vec
from functools import wraps as _wraps
from .mathutil import Vec as _Vec


def _vecargsmethod(func):
    '''
    Decorates a function of a vec object to accept the following signatures:

        func(vec, **kwds)
        func(x, y, **kwds)

    A Vec object is always passed to the given implementation.
    '''
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
    '''Set a list of function aliases for TurtleFunction methods. 
    
    The aliases are automatically included in the resulting namespace.'''
    
    def decorator(func):
        func.alias_list = args
        return func
    return decorator


class TurtleNamespaceEnglish(MutableMapping):
    '''
    Defines the namespace of turtle functions. 
    
    The TurtleFunction namespace behaves like a dictionary and requires a 
    TurtleScene as a first argument. Additional keyword arguments are
    inserted into the dictionary. 
    '''
    
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
        

    def _getstate(self, name):
        '''Get the current (tip) value of the state of the current turtle.'''
        
        return self._scene.turtleState(name)
        
    def _setstate(self, name, value, **kwds):
        '''Modify the state of the current turtle.'''
        
        self._scene.setTurtleState(name, value, **kwds)
        
    def _getturtle(self):
        '''Return the current turtle'''
        
        return self._scene.turtle()
        
    def blacklist(self, name):
        '''Adds given name to blacklist of function names'''
        
        self._blacklist.add(name)
        
    def _threaded_factory(self, func):
        '''Return a threaded factory function'''
        
    #
    # Speed control
    #
    def speed(self, n):
        '''Set the simulation speed: its a number between 1 and 10, where
        0 is the slowest and 10 is the fastest'''
        
        self._delay = max(0.05/n**2 - 0.0005, 0)
        
    #
    # Direct state control
    #
    def getpos(self):
        '''Return a vector (x, y) with turtle's position (in pixels)'''
        
        return self._getstate('pos')
    
    @_vecargsmethod
    def setpos(self, value):
        '''Modifies turtle's position (in pixels)
        
        User can pass the x, y coordinates of the new position or a tuple of 
        (x, y) values.'''
        
        return self._setstate('pos', value, draw=False, delay=0)
    
    def getheading(self):
        '''Return current heading of the turtle (in degrees)'''
        
        return self._getstate('heading')
    
    def setheading(self, value):
        '''Modifies turtle's heading (in degrees)'''
        
        return self._setstate('heading', value, delay=0)

    def getwidth(self):
        '''Return the pen width (in pixels)'''
        
        return self._getstate('width')
    
    def setwidth(self, value):
        '''Modifies the pen width heading (in pixels)'''
        
        return self._setstate('width', value)
    
    def getcolor(self):
        '''Return a tuple of (R, G, B) with the current pen color'''
        
        return self._getstate('color')
    
    def setcolor(self, color):
        '''Modifies the pen color.
        
        Color can be specified as an (R, G, B) tuple or as a hex string or by
        name.'''
        
        return self._setstate('color', color)
    
    def getfill(self):
        '''Return a tuple of (R, G, B) with the current fill color'''
        
        return self._getstate('fill')
    
    def setfill(self, color):
        '''Modifies the fill color.
        
        Color can be specified as an (R, G, B) tuple or as a hex string or by
        name.'''
        return self._setstate('fill', color)
    
    @alias('pu')
    def penup(self):
        '''Raises the turtle pen so it stops drawing'''
        
        return self._setstate('isdown', False)
    
    @alias('pd')
    def pendown(self):
        '''Lower the turtle pen so it can draw in the screen'''
        
        return self._setstate('isdown', True)
    
    def isdown(self):
        '''Return True if the pen is down or False otherwise'''
        
        return self._getstate('isdown')

    #
    # Movement functions
    #
    @_vecargsmethod
    def goto(self, pos):
        '''Goes to the given position.

        If the pen is down, it draws a line.'''

        will_draw = self._getstate('isdown')

        self._setstate('pos', pos, draw=will_draw, delay=self._delay)

    @_vecargsmethod
    def jumpto(self, pos):
        '''Goes to the given position without drawing.'''

        self._setstate('pos', pos, draw=False, delay=self._delay)

    @alias('fd')
    def forward(self, step):
        '''Move the turtle forward by the given step size (in pixels)'''
        
        delta = Vec.from_angle(self.getheading()) * step
        self.goto(delta + self.getpos())
    
    @alias('bk', 'back')
    def backward(self, step):
        '''Move the turtle backward by the given step size (in pixels)'''
        
        return self.forward(-step)
    
    @alias('lt')
    def left(self, angle):
        '''Rotate the turtle counter-clockwise by the given angle.
        
        Negative angles produces clockwise rotation.'''
        
        heading = self.getheading()
        self._setstate('heading', heading + angle, delay=self._delay)
    
    @alias('rt')
    def right(self, angle):
        '''Rotate the turtle clockwise by the given angle.
        
        Negative angles produces counter-clockwise rotation.'''
        
        return self.left(-angle)
    
    def restart(self):
        '''Restart the scene.
        
        Clear all elements on the screen and put turtle black to the 
        default position'''
        
        self._scene.clear()
        self._scene.addTurtle(default=True)

    def clear(self):
        '''Clear elements preserving turtle.
        
        Clear all elements on the screen, but preserves turtle state.'''
        
        turtle = self._scene.turtle().copy()
        self._scene.clear()
        self._scene.addTurtle(turtle, default=True)
        
    
    def turtlehelp(self):
        '''Display a help message of all turtle functions'''
        
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
class TurtleNamespace(TurtleNamespaceEnglish):
    '''Quick hack around english namespace'''
    
    ns = TurtleNamespaceEnglish
    frente = ns.forward
    esquerda = ns.left
    direita = ns.right
    trás = ns.backward
    limpar = ns.clear
    reiniciar = ns.restart
    ir_para = ns.goto
    levanta = ns.penup
    abaixa = ns.pendown
    posição = ns.getpos
    definir_posição = ns.setpos
    cor_da_linha = ns.getcolor
    cor_do_fundo = ns.getfill
    definir_cor_da_linha = ns.setcolor
    definir_cor_do_fundo = ns.setfill
    direção = ns.getheading
    definir_direção = ns.setheading
    espessura = ns.getwidth
    definir_espessura = ns.setwidth
    velocidade = ns.speed
    del ns

        
def helpstr(*args):
    '''Returns the output of the help() function as a string'''
    
    stdout, sys.stdout = sys.stdout, io.StringIO()
    try:
        help(*args)
        data = sys.stdout.getvalue()
    finally:
        sys.stdout = stdout
    return data

def function_description(method):
    '''Format function description to show in turtlefunc() help'''
    
    data = helpstr(method).partition('\n\n')[2]
    head, _, descr = data.partition('\n')
    head = head.partition(' method')[0].rjust(20)
    descr = descr.partition('\n')[0].lstrip()
    data = '%s -- %s' % (head, descr)
    alias = getattr(method, 'alias_list', None)
    if alias:
        data += '\n' + (', '.join(alias)).rjust(20)
    return data
    