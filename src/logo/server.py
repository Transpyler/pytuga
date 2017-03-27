from logo import mathutils
from logo.errors import InvalidMessageError
from logo.mathutils import Vec


def object_ctrl(getter, setter=None):
    def fget(self):
        return getattr(self.object, getter)()

    if setter is not None:
        def fset(self, value):
            getattr(self.object, setter)(value)

        return property(fget, fset)
    else:
        return property(fget)


class Cursor:
    """
    A cursor (or turtle) represents a drawing element on screen.
    """

    valid_states = {'pos', 'heading', 'drawing', 'color', 'fillcolor', 'width'}

    @property
    def heading_direction(self):
        return Vec(self.cos(self.heading), self.sin(self.heading))

    def __init__(self, server, id, pos=None, heading=0.0, drawing=True,
                 color='black', fillcolor='black', width=1, hidden=False):
        self.server = server
        self.id = id
        self.pos = self.vec(pos or (0, 0))
        self.heading = heading
        self.is_drawing = drawing
        self.color = color
        self.fillcolor = fillcolor
        self.width = width
        self.hidden = hidden

    def rotate(self, angle):
        """
        Rotate cursor heading.
        """

        self.heading += angle

    def step(self, step):
        """
        Advance the given step in the direction of heading.
        """

        self.pos += self.heading_direction * step

    def get_state(self, state):
        """
        Get a state variable.
        """

        if state not in self.valid_states:
            raise ValueError('invalid state name: %r' % state)
        return getattr(self, 'state')

    def set_state(self, state, value):
        """
        Change value of a state variable.
        """

        if state not in self.valid_states:
            raise ValueError('invalid state name: %r' % state)
        return setattr(self, 'state', value)

    # Mathematical functions. We define them here so they can be overridable in
    # subclasses.
    cos = staticmethod(mathutils.cos)
    sin = staticmethod(mathutils.sin)
    tan = staticmethod(mathutils.tan)
    vec = staticmethod(mathutils.Vec)


class TurtleCursor(Cursor):
    """
    A cursor for Python's builtin turtle module.
    """

    heading = object_ctrl('heading', 'setheading')
    color = object_ctrl('pencolor', 'pencolor')
    fillcolor = object_ctrl('fillcolor', 'fillcolor')
    width = object_ctrl('width', 'width')
    pos = object_ctrl('pos')

    @pos.setter
    def pos(self, value):
        x, y = value
        is_drawing = self.is_drawing
        self.is_drawing = False
        self.object.goto(x, y)
        self.is_drawing = is_drawing

    is_drawing = object_ctrl('isdown')

    @is_drawing.setter
    def is_drawing(self, value):
        if value:
            self.object.pendown()
        else:
            self.object.penup()

    def __init__(self, server, id, object, **kwargs):
        self.object = object
        super().__init__(server, id, **kwargs)

    def __getattr__(self, attr):
        return getattr(self.object, attr)

    def rotate(self, angle):
        if angle > 0:
            self.object.left(angle)
        else:
            self.object.right(-angle)

    def step(self, size):
        if size > 0:
            self.object.forward(size)
        elif size < 0:
            self.object.backward(-size)


class Server:
    """
    Server base class.
    """

    cursor_factory = Cursor

    def __init__(self):
        self.cursors = {}
        self._cursor_idx = 0

    def new_cursor(self, **kwargs):
        """
        Create a new cursor and add to the cursors list.
        """

        new = self.cursor_factory(self, self._cursor_idx, **kwargs)
        self._cursor_idx += 1
        return new

    def start(self):
        """
        Start server.
        """

        self.start_cursors()

    def start_cursors(self):
        """
        Initialize list of cursors.
        """

        cursor = self.new_cursor()
        self.cursors[cursor.id] = cursor

    def dispatch_message(self, message):
        """
        Dispatch message to the appropriate method.
        """

        action = message['action']
        idx = message.get('cursor-id', None)
        try:
            method = getattr(self, 'process_' + action.replace('-', '_'))
        except AttributeError:
            raise InvalidMessageError(message)
        else:
            args = message.get('args', ())
            kwargs = message.get('kwargs', {})
            if idx is not None:
                kwargs['idx'] = idx
            return method(*args, **kwargs)

    def process_set_state(self, state, value, idx=0):
        self.cursors[idx].set_state(state, value)

    def process_get_state(self, state, idx=0):
        return self.cursors[idx].get_state(state)

    def process_draw(self, pos, idx=0):
        self.cursors[idx].draw(pos)

    def process_step(self, step, idx=0):
        self.cursors[0].forward(step)

    def process_rotate(self, angle, idx=0):
        self.cursors[0].rotate(angle)


class InProcessServer(Server):
    """
    Base class for servers that share the same process as client.
    """


class TurtleServer(InProcessServer):
    """
    A server based on Python's builtin turtle module.
    """

    def __init__(self):
        super().__init__()

        # Init turtle module
        import turtle
        self._turtle = turtle

    def start(self):
        self._turtle.showturtle()
        super().start()

    def start_cursors(self):
        turtle = self._turtle.turtles()[0]
        self.cursors[0] = TurtleCursor(self, 0, turtle)
