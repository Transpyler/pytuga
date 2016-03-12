from PyQt5 import QtWidgets, QtCore
from .qsciconsole import PythonConsole
from .qscieditor import PythonEditor


class ReplEditor(QtWidgets.QWidget):
    def __init__(self, parent=None, *,
                 header_text=None,
                 hide_console_margins=False,
                 namespace=None, **kwds):
        super().__init__(parent)
        self._editor = PythonEditor(**kwds)
        self._editor.runCode = self.runCode
        self._console = PythonConsole(namespace=namespace,
                                      header_text=header_text,
                                      hide_margins=hide_console_margins, **kwds)
        
        # Create buttons and connect buttons
        run_button = QtWidgets.QPushButton('Run')
        hideup_button = QtWidgets.QPushButton('\u25b2')
        hidedown_button = QtWidgets.QPushButton('\u25bc')
        run_button.setMaximumWidth(100)
        hideup_button.setFixedWidth(35)
        hidedown_button.setFixedWidth(35)
        buttons = QtWidgets.QWidget()
        button_area = QtWidgets.QHBoxLayout(buttons)
        button_area.addWidget(hideup_button, 20)
        button_area.addWidget(hidedown_button, 20)
        button_area.addStretch(300)
        button_area.addWidget(run_button, 200)
        button_area.setContentsMargins(0, 0, 0, 0)
        buttons.setFixedHeight(25)
        run_button.clicked.connect(self.runCode)
        hideup_button.clicked.connect(self.hideUp)
        hidedown_button.clicked.connect(self.hideDown)

        # Create top area with the Editor and the button area element
        top_widget = QtWidgets.QWidget()
        top_layout = QtWidgets.QVBoxLayout(top_widget)
        top_layout.setContentsMargins(0, 0, 0, 0)
        top_layout.addWidget(self._editor)
        top_layout.addWidget(buttons)
        self._top_widget = top_widget
        
        # Add elements
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        splitter = QtWidgets.QSplitter(QtCore.Qt.Orientation(0))
        splitter.addWidget(top_widget)
        splitter.addWidget(self._console)
        splitter.setSizes([200, 120])
        splitter.setChildrenCollapsible(False)
        layout.addWidget(splitter)
        self._splitter = splitter
        self._splitter_sizes = splitter.sizes()
        
        # Size hints
        self.setMinimumSize(QtCore.QSize(100, 200))

    def console(self):
        return self._console

    def editor(self):
        return self._editor

    def sizeHint(self):
        return QtCore.QSize(100, 200)
        
    def runCode(self):
        text = self._editor.text()
        if text:
            result = self._console.executeCommand(text)
            if result and self._console.isHidden():
                self.toggleConsoleVisibility()
    
    def toggleConsoleVisibility(self):
        if self._console.isHidden():
            self._console.setHidden(False)
            self._splitter.setSizes(self._splitter_sizes)
        else:
            self._splitter_sizes = self._splitter.sizes()
            self._splitter.setSizes([2**16, 1])
            self._console.setHidden(True)
        
    def toggleEditorVisibility(self):
        if self._editor.isHidden():
            self._editor.setHidden(False)
            self._splitter.setSizes(self._splitter_sizes)
        else:
            self._splitter_sizes = self._splitter.sizes()
            self._splitter.setSizes([1, 2**16])
            self._editor.setHidden(True)
        
    def hideUp(self):
        if self._console.isHidden():
            self.toggleConsoleVisibility()
        elif not self._editor.isHidden():
            self.toggleEditorVisibility()
    
    def hideDown(self):
        if self._editor.isHidden():
            self.toggleEditorVisibility()
        elif not self._console.isHidden():
            self.toggleConsoleVisibility()
            
    def setText(self, text):
        self._editor.setText(text)
        
    def text(self):
        return self._editor.text()

    def toggleTheme(self):
        self._console.toggleTheme()
        self._editor.toggleTheme()

    def zoomIn(self):
        self._console.zoomIn()
        self._editor.zoomIn()

    def zoomOut(self):
        self._console.zoomOut()
        self._editor.zoomOut()

    def zoomTo(self, factor):
        self._console.zoomTo(factor)
        self._editor.zoomTo(factor)

    def __getattr__(self, attr):
        if 'Console' in attr:
            head, _, tail = attr.partition('Console')
            return getattr(self._console, head + tail)
        else:
            try:
                return getattr(self._editor, attr)
            except AttributeError:
                try:
                    return getattr(self._console, attr)
                except AttributeError:
                    tname = type(self).__name__
                    msg = '%s object has no attribute %s' % (tname, attr)
                    raise AttributeError(msg)