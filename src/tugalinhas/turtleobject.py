'''
Defines the main turtle object
'''
import os
from .util import QtWidgets, QtGui, QtSvg
from .mathutil import Vec

svg_path = os.path.join(os.path.split(__file__)[0], 'turtleart.svg') 
svg_renderer = QtSvg.QSvgRenderer(svg_path)


class Turtle(QtSvg.QGraphicsSvgItem):
    def __init__(self, x, y, parent=None, svg_id='tuga'):
        super().__init__(parent)
        
        # Loads from turtleart.svg
        self.setSharedRenderer(svg_renderer)
        self.setElementId(svg_id)
        
        # Define local transforms
        rect = self.sceneBoundingRect()
        width, height = rect.width(), rect.height()
        self.setTransform(QtGui.QTransform(1.00, 0.00,
                                           0.00, 1.00,
                                           -width/2, -height/2))
        self.setTransformOriginPoint(0.5 * width, 0.5 * height)
        
        # Put in the desired position and bellow others
        self.setPos(x, y)
        self.setZValue(1.0)
        
        self.tip_pos = Vec(x, y)
        self.tip_heading = 0
        self.tip_down = True
        self.tip_color = (0, 0, 0)
        self.tip_fill = None
        self.tip_width = 2
