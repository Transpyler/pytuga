from PyQt4 import QtGui, QtCore
from tugalinhas.util import SvgRenderer


class Splash(QtGui.QSplashScreen):

    '''Render tugalinhas splash screen'''

    def __init__(self, app):
        # Render image
        renderer = SvgRenderer(app).getrend()
        img = QtGui.QPixmap(500, 250)
        img.fill(QtCore.Qt.transparent)
        painter = QtGui.QPainter(img)
        renderer.render(painter, 'splash')
        painter.end()

        # Init splash scre10en
        super(Splash, self).__init__(img, QtCore.Qt.WindowStaysOnTopHint)
        self.setMask(img.mask())
        self.away_later()

    def away_later(self):
        QtCore.QTimer.singleShot(200, self.away)

    def away(self):
        if hasattr(self, 'window'):
            self.finish(self.window)
        else:
            self.away_later()
