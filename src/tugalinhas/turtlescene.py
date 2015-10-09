'''
The main TurtleScene and TurtleView classes. 

These are derived from QGraphicsScene and QGraphicsView and can be used anywhere
these two classes are expected.
'''

import time
from .util import QtGui, QtWidgets
from .mathutil import Vec
from .turtleobject import Turtle


class TurtleView(QtWidgets.QGraphicsView):
    '''
    A TurtleView is a widget that can be inserted anywhere in the GUI and is
    responsible to render and display a TurtleScene.
    
    By default, the TurtleView applies a transforms that inverts the 
    y-coordinate so that it point upwards instead of downwards (as is the 
    default in many computer graphics applications). This transform also invert
    the direction of rotations: positive rotations are counter-clockwise and 
    negative rotations are clockwise.
    
    '''
    def __init__(self, scene=None):
        if scene is None:
            scene = TurtleScene()
        super().__init__(scene)
        transform = QtGui.QTransform(+1, +0, 
                                     +0, -1, 
                                     +0, +0)
        self.setTransform(transform)
        self._zoomfactor = 1
        self._zoomstep = 0.2
         
    def zoomIn(self):
        self._zoomfactor *= self._zoomstep + 1
        self.scale(self._zoomfactor, self._zoomfactor)
    
    def zoomOut(self):
        self._zoomfactor /= self._zoomstep + 1
        self.scale(self._zoomfactor, self._zoomfactor)


class TurtleScene(QtWidgets.QGraphicsScene):
    '''
    The TurtleScene defines the scene in which geometric objects resides.
    
    It controls the Turtle object and how it draws in the screen.
    '''
    
    def __init__(self, parent=None, fps=30):
        super().__init__(parent)
        self.fps = fps
        self._interval = 1 / fps
        self.startTimer(1000 / fps)
        self._init(fps=fps, addturtle=True)
        
    def _init(self, fps=30, addturtle=False):
        self._lines = []
        self._turtles = []
        self._turtle = None
        self._tasks = []
        self._pen = QtGui.QPen(QtGui.QColor(0, 0, 0))
        self._pen.setWidth(2)
        self._brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        if addturtle:
            self.addTurtle(default=True)

    def clear(self):
        super().clear()
        self._init(self.fps)
        
    def iterTasks(self):
        '''Iterate over all _tasks.'''
        while self._tasks:
            for task in self._tasks[0]:
                yield task
            else:
                self._tasks.pop(0)
        yield True

    def consumeTask(self):
        '''Consumes a task in the queue of _turtle modifications.

        Each task return a True/False value telling if the scheduler should
        wait for the next frame to process the next task.'''
        
        for result in self.iterTasks():
            if result:
                return 
        
    def timerEvent(self, timer):
        '''Scheduled to be executed at some given framerate. 
        
        It process all queued animation _tasks.'''
        
        self.consumeTask()
        
    def addTurtle(self, turtle=None, *, default=False, **kwds):
        '''Adds new _turtle to the scene.'''
        
        if turtle is None:
            turtle = Turtle(**kwds)
            self.addItem(turtle)
            self._turtles.append(turtle)
        else:
            self.addItem(turtle)
        if default:
                self.setTurtle(turtle)
    
    def turtle(self):
        '''Return the active turtle'''
        
        return self._turtle

    def setTurtle(self, turtle):
        '''Configures the active Turtle object'''
         
        self._turtle = turtle
        
    def getNamespace(self, D={}, **kwds):
        '''Return a mapping with all _turtle module functions.'''
        
        from .turtlenamespace import TurtleNamespace 
        return TurtleNamespace(self, D, **kwds)

    #
    # Communication with the TurtleNamespace object is done exclusivelly through
    # the two functions bellow
    #
    def turtleState(self, name):
        '''Return the requested variable value in current _turtle's state tip.'''
        
        if name == 'pos':
            return self._turtle.tip_pos
        elif name == 'heading':
            return self._turtle.tip_heading
        elif name == 'isdown':
            return self._turtle.tip_isdown
        elif name == 'color':
            return self._turtle.self.tip_color
        elif name == 'fill':
            return self._turtle.tip_fill
        elif name == 'width':
            return self._turtle.tip_width
        else:
            raise ValueError('invalid _turtle property: %r' % name)
        
    def setTurtleState(self, name, value, *, draw=True, delay=0):
        '''Deffered update of _turtle's state.
        
        It modifies the tip and queues changes to be applied to the actual 
        _turtle's state. If delay is given, the complete modification to _turtle's 
        state may requires more that one frame of animation.'''
        
        if name == 'pos':
            subtasks = self.__setPos(value, delay, draw)
        elif name == 'heading':
            subtasks = self.__setHeading(value, delay)
        elif name == 'isdown':
            subtasks = self.__setProp('isdown', value)
        elif name == 'color':
            subtasks = self.__setProp('color', value)
        elif name == 'fill':
            subtasks = self.__setProp('fill', value)
        elif name == 'width':
            subtasks = self.__setProp('width', value)
        else:
            raise ValueError('invalid _turtle property: %r' % name)
        
        subtasks = iter(subtasks)
        next(subtasks)
        self._tasks.append(subtasks) 
        
    #
    # Set state helpers
    #
    def __setHeading(self, angle, delay):
        startangle = self._turtle.tip_heading
        self._turtle.tip_heading = angle
        yield
        
        if delay:
            t0 = time.time()
            t = 0
            delta = angle - startangle
            
            while t < delay:
                theta = startangle + delta * t / delay
                self._turtle.setRotation(theta)
                t = time.time() - t0
                yield True
                
        self._turtle.setRotation(angle)
        
            
    def __setPos(self, pos, delay, draw):
        # Update tip
        turtle = self._turtle
        x0, y0 = pos0 = self._turtle.tip_pos
        endpos = pos = Vec(*pos)
        turtle.tip_pos = pos
        yield
        
        # Create a line and draw
        xf, yf = pos
        line = self.addLine(x0, y0, x0, y0, self._pen)
        if not (draw and turtle.tip_isdown):
            self.removeItem(line)
        else:
            self._lines.append(line)
        
        if delay:
            t0 = time.time()
            t = 0
            delta = pos - pos0
            
            while t < delay:
                pos = pos0 + delta * (t / delay)
                line.setLine(x0, y0, *pos)
                turtle.setPos(*pos)
                t = time.time() - t0
                yield True
        
        line.setLine(x0, y0, xf, yf)
        turtle.setPos(*endpos)
        
    def __setProp(self, prop, value):
        setattr(self._turtle, 'tip_' + prop, value)
        yield