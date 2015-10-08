import os
import sys
from tugalinhas2 import QtWidgets, TurtleWidget, uic


class Tugalinhas(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self._filename = None
        base = os.path.split(__file__)[0]
        uic.loadUi(os.path.join(base, 'main.ui'), self)
        self.turtlearea = TurtleWidget()
        self._layout = QtWidgets.QVBoxLayout(self.centralwidget)
        self._layout.addWidget(self.turtlearea)
        self.setMinimumSize(800, 600)
        
    #
    # File operations    
    #
    def openFile(self):
        fname = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file')[0]
        with open(fname) as F:
            data = F.read()
        self.turtlearea.setText(data)
        
    def saveFile(self):
        if self._filename is None:
            self.saveFileAs()
        else:
            with open(self._filename, 'w') as F:
                F.write(self.turtlearea.text())
        
    def saveFileAs(self):
        fname = QtWidgets.QFileDialog.getSaveFileName(self, 'Save file')[0]
        with open(fname, 'w') as F:
            F.write(self.turtlearea.text())
        self._filename = fname
        
    def newFile(self):
        self._filename = None
        self.turtlearea.setText('')

def main():
    '''Main function entry point for turtle'''
    
    app = QtWidgets.QApplication(sys.argv)
    window = Tugalinhas()
    window.show()
    sys.exit(app.exec_())
    
if __name__ == '__main__':
    main()