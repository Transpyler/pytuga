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
        margins_background='#e3e3dd',
        caret_line_background='#f0f0d0',
        background='#eeeedd',
        
        # Lexer colors
        lexer_default='#000000',
        lexer_comment='#000080',
        lexer_number='#008000',
        lexer_double_quoted_string='#a00000',
        lexer_single_quoted_string='#a00000',
        lexer_keyword='#000080',
        lexer_triple_single_quoted_string='#a00000',
        lexer_triple_double_quoted_string='#a00000',
        lexer_class_name='#000000',
        lexer_function_method_name='#000000',
        lexer_operator='#000000',
        lexer_identifier='#000000',
        lexer_comment_block='#000080',
        lexer_unclosed_string='#a00000',
        lexer_highlighted_identifier='#000000',
        lexer_decorator='#808000',
    )
    
    BOLD_STYLES = {5, 9, 10, 14}
    
    LEXER_STYLES = dict(
        Default=0, Comment=1, Number=2, 
        DoubleQuotedString=3, SingleQuotedString=4,
        Keyword=5, TripleSingleQuotedString=6, TripleDoubleQuotedString=7, 
        ClassName=8, FunctionMethodName=9, 
        Operator=10, Identifier=11, CommentBlock=12, UnclosedString=13, 
        HighlightedIdentifier=14, Decorator=15)
    
    def __init__(self, 
            parent=None, *, 
            fontsize=11, fontfamily='monospace', 
            autocompletion_words=(), autocomplete_python=True,
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
        words = list(autocompletion_words) 
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

    def sizeHint(self):
        return QtCore.QSize(100, 200)
        
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

        # Margin 0 is used for line numbers
        fontmetrics = QtGui.QFontMetrics(font)
        self.setMarginsFont(font)
        self.setMarginWidth(0, fontmetrics.width('___') + 0)
        self.setMarginWidth(1, 0)
        self.setMarginLineNumbers(0, True)
        
        # Change lexer font
        bfamily = bytes(family, encoding='utf8')
        lexer = self.lexer()
        if lexer is not None:
            font_bold = QFont(font)
            font_bold.setBold(True)
            for style in self.LEXER_STYLES.values():
                if style in self.BOLD_STYLES:
                    lexer.setFont(style, font_bold)
                else:
                    lexer.setFont(style, font)
            self.SendScintilla(Qsci.QsciScintilla.SCI_STYLESETFONT, 1, bfamily)
            
    def setColors(self, **kwds):
        '''Set colors for all given properties.
        
        Properties are of the form `margins_background` to set the 
        `marginsBackgroundColor` property.
        '''
        tasks = []
        
        # Handle special colors
        text_color = kwds.pop('text', self.color())
        self.setColor(QColor(text_color))
        
        # Background
        background_color = kwds.pop('background', self.paper())
        self.setPaper(QColor(background_color))
        self.lexer().setPaper(QColor(background_color))
        self.lexer().setDefaultPaper(QColor(background_color))
        
        # Grab lexer colors
        lexer_colors = {}
        for key, value in list(kwds.items()):
            inputkey = key
            key = ''.join([x.title() for x in key.split('_')])
            if key.startswith('Lexer'):
                key = key[5:]
                if key not in self.LEXER_STYLES:
                    raise ValueError('%s is not a valid lexer style' % inputkey)
                lexer_colors[key] = value
            else:
                attr = 'set%sColor' % key
                method = getattr(self, attr)
                tasks.append((method, QColor(value)))
        
        # Apply main UI colors 
        for method, arg in tasks:
            method(arg)
            
        # Apply lexer colors
        lexer = self.lexer()
        for style, color in lexer_colors.items():
            color = QtGui.QColor(color)
            style_idx = self.LEXER_STYLES[style]
            lexer.setColor(color, style_idx)
    
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
