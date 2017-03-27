import sys
# Here, you might want to set the ``QT_API`` to use.
# Valid values are: 'pyqt5', 'pyqt4' or 'pyside'
# See
# import os; os.environ['QT_API'] = 'pyside'
from pyqode.qt import QtWidgets

from pyqode_pytuga.code_edit import PytugaCodeEdit

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    # create editor and window
    window = QtWidgets.QMainWindow()
    editor = PytugaCodeEdit()
    window.setCentralWidget(editor)

    # start the backend as soon as possible
    editor.backend.start('server.py')

    # open a file
    editor.file.open(__file__)

    # run
    window.show()
    app.exec_()
