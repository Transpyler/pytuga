import functools
import time

import sys

from logo.connection import TCPConnection, InProcessConnection
from logo.core import function_description
from logo.errors import InvalidResponseError
from logo.manager import InProcessManager, Manager
from logo.server import TurtleServer
from logo.utils import vecargsmethod


def public(func):
    """
    Mark function as public.
    """

    func._is_pylogo_public = True

    @functools.wraps(func)
    def decorated(self, *args, **kwargs):
        msg = func(self, *args, **kwargs)
        if isinstance(self, CursorManager):
            msg['cursor-id'] = self._id
            return self._client.send(msg)
        else:
            return self.send_message(msg)

    return decorated


def is_public(func):
    """
    Return True for functions marked with the @public decorator.
    """

    return getattr(func, '_is_pylogo_public', False)


class CursorMessagesMixin:
    """
    Public cursor functions.
    """

    # Speed control
    @public
    def speed(self, speed):
        """
        Set the simulation speed: its a number between 1 and 10, where
        0 is the slowest and 10 is the fastest.
        """

        return {'action': 'set-state', 'args': ['speed', speed]}

    # Direct state control
    @public
    def getpos(self):
        """
        Return a vector (x, y) with turtle's position (in pixels).
        """

        return {'action': 'get-state', 'args': ['pos']}

    @public
    @vecargsmethod
    def setpos(self, value):
        """
        Modifies turtle's position (in pixels)

        User can pass the x, y coordinates of the new position or a tuple of
        (x, y) values.
        """

        return {'action': 'set-state', 'args': ['pos', value]}

    @public
    def getheading(self):
        """
        Return current heading of the turtle (in degrees).
        """

        return {'action': 'get-state', 'args': ['heading']}

    @public
    def setheading(self, value):
        """
        Sets turtle's heading (in degrees).
        """

        return {'action': 'set-state', 'args': ['heading', value]}

    @public
    def getwidth(self):
        """
        Return the pen width (in pixels):
        """

        return {'action': 'get-state', 'args': ['width']}

    @public
    def setwidth(self, value):
        """
        Modifies the pen width (in pixels)
        """

        return {'action': 'set-state', 'args': ['width', value]}

    @public
    def getcolor(self):
        """
        Return a tuple of (R, G, B) with the current pen color.
        """

        return {'action': 'get-state', 'args': ['color']}

    @public
    def setcolor(self, value):
        """
        Modifies the pen color.

        Color can be specified as an (R, G, B) tuple or as a hex string or by
        name.
        """

        return {'action': 'set-state', 'args': ['color', value]}

    @public
    def getfillcolor(self):
        """
        Return a tuple of (R, G, B) with the current fill color.
        """

        return {'action': 'get-state', 'args': ['fillcolor']}

    @public
    def setfillcolor(self, value):
        """
        Modifies the fill color.

        Color can be specified as an (R, G, B) tuple or as a hex string or by
        name.
        """

        return {'action': 'set-state', 'args': ['fillcolor', value]}

    @public
    def penup(self):
        """
        Raises the turtle pen so it stops drawing.
        """

        return {'action': 'set-state', 'args': ['is_drawing', False]}

    @public
    def pendown(self):
        """
        Lower the turtle pen so it can draw in the screen.
        """

        return {'action': 'set-state', 'args': ['is_drawing', True]}

    @public
    def isdown(self):
        """
        Return True if the pen is down or False otherwise.
        """

        return {'action': 'get-state', 'args': ['is_drawing']}

    # Movement functions
    @vecargsmethod
    def goto(self, pos):
        """
        Goes to the given position.

        If the pen is down, it draws a line.
        """

        return {'action': 'set-state', 'args': ['goto', pos, None]}

    @vecargsmethod
    def jumpto(self, pos):
        """
        Goes to the given position without drawing.
        """

        return {'action': 'set-state', 'args': ['goto', pos, False]}

    @public
    def forward(self, step):
        """
        Move the turtle forward by the given step size (in pixels).
        """

        return {'action': 'step', 'args': [step]}

    @public
    def backward(self, step):
        """
        Move the turtle backward by the given step size (in pixels).
        """

        return {'action': 'step', 'args': [-step]}

    @public
    def left(self, angle):
        """
        Rotate the turtle counter-clockwise by the given angle.

        Negative angles produces clockwise rotation.
        """

        return {'action': 'rotate', 'args': [angle]}

    @public
    def right(self, angle):
        """
        Rotate the turtle clockwise by the given angle.

        Negative angles produces counter-clockwise rotation. Return final
        heading.
        """

        return {'action': 'rotate', 'args': [-angle]}


class GlobalMessagesMixin:
    """
    Public global functions.
    """

    @public
    def reset(self):
        """
        Clear all elements on the screen and put turtle black to the
        default state.
        """

        return {'action': 'reset'}

    @public
    def clear(self):
        """
        Clear all elements on the screen, but preserves turtle state.
        """

        return {'action': 'clear'}


class CursorManagerBase:
    """
    Controls a cursor object in the server.
    """

    def __init__(self, client, id):
        self._client = client
        self._id = id


class CursorManager(CursorMessagesMixin, CursorManagerBase):
    """
    Default manager for cursor obects.
    """


class ClientBase:
    """
    Client base features. Do not include cursor and public API.
    """

    connection_factory = TCPConnection
    manager_factory = Manager
    cursor_factory = CursorManager

    def __init__(self, manager=None, connection=None):
        self.manager = manager or self.manager_factory()
        self.connection = connection or self.connection_factory(self.manager)

    def start(self):
        """
        Starts client.
        """

        self.manager.start()
        self.connection.start()

    def send_message(self, msg):
        """
        Sends a message through the default conection.
        """

        reply = self.connection.send(msg)
        return self.process_response(reply)

    def process_response(self, response):
        """
        Process message response.
        """

        status = response.get('status', None)
        if status == 'error':
            raise self.reconstruct_exception(response)
        elif status == 'result':
            return response.get('value')
        elif status == 'ok':
            return None
        else:
            raise InvalidResponseError('invalid response: %r' % response)

    def reconstruct_exception(self, response):
        """
        Create an exception from error message.
        """

        if response['status'] != 'error':
            raise InvalidResponseError(response)

        # Get class
        full_name = response.get('error', 'builtins.Exception')
        modname, name = full_name.rpartition('.')
        mod = __import__(modname, fromlist=[name])
        cls = getattr(mod, name)
        args = response.get('args', [])
        kwargs = response.get('kwargs', {})
        return cls(*args, **kwargs)

    def sleep(self, interval):
        """
        Sleeps during the given interval.
        """

        time.sleep(interval)

    def help_string(self):
        """
        Return a help message of all turtle functions.
        """

        L = ["List of supported turtle functions.\n"]
        for name, method in sorted(self.namespace().items()):
            try:
                if callable(method):
                    L.append(function_description(method))
            except AttributeError:
                pass
        return '\n\n'.join(L)

    def namespace(self):
        """
        Return a dictionary with the public namespace for client.
        """

        namespace = {}
        for funcname in dir(self):
            func = getattr(self, funcname)
            if is_public(func):
                namespace[funcname] = func
        return namespace

    def inject_namespace(self, globals=None):
        """
        Inject all namespace functions into the callee globals
        """

        if globals is None:
            frame = sys._getframe()
            frame = frame.f_back
            globals = frame.f_globals
        globals.update(self.namespace())


class Client(CursorMessagesMixin, GlobalMessagesMixin, ClientBase):
    """
    Default client class.
    """


class TurtleClient(Client):
    """
    A client based on Python's builtin turtle module.
    """

    server_factory = TurtleServer
    connection_factory = InProcessConnection
    manager_factory = InProcessManager

    def __init__(self, **kwargs):
        server = self.server_factory()
        manager = self.manager_factory(server=server)
        super().__init__(manager=manager, **kwargs)
        self.server = server


t = TurtleClient()
t.start()
t.inject_namespace()

print(t.namespace().keys())

for _ in range(12):
    forward(200)
    left(5 * 360 / 12)
t.sleep(2)
