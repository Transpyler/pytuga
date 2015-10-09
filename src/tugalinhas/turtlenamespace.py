'''
This class implements the namespace of turtle-art functions.

It can be overriden in order to create a different set of functions, either by
inclusion of exclusion of items. 
'''

import io
import sys
from collections import MutableMapping
from .util import vecargsmethod
from .mathutil import Vec


def alias(*args):
    '''Set a list of function aliases for TurtleFunction methods. 
    
    The aliases are automatically included in the resulting namespace.'''
    
    def decorator(func):
        func.alias_list = args
        return func
    return decorator


class TurtleNamespace(MutableMapping):
    '''
    Defines the namespace of turtle functions. 
    
    The TurtleFunction namespace behaves like a dictionary and requires a 
    TurtleScene as a first argument. Additional keyworkd arguments are 
    inserted into the dictionary. 
    '''
    
    _BLACKLIST = ['items', 'keys', 'values', 'get', 'blacklist', 
                  'update', 'setdefault', 'pop', 'popitem', 'clear']
    
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
        
        return self._scene.getTurtleState(name)
        
    def _setstate(self, name, value, **kwds):
        '''Modify the state of the current turtle.'''
        
        self._scene.setTurtleState(name, value, **kwds)
        
    def blacklist(self, name):
        '''Adds given name to blacklist of function names'''
        
        self._blacklist.add(name)
        
    def _threaded_factory(self, func):
        '''Return a threaded factory function'''
        
    #
    # Direct state control
    #
    def getpos(self):
        '''Return a vector (x, y) with turtle's position (in pixels)'''
        
        return self._getstate('pos')
    
    @vecargsmethod
    def setpos(self, value):
        '''Modifies turtle's position (in pixels)
        
        User can pass the x, y coordinates of the new position or a tuple of 
        (x, y) values.'''
        
        return self._setstate('pos', value)
    
    def getheading(self):
        '''Return current heading of the turtle (in degrees)'''
        
        return self._getstate('heading')
    
    def setheading(self, value):
        '''Modifies turtle's heading (in degrees)'''
        
        return self._setstate('heading', value)

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
    
    def penup(self):
        '''Raises the turtle pen so it stops drawing'''
        
        return self._setstate('isdrawing', False)
    
    def pendown(self):
        '''Lower the turtle pen so it can draw in the screen'''
        
        return self._setstate('isdrawing', True)
    
    def isdrawing(self):
        '''Return True if the pen is down or False otherwise'''
        
        return self._getstate('isdrawing')
            
    #
    # Movement functions
    #
    @vecargsmethod
    def goto(self, pos):
        '''Goes to the given position.
        
        If the pen is down, it draws a line.'''
        
        self._setstate('pos', pos, draw=True, delay=self._delay)
    
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
    