'''
The main editor with python syntax highlighting
'''
import io
import sys
import traceback
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

UnlockedControlKeys = set([A, C, Z, Minus, Plus, Equal])
UnlockedNavKeys = set([Up, Down, Right, Left, PageUp, PageDown, Home])
UnlockedShiftKeys = set()

class PythonConsole(PythonEditor):
    '''
    A Scintilla based console.
    '''
    
    def __init__(self, 
                 parent=None, *, 
                 namespace=None,
                 header_text=None, 
                 hide_margins=True, **kwds):
        super().__init__(parent, **kwds)
        if hide_margins:
            self.setMarginWidth(0, 0)
            self.setMarginWidth(1, 0)
        self.current_command = []
        self.console_namespace = dict(namespace or {})
        
        # Set header text
        if header_text is None:
            header_text = '>>> '
        else:
            header_text = '%s\n>>> ' % header_text
        self.setText(header_text)
        lineno = header_text.count('\n')
        self.locked = (lineno, 3)
        self.pylexer = self.lexer()
        self.history = []
        self.history_idx = 0
        
    def addPrompt(self, newline=True):
        data = '\n' if newline else ''
        self.setCursorAtEndPosition()
        self.insert('%s>>> ' % data)
        self.setCursorAtEndPosition()
        self.lockAtCurrent()
        
    def setNamespace(self, value):
        self.console_namespace.clear()
        self.console_namespace.update(value)
        
    def setCursorAtEndPosition(self):
        lineno = self.lines() - 1
        lineindex = self.lineLength(lineno)
        self.setCursorPosition(lineno, lineindex)
        
    def lockAtCurrent(self):
        lineno, lineindex = self.getCursorPosition()
        self.locked = (lineno, lineindex - 1)
        
    def processCurrentCommand(self):
        '''Process the current command. 
        
        Return the output of the command.'''
        
        cmd = '\n'.join(self.current_command)
        self.current_command.clear()
        if not cmd:
            self.addPrompt(newline=False)
        else:
            result = self.executeCommand(cmd)
            
            # Insert result in text
            self.insert(result)
            self.addPrompt(newline=bool(result))
            self.history.append(cmd)
        return cmd
        
    def currentCommandIsComplete(self):
        '''Return True or False depending if the current command is complete'''
        
        cmd = self.current_command
        if cmd[-1].rstrip().endswith(':'):
            return False
        elif len(cmd) == 1:
            return True
        else:
            if not cmd[-1].strip():
                return True
            else:
                return False
        
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
        
    def cancelCurrent(self):
        '''Cancel de current command and clear all input lines'''
        
        self.current_command.clear()
        i, j = self.locked
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
        self.current_command[:] = cmd.splitlines()[:-1]
        
    def runCommand(self, cmd):
        '''Run command in the console as if it was inserted by the user''' 
        
        self.cancelCurrent()
        result = self.executeCommand(cmd, 'exec')
        if result:
            self.insert('...\n' + result)
            self.addPrompt()
        self.history_idx = 0
        return result
    
    def keyPressEvent(self, ev):
        key = ev.key()
        modifiers = ev.modifiers()
        lineno, lineindex = self.getCursorPosition()

        # We are in a locked area. Only a few key take effect, and many of these
        # just passthru
        if (lineno, lineindex) <= self.locked:
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
            self.current_command.append(line[4:])
            
            # Process command, if complete
            if self.currentCommandIsComplete():
                self.processCurrentCommand()
            
            # Keep adding '... ' lines at the right indentation until the 
            # command is complete 
            else:
                lineno, lineindex = self.getCursorPosition()
                indent, _ = _splitindent(self.current_command[-1])
                self.insertAt('... ' + indent, lineno, 0)
                self.setCursorPosition(lineno, lineindex + 4 + len(indent))
            
        # Prevents it from deleting the first locked whitespace
        elif key in (Backspace, Backtab):
            if (lineno, lineindex - 1) > self.locked:
                super().keyPressEvent(ev)
                
        # Chooses commands in history
        elif key in (Up, Down):
            delta = 1 if key else 1 
            N = len(self.history)
            if N:
                idx = (N - self.history_idx - delta) % N
                self.replaceCurrentBy(self.history[idx])
                self.history_idx += delta
            else:
                self.cancelCurrent()
                
        # Ctrl + D deletes the current command
        elif modifiers & Control and key == D:
            self.cancelCurrent()
            
        # Passthru
        else:
            super().keyPressEvent(ev)
            
    def runner_(self, cmd, mode, out):
        '''Run code in an interpreter'''

        try:
            code = compile(cmd, '<input>', mode)
            exec(code, self.console_namespace)
        except:
            traceback.print_exc(file=out)

    # Pytuga hack!
    def runner(self, cmd, mode, out):
        import pytuga
        import tugalib
        tuganames = {k: getattr(tugalib, k) for k in dir(tugalib)}
        tuganames.update(self.console_namespace)
        self.console_namespace = tuganames
        pycmd = pytuga.transpile(cmd)
        self.runner_(pycmd, mode, out)


def _splitindent(line):
    '''Split a string into an indentation part and the rest of the string.

    Only process indentation of the first line of the string.'''

    idx = 0
    while line[idx] in [' ', '\t']:
        idx += 1
    return line[:idx], line[idx:]