'''
This class implements the namespace of turtle-art functions.

It can be overriden in order to create a different set of functions, either by
inclusion of exclusion of items. 
'''

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
    
    _BLACKLIST = ['items', 'keys', 'values', 'get', 'blacklist']
    
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
        return self._getstate('pos')
    
    @vecargsmethod
    def setpos(self, value):
        return self._setstate('pos', value)
    
    def getheading(self):
        return self._getstate('heading')
    
    def setheading(self, value):
        return self._setstate('heading', value)

    def getwidth(self):
        return self._getstate('width')
    
    def setwidth(self, value):
        return self._setstate('width', value)
    
    def getcolor(self):
        return self._getstate('color')
    
    def setcolor(self, color):
        return self._setstate('color', color)
    
    def getfill(self):
        return self._getstate('fill')
    
    def setfill(self, color):
        return self._setstate('fill', color)
    
    def penup(self):
        return self._setstate('isdrawing', False)
    
    def pendown(self):
        return self._setstate('isdrawing', True)
    
    def isdrawing(self):
        return self._getstate('isdrawing')
            
    #
    # Movement functions
    #
    @vecargsmethod
    def goto(self, pos):
        self._setstate('pos', pos, draw=True, delay=self._delay)
    
    @alias('fd')
    def forward(self, step):
        delta = Vec.from_angle(self.getheading()) * step
        self.goto(delta + self.getpos())
    
    @alias('bk', 'back')
    def backward(self, step):
        return self.forward(-step)
    
    @alias('lt')
    def left(self, angle):
        heading = self.getheading()
        self._setstate('heading', heading + angle, delay=self._delay)
    
    @alias('rt')
    def right(self, angle):
        return self.left(-angle)
    
