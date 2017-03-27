"""
Useful mathemtatical functions and objects.
"""

import math as _math
from collections import namedtuple as _namedtuple 

_dg = _math.pi / 180


def cos(angle):
    """Cosine of an angle (in degrees)"""
    return _math.cos(angle * _dg)


def sin(angle):
    """Sine of an angle (in degrees)"""
    return _math.sin(angle * _dg)


class Vec(_namedtuple('Vec', ['x', 'y'])):
    """A tuple-based 2D vector.

    Supports all basic arithmetic operations."""
    
    @classmethod
    def from_angle(cls, angle):
        return cls(cos(angle), sin(angle))
    
    def __new__(cls, x, y=None):
        if y is None:
            x, y = x
        return super(Vec, cls).__new__(cls, x + 0.0, y + 0.0)
    
    def __repr__(self):
        return '%s(%.1f, %.1f)' % (type(self).__name__, self.x, self.y)

    def __add__(self, other):
        x, y = other
        return Vec(x + self.x, y + self.y)
    
    def __sub__(self, other):
        x, y = other
        return Vec(self.x - x, self.y - y)

    def __mul__(self, other):
        return Vec(other * self.x, other * self.y)
    
    def __truediv__(self, other):
        return Vec(self.x / other, self.y / other)
    
    def __radd__(self, other):
        return self + other
    
    def __rsub__(self, other):
        return self * (-1) + other
    
    def __rmul__(self, other):
        return self * other

    def __neg__(self):
        return Vec(-self.x, -self.y)
    
    def __abs__(self):
        return _math.sqrt(self.x**2 + self.y**2)
