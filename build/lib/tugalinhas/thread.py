import threading
import inspect
import ctypes
from PyQt4 import QtCore


def async_raise(tid, exctype):
    """raises the exception, performs cleanup if needed"""

    if not inspect.isclass(exctype):
        raise TypeError("Only types can be raised (not instances)")
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(
        tid,
        ctypes.py_object(exctype))
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        # """if it returns a number greater than one, you're in trouble,
        # and you should call it again with exc=NULL to revert the effect"""
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, 0)
        raise SystemError("PyThreadState_SetAsyncExc failed")


class Thread(threading.Thread):

    def _get_my_tid(self):
        """determines this (self's) thread id"""
        if not self.isAlive():
            return -1

        # do we have it cached?
        if hasattr(self, "_thread_id"):
            return self._thread_id

        # no, look for it in the _active dict
        for tid, tobj in threading._active.items():
            if tobj is self:
                self._thread_id = tid
                return tid

        raise AssertionError("could not determine the thread's id")

    def raise_exc(self, exctype):
        """raises the given exception type in the context of this thread"""

        tid = self._get_my_tid()
        if tid != -1:
            async_raise(tid, exctype)

    def terminate(self):
        """raises SystemExit in the context of the given thread, which should
        cause the thread to exit silently (unless caught)"""

        self.raise_exc(SystemExit)


class WatcherThread(QtCore.QThread):

    def __init__(self, cmd_thread):
        QtCore.QThread.__init__(self)
        self.cmd_thread = cmd_thread

    def run(self):
        self.cmd_thread.join()


class CmdThread(Thread):

    def __init__(self, editor, text):
        '''set up a separate thread to run the code given in txt in the
        InteractiveInterpreter editor.'''

        Thread.__init__(self)
        self.editor = editor
        self.text = text

    def run(self):
        lines = self.text.split('\n')
        if len(lines) > 1:
            self.editor.interpreter.runcode(self.text)
        else:
            self.editor.needmore = self.editor.interpreter.push(self.text)
