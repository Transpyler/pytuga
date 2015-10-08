from .util import QtWidgets
from . import ReplEditor, TurtleScene, TurtleView

class TurtleWidget(QtWidgets.QWidget):
    def __init__(self, parent=None, text='', **kwds):
        super().__init__(parent)
        
        # Configure scene
        self.scene = TurtleScene()
        self.view = TurtleView(self.scene)
        self.namespace = dict(self.scene.getNamespace())
        
        # Configure editor
        self.editor = ReplEditor(namespace=self.namespace)
        self.editor.setText(text)
        self.editor.setNamespace(self.namespace)
        
        # Configure layout
        self._layout = QtWidgets.QHBoxLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.addWidget(self.view, 2)
        self._layout.addWidget(self.editor, 1)
                
    def setText(self, text):
        self.editor.setText(text)
        
    def text(self):
        return self.editor.text()