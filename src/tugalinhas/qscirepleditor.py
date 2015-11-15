from PyQt5 import QtWidgets, QtCore
from .qsciconsole import PythonConsole
from .qscieditor import PythonEditor


class ReplEditor(QtWidgets.QWidget):
    def __init__(self, parent=None, *,
                 header_text=None,
                 hide_console_margins=False,
                 namespace=None, **kwds):
        super().__init__(parent)
        self.editor = PythonEditor(**kwds)
        self.editor.runCode = self.runCode
        self.console = PythonConsole(namespace=namespace,
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
        top_layout.addWidget(self.editor)
        top_layout.addWidget(buttons)
        self._top_widget = top_widget
        
        # Add elements
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        splitter = QtWidgets.QSplitter(QtCore.Qt.Orientation(0))
        splitter.addWidget(top_widget)
        splitter.addWidget(self.console)
        splitter.setSizes([200, 120])
        splitter.setChildrenCollapsible(False)
        layout.addWidget(splitter)
        self._splitter = splitter
        self._splitter_sizes = splitter.sizes()
        
        # Size hints
        self.setMinimumSize(QtCore.QSize(100, 200))
        
    def sizeHint(self):
        return QtCore.QSize(100, 200)
        
    def runCode(self):
        text = self.editor.text()
        if text:
            result = self.console.executeCommand(text)
            if result and self.console.isHidden():
                self.toggleConsoleVisibility()
    
    def toggleConsoleVisibility(self):
        if self.console.isHidden():
            self.console.setHidden(False)
            self._splitter.setSizes(self._splitter_sizes)
        else:
            self._splitter_sizes = self._splitter.sizes()
            self._splitter.setSizes([2**16, 1])
            self.console.setHidden(True)
        
    def toggleEditorVisibility(self):
        if self.editor.isHidden():
            self.editor.setHidden(False)
            self._splitter.setSizes(self._splitter_sizes)
        else:
            self._splitter_sizes = self._splitter.sizes()
            self._splitter.setSizes([1, 2**16])
            self.editor.setHidden(True)
        
    def hideUp(self):
        if self.console.isHidden():
            self.toggleConsoleVisibility()
        elif not self.editor.isHidden():
            self.toggleEditorVisibility()
    
    def hideDown(self):
        if self.editor.isHidden():
            self.toggleEditorVisibility()
        elif not self.console.isHidden():
            self.toggleConsoleVisibility()
            
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