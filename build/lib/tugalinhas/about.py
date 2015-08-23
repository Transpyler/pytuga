import os

from PyQt4 import QtGui, QtCore, uic

from tugalinhas import UI_FILES_PATH
from tugalinhas import util
from tugalinhas import FULL_NAME


class AboutDialog(QtGui.QDialog):

    '''Loads the about dialog UI file'''

    def __init__(self, app):
        QtGui.QDialog.__init__(self)
        uipath = os.path.join(UI_FILES_PATH, 'about.ui')
        self.ui = uic.loadUi(uipath, self)

        svgrenderer = util.SvgRenderer(app)
        renderer = svgrenderer.getrend()
        img = QtGui.QPixmap(300, 150)
        img.fill(QtCore.Qt.transparent)
        self.img = img
        painter = QtGui.QPainter(img)
        renderer.render(painter, 'splash')
        painter.end()

        self.ui.splasharea.setPixmap(self.img)
        self.ui.progtitle.setText(FULL_NAME)
