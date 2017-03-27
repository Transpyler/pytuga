"""
Scintilla based console with python syntax highlighting
"""
import sys
import threading
from collections import deque
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from .qscieditor import PythonEditor

_stdout = sys.stdout
Tab = QtCore.Qt.Key_Tab
Backtab = QtCore.Qt.Key_Backtab
Backspace = QtCore.Qt.Key_Backspace
Escape = QtCore.Qt.Key_Escape
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
H = QtCore.Qt.Key_H
Z = QtCore.Qt.Key_Z
Plus = QtCore.Qt.Key_Plus
Minus = QtCore.Qt.Key_Minus
Equal = QtCore.Qt.Key_Equal

# Key groups
UnlockedControlKeys = {A, C, Z, Minus, Plus, Equal}
UnlockedNavKeys = {Up, Down, Right, Left, PageUp, PageDown, Home}
UnlockedShiftKeys = set()


class PythonConsole(PythonEditor):
    """
    A Scintilla based console.
    """

    printToConsoleSignal = QtCore.pyqtSignal(str, bool)

    def __init__(self,
                 parent=None, *,
                 runner=None,
                 header_text=None,
                 hide_margins=True, **kwds):
        super().__init__(parent, **kwds)
        if hide_margins:
            self.setMarginWidth(0, 0)
            self.setMarginWidth(1, 0)
        self._current_command = []

        # Connect signals to runner
        self._runner = runner
        self._runner.askInputSignal.connect(self.inputDialog)
        self._runner.askAlertSignal.connect(self.alertDialog)
        self._runner.askFileSignal.connect(self.fileDialog)
        self._runner.pauseExecutionSignal.connect(self.pauseDialog)
        self.printToConsoleSignal.connect(self.printToConsole)

        # Set header text
        if header_text is None:
            header_text = '>>> '
        else:
            header_text = '%s\n>>> ' % header_text
        self.setText(header_text)
        lineno = header_text.count('\n')
        self._locked_position = (lineno, 3)

        # Start lexer and history
        self._pylexer = self.lexer()
        self._history = History()

        # Configure timer for polling runner object (60 fps)
        self.startTimer(100 / 6)
        self._background_tasks = deque()

    def inputDialog(self, message):
        """Ask user for input. Return a string with the user supplied value."""

        text, ok = QtWidgets.QInputDialog.getText(
                self, 'Entrada de dados', message or 'Valor:'
        )
        self._runner.receiveInputSignal.emit(text)

    def pauseDialog(self):
        QtWidgets.QMessageBox.about(
                self, 'Esperando...', 'Pressione "OK" para continuar'
        )
        self._runner.resumeExecutionSignal.emit()

    def alertDialog(self, msg):
        QtWidgets.QMessageBox.about(self, 'Esperando...', msg)
        self._runner.resumeExecutionSignal.emit()

    def fileDialog(self, do_open):
        if do_open:
            fname = \
                QtWidgets.QFileDialog.getOpenFileName(self, 'Abrir arquivo')[0]
        else:
            fname = \
                QtWidgets.QFileDialog.getSaveFileName(self, 'Salvar arquivo')[0]
        self._runner.receiveInputSignal.emit(fname)

    def printToConsole(self, text, add_newline=True):
        self.insert(text)
        self.addPrompt(newline=add_newline)

    def timerEvent(self, timer):
        if self._background_tasks:
            started, thread = self._background_tasks[0]
            if not started:
                thread.start()
                self._background_tasks[0] = (True, thread)
            if not thread.is_alive():
                self._background_tasks.popleft()

    def scheduleBackgroundTask(self, func, args=()):
        thread = threading.Thread(target=func, args=args)
        started = False
        if not self._background_tasks:
            thread.start()
            started = True
        self._background_tasks.append((started, thread))

    def addPrompt(self, newline=True):
        data = '\n' if newline else ''
        self.setCursorAtEndPosition()
        self.insert('%s>>> ' % data)
        self.setCursorAtEndPosition()
        self.lockAtCurrent()

    def setNamespace(self, value):
        self._runner.updateNamespace(value)

    def setCursorAtEndPosition(self):
        lineno = self.lines() - 1
        lineindex = self.lineLength(lineno)
        self.setCursorPosition(lineno, lineindex)
        
    def lockAtCurrent(self):
        lineno, lineindex = self.getCursorPosition()
        self._locked_position = (lineno, lineindex - 1)

    def currentCommandIsComplete(self):
        """Returns a boolean telling if the current command is complete"""

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

    def getCurrentCommand(self):
        lines = list(self._current_command)
        lineno, _ = self.getCursorPosition()
        lines.append(self.text(lineno)[4:])
        return '\n'.join(lines)

    def processCurrentCommand(self):
        """Process the current command."""

        cmd = '\n'.join(self._current_command)
        self._current_command.clear()
        if not cmd.strip():
            self.addPrompt(newline=False)
        else:
            def run_command():
                if cmd.strip():
                    self._history.add(cmd)
                    result = self.run(cmd.strip() + '\n', 'single')
                else:
                    result = ''

                # Insert result in text
                self.printToConsoleSignal.emit(result, bool(result))

            self.scheduleBackgroundTask(run_command)

    def executeCommand(self, cmd, cancel_current=True, mode='exec'):
        """Run command in the console as if it was inserted by the user"""

        if cancel_current:
            self.cancelCurrent()

        def run_command():
            if not cmd.strip():
                return
            result = self.run(cmd.strip() + '\n', mode)
            if result:
                self.printToConsoleSignal.emit('...\n' + result, True)

        self.scheduleBackgroundTask(run_command)

    def run(self, cmd, mode):
        """Call the runner to execute the given command (either in 'single' or
        in 'exec' mode)."""

        if mode == 'exec':
            return self._runner.runExec(cmd)
        elif mode == 'single':
            return self._runner.runSingle(cmd)

    def cancelExecution(self):
        """Cancel execution of current command"""

        is_running, thread = self._background_tasks.popleft()
        if is_running:
            try:
                thread.join(0)
            except TimeoutError:
                pass
            self.addPrompt()

    def cancelCurrent(self):
        """Cancel de current command and clear all input lines"""
        
        self._current_command.clear()
        i, j = self._locked_position
        m = self.lines()
        n = self.lineLength(m)
        self.setSelection(i, j + 1, m, n)
        self.removeSelectedText()

    def replaceCurrentBy(self, cmd):
        """Replaces the current command by the given command"""

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
        is_locked = bool(self._background_tasks)
        if (lineno, lineindex) <= self._locked_position or is_locked:
            if key == Escape and is_locked:
                self.cancelExecution()
            elif (key in UnlockedNavKeys or
                    modifiers & Control and key in UnlockedControlKeys or
                    modifiers & Shift and key in UnlockedShiftKeys):
                super().keyPressEvent(ev)

            # Cancel selections if backspace is pressed
            elif key == Backspace and self.getSelection() != (-1, -1, -1, -1):
                line_start, idx_start, line_end, idx_end = self.getSelection()
                if (line_end, idx_end) > self._locked_position:
                    line_start, idx_start = self._locked_position
                    self.setSelection(line_start, idx_start + 1, line_end,
                                      idx_end)
                    self.removeSelectedText()
                else:
                    self.setSelection(-1, -1, -1, -1)
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

        # Prevents it from deleting the first locked whitespace.
        # Completely delete the margins with a single backspace stroke
        # Tab delete when deleting on empty margins
        # Delete selection up to the lock position
        elif key in (Backspace, Backtab):
            lock_line, lock_idx = self._locked_position

            if self.getSelection() != (-1, -1, -1, -1):
                line_start, idx_start, line_end, idx_end = self.getSelection()
                if (line_start, idx_start) <= self._locked_position:
                    line_start, idx_start = self._locked_position
                    self.setSelection(line_start, idx_start + 1,
                                      line_end, idx_end)
                super().keyPressEvent(ev)

            elif (lineno, lineindex - 1) <= self._locked_position:
                pass

            elif lineno > lock_line and lineindex <= 4:
                line_size = self.lineLength(lineno)
                self.setSelection(lineno, 0, lineno, line_size)
                self.replaceSelectedText('')
                new_lineno = lineno - 1
                new_lineidx = self.lineLength(new_lineno) - 1
                self.setCursorPosition(new_lineno, new_lineidx)

            elif lineno > lock_line:
                line = list(self.text(lineno)[4:lineindex])
                if all(c == ' ' for c in line):
                    for i in range(max(3, len(line))):
                        super().keyPressEvent(ev)
                else:
                    super().keyPressEvent(ev)

            else:
                super().keyPressEvent(ev)

        # Chooses commands in history
        elif key in (Up, Down):
            if not self._history.browsing:
                cmd = self.getCurrentCommand()
                self._history.add(cmd, is_complete=False)
                self._history.browsing = True

            if key == Up:
                self._history.incr()
            else:
                self._history.decr()
            self.replaceCurrentBy(self._history.get())

        # Ctrl + D deletes the current command
        elif modifiers & Control and key == D:
            self.cancelCurrent()

        # Correct paste behavior
        elif modifiers & Control and key == V:
            clipboard = QtWidgets.QApplication.clipboard()
            data = clipboard.text()
            if '\n' in data:
                mod_data = ' \n... '.join(data.split('\n'))
                clipboard.setText(mod_data)
            super().keyPressEvent(ev)
            clipboard.setText(data)

        # Passthru
        else:
            super().keyPressEvent(ev)

    # Disable context menu
    def contextMenuEvent(self, e):
        pass


def _splitindent(line):
    """Split a string into an indentation part and the rest of the string.

    Only process indentation of the first line of the string."""

    idx = 0
    while line[idx] in [' ', '\t']:
        idx += 1
    return line[:idx], line[idx:]


class HistoryItem:
    def __init__(self, command, is_complete=True):
        self.command = str(command)
        self.is_complete = is_complete

    def __str__(self):
        return self.command

    def __repr__(self):
        return ('' if self.is_complete else '*') + repr(self.command)

    def __hash__(self):
        return hash(self.command)

    def __eq__(self, other):
        if isinstance(other, HistoryItem):
            return self.command == other.command
        elif isinstance(other, str):
            return self.command == other.command
        else:
            return NotImplemented


class History:
    def __init__(self):
        self._data = [HistoryItem('')]
        self.index = 0
        self.browsing = False

    def add(self, element, is_complete=None, reset_index=True, clean=True):
        # Prepare history
        if clean:
            self.clean()
        if reset_index:
            self.index = 0

        # Add element
        elem = HistoryItem(element)
        try:
            del self._data[self._data.index(elem)]
            is_present = True
        except ValueError:
            is_present = False

        if is_complete is not None:
            elem.is_complete = is_present or is_complete
        self._data.append(elem)

    def incr(self):
        self.index += 1

    def decr(self):
        self.index -= 1

    def clean(self):
        self._data = [x for x in self._data if x.is_complete]
        self.browsing = False

    def get(self):
        N = len(self._data)
        return self._data[(N - self.index) % N].command

    def __str__(self):
        return str(self._data)

    def __len__(self):
        return len(self._data)
