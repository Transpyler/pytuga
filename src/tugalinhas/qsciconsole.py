'''
The main editor with python syntax highlighting
'''
import io
import sys
import traceback
import abc
import multiprocessing
import subprocess
from PyQt5 import QtCore
from .qscieditor import PythonEditor


Tab = QtCore.Qt.Key_Tab
Backtab = QtCore.Qt.Key_Backtab
Backspace = QtCore.Qt.Key_Backspace
Left = QtCore.Qt.Key_Left
Right = QtCore.Qt.Key_Right
Return = QtCore.Qt.Key_Return
Enter = QtCore.Qt.Key_Enter
Up = QtCore.Qt.Key_Up
PageUp = QtCore.Qt.Key_PageUp
Down = QtCore.Qt.Key_Down
PageDown = QtCore.Qt.Key_PageDown
Control = QtCore.Qt.ControlModifier
Home = QtCore.Qt.Key_Home
Shift = QtCore.Qt.ShiftModifier
U = QtCore.Qt.Key_U
D = QtCore.Qt.Key_D
C = QtCore.Qt.Key_C
V = QtCore.Qt.Key_V
X = QtCore.Qt.Key_X
A = QtCore.Qt.Key_A
E = QtCore.Qt.Key_E
D = QtCore.Qt.Key_D
H = QtCore.Qt.Key_H
Z = QtCore.Qt.Key_Z
Plus = QtCore.Qt.Key_Plus
Minus = QtCore.Qt.Key_Minus
Equal = QtCore.Qt.Key_Equal

# Key groups
UnlockedControlKeys = {A, C, Z, Minus, Plus, Equal}
UnlockedNavKeys = {Up, Down, Right, Left, PageUp, PageDown, Home}
UnlockedShiftKeys = set()


#
# Classes
#
class AbstractRunner(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def checkComplete(self, src):
        '''Return True if source code can represent a complete command.'''

        return True

    @abc.abstractmethod
    def checkValidSyntax(self, src):
        '''Return True if source code has a valid syntax.'''

        return False

    @abc.abstractmethod
    def runSingle(self, src):
        '''Runs command in 'single' mode: returns a string with the representation
        of the command output.'''

        raise NotImplementedError

    @abc.abstractmethod
    def runExec(self, src):
        '''Runs command in "exec" mode: returns a string with all prints during
        the command's execution.'''

        raise NotImplementedError

    @abc.abstractmethod
    def kill(self):
        '''Kills runner processs'''

        raise NotImplementedError


class PythonRunner(AbstractRunner):
    '''Runs code in a Python 3 interpreter'''

    def __init__(self, namespace=None):
        self._pool = multiprocessing.Pool()
        self._namespace = dict(namespace or {})

    def checkComplete(self, src):
        header, *_ = src.splitlines()
        return header.strip().endswith(':')

    def checkValidSyntax(self, src):
        try:
            compile(src, '<input>', 'eval')
            return True
        except SyntaxError:
            return False

    def runSingle(self, src):
        self._pool.apply(self._runWorker, args=(src, 'single'))

    def runExec(self, src):
        self._pool.apply(self._runWorker, args=(src, 'exec'))

    @staticmethod
    def _runWorker(self, cmd, mode, io_out):
        try:
            stdout, stderr = sys.stdout, sys.stderr
            out = sys.stdout = io.StringIO()
            err = sys.sterr = io.StringIO()
            code = compile(cmd, '<input>', mode)
            exec(code, self._namespace)
        except:
            traceback.print_exc(file=out)
        finally:
            sys.stdout, sys.stderr = stdout, stderr
            return out.getvalue() + err.getvalue()


class PyTranspilableRunner(PythonRunner):
    @abc.abstractmethod
    def transpile(self, src):
        '''Transpile source to Python 3'''

        raise NotImplementedError

    def runSingle(self, src):
        return super().runSingle(self.transpile(src))

    def runExec(self, src):
        return super().runExec(self.transpile(src))


class PyTugaRunner(PyTranspilableRunner):
    def __init__(self, namespace=None):
        import pytuga
        import tugalib

        self._pytuga = pytuga
        namespace = {k: v
            for (k, v) in vars(tugalib).items()
                if not k.startswith('_')}
        namespace.update(dict(namespace or {}))
        super().__init__(namespace=namespace)

    def transpile(self, src):
        return self._pytuga.transpile(src)


class CRunner(AbstractRunner):
    def __init__(self):
        self._cdll = None

    def getSymbols(self, src):
        '''Return a mapping from {name: type} for all symbols defined in the
        source'''

    def forceExtern(self, src):
        '''Convert all declarations in C source to extern declarations.'''

        return src

    def compile(self, src):
        '''Compiles and saves the ctypes cdll object internally'''

    def runSingle(self, src):
        raise NotImplementedError('CRunner cannot run in single mode')

    def runExec(self, src):
        extern_src = self.forceExtern(src)
        self.compile(extern_src)
        raise NotImplementedError


class PythonConsole(PythonEditor):
    '''
    A Scintilla based console.
    '''
    
    def __init__(self, 
                 parent=None, runner=None, *,
                 namespace=None,
                 header_text=None, 
                 hide_margins=True, **kwds):
        super().__init__(parent, **kwds)
        if hide_margins:
            self.setMarginWidth(0, 0)
            self.setMarginWidth(1, 0)
        self._current_command = []
        self._runner = runner or PythonRunner(dict(namespace or {}))
        
        # Set header text
        if header_text is None:
            header_text = '>>> '
        else:
            header_text = '%s\n>>> ' % header_text
        self.setText(header_text)
        lineno = header_text.count('\n')
        self._locked = (lineno, 3)
        self._pylexer = self.lexer()
        self._history = []
        self._history_idx = 0
        
    def addPrompt(self, newline=True):
        data = '\n' if newline else ''
        self.setCursorAtEndPosition()
        self.insert('%s>>> ' % data)
        self.setCursorAtEndPosition()
        self.lockAtCurrent()
        
    def setNamespace(self, value):
        self._console_namespace.clear()
        self._console_namespace.update(value)
        
    def setCursorAtEndPosition(self):
        lineno = self.lines() - 1
        lineindex = self.lineLength(lineno)
        self.setCursorPosition(lineno, lineindex)
        
    def lockAtCurrent(self):
        lineno, lineindex = self.getCursorPosition()
        self._locked = (lineno, lineindex - 1)

    def currentCommandIsComplete(self):
        '''Return True or False depending if the current command is complete'''

        cmd = self._current_command
        if cmd[-1].rstrip().endswith(':'):
            return False
        elif len(cmd) == 1:
            return True
        else:
            if not cmd[-1].strip():
                return True
            else:
                return False

    def processCurrentCommand(self):
        '''Process the current command.

        Return the output of the command.'''

        cmd = '\n'.join(self._current_command)
        self._current_command.clear()
        if not cmd:
            self.addPrompt(newline=False)
        else:
            result = self.executeCommand(cmd)

            # Insert result in text
            self.insert(result)
            self.addPrompt(newline=bool(result))
            self._history.append(cmd)
        return cmd

    def executeCommand(self, cmd, mode='single'):
        '''Return a string with the print messages yielded after the execution
        of a command string.
        
        This would possibly change an internal state such as the
        `console_namespace` attribute.
        '''
        
        cmd = cmd.rstrip() + '\n'
        try:
            stdout, stderr = sys.stdout, sys.stderr
            out = sys.stdout = io.StringIO()
            err = sys.sterr = io.StringIO()
            self.runner(cmd, mode, out)
            result = out.getvalue() + err.getvalue()
        finally:
            sys.stdout, sys.stderr = stdout, stderr

        return result

    def runCommand(self, cmd):
        '''Run command in the console as if it was inserted by the user'''

        self.cancelCurrent()
        result = self.executeCommand(cmd, 'exec')
        if result:
            self.insert('...\n' + result)
            self.addPrompt()
        self._history_idx = 0
        return result

    def run(self, cmd, mode, out):
        if mode == 'exec':
            return self._runner.runExec(src)

        import pytuga
        import tugalib
        tuganames = {k: getattr(tugalib, k) for k in dir(tugalib)}
        tuganames.update(self._console_namespace)
        self._console_namespace = tuganames
        pycmd = pytuga.transpile(cmd)
        self.runner_(pycmd, mode, out)

    def cancelCurrent(self):
        '''Cancel de current command and clear all input lines'''
        
        self._current_command.clear()
        i, j = self._locked
        m = self.lines()
        n = self.lineLength(m)
        self.setSelection(i, j + 1, m, n)
        self.removeSelectedText()

    def replaceCurrentBy(self, cmd):
        '''Replaces the current command by the given command'''

        cmd_lines = cmd.splitlines()
        cmd_lines[1:] = ['... ' + line for line in cmd_lines[1:]]
        self.cancelCurrent()
        self.setCursorAtEndPosition()
        self.insert('\n'.join(cmd_lines))
        self.setCursorAtEndPosition()
        self._current_command[:] = cmd.splitlines()[:-1]

    def keyPressEvent(self, ev):
        key = ev.key()
        modifiers = ev.modifiers()
        lineno, lineindex = self.getCursorPosition()

        # We are in a locked area. Only a few key take effect, and many of these
        # just passthru
        if (lineno, lineindex) <= self._locked:
            if (key in UnlockedNavKeys or
                    modifiers & Control and key in UnlockedControlKeys or
                    modifiers & Shift and key in UnlockedShiftKeys):
                super().keyPressEvent(ev)
            else:
                return
        
        # We are not in a locked area
        # Return control command execution in various ways
        if key in (Return, Enter):
            if modifiers & Control:
                return

            self.setCursorAtEndPosition()
            lineno, lineindex = self.getCursorPosition()            
            line = self.text(lineno)
            super().keyPressEvent(ev)

            # Add current line to the command list
            self._current_command.append(line[4:])

            # Process command, if complete
            if self.currentCommandIsComplete():
                self.processCurrentCommand()

            # Keep adding '... ' lines at the right indentation until the 
            # command is complete 
            else:
                lineno, lineindex = self.getCursorPosition()
                indent, _ = _splitindent(self._current_command[-1])
                self.insertAt('... ' + indent, lineno, 0)
                self.setCursorPosition(lineno, lineindex + 4 + len(indent))
            
        # Prevents it from deleting the first locked whitespace
        elif key in (Backspace, Backtab):
            if (lineno, lineindex - 1) > self._locked:
                super().keyPressEvent(ev)
                
        # Chooses commands in history
        elif key in (Up, Down):
            delta = 1 if key else 1 
            N = len(self._history)
            if N:
                idx = (N - self._history_idx - delta) % N
                self.replaceCurrentBy(self._history[idx])
                self._history_idx += delta
            else:
                self.cancelCurrent()

        # Ctrl + D deletes the current command
        elif modifiers & Control and key == D:
            self.cancelCurrent()

        # Passthru
        else:
            super().keyPressEvent(ev)


def _splitindent(line):
    '''Split a string into an indentation part and the rest of the string.

    Only process indentation of the first line of the string.'''

    idx = 0
    while line[idx] in [' ', '\t']:
        idx += 1
    return line[:idx], line[idx:]