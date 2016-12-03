# from metakernel_python import MetaKernelPython as KernelBase
from ast import PyCF_ONLY_AST

from IPython.core.compilerop import CachingCompiler
from IPython.utils import py3compat
from ipykernel.ipkernel import IPythonKernel as KernelBase
from ipykernel.zmqshell import ZMQInteractiveShell
from traitlets import Type

import pytuga
import pytuga.console


# We mokey-patch a few modules and functions to replace Python's compile
# function with pytuga's version. This is potentially fragile, but it seems to
# work well so far.
def ast_parse(self, source, filename='<unknown>', symbol='exec'):
    flags = self.flags | PyCF_ONLY_AST
    return pytuga.compile(source, filename, symbol, flags, 1)


CachingCompiler.ast_parse = ast_parse
py3compat.compile = pytuga.compile


class PrettyCallable:
    """
    Callable that is represented with a pretty message.
    """

    def __init__(self, func, name=None, doc=None, str=None,
                 autoexec=False, autoexec_message=None):
        self.__func = func
        self.__autoexec = autoexec
        self.__autoexec_message = autoexec_message
        self.__repr = str or 'please call %s()' % self.__name__
        self.__name__ = name or func.__name__
        self.__doc__ = doc or func.__doc__

    def __call__(self, *args, **kwargs):
        return self.__func(*args, **kwargs)

    def __repr__(self):
        if self.__autoexec:
            self.__func()
            return self.__autoexec_message or ''
        return self.__repr

    def __getattr__(self, attr):
        return getattr(self.__func, attr)


def pretty_callable(str=None, **kwargs):
    """
    Decorate function to be a pretty callable.

    Example:
        >>> @pretty_callable('call exit() to finish interactive shell')
        ... def exit():
        ...     raise SystemExit
    """

    def decorator(func):
        return PrettyCallable(func, str=str, **kwargs)

    return decorator


class PytugaShell(ZMQInteractiveShell):
    """
    A IPython based shell for pytuga.
    """

    def init_user_ns(self):
        """
        Additional symbols for pytuga environment.
        """

        super().init_user_ns()
        ns = self.user_ns

        @pretty_callable('digite "sair()" para terminar a execução',
                         autoexec=True, autoexec_message='tchau! ;-)')
        def sair():
            """
            Finaliza a execução do terminal de Pytuguês.
            """

            ns['exit']()

        ns['sair'] = sair

    def ex(self, cmd):
        return super().ex(pytuga.transpile(cmd))

    def ev(self, cmd):
        return super().ev(pytuga.transpile(cmd))


class PytugaKernel(KernelBase):
    """
    A meta kernel based backend to use Pytuga in Jupyter/iPython.
    """

    implementation = 'ipytuga'
    implementation_version = pytuga.__version__
    language = 'pytuga'
    language_version = pytuga.__version__
    banner = pytuga.console.pytuga_banner

    language_info = {
        'mimetype': 'text/x-pytuga',
        'file_extension': 'pytg',
        'codemirror_mode': {
            "version": 3,
            "name": "ipython"
        },
        'pygments_lexer': 'python',
    }

    shell_class = Type(PytugaShell)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        pytuga.init()

    def __do_execute(self, code, *args, **kwargs):
        print('do_execute', code, args)
        return super().do_execute(code, *args, **kwargs)

    def do_is_complete(self, code):
        return super().do_is_complete(pytuga.transpile(code))


def start_kernel():
    """
    Start Pytuga Jupyter kernel.
    """

    from ipykernel.kernelapp import IPKernelApp
    IPKernelApp.launch_instance(kernel_class=PytugaKernel)


if __name__ == '__main__':
    start_kernel()
