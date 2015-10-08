from .util import QtWidgets, QtCore
from .qsciconsole import PythonConsole
from .qscieditor import PythonEditor

class ReplEditor(QtWidgets.QWidget):
    def __init__(self, parent=None, namespace=None, **kwds):
        super().__init__(parent)
        self.editor = PythonEditor(**kwds)
        self.editor.runCode = self.runCode
        self.console = PythonConsole(namespace=namespace, **kwds)
        
        # Create buttons and connect buttons
        button_area = QtWidgets.QHBoxLayout()
        run_button = QtWidgets.QPushButton('Run')
        hide_button = QtWidgets.QPushButton('Hide')
        button_area.addWidget(hide_button)
        button_area.addStretch(2)
        button_area.addWidget(run_button, 1.5)
        run_button.clicked.connect(self.runCode)
        hide_button.clicked.connect(self.toggleConsoleVisibility)
        self._hidebutton = hide_button
        self._consolehidden = False

        # Add elements
        self._layout = QtWidgets.QVBoxLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._splitter = QtWidgets.QSplitter(QtCore.Qt.Orientation(0))
        self._top = QtWidgets.QWidget(self._splitter)
        self._top_layout = QtWidgets.QVBoxLayout(self._top)
        self._top_layout.setContentsMargins(0, 0, 0, 0) 
        self._top_layout.addWidget(self.editor)
        self._top_layout.addLayout(button_area)
        self._splitter.addWidget(self.console)        
        self._splitter.setSizes([2, 1])
        self._layout.addWidget(self._splitter)
        
    def runCode(self):
        text = self.editor.text()
        if text:
            result = self.console.runCommand(text)
            if result and self.console.isHidden():
                self.toggleConsoleVisibility()
    
    def toggleConsoleVisibility(self):
        if self._consolehidden:
            self._splitter.setSizes([200, 100])
        else:
            self._splitter.setSizes([100, 0])
            
        self._consolehidden = not self._consolehidden
        text = 'Show' if self._consolehidden else 'Hide'
        self._hidebutton.setText(text)
        
    def setText(self, text):
        self.editor.setText(text)
        
    def text(self):
        return self.editor.text()
        
    def __getattr__(self, attr):
        if 'Console' in attr:
            head, _, tail = attr.partition('Console')
            return getattr(self.console, head + tail)
        else:
            try:
                return getattr(self.editor, attr)
            except AttributeError:
                try:
                    return getattr(self.console, attr)
                except AttributeError:
                    tname = type(self).__name__
                    msg = '%s object has no attribute %s' % (tname, attr)
                    raise AttributeError(msg)