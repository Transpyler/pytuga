from PyQt5 import QtWidgets

from lazyutils import delegate_to

from . import TurtleScene, TurtleView
from .repl_editor import ReplEditor


class TurtleWidget(QtWidgets.QWidget):
    text = delegate_to('_editor')
    setText = delegate_to('_editor')
    zoomIn = delegate_to('_view')
    zoomOut = delegate_to('_view')
    increaseFont = delegate_to('_editor')
    decreaseFont = delegate_to('_editor')
    toggleTheme = delegate_to('_editor')
    saveImage = delegate_to('_view')
    flushExecution = delegate_to('_scene')

    def __init__(self, 
                 parent=None, 
                 text='', header_text=None,
                 **kwds):
        super().__init__(parent)
        
        # Configure scene
        self._scene = TurtleScene()
        self._view = TurtleView(self._scene)
        self._namespace = dict(self._scene.getNamespace())

        # Configure editor
        self._editor = ReplEditor(namespace=self._namespace,
                                  header_text=header_text)
        self._editor.setText(text)
        self._editor.setNamespace(self._namespace)
        self._editor.sizePolicy().setHorizontalPolicy(7)
        
        # Configure layout
        self._splitter = QtWidgets.QSplitter()
        self._splitter.addWidget(self._view)
        self._splitter.addWidget(self._editor)
        self._layout = QtWidgets.QHBoxLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.addWidget(self._splitter)
        self._splitter.setSizes([200, 120])

    def scene(self):
        return self._scene

    def view(self):
        return self._view

    def namespace(self):
        return self._namespace

    def editor(self):
        return self._editor

    def fontZoomIn(self):
        self._editor.zoomIn()

    def fontZoomOut(self):
        self._editor.zoomOut()

    def fontZoomTo(self, factor):
        self._editor.zoomTo(factor)

