'''A random collection of utility functions'''

import os
import math
from random import randrange
from math import copysign
from PyQt4 import QtSvg, QtGui, QtCore
from tugalinhas import SHARED_ART_PATH, NODEFAULT


#
# Custom errors
#
class TooManyPens(RuntimeError):
    pass


#
# Custom functions
#
def as_qpoint(pt):
    '''enforce that pt is an instance of QPointF'''

    if isinstance(pt, QtCore.QPointF):
        return pt
    else:
        return QtCore.QPointF(*pt)


def sign(x):
    'return 1 if x is positive, -1 if negative, or zero'

    return copysign(1, x)


def plist(f):
    '''given function object,
        return a list of [(arg name: default value or None), ...]
    '''
    parameter_defaults = []
    defaults = f.__defaults__
    if defaults is not None:
        defaultcount = len(defaults)
    else:
        defaultcount = 0
    argcount = f.__code__.co_argcount
    for i in range(f.__code__.co_argcount):
        name = f.__code__.co_varnames[i]
        value = NODEFAULT
        if i >= argcount - defaultcount:
            value = defaults[i - (argcount - defaultcount)]
        parameter_defaults.append((name, value))
    return parameter_defaults


class SvgRenderer(object):

    'factory for svg renderer objects'

    def __init__(self, app):
        self.app = app

    def getrend(self, filepath=None):
        '''Return a handle to the shared SVG renderer for the given svg file.

        If no filepath is given, return the renderer for the default svg file.
        '''
        if filepath is None:
            filepath = os.path.join(SHARED_ART_PATH)
        return QtSvg.QSvgRenderer(filepath, self.app)


def choose_color(r=None, g=None, b=None, a=None):
    '''Normalize input to a tuple of (r, g, b, a)'''

    if a is None:
        a = 255
    elif not (0 <= a <= 255):
        raise ValueError('Alpha value must be between 0 and 255')

    # Random colors
    if r == 'random':
        r, g, b = [randrange(256) for _ in range(3)]
    elif r == 'rlight':
        r, g, b = [randrange(200, 256) for _ in range(3)]
    elif r == 'rmedium':
        r, g, b = [randrange(100, 200) for _ in range(3)]
    elif r == 'rdark':
        r, g, b = [randrange(100) for _ in range(3)]
    elif r == 'ralpha':
        r, g, b = [randrange(256) for _ in range(3)]
        a = randrange(100, 200)

    # Null colors (shouldn't raise an error?)
    elif r is g is b is None:
        return None, None, None, None

    # From RGB components
    elif g is not None and b is not None:
        if not (0 <= r <= 255 and 0 <= g <= 255 and 0 <= b <= 255):
            raise ValueError('Color components must be between 0 and 255')
        c = QtGui.QColor.fromRgb(r, g, b, a)
        r, g, b, a = c.red(), c.green(), c.blue(), c.alpha()

    # From a tuple or sequence
    elif r is not None:
        try:
            if len(r) == 4:
                rr, gg, bb, aa = r
                rr, gg, bb, aa = int(rr), int(gg), int(bb), int(aa)
            elif len(r) == 3:
                rr, gg, bb = r
                rr, gg, bb = int(rr), int(gg), int(bb)
                aa = 255
            else:
                raise ValueError
        except ValueError:
            try:
                ci = int(r)
                c = QtGui.QColor.fromRgba(ci)
            except ValueError:
                if not QtGui.QColor.isValidColor(r):
                    raise ValueError
                c = QtGui.QColor(r)
            r, g, b, a = c.red(), c.green(), c.blue(), c.alpha()
        else:
            r, g, b, a = rr, gg, bb, aa

    # Bad input...
    elif r is None or g is None or b is None:
        raise TypeError

    return r, g, b, a


def nudge_color(color, r=None, g=None, b=None, a=None):
    """Change the color (a 3-element tuple) by given amounts,
        return the new RGB tuple.

    Clamps the RGB return values such that 0 <= RGB <= 255
        but does not necessarily return only integer values.

        Not returning strictly integers allows for smoother color
        variations, but note that when the values are passed
        to the tugalinhas color() function the values will be
        converted to integers. So in order to take advantage
        of the more precise values you will need to keep those
        separately from the actual tugalinhas color values.

    The function's r, g, b parameters can be either:

    numbers to be added to or subtracted from the RGB tuple
        components, or

    percentages (as strings) that will be multiplied by the component
        to increase or decrease that component by given the given
        percent.

    >>> color = (100, 100, 100)
    >>> nudge_color(color, g=15)
    (100, 115, 100)

    >>> color = (100, 100, 100)
    >>> nudge_color(color, r=-12.5)
    (87.5, 100, 100)

    >>> color = (100, 100, 100)
    >>> color = nudge_color(color, b='75%')
    >>> color
    (100, 100, 75.0)
    >>> nudge_color(color, b='75%')
    (100, 100, 57.25)

    >>> color = (100, 100, 100)
    >>> nudge_color(color, r=50, g='105%', b=-10)
    (150, 105, 90)
    """

    if len(color) == 3:
        rc, gc, bc = color
        ac = 255
    elif len(color) == 4:
        rc, gc, bc, ac = color
    else:
        raise ValueError

    if r is not None:
        try:
            rc += r
        except TypeError:
            rc *= (float(r[:-1]) / 100.0)

    if g is not None:
        try:
            gc += g
        except TypeError:
            gc *= (float(g[:-1]) / 100.0)

    if b is not None:
        try:
            bc += b
        except TypeError:
            bc *= (float(b[:-1]) / 100.0)

    if a is not None:
        try:
            ac += a
        except TypeError:
            ac *= (float(a[:-1]) / 100.0)

    rc = min(rc, 255)
    gc = min(gc, 255)
    bc = min(bc, 255)
    ac = min(ac, 255)
    rc = max(rc, 0)
    gc = max(gc, 0)
    bc = max(bc, 0)
    ac = max(ac, 0)

    return (rc, gc, bc, ac)


def docfrom(function, decorated=None):
    '''Creates a decorator that saves documentation from the given
    function.

    >>> @docfrom(sum)
    ... def my_sum(args):
    ...     return sum(args, 0.0)
    '''

    if decorated is not None:
        decorated.__doc__ = function.__doc__
        return decorated
    else:
        def decorator(func):
            return docfrom(function, func)
        return decorator

#
# From Python's turtle module
#


class Vec2D(tuple):

    """Simple 2D vector arithmetic

    Provides (for a, b vectors, k number):
       a + b vector addition
       a - b vector subtraction
       a * b inner product
       k * a and a * k multiplication with scalar
       abs(a) absolute value of a
       a.rotate(angle) rotation
    """
    def __new__(cls, x, y):
        return tuple.__new__(cls, (x, y))

    def __add__(self, other):
        return Vec2D(self[0] + other[0], self[1] + other[1])

    def __mul__(self, other):
        if isinstance(other, Vec2D):
            return self[0] * other[0] + self[1] * other[1]
        return Vec2D(self[0] * other, self[1] * other)

    def __rmul__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            return Vec2D(self[0] * other, self[1] * other)

    def __sub__(self, other):
        return Vec2D(self[0] - other[0], self[1] - other[1])

    def __neg__(self):
        return Vec2D(-self[0], -self[1])

    def __abs__(self):
        return (self[0] ** 2 + self[1] ** 2) ** 0.5

    def rotate(self, angle):
        """rotate self counterclockwise by angle
        """
        perp = Vec2D(-self[1], self[0])
        angle = angle * math.pi / 180.0
        c, s = math.cos(angle), math.sin(angle)
        return Vec2D(self[0] * c + perp[0] * s, self[1] * c + perp[1] * s)

    def __getnewargs__(self):
        return (self[0], self[1])

    def __repr__(self):
        return "(%.2f,%.2f)" % self
