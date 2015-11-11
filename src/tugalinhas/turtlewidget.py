from PyQt5 import QtWidgets
from . import ReplEditor, TurtleScene, TurtleView

class TurtleWidget(QtWidgets.QWidget):
    def __init__(self, 
                 parent=None, 
                 text='', header_text=None,
                 **kwds):
        super().__init__(parent)
        
        # Configure scene
        self.scene = TurtleScene()
        self.view = TurtleView(self.scene)
        self.namespace = dict(self.scene.getNamespace())
        autocompletion_words = self.namespace.keys()
        
        # Configure editor
        self.editor = ReplEditor(namespace=self.namespace, 
                                 header_text=header_text,
                                 autocompletion_words=autocompletion_words)
        self.editor.setText(text)
        self.editor.setNamespace(self.namespace)
        self.editor.sizePolicy().setHorizontalPolicy(7)
        
        # Configure layout
        self._splitter = QtWidgets.QSplitter()
        self._splitter.addWidget(self.view)
        self._splitter.addWidget(self.editor)
        self._layout = QtWidgets.QHBoxLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.addWidget(self._splitter)
        self._splitter.setSizes([200, 120])
                        
    def setText(self, text):
        self.editor.setText(text)
        
    def text(self):
        return self.editor.text()
    
    def zoomIn(self):
        self.view.zoomIn()
    
    def zoomOut(self):
        self.view.zoomOut()
