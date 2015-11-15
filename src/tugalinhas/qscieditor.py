'''
The main editor with python syntax highlighting
'''

import keyword
from PyQt5 import Qsci, QtGui, QtCore
from PyQt5.QtGui import QColor, QFont

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
Key_D = QtCore.Qt.Key_D

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

    NAMED_COLORS_INV = dict(
        lexer_default='default',
        lexer_comment='comment',
        lexer_number='number',
        lexer_double_quoted_string='string',
        lexer_single_quoted_string='string',
        lexer_keyword='keyword',
        lexer_triple_single_quoted_string='string',
        lexer_triple_double_quoted_string='string',
        lexer_class_name='definition',
        lexer_function_method_name='definition',
        lexer_operator='default',
        lexer_identifier='default',
        lexer_comment_block='comment',
        lexer_unclosed_string='badstring',
        lexer_highlighted_identifier='default',
        lexer_decorator='decorator',
    )
    COLOR_NAMES = set(NAMED_COLORS_INV.values())
    NAMED_COLORS = {'lexer_' + c: [] for c in COLOR_NAMES}
    for c, v in NAMED_COLORS_INV.items():
        NAMED_COLORS['lexer_' + v].append(c)
    
    DARK_COLORS = dict(
        margins_background='#000000',
        margins_foreground='#555753',
        caret_line_background='#555753',
        background='#2e3436',
        
        # Lexer colors
        lexer_default='#d3c7cf',
        lexer_comment='#888a85',
        lexer_number='#ff6c10',
        lexer_string='#edd400',
        lexer_keyword='#ffffff',
        lexer_definition='#729fcf',
        lexer_decorator='#ad7fa8',
        lexer_badstring='#ff0000',
    )
    
    WHITE_COLORS = dict(
        margins_background='#f6f6f6',
        margins_foreground='#8d9091',
        caret_line_background='#eeeeec',
        background='#ffffff',
        
        # Lexer colors
        lexer_default='#000000',
        lexer_comment='#0000ff',
        lexer_number='#ff00ff',
        lexer_string='#ff00ff',
        lexer_keyword='#a52a2a',
        lexer_definition='#008a8c',
        lexer_decorator='#a02ff0',
        lexer_badstring='#ff0000',
    )
    
    LIGHT_COLORS = dict(
        margins_background='#f0f0f0',
        margins_foreground='#a2a3a3',
        caret_line_background='#f1f1ef',
        background='#f6f7f8',
        
        # Lexer colors
        lexer_default='#4d4e53',
        lexer_comment='#708090',
        lexer_number='#0077aa',
        lexer_string='#0077aa',
        lexer_keyword='#669900',
        lexer_definition='#4186a8',
        lexer_decorator='#dd4a68',
        lexer_badstring='#ff0000',
    )
    
    DEFAULT_COLORS = DARK_COLORS
    
    BOLD_STYLES = {1, 5, 9, 14}
    
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
        self.setAllFonts(fontfamily, fontsize, True)
        
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
                    lexer.setFont(font_bold, style)
                else:
                    lexer.setFont(font, style)
            self.SendScintilla(Qsci.QsciScintilla.SCI_STYLESETFONT, 1, bfamily)
            
    def setColors(self, **kwds):
        '''Set colors for all given properties.
        
        Properties are of the form `margins_background` to set the 
        `marginsBackgroundColor` property.
        '''
        tasks = []
        
        # Handle color names:
        for k, v in list(kwds.items()):
            if k in self.NAMED_COLORS:
                color = kwds.pop(k)
                for k in self.NAMED_COLORS[k]:
                    kwds.setdefault(k, v)
        
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
            
        # Delete a line with Ctrl+D
        elif modifiers & Control and key == Key_D:
            if self.hasSelectedText():
                self.removeSelectedText()
            else:
                lineno, _ = self.getCursorPosition()
                lineend = self.lineLength(lineno)
                self.setSelection(lineno, 0, lineno, lineend)
                self.removeSelectedText()
            
        # Passthru to Scintilla
        else:
            super().keyPressEvent(ev)
