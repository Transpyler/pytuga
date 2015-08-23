'''
Loads and initialize the main application. This is the entry point to the
tugalinhas program.
'''

import os
import sys
import warnings
from PyQt4 import QtGui, QtCore
from tugalinhas import TRANSLATIONS_PATH
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


def dumpfile():
    fp = sys.argv[-1]
    app = QtGui.QApplication(sys.argv)
    win = MainWindow(app)
    sys.stdout = win.interpretereditor.save_stdout
    sys.stderr = win.interpretereditor.save_stderr
    win._openfile(fp, add_to_recent=False, dump=True)


def run(filepath=None):
    '''Create the main window and run application'''

    # Load translations
    translator = QtCore.QTranslator()
    localename = QtCore.QLocale.system().name()
    translation = TRANSLATIONS_PATH + localename + '.qm'
    if not os.path.exists(translation):
        warnings.warn(
            'could not find translation for your locale: %r' % localename)
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

    if filepath is not None:
        filepath = os.path.abspath(filepath)
        QtCore.QTimer.singleShot(250, lambda: window.open(filepath))
    app.exec_()

if __name__ == "__main__":
    run()
