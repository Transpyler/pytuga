import os

from PyQt4 import QtCore, QtGui, uic
from tugalinhas import UI_FILES_PATH, BACKUP_FILENAME, DEFAULT_BGCOLOR, DEFAULT_COLOR,\
    DEFAULT_FILLCOLOR


class Settings(QtGui.QDialog):

    def __init__(self, parent):
        self.parent = parent
        QtGui.QDialog.__init__(self)
        uipath = os.path.join(UI_FILES_PATH, 'settings.ui')
        SClass, _ = uic.loadUiType(uipath)
        self.ui = SClass()
        self.ui.setupUi(self)
        self.setcurrent()

    def setcurrent(self):
        settings = QtCore.QSettings()
        ui = self.ui

        savesingle = settings.value('file/savesingle', True, bool)
        if savesingle:
            ui.savesingle.setChecked(True)
        else:
            ui.savefolder.setChecked(True)

        reloadexternal = settings.value('file/reloadexternal', True, bool)
        ui.reloadexternal.setChecked(reloadexternal)
        autorun = settings.value('file/autorun', False, bool)
        ui.autorun.setChecked(autorun)

        bfp = settings.value('file/backupfolderpath', '')
        ui.backupfolderpath.setText(bfp)
        bfn = settings.value('file/backupfilename', BACKUP_FILENAME)
        ui.backupfilename.setText(bfn)
        brate = settings.value('file/backuprate', 3, int)
        ui.backuprate.setValue(brate)
        bkeep = settings.value('file/backupkeep', 5, int)
        ui.backupkeep.setValue(bkeep)

        reset = settings.value('editor/testrun_reset', True, bool)
        ui.testrun_reset.setChecked(reset)
        mainfirst = settings.value('editor/mainfirst', True, bool)
        if mainfirst:
            ui.editor_mainfirst.setChecked(True)
        else:
            ui.editor_mainlast.setChecked(True)
        rev = settings.value('editor/testall_reverse', False, bool)
        ui.testall_reverse.setChecked(rev)
        autocall = settings.value('editor/testall_autocall', False, bool)
        ui.testall_autocall.setChecked(autocall)

        # Background color
        default = DEFAULT_BGCOLOR
        c = settings.value('view/bgcolor', default)
        color = QtGui.QColor(c)
        self.set_bgcolor_swatch(color)
        ui._bgcolor = color
        # Pen color
        default = DEFAULT_COLOR
        rgba = int(settings.value('tugalinhas/color', default))
        color = QtGui.QColor.fromRgba(rgba)
        self.set_pencolor_swatch(color)
        ui._color = color
        # Fill color
        default = DEFAULT_FILLCOLOR
        rgba = int(settings.value('tugalinhas/fillcolor', default))
        color = QtGui.QColor.fromRgba(rgba)
        self.set_fillcolor_swatch(color)
        ui._fillcolor = color

        reset_forces_visible = settings.value(
            'tugalinhas/reset_forces_visible',
            True,
            bool)
        ui.reset_forces_visible.setChecked(reset_forces_visible)
        allow_start_hidden = settings.value(
            'tugalinhas/allow_start_hidden',
            False,
            bool)
        ui.allow_start_hidden.setChecked(allow_start_hidden)
        quietinterrupt = settings.value('console/quietinterrupt', False, bool)
        ui.quietinterrupt.setChecked(quietinterrupt)

    def backupbrowse(self):
        filepath = QtGui.QFileDialog.getExistingDirectory(
            self,
            'Choose folder to store backups')
        if filepath:
            self.ui.backupfolderpath.setText(filepath)

    def externaloption(self):
        rel = self.ui.reloadexternal.isChecked()
        self.ui.autorun.setEnabled(rel)

    def backupoption(self, val):
        backup = bool(val)
        self.ui.backupfolderpath.setEnabled(backup)
        self.ui.backupfilename.setEnabled(backup)
        self.ui.backuprate.setEnabled(backup)

    def defaultsettings(self):
        self.parent.clear_settings()
        self.setcurrent()

    def bgcolorbrowse(self):
        settings = QtCore.QSettings()
        default = DEFAULT_BGCOLOR
        c = settings.value('view/bgcolor', default)
        color = QtGui.QColor(c)
        color = self.colorbrowse(color, False)
        self.set_bgcolor_swatch(color)
        self.ui._bgcolor = color

    def set_bgcolor_swatch(self, c):
        btn = self.ui.bgcolor
        pix = QtGui.QPixmap(150, 30)
        pix.fill(c)
        i = QtGui.QIcon(pix)
        btn.setIcon(i)
        btn.setIconSize(QtCore.QSize(150, 30))

    def pencolorbrowse(self):
        settings = QtCore.QSettings()
        default = DEFAULT_COLOR
        rgba = int(settings.value('tugalinhas/color', default))
        color = QtGui.QColor.fromRgba(rgba)
        color = self.colorbrowse(color, True)
        self.set_pencolor_swatch(color)
        self.ui._color = color

    def set_pencolor_swatch(self, c):
        btn = self.ui.pencolor
        pix = QtGui.QPixmap(150, 30)
        pix.fill(c)
        i = QtGui.QIcon(pix)
        btn.setIcon(i)
        btn.setIconSize(QtCore.QSize(150, 30))

    def fillcolorbrowse(self):
        settings = QtCore.QSettings()
        default = DEFAULT_FILLCOLOR
        rgba = int(settings.value('tugalinhas/fillcolor', default))
        color = QtGui.QColor.fromRgba(rgba)
        color = self.colorbrowse(color, True)
        self.set_fillcolor_swatch(color)
        self.ui._fillcolor = color

    def set_fillcolor_swatch(self, c):
        btn = self.ui.fillcolor
        pix = QtGui.QPixmap(150, 30)
        pix.fill(c)
        i = QtGui.QIcon(pix)
        btn.setIcon(i)
        btn.setIconSize(QtCore.QSize(150, 30))

    def colorbrowse(self, color, alpha=True):
        if alpha:
            ncolor = QtGui.QColorDialog.getColor(
                color,
                self,
                'Select Color',
                QtGui.QColorDialog.ShowAlphaChannel)
        else:
            ncolor = QtGui.QColorDialog.getColor(color,
                                                 self,
                                                 'Select Color')

        if ncolor.isValid():
            r, g, b, a = ncolor.getRgb()
            return QtGui.QColor(r, g, b, a)
        else:
            return False

    def set_colors_to_current(self):
        pyn = self.parent.pen

        r, g, b = pyn.bgcolor()
        color = QtGui.QColor(r, g, b)
        self.set_bgcolor_swatch(color)
        self.ui._bgcolor = color

        r, g, b, a = pyn.color()
        color = QtGui.QColor.fromRgb(r, g, b, a)
        self.set_pencolor_swatch(color)
        self.ui._color = color

        r, g, b, a = pyn.fillcolor()
        color = QtGui.QColor.fromRgb(r, g, b, a)
        self.set_fillcolor_swatch(color)
        self.ui._fillcolor = color
