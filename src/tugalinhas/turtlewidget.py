from PyQt5 import QtWidgets
from . import ReplEditor, TurtleScene, TurtleView


class TurtleWidget(QtWidgets.QWidget):
    def __init__(self, 
                 parent=None, 
                 text='', header_text=None,
                 **kwds):
        super().__init__(parent)
        
        # Configure scene
        self._scene = TurtleScene()
        self._view = TurtleView(self._scene)
        self._namespace = dict(self._scene.getNamespace())
        autocompletion_words = self._namespace.keys()
        
        # Configure editor
        self._editor = ReplEditor(namespace=self._namespace,
                                  header_text=header_text,
                                  autocompletion_words=autocompletion_words)
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
                        
    def setText(self, text):
        self._editor.setText(text)
        
    def text(self):
        return self._editor.text()
    
    def zoomIn(self):
        self._view.zoomIn()
    
    def zoomOut(self):
        self._view.zoomOut()

    def fontZoomIn(self):
        self._editor.zoomIn()

    def fontZoomOut(self):
        self._editor.zoomOut()

    def fontZoomTo(self, factor):
        self._editor.zoomTo(factor)

    def increaseFont(self):
        self._editor.increaseFont()

    def decreaseFont(self):
        self._editor.decreaseFont()

    def toggleTheme(self):
        self._editor.toggleTheme()

    def saveImage(self, fname):
        self._view.saveImage(fname)

    def flushExecution(self):
        self._scene.flushExecution()
