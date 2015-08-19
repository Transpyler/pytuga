'''Implements the interactive interpreter in the tugalinhas section.'''

import sys
import time
from PyQt4 import QtCore, QtGui
from PyQt4.Qsci import QsciScintilla
from pytuga import PyTugaConsole
from tugalinhas import LOG
from tugalinhas.pen import Pen
from tugalinhas.editor import PythonEditor
from tugalinhas.thread import CmdThread, WatcherThread


class Console(PyTugaConsole):

    def __init__(self, ilocals, editor):
        PyTugaConsole.__init__(self, ilocals)
        self.editor = editor

    def showtraceback(self):
        LOG.info('showtraceback')
        settings = QtCore.QSettings()
        quiet = settings.value('console/quietinterrupt', False, bool)
        exc_type, exc_value, exc_traceback = sys.exc_info()
        LOG.info(exc_type)
        LOG.info(exc_value)
        LOG.info(exc_traceback)
        if exc_type is KeyboardInterrupt and quiet:
            pass
        else:
            PyTugaConsole.showtraceback(self)


class Interpreter(PythonEditor):

    def setup_margin0(self):
        # Disable 1st margin
        self.setMarginWidth(0, 0)

    def show_line_numbers(self):
        pass

    def setup_custom(self):
        self.editor = self
        self._fontsize = 0

        self.wrap()

        self.history = []
        self._outputq = []
        self.historyp = -1

        self.reading = False
        self.pt = None

        self.save_stdout = sys.stdout
        self.save_stdin = sys.stdin
        self.save_stderr = sys.stderr

        sys.stdout = self
        sys.stderr = self
        sys.stdin = self

        self.needmore = False
        self.cmdthread = None

        QtCore.QTimer.singleShot(10, self.writeoutputq)
        self.write('>>> ')

    def wrap(self):
        self.setWrapMode(QsciScintilla.SC_WRAP_CHAR)

    def flush(self):
        # to suppress AttributeError ...
        # Not sure why that is happening and why it is not crashing, but...
        pass

    def clear(self):
        self.history = []
        self._outputq = []
        super().clear()
        self.write('>>> ')

    def addcmd(self, cmd, force=False):
        '''Clear the current line and write the given command to the
        interpreter'''

        if not force and self.cmdthread is not None:
            # Don't bother writing cmd if there is already
            #   a thread in progress...
            # force=True forces write even if cmd in progress.
            return

        self.clearline()
        self.write(cmd)
        if cmd[-1] == '\n':
            self.write('>>> ')
            self.history.append(cmd.rstrip())

    def readline(self):
        self.reading = True
        while self.reading:
            time.sleep(0.1)

        pt2 = self.pt
        self.pt = None

        lenbefore = len(pt2)
        pt = self.text()
        r = pt[lenbefore:]
        r = r.rstrip('\n')
        if not r:
            r = '\n'
        return r

    def write(self, text):
        '''cannot write directly to the console...
            instead, append this text to the output queue for later use.
        '''
        if text:
            self._outputq.append(text)
            if len(self._outputq) > 10:
                time.sleep(.1)

        if Pen.ControlC == 1:
            Pen.ControlC += 1
            raise KeyboardInterrupt

        self.save_stdout.write(text)

    def writeoutputq(self):
        '''process the text output queue. Must be done from the main thread.
        '''
        while self._outputq:
            text = self._outputq.pop(0)
            line, col = self.getCursorPosition()
            self.insert(text)
            self.setCursorPosition(line, col + len(text))
            QtCore.QTimer.singleShot(100, self.scrolldown)

        QtCore.QTimer.singleShot(10, self.writeoutputq)

    def checkprompt(self):
        line, _col = self.getCursorPosition()
        txt = self.text(line)
        if not txt:
            self.write('>>> ')

    def cleanup_ControlC(self):
        Pen.ControlC = False
        self.cmdthread = None

        to_remove = []
        for pen in self.main_window.user_pens:
            if not hasattr(pen, 'drawable') or pen.drawable is None:
                to_remove.append(pen)

        for pen in to_remove:
            self.main_window.defunct_pens.append(pen)
            self.main_window.user_pens.remove(pen)

    def testthreaddone(self):
        self.cleanup_ControlC()
        QtCore.QTimer.singleShot(100, self.checkprompt)

    def threaddone(self):
        self.cleanup_ControlC()

        if not self.needmore:
            QtCore.QTimer.singleShot(100, self.checkprompt)
        else:
            self.write('... ')
            self.write(' ' * self._indent_level)
            self._indent_level = 0

    def go(self):
        'react as if the ENTER key has been pressed on the keyboard'
        ev = QtGui.QKeyEvent(QtCore.QEvent.KeyPress,
                             QtCore.Qt.Key_Enter,
                             QtCore.Qt.NoModifier, '\n')
        self.keyPressEvent(ev)

    def spin(self, n, delay=0.01):
        '''call processEvents n times.
            If n is 0, continue until cmdthread is None
        '''
        if n:
            for _ in range(n):
                time.sleep(delay)
                QtGui.QApplication.processEvents(QtCore.QEventLoop.AllEvents)
        else:
            self.spin(1)
            cs = 500
            while self.cmdthread is not None:
                if not cs:
                    LOG.info('spin fail')
                    self.ctrl_c_thread_running()
                    return False
                cs -= 1
                time.sleep(delay)
                QtGui.QApplication.processEvents(QtCore.QEventLoop.AllEvents)

        return True

    def indentation(self, linen):
        i = 0
        txt = self.text(linen)[4:]
        if txt.isspace():
            return len(txt)

        for i, c in enumerate(txt):
            if c != ' ':
                break
        return i

    def keyPressEvent(self, ev):
        k = ev.key()
        mdf = ev.modifiers()

        if self.reading and self.pt is None:
            self.pt = self.text()

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
        Shift = QtCore.Qt.ShiftModifier
        U = QtCore.Qt.Key_U
        C = QtCore.Qt.Key_C
        V = QtCore.Qt.Key_V
        X = QtCore.Qt.Key_X
        A = QtCore.Qt.Key_A
        Home = QtCore.Qt.Key_Home
        E = QtCore.Qt.Key_E
        D = QtCore.Qt.Key_D
        H = QtCore.Qt.Key_H
        Z = QtCore.Qt.Key_Z

        passthru = True
        scrolldown = True

        if k in (Return, Enter):
            if self.reading:
                self.reading = False

            self.movetoend()

            line, col = self.getCursorPosition()
            txt = self.text(line)
            txt = txt[4:].rstrip()
            if txt:
                if self.history and not self.history[-1]:
                    # last history entry is blank line
                    del self.history[-1]
                self.history.append(txt)
            self.historyp = -1

            self.append('\n')

            if self.cmdthread is None:
                i = self.indentation(line)
                if txt.endswith(':'):
                    i += 4
                self._indent_level = i

                self.main_window.pen._mark_undo()

                self.cmdthread = CmdThread(self, txt)
                self.cmdthread.start()
                self.watcherthread = WatcherThread(self.cmdthread)
                self.watcherthread.finished.connect(self.threaddone)
                self.watcherthread.start()

                passthru = False
            else:
                passthru = True

        elif k in (Backspace, Tab, Backtab):
            line, col = self.getCursorPosition()
            lines = self.lines()
            i = self.indentation(line)

            if line < lines - 1:
                passthru = False
                scrolldown = True
            elif col <= 4 and k != Tab:
                passthru = False
                self.scroll_left()
            elif col <= i + 4:
                passthru = False
                spaces = col % 4
                if not spaces:
                    spaces = 4
                if k != Tab:
                    self.setSelection(line, 4, line, 4 + spaces)
                    self.replaceSelectedText('')
                    self.setCursorPosition(line, col - spaces)
                else:
                    self.insert(' ' * spaces)
                    self.setCursorPosition(line, 4 + i + spaces)
            elif line == lines - 1:
                passthru = True
            else:
                passthru = False

        elif mdf & Shift and k == Up:
            vbar = self.verticalScrollBar()
            vbar.setValue(vbar.value() - vbar.singleStep())
            passthru = False

        elif mdf & Shift and k == Down:
            vbar = self.verticalScrollBar()
            vbar.setValue(vbar.value() + vbar.singleStep())
            passthru = False

        elif mdf & Shift and k == PageUp:
            vbar = self.verticalScrollBar()
            vbar.setValue(vbar.value() - vbar.pageStep())
            passthru = False

        elif mdf & Shift and k == PageDown:
            vbar = self.verticalScrollBar()
            vbar.setValue(vbar.value() + vbar.pageStep())
            passthru = False

        elif k == Left:
            line, col = self.getCursorPosition()
            lines = self.lines()
            if line < lines - 1:
                passthru = False
                scrolldown = True
            elif col <= 4:
                passthru = False
                self.scroll_left()

        elif k == Right:
            line, col = self.getCursorPosition()
            lines = self.lines()
            if line < lines - 1:
                passthru = False
                scrolldown = True

        elif k in (Up, Down):
            self.scrolldown()

            line, col = self.getCursorPosition()

            txt = self.text(line)[4:].strip()

            if self.cmdthread is not None:
                pass

            elif not self.history:
                QtGui.QApplication.beep()

            else:
                changeline = True
                addthisline = False

                lenhist = len(self.history)

                if k == Up and self.historyp == -1:
                    addthisline = True

                if k == Up and lenhist == 1:
                    self.historyp -= 1
                elif k == Up and self.historyp <= -lenhist:
                    QtGui.QApplication.beep()
                    changeline = False
                elif k == Up:
                    self.historyp -= 1
                elif k == Down and self.historyp >= -1:
                    QtGui.QApplication.beep()
                    changeline = False
                elif k == Down:
                    self.historyp += 1

                if addthisline:
                    self.history.append(txt)

                if changeline:
                    txt = self.history[self.historyp]
                    endpos = len(self.text(line))

                    if self.historyp == -1:
                        del self.history[-1]

                    self.setSelection(line, 4, line, endpos)
                    self.replaceSelectedText(txt)

            passthru = False

        elif mdf & Control and k == U:
            # erase from pen to beginning of line
            self.scroll_left()
            self.erasetostart()

        elif mdf & Control and k == X:
            # Cut # No action. Disabled.
            scrolldown = False
            passthru = False

        elif mdf & Control and mdf & Shift and k == X:
            # Cut
            self.cut()  # No action. Disabled.
            scrolldown = False
            passthru = False

        elif mdf & Control and mdf & Shift and k == C:
            # Copy
            self.copy()
            scrolldown = False
            passthru = False

        elif mdf & Control and mdf & Shift and k == V:
            # Paste
            self.paste()
            scrolldown = False
            passthru = False

        elif mdf & Control and k == Z:
            self.main_window.pen._undo()
            scrolldown = True
            passthru = False

        elif mdf & Control and k == C:
            # send keyboard interrupt
            LOG.info('Ctrl-C pressed')

            import threading
            if hasattr(threading, 'threads'):
                for pen in threading.threads:
                    threading.threads[pen] = 0

            if self.cmdthread is not None and self.cmdthread.isAlive():
                self.ctrl_c_thread_running()

            else:
                self.ctrl_c_no_thread_running()

            self.sync_pens_lists()

        elif (mdf & Control and k == A) or k == Home:
            self.movetostart()
            self.scroll_left()
            passthru = False
            scrolldown = False

        elif mdf & Control and k == E:
            self.movetoend()
            passthru = False

        elif mdf & Control and k == D:
            self.main_window.close()
            passthru = False

        elif mdf & Control and mdf & Shift and k == H:
            # Clear history
            self.history = []

        if scrolldown and ev.text():
            self.scrolldown()

        if passthru:
            super().keyPressEvent(ev)

    def update_window_modified(self):
        pass

    def ctrl_c_thread_running(self):
        Pen.ControlC = True
        Pen._stop_testall = True
        self.main_window.pen._empty_move_queue(lock=True)
        for pen in self.main_window.user_pens:
            pen._sync_items()
        self.needmore = False
        self.interpreter.resetbuffer()

    def ctrl_c_no_thread_running(self):
        Pen.ControlC = False
        Pen._stop_testall = True
        self.cmdthread = None

        self.main_window.pen._empty_move_queue(lock=True)

        settings = QtCore.QSettings()
        quiet = settings.value('console/quietinterrupt', False, bool)

        self.movetoend()
        if not quiet:
            self.write('\nKeyboardInterrupt\n')
        else:
            self.write('\n')
        self.interpreter.resetbuffer()
        self.write('>>> ')

    def sync_pens_lists(self):
        for p in self.main_window.all_pens:
            if p not in self.main_window.user_pens:
                p.remove()

        if self.main_window.pen not in self.main_window.user_pens:
            self.main_window.user_pens.append(self.main_window.pen)

    def scrolldown(self):
        '''force the console to scroll all the way down.

            If the pen is already in the last line,
                do not change location of the pen.

            If not, move the pen to the last position
                in the line.
        '''

        txt = self.text()
        nlines = len(txt.split('\n'))
        lastlinen = nlines - 1
        lastline = self.text(lastlinen)

        line, col = self.getCursorPosition()

        if line != lastlinen:
            self.setCursorPosition(lastlinen, len(lastline))

        if col < 4:
            self.setCursorPosition(lastlinen, 4)

        vbar = self.verticalScrollBar()
        vbar.setValue(vbar.maximum())

    def scroll_left(self):
        hbar = self.horizontalScrollBar()
        hbar.setValue(hbar.minimum())

    def mouseReleaseEvent(self, ev):
        super().mouseReleaseEvent(ev)

        line, col = self.getCursorPosition()
        txt = self.text(line)
        if col < 4 and not self.hasSelectedText():
            if txt.startswith('>>>') or txt.startswith('...'):
                self.setCursorPosition(line, 4)

    def contextMenuEvent(self, ev):
        '''right-click to pop up the context menu.
        Adjust displayed shortcut key combo since this is an interactive
            shell and ctrl-c is needed for stopping running code.

        Connection of actual typed shortcuts is in keyPressEvent()
        '''

        menu = self.createStandardContextMenu()
        actions = menu.actions()
        undo = actions[0]
        redo = actions[1]
        sep0 = actions[2]
        cut = actions[3]
        copy = actions[4]
        paste = actions[5]
        delete = actions[6]
        menu.removeAction(undo)
        menu.removeAction(redo)
        menu.removeAction(sep0)
        menu.removeAction(cut)

        menu.removeAction(copy)
        copyaction = QtGui.QAction('Copy', menu)
        copyshortcut = QtGui.QKeySequence(QtCore.Qt.CTRL +
                                          QtCore.Qt.SHIFT +
                                          QtCore.Qt.Key_C)
        copyaction.setShortcut(copyshortcut)
        copyaction.triggered.connect(self.copy)
        menu.insertAction(paste, copyaction)

        menu.removeAction(paste)
        pasteaction = QtGui.QAction('Paste', menu)
        pasteshortcut = QtGui.QKeySequence(QtCore.Qt.CTRL +
                                           QtCore.Qt.SHIFT +
                                           QtCore.Qt.Key_V)
        pasteaction.setShortcut(pasteshortcut)
        pasteaction.triggered.connect(self.paste)
        menu.insertAction(delete, pasteaction)

        menu.removeAction(delete)
        menu.exec_(ev.globalPos())

    def cut(self):
        pass

    def insertFromMimeData(self, data):
        self.scrolldown()
        super().insertFromMimeData(data)

    def movetostart(self):
        '''move the pen to the start of the line (after the prompt)'''
        line, _col = self.getCursorPosition()
        self.setCursorPosition(line, 4)

    def movetoend(self):
        '''move the pen to the end of the line'''
        line, _col = self.getCursorPosition()
        self.setCursorPosition(line, len(self.text(line)))

    def erasetostart(self):
        '''erase from the current pen position to the beginning
            of the line
        '''
        line, col = self.getCursorPosition()
        if col == 4:
            # line is already empty
            return
        self.setSelection(line, 4, line, col)
        self.replaceSelectedText('')
        self.setCursorPosition(line, 4)

    def clearline(self):
        self.scrolldown()
        self.movetoend()
        self.erasetostart()

    def settitle(self):
        pass

    def zoomout(self):
        self.setfontsize(self._fontsize - 1)

    def setfontsize(self, size):
        self._fontsize = size
        self.zoomTo(size)
