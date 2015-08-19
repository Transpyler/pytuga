import re
from pygments import unistring as uni
from pygments.util import shebang_matches
from pygments.token import Text, Operator, Keyword, Name, String, Number
from pygments.lexer import RegexLexer
from pygments.lexer import bygroups, default, words
from pygments.lexers.python import Python3Lexer, PythonTracebackLexer


class PytugaLexer(RegexLexer):

    """
    For `pytuga <http://www.pytuga.org.br?>`_ source code.
    """

    name = 'Pytuga'
    aliases = ['pytuga', 'pytg', 'pytuguês']
    filenames = ['pytg']  # Nothing until Python 3 gets widespread
    mimetypes = ['text/x-pytuga', 'application/x-pytuga']

    flags = re.MULTILINE | re.UNICODE

    uni_name = "[%s][%s]*" % (uni.xid_start, uni.xid_continue)

    tokens = Python3Lexer.tokens.copy()  # @UndefinedVariable

    tokens['keywords'] = [
        (words((
            'assert', 'break', 'continue', 'del', 'elif', 'else', 'except',
            'finally', 'for', 'global', 'if', 'lambda', 'pass', 'raise',
            'nonlocal', 'return', 'try', 'while', 'yield', 'yield from', 'as',
            'with'), suffix=r'\b'),
         Keyword),
        (words((
            'True', 'False', 'None'), suffix=r'\b'),
         Keyword.Constant),
    ]
    tokens['builtins'] = [
        (words((
            '__import__', 'abs', 'all', 'any', 'bin', 'bool', 'bytearray', 'bytes',
            'chr', 'classmethod', 'cmp', 'compile', 'complex', 'delattr', 'dict',
            'dir', 'divmod', 'enumerate', 'eval', 'filter', 'float', 'format',
            'frozenset', 'getattr', 'globals', 'hasattr', 'hash', 'hex', 'id',
            'input', 'int', 'isinstance', 'issubclass', 'iter', 'len', 'list',
            'locals', 'map', 'max', 'memoryview', 'min', 'next', 'object', 'oct',
            'open', 'ord', 'pow', 'print', 'property', 'range', 'repr', 'reversed',
            'round', 'set', 'setattr', 'slice', 'sorted', 'staticmethod', 'str',
            'sum', 'super', 'tuple', 'type', 'vars', 'zip'), prefix=r'(?<!\.)',
            suffix=r'\b'),
         Name.Builtin),
        (r'(?<!\.)(self|Ellipsis|NotImplemented)\b',
         Name.Builtin.Pseudo),  # @UndefinedVariable
        (words((
            'ArithmeticError', 'AssertionError', 'AttributeError',
            'BaseException', 'BufferError', 'BytesWarning', 'DeprecationWarning',
            'EOFError', 'EnvironmentError', 'Exception', 'FloatingPointError',
            'FutureWarning', 'GeneratorExit', 'IOError', 'ImportError',
            'ImportWarning', 'IndentationError', 'IndexError', 'KeyError',
            'KeyboardInterrupt', 'LookupError', 'MemoryError', 'NameError',
            'NotImplementedError', 'OSError', 'OverflowError',
            'PendingDeprecationWarning', 'ReferenceError', 'ResourceWarning',
            'RuntimeError', 'RuntimeWarning', 'StopIteration',
            'SyntaxError', 'SyntaxWarning', 'SystemError', 'SystemExit', 'TabError',
            'TypeError', 'UnboundLocalError', 'UnicodeDecodeError',
            'UnicodeEncodeError', 'UnicodeError', 'UnicodeTranslateError',
            'UnicodeWarning', 'UserWarning', 'ValueError', 'VMSError', 'Warning',
            'WindowsError', 'ZeroDivisionError',
            # new builtin exceptions from PEP 3151
            'BlockingIOError', 'ChildProcessError', 'ConnectionError',
            'BrokenPipeError', 'ConnectionAbortedError', 'ConnectionRefusedError',
            'ConnectionResetError', 'FileExistsError', 'FileNotFoundError',
            'InterruptedError', 'IsADirectoryError', 'NotADirectoryError',
            'PermissionError', 'ProcessLookupError', 'TimeoutError'),
            prefix=r'(?<!\.)', suffix=r'\b'),
         Name.Exception),
    ]
    tokens['numbers'] = [
        (r'(\d+\.\d*|\d*\.\d+)([eE][+-]?[0-9]+)?', Number.Float),
        (r'0[oO][0-7]+', Number.Oct),
        (r'0[bB][01]+', Number.Bin),
        (r'0[xX][a-fA-F0-9]+', Number.Hex),
        (r'\d+', Number.Integer)
    ]
    tokens['backtick'] = []
    tokens['name'] = [
        (r'@\w+', Name.Decorator),
        (uni_name, Name),
    ]
    tokens['funcname'] = [
        (uni_name, Name.Function, '#pop')
    ]
    tokens['classname'] = [
        (uni_name, Name.Class, '#pop')
    ]
    tokens['import'] = [
        (r'(\s+)(as)(\s+)', bygroups(Text, Keyword, Text)),
        (r'\.', Name.Namespace),
        (uni_name, Name.Namespace),
        (r'(\s*)(,)(\s*)', bygroups(Text, Operator, Text)),
        default('#pop')  # all else: go back
    ]
    tokens['fromimport'] = [
        (r'(\s+)(import)\b', bygroups(Text, Keyword), '#pop'),
        (r'\.', Name.Namespace),
        (uni_name, Name.Namespace),
        default('#pop'),
    ]
    tokens['strings'] = [
        # the old style '%s' % (...) string formatting (still valid in Py3)
        (r'%(\(\w+\))?[-#0 +]*([0-9]+|[*])?(\.([0-9]+|[*]))?'
         '[hlL]?[diouxXeEfFgGcrs%]', String.Interpol),
        # the new style '{}'.format(...) string formatting
        (r'\{'
         '((\w+)((\.\w+)|(\[[^\]]+\]))*)?'  # field name
         '(\![sra])?'                      # conversion
         '(\:(.?[<>=\^])?[-+ ]?#?0?(\d+)?,?(\.\d+)?[bcdeEfFgGnosxX%]?)?'
         '\}', String.Interpol),
        # backslashes, quotes and formatting signs must be parsed one at a time
        (r'[^\\\'"%\{\n]+', String),
        (r'[\'"\\]', String),
        # unhandled string formatting sign
        (r'%|(\{{1,2})', String)
        # newlines are an error (use "nl" state)
    ]

    def analyse_text(text):  # @NoSelf
        return shebang_matches(text, r'pythonw?3(\.\d)?')


class PytugaTracebackLexer(PythonTracebackLexer):
    pass


def mokey_patch():
    '''Mokey patch pygments in order to accept pytuga source'''

if __name__ == '__main__':
    pass
