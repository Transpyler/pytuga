'''
Defines the main turtle object
'''
from .util import QtWidgets, QtGui
from .mathutil import Vec


class Turtle(QtWidgets.QGraphicsEllipseItem):
    def __init__(self, x, y, *, color=(255, 0, 0)):
        super().__init__(x, y, 15, 5)
        self.setBrush(QtGui.QBrush(QtGui.QColor(*color)))
        self.setPen(QtGui.QPen(QtGui.QColor(*color)))
        #self.setTransformOriginPoint(7.5, 2.5)
        self.setPos(x - 7.5, y - 2.5)
        self.tip_pos = Vec(x, y)
        self.tip_heading = 0
        self.tip_down = True
        self.tip_color = (0, 0, 0)
        self.tip_fill = None
        self.tip_width = 2
