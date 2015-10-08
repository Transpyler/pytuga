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
        transform = QtGui.QTransform(1, 0, 0, -1, 0, 0)
        self.setTransform(transform)
        

class TurtleScene(QtWidgets.QGraphicsScene):
    '''
    The TurtleScene defines the scene in which geometric objects resides.
    
    It controls the Turtle object and how it draws in the screen.
    '''
    
    def __init__(self, fps=30):
        super().__init__()
        self.fps = fps
        self._interval = 1 / fps
        self._lines = []
        self._turtles = []
        self.turtle = None
        self.tasks = []
        self.startTimer(1000 * self._interval)
        self.pen = QtGui.QPen(QtGui.QColor(0, 0, 0))
        self.pen.setWidth(2)
        self.brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        self.init()
        
    def init(self):
        self.addTurtle(default=True)
        
    def iterTasks(self):
        '''Iterate over all tasks.'''
        while self.tasks:
            for task in self.tasks[0]:
                yield task
            else:
                self.tasks.pop(0)
        yield True

    def consumeTask(self):
        '''Consumes a task in the queue of turtle modifications.

        Each task return a True/False value telling if the scheduler should
        wait for the next frame to process the next task.'''
        
        for result in self.iterTasks():
            if result:
                return 
        
    def timerEvent(self, timer):
        '''Scheduled to be executed at some given framerate. 
        
        It process all queued animation tasks.'''
        
        self.consumeTask()
        
    def addTurtle(self, pos=(0, 0), default=False):
        '''Adds new turtle to the scene.'''
        
        turtle = Turtle(*pos)
        self.addItem(turtle)
        self._turtles.append(turtle)
        if default:
            self.setActiveTurtle(turtle)

    def setActiveTurtle(self, turtle):
        '''Configures the active Turtle object'''
         
        self.turtle = turtle
        
    def getNamespace(self, D={}, **kwds):
        '''Return a mapping with all turtle module functions.'''
        
        from .turtlenamespace import TurtleNamespace 
        return TurtleNamespace(self, D, **kwds)

    #
    # Communication with the TurtleNamespace object is done exclusivelly through
    # the two functions bellow
    #
    def getTurtleState(self, name):
        '''Return the requested variable value in current turtle's state tip.'''
        
        if name == 'pos':
            return self.turtle.tip_pos
        elif name == 'heading':
            return self.turtle.tip_heading
        else:
            raise ValueError('invalid turtle property: %r' % name)
        
    def setTurtleState(self, name, value, *, draw=True, delay=0):
        '''Deffered update of turtle's state.
        
        It modifies the tip and queues changes to be applied to the actual 
        turtle's state. If delay is given, the complete modification to turtle's 
        state may requires more that one frame of animation.'''
        
        if name == 'pos':
            subtasks = self.__setPos(value, delay, draw)
        elif name == 'heading':
            subtasks = self.__setHeading(value, delay)
        else:
            raise ValueError('invalid turtle property: %r' % name)
        
        subtasks = iter(subtasks)
        next(subtasks)
        self.tasks.append(subtasks) 
        
    #
    # Set state helpers
    #
    def __setHeading(self, angle, delay):
        startangle = self.turtle.tip_heading
        self.turtle.tip_heading = angle
        yield
        
        if delay:
            t0 = time.time()
            t = 0
            delta = angle - startangle
            
            while t < delay:
                theta = startangle + delta * t / delay
                self.turtle.setRotation(theta)
                t = time.time() - t0
                yield True
                
        self.turtle.setRotation(angle)
        
            
    def __setPos(self, pos, delay, draw):
        # Update tip
        x0, y0 = pos0 = self.turtle.tip_pos
        endpos = pos = Vec(*pos)
        self.turtle.tip_pos = pos
        yield
        
        # Create a line and draw
        xf, yf = pos
        line = self.addLine(x0, y0, x0, y0, self.pen)
        if not draw:
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
                self.turtle.setPos(*pos)
                t = time.time() - t0
                yield True
        
        line.setLine(x0, y0, xf, yf)
        self.turtle.setPos(*endpos)
        