import code
import sys
import traceback
from pytuga import core
from pytuga import __version__


pytuga_banner = \
    '''Benvindo ao Pytuguês, um Python com sotaque lusitano.
Pytuga %s
Python %s
digite "ajuda()", "licença()" ou "tutorial()" para maiores informações
''' % ( __version__, sys.version.splitlines()[0])


class PyTugaConsole(code.InteractiveConsole):
    """
    Very simple console for Pytuguês language.
    """

    def __init__(self, locals=None, filename='<console>', forbidden=True):
        tuga_ns = core.tugalib_namespace(forbidden=forbidden)
        locals = locals if locals is not None else {}
        locals.update(tuga_ns)
        super().__init__(locals, filename)

    def runsource(self, source, filename="<input>", symbol="single"):
        try:
            source = core.transpile(source)
            if source.endswith('\n'):
                source = source[:-1]
            code = self.compile(source, filename, symbol)
        except (OverflowError, SyntaxError, ValueError):
            # Case 1
            print(source)
            self.showsyntaxerror(filename)
            return False

        if code is None:
            # Case 2
            return True

        # Case 3
        self.runcode(code)
        return False

    def runcode(self, code):
        if isinstance(code, str):
            code = core.transpile(code)
        super(PyTugaConsole, self).runcode(code)

    def showsyntaxerror(self, filename=None):
        type, value, tb = sys.exc_info()
        sys.last_type = type
        sys.last_value = value
        sys.last_traceback = tb

        if filename and type is SyntaxError:
            # Work hard to stuff the correct filename in the exception
            try:
                msg, (dummy_filename, lineno, offset, dummy_line) = value.args
            except ValueError:
                # Not the format we expect; leave it alone
                pass
            else:
                # Stuff in the right filename and line
                print(self.buffer, lineno)
                line = dummy_line
                value = SyntaxError(msg, (filename, lineno, offset, line))
                sys.last_value = value
        if sys.excepthook is sys.__excepthook__:
            lines = traceback.format_exception_only(type, value)
            self.write(''.join(lines))
        else:
            # If someone has set sys.excepthook, we let that take precedence
            # over self.write
            sys.excepthook(type, value, tb)


def run_console():
    """
    Run the main console.
    """

    console = PyTugaConsole()
    try:
        import readline
    except ImportError:
        pass
    console.interact(pytuga_banner)


if __name__ == '__main__':
    run_console()
