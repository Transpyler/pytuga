import abc
from PyQt5 import QtCore


class QMeta(abc.ABCMeta, type(QtCore.QObject)):
    pass


class Runner(QtCore.QObject, metaclass=QMeta):
    askInputSignal = QtCore.pyqtSignal(str)
    askAlertSignal = QtCore.pyqtSignal(str)
    askFileSignal = QtCore.pyqtSignal(bool)
    pauseExecutionSignal = QtCore.pyqtSignal()

    # Sent for resuming execution from any ask* signal
    resumeExecutionSignal = QtCore.pyqtSignal()
    receiveInputSignal = QtCore.pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self._waiting = False
        self._userinput = None
        self.resumeExecutionSignal.connect(self._resumeExecution)
        self.receiveInputSignal.connect(self._receiveInput)

    def _resumeExecution(self):
        self._waiting = False

    def _receiveInput(self, value):
        self._userinput = value
        self._resumeExecution()

    @abc.abstractmethod
    def checkComplete(self, src):
        """Return True if source code can represent a complete command."""

        return True

    @abc.abstractmethod
    def checkValidSyntax(self, src):
        """Return True if source code has a valid syntax."""

        return False

    @abc.abstractmethod
    def runSingle(self, src):
        """Runs command in 'single' mode: returns a string with the representation
        of the command output."""

        raise NotImplementedError

    @abc.abstractmethod
    def runExec(self, src):
        """Runs command in "exec" mode: returns a string with all prints during
        the command's execution."""

        raise NotImplementedError

    @abc.abstractmethod
    def kill(self):
        """Kills runner processs"""

        raise NotImplementedError

    def poll(self):
        """Poll runner and return a boolean telling if runner is running"""

        return False

    def cancel(self):
        """Cancel execution of a runner process"""

        raise NotImplementedError
