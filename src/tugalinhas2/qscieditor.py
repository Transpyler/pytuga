'''
The main editor with python syntax highlighting
'''

import keyword
from .util import Qsci, QtGui, QColor, QFont, QtCore

Return = QtCore.Qt.Key_Return
Enter = QtCore.Qt.Key_Enter
Backspace = QtCore.Qt.Key_Backspace
Equal = QtCore.Qt.Key_Equal
Tab = QtCore.Qt.Key_Tab
Control = QtCore.Qt.ControlModifier
Shift = QtCore.Qt.ShiftModifier
Slash = QtCore.Qt.Key_Slash
Question = QtCore.Qt.Key_Question
Minus = QtCore.Qt.Key_Minus
Plus = QtCore.Qt.Key_Plus
Key_V = QtCore.Qt.Key_V
Key_Z = QtCore.Qt.Key_Z

# Python keywords and common functions for autocompletion
PYTHON_WORDS = tuple(list(__builtins__) + keyword.kwlist)

#
# Thanks to Eli Bendersky:
# http://eli.thegreenplace.net/2011/04/01/sample-using-qscintilla-with-pyqt
#
class PythonEditor(Qsci.QsciScintilla):
    '''
    A Scintilla based text editor with Python syntax highlight.
    '''

    DEFAULT_COLORS = dict(
        margins_background='#cccccc',
        caret_line_background='#ffffee',
    )
    
    def __init__(self, 
            parent=None, *, 
            
            # font configuration
            fontsize=12, fontfamily='monospace', 
            
            # default list of words to autocomplete
            autocomplete_words=(), autocomplete_python=True,
             
            # set colors and other stuff
            **kwds
            ): 
        super().__init__(parent)
        
        # Fonts
        self.setAllFonts(fontfamily, fontsize)
        self.setMarginSensitivity(1, False)
        self.setCaretLineVisible(True)

        # Configure lexer and api for autocompletion
        lexer = Qsci.QsciLexerPython(self)
        lexer.setDefaultFont(self.font())
        words = list(autocomplete_words) 
        if autocomplete_python:
            words.extend(PYTHON_WORDS)
        if words:
            api = Qsci.QsciAPIs(lexer)
            for word in words:
                api.add(word)
            api.prepare()
        self.setLexer(lexer)
        
        # Set font for lexer again?
        bfamily = bytes(fontfamily, encoding='utf8')
        self.SendScintilla(Qsci.QsciScintilla.SCI_STYLESETFONT, 1, bfamily)
        
        # General indentation behavior
        self.setAutoIndent(True)
        self.setTabWidth(4)
        self.setIndentationsUseTabs(False)
        self.setTabIndents(True)
        self.setBackspaceUnindents(True)
        self.setIndentationGuides(True)
        
        # Configure autocompletion and brace matching
        self.setBraceMatching(Qsci.QsciScintilla.SloppyBraceMatch)
        self.setAutoCompletionThreshold(2)
        self.setAutoCompletionSource(Qsci.QsciScintilla.AcsAPIs)
        
        # Set colors
        colors = dict(self.DEFAULT_COLORS)
        for k, v in kwds.items():
            if k.endswith('_color'):
                colors[k[:-6]] = v
        self.setColors(**colors)
        
        # Check for any rogue parameter
        if kwds:
            raise TypeError('invalid parameter: %r' % kwds.popitem()[0])
        
    def setAllFonts(self, family='monospace', size=10, fixedpitch=True):
        '''Set the font of all visible elements in the text editor.
        
        This syncronizes the font in the main text area with the margins and 
        calltips.
        '''
        self.fontfamily = family
        self.fontsize = size
        self.fontfixedpitch = True
        
        # Configure editor font size
        font = QFont()
        font.setFamily(family)
        font.setFixedPitch(fixedpitch)
        font.setPointSize(size)
        self.setFont(font)
        self.setMarginsFont(font)

        # Margin 0 is used for line numbers
        fontmetrics = QtGui.QFontMetrics(font)
        self.setMarginsFont(font)
        self.setMarginWidth(0, fontmetrics.width('___') + 0)
        self.setMarginLineNumbers(0, True)
        
        # Change lexer font
        bfamily = bytes(family, encoding='utf8')
        if self.lexer() is not None:
            self.lexer().setFont(font)
            self.SendScintilla(Qsci.QsciScintilla.SCI_STYLESETFONT, 1, bfamily)
            
    def setColors(self, **kwds):
        '''Set colors for all given properties.
        
        Properties are of the form `margins_background` to set the 
        `marginsBackgroundColor` property.
        '''
        tasks = []
        
        for key, value in list(kwds.items()):
            key = ''.join([x.title() for x in key.split('_')])
            attr = 'set%sColor' % key
            method = getattr(self, attr)
            tasks.append((method, QColor(value)))
            
        for method, arg in tasks:
            method(arg)              
    
    def runCode(self):
        '''Runs the source code in the editor when user press Control + Return
        '''
        
    def keyPressEvent(self, ev):
        key = ev.key()
        modifiers = ev.modifiers()
        
        # Auto indentation
        if modifiers & Control and key in (Return, Enter):
            self.runCode()
            
        # Change zoom factor
        elif modifiers & Control and key == Minus:
            self.zoomOut()
        elif modifiers & Control and key == Plus:
            self.zoomIn()
        elif modifiers & Control and key == Equal:
            self.zoomTo(1)
            
        # Passthru to Scintilla
        else:
            super().keyPressEvent(ev)
