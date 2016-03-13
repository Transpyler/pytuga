"""
The main TurtleScene and TurtleView classes.

These are derived from QGraphicsScene and QGraphicsView and can be used anywhere
these two classes are expected.
"""

import time
from collections import deque
from PyQt5 import QtGui, QtWidgets, QtCore
from .mathutil import Vec
from .turtleobject import Turtle

_LABEL_FONT = QtGui.QFont('Helvetica', 8)
_LABEL_FONT.setStyleStrategy(QtGui.QFont.NoAntialias)
_LABEL_PADDING = 2


class TurtleView(QtWidgets.QGraphicsView):
    """
    A TurtleView is a widget that can be inserted anywhere in the GUI and is
    responsible to render and display a TurtleScene.

    By default, the TurtleView applies a transforms that inverts the
    y-coordinate so that it point upwards instead of downwards (as is the
    default in many computer graphics applications). This transform also invert
    the direction of rotations: positive rotations are counter-clockwise and
    negative rotations are clockwise.
    """

    def __init__(self, scene=None):
        if scene is None:
            scene = TurtleScene()
        self._scene = scene
        super().__init__(scene)
        transform = QtGui.QTransform(1,  0,
                                     0, -1,
                                     0,  0)
        self.setTransform(transform)
        self._zoomfactor = 1.2

        # This will crash if I put it in the module namespace, probably
        # because the QApplication instance does not exist yet
        _LABEL_HEIGHT = QtGui.QFontMetrics(_LABEL_FONT).height()+2*_LABEL_PADDING

        w = self._posLabel = QtWidgets.QLabel(self)
        # http://stackoverflow.com/questions/7928519/how-to-make-the-qlabel-background-semi-transparent
        # Fourth parameter in color tuple is alpha: 0-transparent; 255-opaque
        w.setStyleSheet('color: rgba(0, 0, 0, 196); '
                        'background-color: rgba(0, 0, 0, 0);'
                        'padding: %d' % _LABEL_PADDING)
        w.setAlignment(QtCore.Qt.AlignRight)
        w.setFont(_LABEL_FONT)
        w.setGeometry(0, 0, 100, _LABEL_HEIGHT)
        self.__posLabel_makeText((0, 0))
        self.__posLabel_position()

    def zoomIn(self):
        self.scale(self._zoomfactor, self._zoomfactor)

    def zoomOut(self):
        self.scale(1 / self._zoomfactor, 1 / self._zoomfactor)

    def notifyPosChanged(self, turtle, pos):
        assert isinstance(turtle, Turtle)
        assert isinstance(pos, Vec)  # May remove these assertions later
        self.__posLabel_makeText(pos)

    def resizeEvent(self, QResizeEvent):
        self.__posLabel_position()
        super().resizeEvent(QResizeEvent)

    def __posLabel_position(self):
        size = self.viewport().size()
        w = self._posLabel
        margin = 3
        w.move(size.width() - w.width() - margin,
               size.height()-w.height() - margin)

    def __posLabel_makeText(self, pos):
        s = "x=%s, y=%s" % (round(pos[0]), round(pos[1]))
        self._posLabel.setText(s)

    def saveImage(self, fname):
        rect = self.viewport()
        rgb = QtGui.QImage.Format_RGB32
        image = QtGui.QImage(rect.width(), rect.height(), rgb)
        image.fill(QtGui.QColor(255, 255, 255))
        painter = QtGui.QPainter(image)
        self.render(painter)
        if not image.save(fname):
            raise ValueError('could not save image %s' % fname)
        del painter


class TurtleScene(QtWidgets.QGraphicsScene):
    """
    The TurtleScene defines the scene in which geometric objects resides.

    It controls the Turtle object and how it draws in the screen.
    """

    def __init__(self, parent=None, fps=30):
        super().__init__(parent)
        self._fps = fps
        self._interval = 1 / fps
        self.startTimer(1000 / fps)
        self._init(fps=fps)

        # Connect signals to slots
        self.clear_screen_signal.connect(self.clearScreen)
        self.restart_screen_signal.connect(self.restartScreen)

    def _init(self, fps=30):
        self._lines = []
        self._turtles = []
        self._turtle = None
        self._tasks = deque()
        self._pen = QtGui.QPen(QtGui.QColor(0, 0, 0))
        self._pen.setWidth(2)
        self._brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        self.addTurtle(default=True)

    def clear(self):
        super().clear()
        self._init(self._fps)

    #
    # Events and signals
    #
    clear_screen_signal = QtCore.pyqtSignal()
    restart_screen_signal = QtCore.pyqtSignal()

    def clearScreen(self):
        state = self.fullTurtleState()
        self.clear()
        self.setFullTurtleState(state)

    def restartScreen(self):
        self.clear()

    #
    # Task control
    #
    def cancelTasks(self):
        """Cancel all pending tasks"""

        self._tasks = deque()

    def iterTasks(self):
        """Iterate over all tasks."""

        while self._tasks:
            for task in self._tasks[0]:
                yield task
            else:
                self._tasks.popleft()
        yield True

    def consumeTask(self):
        """Consumes a task in the queue of _turtle modifications.

        Each task return a True/False value telling if the scheduler should
        wait for the next frame to process the next task."""

        for should_wait_flag in self.iterTasks():
            if should_wait_flag:
                return

    def timerEvent(self, timer):
        """Scheduled to be executed at some given framerate.

        It process all queued animation _tasks."""

        self.consumeTask()

    def flushExecution(self):
        while self._tasks:
            for _task_result in self._tasks[0]:
                pass
            else:
                self._tasks.popleft()

    #
    # Turtle control
    #
    def addTurtle(self, turtle=None, *, default=False, **kwds):
        """Adds new _turtle to the scene."""

        if turtle is None:
            turtle = Turtle(**kwds)
            self.addItem(turtle)
            self._turtles.append(turtle)
        else:
            self.addItem(turtle)
        if default:
                self.setTurtle(turtle)

    def turtle(self):
        """Return the active turtle"""

        return self._turtle

    def setTurtle(self, turtle):
        """Configures the active Turtle object"""

        self._turtle = turtle

    def getNamespace(self, D={}, **kwds):
        """Return a mapping with all turtle module functions."""

        from .turtlenamespace import TurtleNamespace
        return TurtleNamespace(self, D, **kwds)

    #
    # Turtle visibility
    #
    def isTurtleVisible(self):
        if self._turtle is None:
            return False
        return self._turtle.isVisible()

    def isTurtleHidden(self):
        return not self.isTurtleVisible()

    def hideTurtle(self):
        if self._turtle is not None:
            self._turtle.hide()

    def showTurtle(self):
        if self._turtle is None:
            raise TypeError('no turtle is defined')
        self._turtle.show()

    #
    # Communication with the TurtleNamespace object is done exclusively through
    # the two functions bellow
    #
    def turtleState(self, name):
        """Return the requested variable value in current turtle's state
        tip."""

        if name == 'pos':
            return self._turtle.tip_pos
        elif name == 'heading':
            return self._turtle.tip_heading
        elif name == 'isdown':
            return self._turtle.tip_isdown
        elif name == 'color':
            return self._turtle.tip_color
        elif name == 'fill':
            return self._turtle.tip_fill
        elif name == 'width':
            return self._turtle.tip_width
        else:
            raise ValueError('invalid _turtle property: %r' % name)

    def setTurtleState(self, name, value, *, draw=True, delay=0):
        """Deferred update of turtle's state.

        It modifies the tip and queues changes to be applied to the actual
        turtle's state. If delay is given, the complete modification to turtle's
        state may requires more that one frame of animation."""

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

    def fullTurtleState(self):
        state = {}
        for attr in ['pos', 'heading', 'isdown', 'color', 'fill', 'width']:
            state[attr] = self.turtleState(attr)
        return state

    def setFullTurtleState(self, state):
        for attr, value in state.items():
            self.setTurtleState(attr, value, draw=False, delay=0)

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
                self.__notifyPosChanged(turtle, pos)
                t = time.time() - t0
                yield True

        line.setLine(x0, y0, xf, yf)
        turtle.setPos(*endpos)
        self.__notifyPosChanged(turtle, endpos)

    def __setProp(self, prop, value):
        setattr(self._turtle, 'tip_' + prop, value)
        yield

    def __notifyPosChanged(self, turtle, pos):
        """Notifies scene view that the position of a turtle has changed,
        callback way."""

        for view in self.views():
            view.notifyPosChanged(turtle, pos)

    def __getView(self):
        views = self.views()
        if len(views) > 0:
          return views[0]
        return None
