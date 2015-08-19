'''
Loads and initialize the main application. This is the entry point to the
tugalinhas program.
'''

import os
import sys
from PyQt4 import QtGui, QtCore

from tugalinhas.main_window import MainWindow
from tugalinhas.splash import Splash


# Need to use logging when debugging, since stdout and stderr
#  are redirected to the internal console.

def setup_logging(level='debug'):
    '''Setup logging'''

    import logging.handlers
    from tugalinhas import LOG_FILENAME

    levels = {'debug': logging.DEBUG,
              'info': logging.INFO,
              'critical': logging.CRITICAL,
              }
    if level not in levels:
        loglevel_error = level
        level = 'debug'
    elif not level:
        loglevel_error = '<empty>'
        level = 'debug'
    else:
        loglevel_error = False
    loglevel = levels[level]

    logger = logging.getLogger('TugalinhasLogger')
    logger.setLevel(loglevel)
    handler = logging.handlers.RotatingFileHandler(
        LOG_FILENAME, maxBytes=1000000, backupCount=3)
    logger.addHandler(handler)

    if loglevel_error:
        logger.debug(
            'Log level error: level %s not available.' %
            loglevel_error)
    logger.critical('Logging started at level "%s".' % level)


def run(pynfile=None):
    '''Create the main window and run application'''

    # Load translations -- portuguese translation is pending :\
    translator = QtCore.QTranslator()
    localename = QtCore.QLocale.system().name()
    translation = 'data/translations/tugalinhas_' + localename
    translator.load(translation)

    # Start app with splash screen
    app = QtGui.QApplication(sys.argv)
    app.installTranslator(translator)

    splash = Splash(app)
    splash.show()
    app.processEvents()

    splash.window = window = MainWindow(app)
    window.show()
    splash.raise_()

    if pynfile is not None:
        pynfile = os.path.abspath(pynfile)
        QtCore.QTimer.singleShot(250, lambda: window.open(pynfile))

    app.exec_()


def dumpfile():
    fp = sys.argv[-1]
    app = QtGui.QApplication(sys.argv)
    win = MainWindow(app)
    sys.stdout = win.interpretereditor.save_stdout
    sys.stderr = win.interpretereditor.save_stderr
    win._openfile(fp, add_to_recent=False, dump=True)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == '-D':
            if len(sys.argv) > 2:
                level = sys.argv[2]
                setup_logging(level)
            else:
                setup_logging()
    run()
