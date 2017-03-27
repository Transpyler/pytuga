'''
Defines the main turtle object
'''
import os
from PyQt5 import QtGui, QtSvg
from PyQt5.QtCore import pyqtSignal
from .mathutil import Vec

svg_path = os.path.join(os.path.split(__file__)[0], 'turtleart.svg') 
svg_renderer = QtSvg.QSvgRenderer(svg_path)


class Turtle(QtSvg.QGraphicsSvgItem):
    def __init__(self, parent=None, 
                 svg_id='tuga', 
                 pos=(0, 0), heading=0, isdown=True, 
                 color=(0, 0, 0), fill=None, width=2, size=45):
        super().__init__(parent)
        
        # Loads from turtleart.svg
        self.setSharedRenderer(svg_renderer)
        self.setElementId(svg_id)
        
        # Define local transforms
        rect = self.sceneBoundingRect()
        curr_width, curr_height = rect.width(), rect.height()
        self.setTransform(QtGui.QTransform(1.00, 0.00,
                                           0.00, 1.00,
                                           -curr_width/2, -curr_height/2))
        self.setTransformOriginPoint(0.5 * curr_width, 0.5 * curr_height)
        self.setScale(size / curr_width)
        
        # Put in the desired position and bellow others
        self.setPos(*pos)
        self.setZValue(1.0)
        self.setRotation(heading)
        self.tip_pos = Vec(*pos)
        self.tip_heading = 0
        self.tip_isdown = isdown
        self.tip_color = color
        self.tip_fill = fill
        self.tip_width = width
        self.svg_id = svg_id
        self.oldpos = [None, None]

    def copy(self):
        return type(self)(
            pos=self.tip_pos, heading=self.tip_heading, isdown=self.tip_isdown,
            color=self.tip_color, fill=self.tip_fill, width=self.tip_width,
            svg_id=self.svg_id)
