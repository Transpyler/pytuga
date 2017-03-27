import re

from lazyutils import lazy
import pytuga
from pyqode.python.modes.sh import PythonSH, make_python_patterns

pytuga_builtins = [x for x in dir(pytuga.lib) if not x.startswith('_')]


class PytugaSyntaxHighlighter(PythonSH):
    """
    Highlights pytuga syntax in the editor.
    """

    mimetype = 'text/x-pytuga'
    EXTRA_KEYWORDS = list(pytuga.keyword.PURE_PYTG_KEYWORDS)
    EXTRA_BUILTINS = pytuga_builtins

    @lazy
    def PROG(self):
        patterns = make_python_patterns(
            additional_builtins=self.EXTRA_BUILTINS,
            additional_keywords=self.EXTRA_KEYWORDS,
        )
        return re.compile(patterns, re.S)
