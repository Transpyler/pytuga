import os
import pytuga
from PyQt5 import QtWidgets, QtGui, uic
from . import TurtleWidget


VERSION = pytuga.__version__


class Tugalinhas(QtWidgets.QMainWindow):
    '''
    Main window for Tugalinhas
    '''

    def __init__(self):
        super().__init__()
        self._filename = 'turtle-test.py'
        base = os.path.split(__file__)[0]
        uic.loadUi(os.path.join(base, 'main.ui'), self)
        self._turtlewidget = TurtleWidget(header_text='Tugalinhas %s\nType `turtlehelp()` for a list of commands' % VERSION)
        self._turtlescene = self._turtlewidget.scene
        self._layout = QtWidgets.QVBoxLayout(self.centralwidget)
        self._layout.addWidget(self._turtlewidget)
        self._layout.setContentsMargins(2, 0, 2, 2)
        self.setMinimumSize(800, 600)
        self.updateTitle()
        self.setWindowIcon(_window_icon())

    #
    # File operations
    #
    def openFile(self):
        fname = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file')[0]
        if fname:
            with open(fname) as F:
                data = F.read()
            self._turtlewidget.setText(data)
            self._filename = fname
        self.updateTitle()

    def saveFile(self):
        if self._filename is None:
            self.saveFileAs()
        else:
            with open(self._filename, 'w') as F:
                F.write(self._turtlewidget.text())

    def saveFileAs(self):
        fname = QtWidgets.QFileDialog.getSaveFileName(self, 'Save file')[0]
        if fname:
            with open(fname, 'w') as F:
                F.write(self._turtlewidget.text())
            self._filename = fname
        self.updateTitle()

    def newFile(self):
        self._filename = None
        self._turtlewidget.setText('')
        self.updateTitle()

    #
    # View menu
    #
    def zoomIn(self):
        self._turtlewidget.zoomIn()

    def zoomOut(self):
        self._turtlewidget.zoomOut()

    def clearScene(self):
        self._turtlescene.clear()

    #
    # help menu
    #
    def openDocumentation(self):
        pass

    def about(self):
        QtWidgets.QMessageBox.about(
                self,
                'Pytuguês',
                'Pytuguês é uma linguagem para o ensino de programação em '
                'português. Aqui aprendemos a programar em português e dentro '
                'de um ambiente gráfico e lúdico.')

    #
    # Other commands and utility methods
    #
    def updateTitle(self):
        if self._filename:
            self.setWindowTitle('Tugalinhas (%s)' % self._filename)
        else:
            self.setWindowTitle('Tugalinhas (not saved)')

if not hasattr(Tugalinhas, 'setUnifiedTitleAndToolBarOnMac'):
    def setUnifiedTitleAndToolBarOnMac(*arg, **kwds):
        pass

    Tugalinhas.setUnifiedTitleAndToolBarOnMac = setUnifiedTitleAndToolBarOnMac


#
# Utility function
#
def _window_icon():
    dirpath = os.path.dirname(__file__)
    icon_path = os.path.join(dirpath, 'icon.svg')
    return QtGui.QIcon(icon_path)
