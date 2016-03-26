import io
import sys
import time
import functools
import traceback
import builtins

from .base import Runner


class PythonRunner(Runner):
    """Runs code in a Python 3 interpreter"""

    def __init__(self, namespace=None):
        super().__init__()
        self._namespace = dict(namespace or {})
        self._update_special_functions()

    def _update_special_functions(self):
        @functools.wraps(input)
        def input_function(msg=None):
            self._waiting = True
            self._userinput = None
            self.askInputSignal.emit(str(msg or ''))
            while self._waiting:
                time.sleep(0.05)
            return self._userinput

        def alert(*args, sep=' ', end='\n'):
            """Opens an alert dialog displaying the input message."""

            data = sep.join(map(str, args)) + end
            self._waiting = True
            self.askAlertSignal.emit(data)
            while self._waiting:
                time.sleep(0.05)

        def pause():
            """Opens a dialog that pauses execution until the user cancels
            it."""
            self._waiting = True
            self.pauseExecutionSignal.emit()
            while self._waiting:
                time.sleep(0.05)

        def filechooser(do_open):
            self._waiting = True
            self._userinput = None
            self.askFileSignal.emit(do_open)
            while self._waiting:
                time.sleep(0.05)
            return self._userinput

        builtins.input = input_function
        self._namespace['input'] = input_function
        self._namespace['alert'] = alert
        self._namespace['pause'] = pause
        self._namespace['filechooser'] = filechooser

    def checkComplete(self, src):
        header, *_ = src.splitlines()
        return header.strip().endswith(':')

    def checkValidSyntax(self, src):
        try:
            compile(src, '<input>', 'eval')
            return True
        except SyntaxError:
            return False

    def kill(self):
        raise NotImplementedError

    def cancel(self):
        raise NotImplementedError

    def updateNamespace(self, D):
        self._namespace.update(D)

    def runSingle(self, src):
        return self._run_worker(src, 'single', self._namespace)

    def runExec(self, src):
        return self._run_worker(src, 'exec', self._namespace)

    @staticmethod
    def _run_worker(cmd, mode, ns):
        stdout, stderr = sys.stdout, sys.stderr
        out = sys.stdout = io.StringIO()
        err = sys.sterr = io.StringIO()
        try:
            code = compile(cmd, '<input>', mode)
            exec(code, ns)
        except:
            traceback.print_exc(file=out)
        finally:
            sys.stdout, sys.stderr = stdout, stderr
            data = out.getvalue() + err.getvalue()
            return data

    @staticmethod
    def _set_subprocess_globals(namespace):
        D = globals()
        D.update(namespace)
