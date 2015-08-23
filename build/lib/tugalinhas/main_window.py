'''Main window GUI'''

import os
import shutil
import time
from math import pi
import zipfile
from pytuga import compile
from bidict import bidict
from PyQt4 import QtGui, QtCore, uic
from PyQt4.Qt import QHBoxLayout
from tugalinhas import LOG, UI_FILES_PATH, BUG_URL, BACKUP_FILENAME, NODEFAULT
from tugalinhas.pen import Pen, INTERPRETER_PROTECT
from tugalinhas.thread import CmdThread, WatcherThread
from tugalinhas.util import SvgRenderer, plist
from tugalinhas.interpreter import Interpreter, Console
from tugalinhas.about import AboutDialog
from tugalinhas.settings import Settings
from tugalinhas.editor import PythonEditor
from tugalinhas.mde import MultiDocumentEditor


class Scene(QtGui.QGraphicsScene):

    '''Hold information for the scene that is being drawn in the tugalinhas
    screen'''

    def __init__(self):
        left = -300
        top = -300
        width = 600
        height = 600

        QtGui.QGraphicsScene.__init__(self)
        self.setSceneRect(left, top, width, height)


class MainWindow(QtGui.QMainWindow):

    '''Main window for the tugalinhas application'''

    def __init__(self, app):
        self.app = app
        self.paused = False
        self.renderer = SvgRenderer(self.app).getrend()

        self._fdir = os.path.expanduser('~')
        self._filepath = None
        self._modified = False

        self._mainthread = QtCore.QThread.currentThread()
        uipath = os.path.join(UI_FILES_PATH, 'tugalinhas.ui')
        MWClass, _ = uic.loadUiType(uipath)

        QtGui.QMainWindow.__init__(self)
        self.ui = MWClass()
        self.ui.setupUi(self)

        self._bgcolor = None
        self.initialize_settings()
        self.setup_pendown_choices()
        self.setup_speed_choices()
        self.setup_fill_choices()
        self.setup_view()
        self.setup_interpreter()
        self.setup_pen()
        self.setup_scale_transform()
        self.setup_splitter_sizes()
        self.setup_viewgroup()
        self.setup_modegroup()
        self.setup_settings()
        self.setup_recent()
        self.setup_timers()
        self.setup_fs_watcher()

        self.update_interpreter_locals(self.pen)
        self._centerview()
        self._leftdragstart = None

    def setup_view(self):
        self.scene = Scene()
        view = self.ui.view
        view.setScene(self.scene)
        self.scene.view = view
        view.show()
        view.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        view.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        view.mousePressEvent = self.onclick
        view.wheelEvent = self.mousewheelscroll
        view.mouseMoveEvent = self.mousemove
        view.mouseReleaseEvent = self.mouserelease

    def setup_interpreter(self):
        # Editor
        hbox = QHBoxLayout(self.ui.edframe)
        hbox.setSpacing(0)
        hbox.setMargin(0)
        self.editor_box = hbox
        self.editor = MultiDocumentEditor(self, PythonEditor)
        self.editor_box.addLayout(self.editor.box)

        # Interpreter editor
        self.interpretereditor = Interpreter(self)
        hbox = QHBoxLayout(self.ui.interpreterframe)
        hbox.setSpacing(0)
        hbox.setMargin(0)
        hbox.addWidget(self.interpretereditor)

        # Interpreter
        self.interpreter_locals = ilocals = {}
        self.interpreter = Console(ilocals, self.interpretereditor)
        self.interpretereditor.interpreter = self.interpreter
        self.interpretereditor.setFocus()

    def setup_pen(self):
        Pen.main_window = self
        Pen.renderer = self.renderer
        self.user_pens = []  # User-code-facing list of user_pens
        self.all_pens = []  # Actual list of existing user_pens
        self.defunct_pens = []
        self.pen = None
        try:
            self.pen = self.new_pen()
        except Exception as e:
            print(e)
            raise
            settings = QtCore.QSettings()
            settings.clear()
            self.pen = self.new_pen()

    def setup_scale_transform(self):
        self._scale = 1
        trans = QtGui.QTransform()
        trans.scale(self._scale, self._scale)
        self.scene.view.setTransform(trans)
        self.ui.view.centerOn(self.pen.drawable)

    def setup_splitter_sizes(self):
        self.ui.rsplitter.setSizes([390, 110])
        self.ui.wsplitter.setSizes([550, 350])
        self.ui.wsplitter.splitterMoved.connect(self.recenter)

    def setup_viewgroup(self):
        self.viewgroup = QtGui.QActionGroup(self)
        self.viewgroup.addAction(self.ui.actionPynguin)
        self.viewgroup.addAction(self.ui.actionArrow)
        self.viewgroup.addAction(self.ui.actionRobot)
        self.viewgroup.addAction(self.ui.actionTurtle)
        self.viewgroup.addAction(self.ui.actionHidden)
        self.viewgroup.setExclusive(True)
        self.viewgroup.triggered.connect(self.setImageEvent)

    def setup_modegroup(self):
        self.modegroup = QtGui.QActionGroup(self)
        self.modegroup.addAction(self.ui.actionModePynguin)
        self.modegroup.addAction(self.ui.actionModeLogo)
        self.modegroup.addAction(self.ui.actionModeTurtle)
        self.modegroup.setExclusive(True)

    def setup_pendown_choices(self):
        choices = ((self.ui.actionPenUp, False),
                   (self.ui.actionPenDown, True))
        self._pendowns = bidict(choices)
        self.pengroup = QtGui.QActionGroup(self)
        self.pengroup.addAction(self.ui.actionPenUp)
        self.pengroup.addAction(self.ui.actionPenDown)
        self.pengroup.setExclusive(True)
        self.pengroup.triggered.connect(self.setPen)

    def setup_speed_choices(self):
        choices = ((self.ui.actionSlow, 5),
                   (self.ui.actionMedium, 10),
                   (self.ui.actionFast, 20),
                   (self.ui.actionInstant, 0))
        self.speeds = bidict(choices)
        self.speedgroup = QtGui.QActionGroup(self)
        self.speedgroup.addAction(self.ui.actionSlow)
        self.speedgroup.addAction(self.ui.actionMedium)
        self.speedgroup.addAction(self.ui.actionFast)
        self.speedgroup.addAction(self.ui.actionInstant)
        self.speedgroup.setExclusive(True)
        self.speedgroup.triggered.connect(self.speedMenuEvent)

    def setup_fill_choices(self):
        choices = ((self.ui.actionFill, 'fill'),
                   (self.ui.actionNofill, 'nofill'))
        self._fills = bidict(choices)
        self.fillgroup = QtGui.QActionGroup(self)
        self.fillgroup.addAction(self.ui.actionFill)
        self.fillgroup.addAction(self.ui.actionNofill)
        self.fillgroup.setExclusive(True)
        self.fillgroup.triggered.connect(self.setFill)

    def setup_fs_watcher(self):
        self.watcher = QtCore.QFileSystemWatcher(self)
        self.watcher.fileChanged.connect(self._filechanged)
        self._watchdocs = {}
        self._writing_external = None

    def setup_timers(self):
        QtCore.QTimer.singleShot(60000, self.autosave)
        self._movetimer = self.startTimer(0)

    def update_interpreter_locals(self, pen):
        '''insert some values in to the interpreter.

        By default, inserts the "main" pen and its methods, but
            can pass in another pen and use it and its methods
            instead. (Useful when switching over from one pen
            to another as the main pen, like in reap() or promote()
        '''

        ilocals = self.interpreter_locals
        ilocals.update(
            PI=pi,
            Pen=Pen,
            pen=pen,
            pens=self.user_pens,
            history=self.history,
        )
        ilocals.update(pen.export_locals())

    def mousewheelscroll(self, ev):
        delta = ev.delta()
        view = self.scene.view
        view.setTransformationAnchor(QtGui.QGraphicsView.AnchorUnderMouse)
        self.zoom(delta)
        view.setTransformationAnchor(QtGui.QGraphicsView.AnchorViewCenter)

    def zoom(self, delta):
        view = self.scene.view

        scaleperc = 1 + ((delta / 120.0) * 0.05)
        self._scale *= scaleperc

        trans = QtGui.QTransform()
        trans.scale(self._scale, self._scale)
        view.setTransform(trans)

        self._centerview()

    def zoomin(self):
        self.zoom(120)

    def zoomout(self):
        self.zoom(-120)

    def zoom100(self):
        self._scale = 1
        self.zoom(0)
        pen = self.pen
        if hasattr(pen, '_pen'):
            gitem = pen._pen.drawable
        else:
            gitem = pen.drawable
        self.scene.view.ensureVisible(gitem)

    def zoomfit(self):
        'Zoom to fit the whole drawing'

        fitrect = self.scene.itemsBoundingRect()
        self.scene.view.fitInView(fitrect, QtCore.Qt.KeepAspectRatio)
        tr = self.scene.view.transform()
        self._scale = tr.m11()
        self.zoom(0)

    def mousemove(self, ev):
        QtGui.QGraphicsView.mouseMoveEvent(self.scene.view, ev)

        if self._leftdragstart is None:
            ev.accept()
            return

        buttons = ev.buttons()
        if buttons & QtCore.Qt.LeftButton:
            pen_pos = ev.posF()
            dpos = self._leftdragstart - pen_pos
            ctr0 = self._dragstartcenter
            ctr = ctr0 + (dpos / self._scale)

            self._cx = ctr.x()
            self._cy = ctr.y()
            self.recenter()

    def pan(self, dx=0, dy=0):
        self._cx -= dx / self._scale
        self._cy += dy / self._scale
        self.recenter()
        self._centerview()

    def panleft(self):
        self.pan(dx=-25)

    def panright(self):
        self.pan(dx=+25)

    def panup(self):
        self.pan(dy=+25)

    def pandown(self):
        self.pan(dy=-25)

    def _viewrect(self):
        view = self.scene.view
        viewportrect = view.viewport().geometry()
        tl = viewportrect.topLeft()
        br = viewportrect.bottomRight()
        tlt = view.mapToScene(tl)
        brt = view.mapToScene(br)
        return QtCore.QRectF(tlt, brt)

    def _viewcenter(self):
        'return the current center of the view'
        ctr = self._viewrect().center()
        return ctr

    def _centerview(self, ctr=None):
        'set _cx and _cy to the given coord or to the current view center'
        if ctr is None:
            ctr = self._viewcenter()
        self._cx = ctr.x()
        self._cy = ctr.y()

    def _sync_track(self, on=True):
        self.ui.actionTrack.setChecked(on)
        settings = QtCore.QSettings()
        settings.setValue('pen/track', on)

    def settrack(self):
        track = self.ui.actionTrack.isChecked()
        self.pen.track(track)
        if track:
            cmd = 'track()\n'
        else:
            cmd = 'notrack()\n'
        self.interpretereditor.addcmd(cmd)

    def onclick(self, ev):
        QtGui.QGraphicsView.mousePressEvent(self.scene.view, ev)

        button = ev.button()
        if not ev.isAccepted() and button == QtCore.Qt.LeftButton:
            self.leftclick(ev)

        elif button == QtCore.Qt.RightButton:
            self.rightclick(ev)

        self.interpretereditor.setFocus()

    def leftclick(self, ev):
        if not ev.isAccepted():
            self._leftdragstart = ev.posF()
            self._dragstartcenter = self._viewcenter()
        else:
            self._leftdragstart = None

    def mouserelease(self, ev):
        QtGui.QGraphicsView.mouseReleaseEvent(self.scene.view, ev)
        self._leftdragstart = None

    def rightclick(self, ev):
        evpos = ev.pos()
        scpos = self.scene.view.mapToScene(evpos)
        for pen in self.user_pens:
            if pen is self.pen and 'onclick' in self.interpreter_locals:
                onclick = self.interpreter_locals['onclick']
            else:
                onclick = pen.onclick
            onclick(scpos.x(), scpos.y())
        ev.ignore()

    def recenter(self):
        center = QtCore.QPointF(self._cx, self._cy)
        self.ui.view.centerOn(center)

    def settings(self):
        'open the settings dialog'

        settings = Settings(self)
        if settings.exec_():
            ui = settings.ui
            settings = QtCore.QSettings()

            savesingle = ui.savesingle.isChecked()
            oldsavesingle = settings.value('file/savesingle', True, bool)
            if savesingle != oldsavesingle:
                # Need to mark all docs as modified to make sure
                # they get written out in the new kind of save file
                for doc in self.editor.documents.values():
                    doc.setModified(True)
            settings.setValue('file/savesingle', savesingle)

            reloadexternal = ui.reloadexternal.isChecked()
            settings.setValue('file/reloadexternal', reloadexternal)
            autorun = ui.autorun.isChecked()
            settings.setValue('file/autorun', autorun)

            bfp = ui.backupfolderpath.text()
            settings.setValue('file/backupfolderpath', bfp)
            bfn = ui.backupfilename.text()
            settings.setValue('file/backupfilename', bfn)
            brate = ui.backuprate.value()
            settings.setValue('file/backuprate', brate)
            # hold on to the old backupkeep value. If it was zero
            # need to start the autosave timer
            bkeep0 = settings.value('file/backupkeep', 5, int)
            bkeep = ui.backupkeep.value()
            settings.setValue('file/backupkeep', bkeep)
            if not bkeep0:
                QtCore.QTimer.singleShot(brate * 60000, self.autosave)

            reset = ui.testrun_reset.isChecked()
            settings.setValue('editor/testrun_reset', reset)
            mainfirst = ui.editor_mainfirst.isChecked()
            settings.setValue('editor/mainfirst', mainfirst)
            rev = ui.testall_reverse.isChecked()
            settings.setValue('editor/testall_reverse', rev)
            autocall = ui.testall_autocall.isChecked()
            settings.setValue('editor/testall_autocall', autocall)

            bgcolor = ui._bgcolor
            settings.setValue('view/bgcolor', bgcolor.name())
            color = ui._color
            settings.setValue('pen/color', color.rgba())
            fillcolor = ui._fillcolor
            settings.setValue('pen/fillcolor', fillcolor.rgba())

            reset_forces_visible = ui.reset_forces_visible.isChecked()
            settings.setValue(
                'pen/reset_forces_visible',
                reset_forces_visible)
            allow_start_hidden = ui.allow_start_hidden.isChecked()
            settings.setValue('pen/allow_start_hidden', allow_start_hidden)
            quiet = ui.quietinterrupt.isChecked()
            settings.setValue('console/quietinterrupt', quiet)

    def clear_settings(self):
        '''reset settings to default values.
        '''
        settings = QtCore.QSettings()
        settings.clear()
        self.setup_settings()
        self.pen.reset(True)

    def initialize_settings(self):
        QtCore.QCoreApplication.setOrganizationName(
            'tugalinhas.googlecode.com')
        QtCore.QCoreApplication.setOrganizationDomain(
            'tugalinhas.googlecode.com')
        QtCore.QCoreApplication.setApplicationName('tugalinhas')

    def setup_settings(self):
        settings = QtCore.QSettings()
        self.settings = settings

        geometry = settings.value('window/geometry', None)
        if geometry is not None:
            self.restoreGeometry(geometry)

        self.pen._set_bgcolor_to_default()
        self.pen._set_color_to_default()
        self.pen._set_fillcolor_to_default()

        fontsize = settings.value('editor/fontsize', -2, int)
        self.editor.setfontsize(fontsize)
        wrap = settings.value('editor/wordwrap', False, bool)
        if wrap:
            self.ui.actionWordwrap.setChecked(True)
            self.wordwrap()
        numbers = settings.value('editor/linenumbers', True, bool)
        if not numbers:
            self.ui.actionShowLineNumbers.setChecked(False)
            self.editor.line_numbers(False)

        default = 'fast'
        speed = settings.value('pen/speed', default)
        try:
            self.pen.speed(speed)
        except ValueError:
            self.pen.speed(default)

        # remember the saved avatar
        imageid = settings.value('pen/avatar', 'tuga')
        allow_start_hidden = settings.value(
            'pen/allow_start_hidden',
            False,
            bool)
        if not allow_start_hidden and imageid == 'hidden':
            imageid = 'tuga'

        # set up any custom avatars
        n = settings.beginReadArray('pen/custom_avatars')
        for i in range(n):
            settings.setArrayIndex(i)
            idp = settings.value('idpath')
            self.set_pen_avatar(idp)
        settings.endArray()

        # then set the saved avatar that we remembered earlier
        self.set_pen_avatar(imageid)

        track = settings.value('pen/track', False, bool)
        if track:
            self.pen.track()

    def setup_recent(self):
        settings = QtCore.QSettings()
        recent = []
        for n in range(settings.beginReadArray('recent')):
            settings.setArrayIndex(n)
            fname = settings.value('fname')
            recent.append(str(fname))
        settings.endArray()

        filemenu = self.ui.filemenu
        actionsave = self.ui.actionSave
        rmenu = QtGui.QMenu('Recent', filemenu)
        rec = filemenu.insertMenu(actionsave, rmenu)
        recmenu = rec.menu()
        for fp in recent:
            _, fn = os.path.split(fp)
            if not fn:
                continue

            def excb(fp=fp):
                self.open_recent(fp)
            recmenu.addAction(fn, excb)

    def open_recent(self, fp):
        if fp.endswith('.py'):
            pass
        elif not self.maybe_save():
            return
        else:
            self._filepath = None

        self._fdir, _ = os.path.split(fp)
        if fp.endswith('.pyn'):
            self._new()
            self._filepath = fp
            self._openfile(fp)
        elif fp.endswith('.py'):
            self._openfile(fp)
        elif fp.endswith('_pynd'):
            self._new()
            self._filepath = fp
            self._opendir(fp)
        else:
            try:
                self._openfile(fp)
            except:
                try:
                    self._opendir(fp)
                except:
                    QtGui.QMessageBox.information(
                        self,
                        'Open failed',
                        'Unable to open file:\n\n%s' %
                        fp)

    def new_pen(self, mname=None, show_cmd=True):
        if mname:
            raise
        settings = QtCore.QSettings()
        class_name = 'Pen'

        cls = globals()[class_name]
        p = cls()
        p._modename = mname

        ilocals = self.interpreter_locals
        if 'p' not in ilocals:
            ilocals['p'] = p
            self.ui.actionModePynguin.setChecked(True)

        elif show_cmd:
            pn = 2
            while True:
                pns = 'p%s' % pn
                if pns not in ilocals:
                    break
                pn += 1
            ilocals[pns] = p
            cmd = '%s = %s()\n' % (pns, class_name)
            self.interpretereditor.addcmd(cmd)

        imageid = settings.value('pen/avatar', 'tuga')
        self.set_pen_avatar(imageid, p)

        return p

    def reset_pen(self):
        self.pen.reset()
        cmd = 'reset()\n'
        self.interpretereditor.addcmd(cmd)

    def clear_canvas(self):
        self.pen.clear()
        cmd = 'clear()\n'
        self.interpretereditor.addcmd(cmd)

    def timerEvent(self, ev):
        Pen._process_moves()

    def closeEvent(self, ev=None):
        if self.maybe_save():
            self.interpretereditor.cmdthread = None
            settings = QtCore.QSettings()
            settings.setValue('window/geometry', self.saveGeometry())
            ev.accept()
        else:
            ev.ignore()

    def history(self, clear=False):
        if not clear:
            for line in self.interpretereditor.history:
                self.interpretereditor.write('%s\n' % line)
        else:
            self.interpretereditor.history = []

    def new(self):
        if self.maybe_save():
            self._new(newdoc=True)
        else:
            pass

    def _new(self, newdoc=False):
        import threading
        if hasattr(threading, 'threads'):
            for pyn in threading.threads:
                threading.threads[pyn] = 0

        self.pen.reset(True)

        # Find objects to delete
        keep_functions = self.pen.export_locals()
        keep_functions.extend(INTERPRETER_PROTECT)
        for name in self.interpreter_locals:
            if name not in keep_functions:
                del self.interpreter_locals[name]

        self.editor.clear_all()
        self.interpretereditor.clear()
        if newdoc:
            self.newdoc()
        self._modified = False
        windowtitle = 'pen [*]'
        self.setWindowTitle(windowtitle)
        self.show_modified_status()
        self._filepath = None

    def check_modified(self):
        if self._modified:
            return True
        elif self.editor._modified:
            return True
        else:
            for tdoc in list(self.editor.documents.values()):
                if tdoc.isModified():
                    return True

        return False

    def show_modified_status(self):
        if self.check_modified():
            self.setWindowModified(True)
        else:
            self.setWindowModified(False)

    def maybe_save(self):
        if self.check_modified():
            ret = QtGui.QMessageBox.warning(
                self,
                self.tr('Save Changes?'),
                self.tr(
                    "The document has been modified.\n"
                    "Do you want to save your changes?"),
                QtGui.QMessageBox.Yes | QtGui.QMessageBox.Default,
                QtGui.QMessageBox.No,
                QtGui.QMessageBox.Cancel | QtGui.QMessageBox.Escape)
            if ret == QtGui.QMessageBox.Yes:
                return self.save()
            elif ret == QtGui.QMessageBox.Cancel:
                return False
        return True

    def autosave(self):
        '''automatically save a copy of the current project.
        Also moves older backups up a number and deletes the
            oldest backup.
        '''
        settings = QtCore.QSettings()
        backupkeep = settings.value('file/backupkeep', 5, int)
        if not backupkeep:
            return

        bfp = settings.value('file/backupfolderpath', '')
        bfp = bfp or self._fdir
        bfn = settings.value('file/backupfilename', BACKUP_FILENAME)
        fp = os.path.join(bfp, bfn % '')
        if self.writeable(fp, savesingle=True):
            self._writefile01(fp, backup=True)
        else:
            QtGui.QMessageBox.warning(
                self,
                'Autosave failed',
                'Cannot complete autosave.\n'
                'Autosave disabled.\n'
                'Check configuration!')
            settings.setValue('file/backupkeep', 0)
            return

        if backupkeep > 1:
            for fn in range(backupkeep, 1, -1):
                fpsrc = os.path.join(bfp, bfn % (fn - 1))
                fpdst = os.path.join(bfp, bfn % fn)
                if os.path.exists(fpsrc):
                    shutil.move(fpsrc, fpdst)
        else:
            fpsrc = os.path.join(bfp, bfn % 1)

        shutil.move(fp, fpsrc)

        brate = settings.value('file/backuprate', 3, int)
        QtCore.QTimer.singleShot(brate * 60000, self.autosave)

    def _correct_filename(self, fp=None):
        'make sure file name ends with .pyn'
        if fp is None:
            fp = self._filepath
        r, ext = os.path.splitext(fp)
        if ext != '.pyn':
            ext = '.pyn'
        return r + ext

    def _writefile(self, fp):
        'Write file list files and history as a zip file called .pyn'
        z = zipfile.ZipFile(fp, 'w')

        mselect = self.ui.mselect
        for n in range(mselect.count()):
            docid = str(mselect.itemData(n))
            doc = self.editor.documents[docid]
            modified = doc.isModified()
            cline, ccol = doc.getCursorPosition()
            arcname = '##%05d##__%s' % (n, docid)
            code = doc.cleancode()
            doc.beginUndoAction()
            doc.selectAll()
            doc.removeSelectedText()
            doc.insert(code)
            doc.setCursorPosition(cline, ccol)
            doc.setModified(modified)
            doc.endUndoAction()
            z.writestr(arcname, code.encode('utf-8'))

        historyname = '@@history@@'
        history = '\n'.join(self.interpretereditor.history)
        z.writestr(historyname, history.encode('utf-8'))

        z.close()

    def _writefile01(self, fp, backup=False):
        '''Write file list files and history as a zip file called *.pyn

        Version 01

        Puts all files in to a folder to make it match the writedir
        method better.

        Also used by _writedir() but all internal files that should be
        written to the related directory will be prefaced with '_@@'

        '''
        VERSION = b'pyn01'

        _, fn = os.path.split(fp)
        fbase, _ = os.path.splitext(fn)
        if not fbase.endswith('_pynd'):
            fbase = fbase + '_pynd'

        z = zipfile.ZipFile(fp, 'w')

        manifest = []

        mselect = self.ui.mselect
        for n in range(mselect.count()):
            docid = str(mselect.itemData(n))
            doc = self.editor.documents[docid]
            modified = doc.isModified()
            cline, ccol = doc.getCursorPosition()
            code = doc.cleancode()
            doc.beginUndoAction()
            doc.selectAll()
            doc.removeSelectedText()
            doc.insert(code)
            doc.setCursorPosition(cline, ccol)
            doc.setModified(modified)
            doc.endUndoAction()

            LOG.info('writing %s' % n)
            if not backup and doc._filepath is not None:
                efp = doc._filepath
                manifest.append(efp)

                LOG.info('external: %s' % efp)

                if efp.startswith('_@@'):
                    dirname, _ = os.path.split(fp)
                    if dirname:
                        efp = efp.replace('_@@', dirname)
                    else:
                        efp = efp[4:]
                self._remwatcher(efp)
                f = open(efp, 'w')
                f.write(code)
                f.close()
                self._addwatcher(efp, doc)

                doc.setModified(False)

            else:
                arcname = '%05d.py' % n

                zipi = zipfile.ZipInfo()
                zipi.filename = '/'.join([fbase, arcname])
                manifest.append(zipi.filename)
                zipi.compress_type = zipfile.ZIP_DEFLATED
                zipi.date_time = time.localtime()
                zipi.external_attr = 0o644 << 16
                zipi.comment = VERSION
                z.writestr(zipi, code.encode('utf-8'))

        historyname = '@@history@@'
        history = '\n'.join(self.interpretereditor.history)

        zipi = zipfile.ZipInfo()
        zipi.filename = os.path.join(fbase, historyname)
        zipi.compress_type = zipfile.ZIP_DEFLATED
        zipi.date_time = time.localtime()
        zipi.external_attr = 0o644 << 16
        zipi.comment = VERSION
        z.writestr(zipi, history)  # .encode('utf-8'))

        manifestname = '@@manifest@@'
        zipi = zipfile.ZipInfo()
        zipi.filename = os.path.join(fbase, manifestname)
        zipi.compress_type = zipfile.ZIP_DEFLATED
        zipi.date_time = time.localtime()
        zipi.external_attr = 0o644 << 16
        zipi.comment = VERSION
        manifeststr = '\n'.join(manifest)
        z.writestr(zipi, manifeststr.encode('utf-8'))

        z.close()

        self.show_modified_status()

    def _related_dir(self, fp=None):
        '''return the directory name related to path fp
        This is the directory that will be used for storing
            the files when not in savesingle mode.
        '''
        if fp is None:
            fp = self._filepath

        dirname, fname = os.path.split(fp)
        fbase, _ext = os.path.splitext(fname)
        fpd = os.path.join(dirname, fbase + '_pynd')

        return fpd

    def _writedir(self, fp):
        'Write file list files in to a directory'

        LOG.info('_writedir %s' % fp)
        fpd = self._related_dir(fp)
        LOG.info('RELATED: %s' % fpd)
        _, dirname = os.path.split(fpd)

        if not os.path.exists(fpd):
            os.mkdir(fpd)

        mselect = self.ui.mselect
        count = mselect.count()
        for n in range(count):
            docid = str(mselect.itemData(n))
            doc = self.editor.documents[docid]
            if doc._filepath is None:
                arcname = '%05d.py' % n
                doc._filepath = os.path.join('_@@', dirname, arcname)
                doc.setModified(True)
                LOG.info('dfp %s' % doc._filepath)
            else:
                LOG.info('DFP %s' % doc._filepath)

        self._writefile01(fp)

        for n in range(count):
            docid = str(mselect.itemData(n))
            doc = self.editor.documents[docid]
            if doc._filepath.startswith('_@@'):
                doc._filepath = None

    def _savestate(self):
        '''write out the files in the editor window, and keep the list
            of history entries.

        if configured to use a single file:
            All of this is packed up in to a zip
            file and given a .pyn filename ending.

        if configured for directory of files:
            The files will be saved in a separate directory.
            The directory will end in _pynd
            A .pyn file will also be saved indexing the contents and
                allowing the files to be easily re-loaded.

        '''

        settings = QtCore.QSettings()
        savesingle = settings.value('file/savesingle', True, bool)

        if self.writeable(self._filepath):
            if savesingle:
                self._writefile01(self._filepath)
            else:
                self._writedir(self._filepath)
        else:
            QtGui.QMessageBox.warning(self,
                                      'Save failed',
                                      '''Cannot write to selected file.''')
            self._filepath = None
            return False

        self._modified = False
        for tdoc in list(self.editor.documents.values()):
            tdoc.setModified(False)
        self.editor._modified = False
        self.show_modified_status()

        self.addrecentfile(self._filepath)

        if savesingle:
            self._verify_saved(self._filepath)

        return True

    def addrecentfile(self, fp):
        settings = QtCore.QSettings()
        recent = [fp]
        for n in range(settings.beginReadArray('recent')):
            settings.setArrayIndex(n)
            fname = settings.value('fname')
            if fname and fname not in recent:
                recent.append(fname)
        settings.endArray()

        recent = recent[:6]

        settings.beginWriteArray('recent')
        for n in range(len(recent)):
            settings.setArrayIndex(n)
            fpath = recent[n]
            settings.setValue('fname', fpath)
        settings.endArray()

    def save(self):
        '''call _savestate with current file name, or get a file name from
            the user and then call _savestate
        '''

        if self._filepath is None:
            return self.saveas()
        else:
            return self._savestate()

    def _make_related_dir(self, fp):
        fpd = self._related_dir(fp)
        if not os.path.exists(fpd):
            os.mkdir(fpd)
        elif os.path.exists(fpd) and not self.overwrite(fpd):
            return False
        elif os.listdir(fpd):
            shutil.rmtree(fpd)
            os.mkdir(fpd)

    def saveas(self):
        if self._fdir is None:
            fdir = os.path.abspath(os.path.curdir)
        else:
            fdir = self._fdir

        fp = str(QtGui.QFileDialog.getSaveFileName(self,
                                                   'Save As', fdir,
                                                   'Text files (*.pyn)'))

        if fp:
            settings = QtCore.QSettings()
            savesingle = settings.value('file/savesingle', True, bool)

            fp = self._correct_filename(fp)
            dirname, fname = os.path.split(fp)
            if not savesingle:
                self._make_related_dir(fp)

            self._filepath = fp
            self._fdir = dirname

        else:
            return False

        retval = self._savestate()

        if retval:
            fdir, fname = os.path.split(self._filepath)
            windowtitle = '%s [*] - Pen' % fname
            self.setWindowTitle(windowtitle)
            self.show_modified_status()

        return retval

    def overwrite(self, fname):
        '''ask the user if they want to overwrite an existing file
            or directory.

        '''
        ret = QtGui.QMessageBox.warning(
            self,
            self.tr('Overwrite?'),
            self.tr(
                "The Directory already exists:\n%s\n"
                "Do you want to delete it and all contents?" %
                fname),
            QtGui.QMessageBox.Yes | QtGui.QMessageBox.Default,
            QtGui.QMessageBox.No,
            QtGui.QMessageBox.Cancel | QtGui.QMessageBox.Escape)
        if ret == QtGui.QMessageBox.Yes:
            return True
        elif ret == QtGui.QMessageBox.Cancel:
            return False

    def writeable(self, fp, savesingle=None):
        'try to write to the given path. return True if sucessful.'
        try:
            fd = open(fp, 'w')
            fd.write('test')
            fd.close()
            os.remove(fp)
        except IOError:
            return False
        else:
            return True

        if savesingle is not None and savesingle:
            savesingle = True
        else:
            settings = QtCore.QSettings()
            savesingle = settings.value('file/savesingle', True, bool)

        if not savesingle:
            fpd = self._related_dir(fp)
            if not os.path.exists(fpd):
                return False
            fp = os.path.join(fpd, 'test')
            return self.writeable(fp, False)
        else:
            return True

    def open(self, fp=None):
        '''read in a previously written set of files,
            or a single python source file.

        If the file is a lone python source file, no further processing
            will occur. However, if the file has been loaded in pen
            previously (it is being loaded from a .pyn or a _pynd):

        Any documents that look like function or class definitions will
            be exec'd to load them in to the interpreter local namespace.
        Any current history will be lost and replaced with the
            history loaded from the file.
        '''
        if not self.maybe_save():
            return

        if self._fdir is None:
            fdir = os.path.abspath(os.path.curdir)
        else:
            fdir = self._fdir

        LOG.info('open at %s' % fdir)

        if fp is None:
            fp = str(
                QtGui.QFileDialog.getOpenFileName(
                    self,
                    'Open file',
                    fdir,
                    'Text files (*.pyn *.py)'))

        if fp:
            if not os.path.exists(fp):
                QtGui.QMessageBox.information(
                    self,
                    'Does not exist',
                    'File does not exist:\n\n%s' %
                    fp)
                return

            self._fdir, _ = os.path.split(fp)

            if not fp.endswith('.py'):
                self._new()
                self._filepath = fp

            self._openfile(fp)

    def _update_after_open(self, fp, add_to_recent=False):
        self.ui.mselect.setCurrentIndex(0)
        self.changedoc(0)

        self._modified = False
        _fdir, fname = os.path.split(fp)
        windowtitle = '%s [*] - Pen' % fname
        self.setWindowTitle(windowtitle)
        self.show_modified_status()

        if add_to_recent:
            self.addrecentfile(self._filepath)

    def _openfile(self, fp, add_to_recent=True, dump=False):
        '''Open the selected file.

        If the file is python source (.py) open the file and
            add it as a new page in the editor window.

        If the file is a pen archive (.pyn) open it and load
            its contents to the correct places.

            First determine which file format version is used in
            the file, then dispatch to the correct function.

        If dump=True, just prints out the various contents of the
            file to stdout if that is possible.

        '''
        if not os.path.exists(fp):
            QtGui.QMessageBox.information(self,
                                          'File not found',
                                          'File not found:\n\n%s' % fp)
            return

        if fp.endswith('.pyn'):
            z = zipfile.ZipFile(fp, 'r')
            infos = z.infolist()
            info = infos[0]

            if not info.comment:
                ok = self._openfile00(fp, dump)
            else:
                if info.comment == b'pyn01':
                    ok = self._openfile01(fp, dump)
                else:
                    QtGui.QMessageBox.information(
                        self,
                        'Unknown Format',
                        'Unknown file format:\n\n"%s"' %
                        info.comment)
                    return

        if fp.endswith('.py'):
            if not dump:
                doc = self.editor.addexternal(fp)
                if doc is not None:
                    self.addrecentfile(fp)
                    self._modified = True
                    self.show_modified_status()
                    self._addwatcher(fp, doc)
            else:
                txt = open(fp).read()
                print(txt)
                print()
        elif ok:
            self._update_after_open(fp, add_to_recent)

    def _addwatcher(self, fp, doc):
        self.watcher.addPath(fp)
        self._watchdocs[str(fp)] = doc

    def _remwatcher(self, fp):
        self.watcher.removePath(fp)

    def _filechanged(self, fp):
        '''called when an external file has changed on disk.
        '''
        LOG.info('_fc %s' % fp)

        settings = QtCore.QSettings()
        autorefresh = settings.value('file/reloadexternal', True, bool)
        if autorefresh:
            doc = self._watchdocs[str(fp)]
            if doc.isModified():
                QtGui.QMessageBox.information(
                    self,
                    'Modified',
                    'Local copy has modifications:\n\n%s\n\n'
                    'Not loading external changes.' % fp)
                return
            txt = open(fp).read()
            doc.setText(txt)
            doc.setModified(False)
            autorun = settings.value('file/autorun', False, bool)
            if autorun:
                self.interpreter.runcode(txt)

        self.show_modified_status()

    def _remove_toplevel(self, data):
        '''When a page has both function definitions and top-level
            code, we only want to exec the function defs and not
            the top-level code when loading the file.

            This function takes the page of code and will return
            only the function and class defs with all other
            top-level code stripped out.
        '''

        newdata = []

        indef = False
        for line in data.splitlines():
            indented = line.startswith(' ')
            blank = line.isspace()
            if not line or blank:
                pass
            elif not indented:
                if line.startswith('def ') or line.startswith('class '):
                    indef = True
                else:
                    indef = False

            if indef:
                newdata.append(line)

        return '\n'.join(newdata)

    def _loaddata(self, data):
        if hasattr(data, 'decode'):
            data = data.decode('utf-8')
        self.editor.add(data)
        if data.startswith('def ') or data.startswith('class '):
            if data[4:12] == 'onclick(':
                # don't install onclick handlers when loading
                pass
            else:
                try:
                    data = self._remove_toplevel(data)
                    LOG.info(data)
                    exec(data, self.interpreter_locals)
                except Exception as e:
                    print()
                    print('problem', e)
                    print('in...')
                    line1 = data.split('\n')[0]
                    print(str(line1))
                    self.interpretereditor.checkprompt()

    def _loadhistory(self, data):
        history = str(data).split('\n')
        self.interpretereditor.history = history

    def _shouldload00(self, ename):
        '''tries to load both original file format and any
            unknown format file.
        '''
        return ename.startswith('##')

    def _openfile00(self, fp, dump=False):
        'Used to open files from version < 0.10'
        z = zipfile.ZipFile(fp, 'r')
        for ename in z.namelist():
            fo = z.open(ename, 'rU')
            data = fo.read()
            data = data.decode('utf-8')

            if dump:
                print(ename)
                print(data)
                print()
            elif self._shouldload00(ename):
                self._loaddata(data)
            elif ename.startswith('@@history@@'):
                self._loadhistory(data)

        return True

    def _shouldload01(self, fp):
        'return true if _openfile01 should load the file contents'
        while '\\' in fp:
            fp = fp.replace('\\', '/')
        while '//' in fp:
            fp = fp.replace('//', '/')
        _edir, ename = os.path.split(fp)
        ok = len(ename) == 8 and \
            ename[:5].isdigit() and \
            ename.endswith('.py')
        LOG.info('SL %s %s' % (ok, fp))
        return ok

    def _openfile01(self, fp, dump=False):
        'used to open files in version 0.10 (file vers. pyn01)'
        fpd, _ = os.path.split(fp)
        z = zipfile.ZipFile(fp, 'r')
        namelist = z.namelist()
        LOG.info(namelist)

        hasmanifest = False
        hashistory = False
        for ename in namelist:
            LOG.info(ename)
            if '@@manifest@@' in ename:
                hasmanifest = ename
            elif '@@history@@' in ename:
                hashistory = ename

        if hasmanifest:
            fo = z.open(hasmanifest, 'rU')
            data = fo.read()
            data = data.decode('utf-8')
            manifest_namelist = data.split('\n')
            if manifest_namelist:
                # Try opening the entries to see if the
                #   manifest is well formed or broken
                broken = False
                for ename in manifest_namelist:
                    if ename.startswith('_@@'):
                        # external
                        continue
                    if '_pynd' not in ename:
                        # manifest or history
                        continue

                    LOG.info('Chk %s' % ename)

                    try:
                        fo = z.open(ename, 'rU')
                    except KeyError:
                        # broken manifest
                        LOG.info(
                            'Broken manifest %s %s' %
                            (ename, manifest_namelist))
                        namelist.sort()
                        broken = True
                        break

                if not broken:
                    # Looks ok. Use the manifest
                    namelist = manifest_namelist
                    if hashistory:
                        namelist.append(hashistory)

        else:
            namelist.sort()

        if dump:
            print('Manifest/files:')
            for name in namelist:
                print('  ', name)

        pages = 0
        for ename in namelist:
            LOG.info('loading %s' % ename)
            if dump:
                print('============================================')

            if ename.startswith('_@@'):
                # directory + .pyn style
                n = ename[4:]
                np = os.path.join(fpd, n)
                LOG.info('NP %s' % np)
                npd, _ = os.path.split(np)
                if not os.path.exists(npd):
                    QtGui.QMessageBox.information(self,
                                                  'Not found',
                                                  '''File does not exist:

%s

This file requires an associated directory of files:

%s

Move this file and that folder to the same place and
try opening it again.

''' % (np, npd))
                    self.new()
                    return False
                try:
                    fo = open(np, 'rU')
                except FileNotFoundError:
                    QtGui.QMessageBox.information(self,
                                                  'Not found',
                                                  '''File does not exist:

%s

Carrying on trying to recover if possible...

''' % np)

            elif os.path.isabs(ename):
                try:
                    self._openfile(ename, dump=dump)
                    pages += 1
                    continue
                except IOError:
                    self.editor.add('Could not load:\n%s' % ename)
                    self.editor._doc._title = 'NOT LOADED'
                    self.editor._doc._filepath = ename
                    self.editor.settitle('NOT LOADED')
                    continue
            else:
                fo = z.open(ename, 'rU')

            data = fo.read()
            LOG.info('OPEN')
            LOG.info(data)
            if hasattr(data, 'decode'):
                data = data.decode('utf-8')
            if dump:
                if '@@history@@' in ename:
                    print('Command history')
                print(data)
                print()
            elif self._shouldload01(ename):
                self._loaddata(data)
                pages += 1
            elif '@@history@@' in ename:
                self._loadhistory(data)

        if not pages:
            self.new()
        return True

    def _opendir(self, d):
        files = os.listdir(d)
        manifestname = '@@manifest@@'
        if manifestname in files:
            manifp = os.path.join(d, manifestname)
            maniff = open(manifp)
            manifest = maniff.read()
            files = manifest.split('\n')
            files = [os.path.join(d, f) for f in files if f]
        else:
            files.sort()

        for ename in files:
            fp = os.path.join(d, ename)
            fo = open(fp, 'rU')
            data = fo.read()
            data = data.decode('utf-8')
            if self._shouldload01(ename):
                self._loaddata(data)
            elif ename == '@@history@@':
                self._loadhistory(data)

        self._update_after_open(d)

    def _verify_saved(self, fp):
        '''verify that the saved file contains the correct data.'''
        z = zipfile.ZipFile(fp, 'r')
        for ename in z.namelist():
            fo = z.open(ename, 'rU')
            data = fo.read()
            data = data.decode('utf-8')
            if ename.startswith('##'):
                hdr = ename[0:9]
                if hdr.startswith('##') and hdr.endswith('##'):
                    docid = ename[11:]
                    if data != self.editor.documents[docid]:
                        QtGui.QMessageBox.warning(self,
                                                  'Unable to save',
                                                  'Files not saved!')
                        break

    def export(self):
        '''save the current drawing'''

        if self._fdir is None:
            fdir = os.path.abspath(os.path.curdir)
        else:
            fdir = self._fdir

        fp = str(QtGui.QFileDialog.getSaveFileName(self, 'Export Image', fdir))
        if fp:
            _root, ext = os.path.splitext(fp)
            if not ext:
                ext = '.png'
                fp += ext
            self._fdir, _ = os.path.split(fp)
        else:
            return False

        for pen in self.user_pens:
            pen.drawable.hide()

        scene = self.scene
        ibr = scene.itemsBoundingRect()

        tl = ibr.topLeft()
        tlx, tly = tl.x(), tl.y()
        tlx -= 20
        tly -= 20
        tlp = QtCore.QPointF(tlx, tly)
        ibr.setTopLeft(tlp)

        br = ibr.bottomRight()
        brx, bry = br.x(), br.y()
        brx += 20
        bry += 20
        brp = QtCore.QPointF(brx, bry)
        ibr.setBottomRight(brp)

        scene.setSceneRect(scene.sceneRect().united(ibr))

        src = scene.sceneRect()

        if ext == '.svg':
            self.export_svg(fp, src)
        else:
            self.export_bitmap(fp, src)

        for pen in self.user_pens:
            pen.drawable.show()

    def export_svg(self, fp, src):
        from PyQt4 import QtSvg

        svgen = QtSvg.QSvgGenerator()
        svgen.setFileName(fp)
        svgen.setSize(src.size().toSize())
        svgen.setTitle('Pen')
        painter = QtGui.QPainter(svgen)
        self.scene.render(painter)
        painter.end()

    def export_bitmap(self, fp, src):
        '''For .png .jpg or .tga'''

        sz = src.size().toSize()
        self._i = i = QtGui.QImage(sz, QtGui.QImage.Format_ARGB32)
        p = QtGui.QPainter(i)
        irf = QtCore.QRectF(0, 0, src.width(), src.height())

        self.scene.render(p, irf, src)
        if not i.save(fp):
            _root, fn = os.path.split(fp)
            fnroot, ext = os.path.splitext(fn)
            if ext not in ('.png', '.jpg', '.jpeg', '.tga'):
                msg = 'Unsupported format.\n\nTry using %s.png' % fnroot
            else:
                msg = 'Cannot export image.'
            QtGui.QMessageBox.warning(self,
                                      'Unable to save',
                                      msg)

    def newdoc(self):
        '''Add a new (blank) page to the document editor'''

        docid = self.editor.new()
        self.editor.switchto(docid)
        self.editor._doc.setFocus()
        idx = self.ui.mselect.count() - 1
        self.ui.mselect.setCurrentIndex(idx)

        self._modified = True
        self.show_modified_status()

    def changedoc(self, idx):
        '''switch which document is visible in the document editor'''

        docid = str(self.ui.mselect.itemData(idx))
        if docid in self.editor.documents:
            self.editor.switchto(docid)
            self.editor._doc.setFocus()

    def removedoc(self):
        '''throw away the currently displayed editor document'''

        mselect = self.ui.mselect
        documents = self.editor.documents
        idx = mselect.currentIndex()
        docid = str(mselect.itemData(idx))
        doc = documents[docid]
        empty = not doc.text()

        if hasattr(self.editor._doc, '_title'):
            external = True
            fp = self.editor._doc._filepath
        else:
            external = False

        modified = doc.isModified()

        if not modified and empty:
            affirm = True
        elif external and not modified:
            affirm = True
        else:
            ret = QtGui.QMessageBox.warning(
                self,
                'Are you sure?',
                'This page will be removed permanently.\n'
                'Are you sure you want to remove this page?',
                QtGui.QMessageBox.Yes | QtGui.QMessageBox.Default,
                QtGui.QMessageBox.No,
                QtGui.QMessageBox.Cancel | QtGui.QMessageBox.Escape)
            affirm = ret == QtGui.QMessageBox.Yes

        if not affirm:
            return
        else:
            mselect = self.ui.mselect
            idx = mselect.currentIndex()
            mselect.removeItem(idx)
            if mselect.count():
                self.changedoc(0)
                mselect.setCurrentIndex(0)
            else:
                self.editor._doc.setText('')
                self.newdoc()

            if docid in self.editor.documents:
                doc = self.editor.documents[docid]
                del self.editor.documents[docid]

            self._modified = True
            self.show_modified_status()

            if external:
                self._remwatcher(fp)

    def nextdoc(self):
        self.editor.shownext()

    def prevdoc(self):
        self.editor.showprev()

    def toggle_editor(self):
        if self.interpretereditor.hasFocus():
            self.editor.setFocus()
        else:
            self.interpretereditor.setFocus()

    def findmain(self, code):
        '''returns information about the main function or class in
            the given code.

        "Main" will depend on the settings and will either be the first
            function or class defined on the page, or the last one.

        returns a dictionary of:
            kind: 'function', 'class'
            name: function or class name
            params: string containing all parameters
            nodefault: list of params that do not have a default value
        '''

        settings = QtCore.QSettings()
        mainfirst = settings.value('editor/mainfirst', True, bool)
        lines = code.split('\n')
        if not mainfirst:
            lines.reverse()
        for line in lines:
            firstparen = line.find('(')
            lastparen = line.rfind(')')
            if line.startswith('def ') and line.endswith(':'):
                kind = 'function'
                name = line[4:firstparen]
            elif line.startswith('class ') and line.endswith(':'):
                kind = 'class'
                name = line[6:firstparen]
            else:
                continue

            if kind == 'function' and firstparen > -1 and lastparen > -1:
                params = line[firstparen + 1:lastparen]
                func = self.interpreter_locals.get(name, None)
                nodefault = []
                if func is not None:
                    defaults = plist(func)
                    if defaults:
                        for param, d in defaults:
                            if d is NODEFAULT:
                                nodefault.append(param)
            elif kind == 'class':
                c = self.interpreter_locals.get(name, None)
                nodefault = []
                params = ''
                if c is not None:
                    func = getattr(c, '__init__', None)
                    if func is not None:
                        defaults = plist(func)
                        if defaults:
                            del defaults[0]  # self
                            count = len(defaults)
                            for i, (param, d) in enumerate(defaults):
                                params += param
                                if d is NODEFAULT:
                                    nodefault.append(param)
                                else:
                                    params += '=%s' % str(d)
                                if i < count - 1:
                                    params += ', '

            return (kind, name, params, nodefault)

        return None, None, None, None

    def testcode(self):
        '''Activated by the Test/Run button (testrun)

            exec the code in the current editor window and load it in
            to the interpreter local namespace

            If the first line looks like a function definition, use
            it to feed a line to the interpreter set up to call the
            function.
        '''
        doc = self.editor._doc
        code = doc.cleancode()
        error = None

        try:
            compile(code, 'current file', 'exec')
        except SyntaxError as e:
            self.editor.selectline(e.lineno)
            self.interpretereditor.clearline()
            self.interpretereditor.write(
                'Syntax Error in line %s\n' %
                e.lineno)
            self.interpretereditor.write('>>> ')
            self.editor.setFocus()
            error = 1
        else:
            self.interpretereditor.setFocus()
            if self.interpretereditor.cmdthread is None:
                self.interpretereditor.cmdthread = CmdThread(
                    self.interpretereditor,
                    code)
                cmdthread = self.interpretereditor.cmdthread
                cmdthread.start()
                self.watcherthread = WatcherThread(cmdthread)
                self.watcherthread.finished.connect(
                    self.interpretereditor.testthreaddone)
                self.watcherthread.start()

                kind, name, params, _nodefault = self.findmain(code)
                if kind is not None:
                    self.interpretereditor.clearline()
                    if kind == 'function':
                        tocall = '%s(%s)' % (name, params)
                    elif kind == 'class':
                        varname = name.lower()
                        if varname == name:
                            self.interpretereditor.write(
                                '# Class names should be capitalized \n')
                            self.interpretereditor.write('>>> ')
                            varname = varname[0]
                        tocall = '%s = %s(%s)' % (varname, name, params)

                    if kind == 'function' and name == 'onclick':
                        self.interpretereditor.write('# set onclick handler\n')
                        self.interpretereditor.write('>>> ')
                    else:
                        self.interpretereditor.addcmd(tocall, force=True)
                else:
                    self.interpretereditor.write('\n')
            else:
                self.interpretereditor.write('not starting...\n')
                self.interpretereditor.write('code already running\n')

        self.interpretereditor.setFocus()
        return error

    def testall(self):
        '''Test/Run each editor page in order.

        If any page throws an error, progress stops, the editor
        switches to that page and highlights the error.
        '''

        ie = self.interpretereditor
        if ie.cmdthread is not None:
            ie.write('not starting...2\n')
            ie.write('code already running\n')
            return

        settings = QtCore.QSettings()
        rev = settings.value('editor/testall_reverse', False, bool)
        autorun = settings.value('editor/testall_autocall', False, bool)
        reset = settings.value('editor/testrun_reset', True, bool)

        count = self.ui.mselect.count()
        Pen._stop_testall = False
        for i in range(count):
            if Pen._stop_testall:
                break

            if not rev:
                idx = i
            else:
                idx = count - i - 1
            docid = str(self.ui.mselect.itemData(idx))
            if docid in self.editor.documents:
                while ie.cmdthread is not None:
                    ie.spin(5)
                    if Pen._stop_testall:
                        break
                    Pen.wait_for_empty_q()
                    if self.pen.ControlC:
                        Pen._stop_testall = True
                        break
                self.editor.switchto(docid)
                self.editor.setFocus()
                if reset and not Pen._stop_testall:
                    ie.checkprompt()
                    ie.spin(5)
                    ie.addcmd('reset()')
                    ie.spin(5)
                    ie.go()

                while ie.cmdthread is not None:
                    ie.spin(5)
                    if Pen._stop_testall:
                        break
                    Pen.wait_for_empty_q()
                    if self.pen.ControlC:
                        Pen._stop_testall = True
                        break

                if Pen._stop_testall:
                    ie.clearline()
                    ie.write('Stopped\n')
                    ie.spin(5)
                    ie.checkprompt()
                    ie.setFocus()
                    break

                ie.clearline()
                ie.spin(5, delay=0.1)
                if self.testcode():
                    break
                ie.spin(5, delay=0.1)

                if autorun:
                    doc = self.editor.documents[docid]
                    code = doc.cleancode()
                    _kind, _name, _params, nodefault = self.findmain(code)
                    missing_vars = []
                    if nodefault:
                        for var in nodefault:
                            if var not in self.interpreter_locals:
                                missing_vars.append(var)

                    if missing_vars:
                        ie.write('\n>>> ')
                        for var in missing_vars:
                            ie.write('# missing %s \n' % var)
                            ie.write('>>> ')
                        ie.spin(5)

                    elif not Pen._stop_testall:
                        ie.go()
                        LOG.info('GO')
                        Pen.wait_for_empty_q()
                        LOG.info('END WAIT')

        ie.clearline()

    def setPenColor(self):
        '''use a color selection dialog to set the pen line color

        sets the color for the primary pen only. For other later
            added user_pens, use p.color()
        '''
        icolor = self.pen.drawable.pen.brush().color()
        ncolor = QtGui.QColorDialog.getColor(
            icolor,
            self,
            'Pen Color',
            QtGui.QColorDialog.ShowAlphaChannel)
        if ncolor.isValid():
            r, g, b, a = ncolor.getRgb()
            self.pen.color(r, g, b, a)
            if a != 255:
                cmd = 'color(%s, %s, %s, %s)\n' % (r, g, b, a)
            else:
                cmd = 'color(%s, %s, %s)\n' % (r, g, b)
            self.interpretereditor.addcmd(cmd)

    def set_background_color(self):
        '''Use color selection dialog to set the background color.
        '''

        r, g, b = self.pen.bgcolor()
        c = QtGui.QColor(r, g, b)
        ncolor = QtGui.QColorDialog.getColor(c, self)
        if ncolor.isValid():
            r, g, b, _ = ncolor.getRgb()
            self.pen.bgcolor(r, g, b)
            cmd = 'bgcolor(%s, %s, %s)\n' % (r, g, b)
            self.interpretereditor.addcmd(cmd)

    def setPenWidth(self):
        '''open a dialog with a spin button to get a new pen line width

        sets the width for the primary pen only. For other later
            added user_pens, use p.width()
        '''
        iwidth = self.pen.drawable.pen.width()
        uifile = 'penwidth.ui'
        uipath = os.path.join(UI_FILES_PATH, uifile)
        DClass, _ = uic.loadUiType(uipath)
        dc = DClass()
        d = QtGui.QDialog(self)
        d.ui = DClass()
        dc.setupUi(d)
        dc.thewid.setValue(iwidth)
        d.exec_()
        nwidth = dc.thewid.value()
        self.pen.width(nwidth)
        cmd = 'width(%s)\n' % nwidth
        self.interpretereditor.addcmd(cmd)

    def _sync_pendown_menu(self, choice):
        action = self._pendowns.inv.get(choice)
        action.setChecked(True)

    def setPen(self, ev):
        '''toggle pen up and pen down

        sets the pen for the primary pen only. For other later
            added user_pens, use p.penup() or p.pendown()
        '''
        if ev == self.ui.actionPenUp:
            self.pen.penup()
            self.interpretereditor.addcmd('penup()\n')
        else:
            self.pen.pendown()
            self.interpretereditor.addcmd('pendown()\n')

    def _sync_fill_menu(self, choice):
        action = self._fills.inv.get(str(choice))
        action.setChecked(True)

    def setFill(self, ev):
        '''toggle fill on / off

        sets the fill for the primary pen only. For other later
            added user_pens, use p.fill() or p.nofill()
        '''
        if ev == self.ui.actionFill:
            self.pen.fill()
            self.interpretereditor.addcmd('fill()\n')
        else:
            self.pen.nofill()
            self.interpretereditor.addcmd('nofill()\n')

    def setFillColor(self):
        '''use a color selection dialog to set the fill color

        sets the fill color for the primary pen only. For other
            later added user_pens, use p.fillcolor()
        '''
        icolor = self.pen.drawable.brush.color()
        ncolor = QtGui.QColorDialog.getColor(
            icolor,
            self,
            'Fill Color',
            QtGui.QColorDialog.ShowAlphaChannel)
        if ncolor.isValid():
            r, g, b, a = ncolor.getRgb()
            self.pen.fill()
            self._sync_fill_menu('fill')
            self.pen.fillcolor(r, g, b, a)
            if a != 255:
                cmd = 'fill(color=(%s, %s, %s, %s))\n' % (r, g, b, a)
            else:
                cmd = 'fill(color=(%s, %s, %s))\n' % (r, g, b)
            self.interpretereditor.addcmd(cmd)

    def makedeleteaction(self):
        def deleteaction(pt, self=self):
            popup = QtGui.QMenu(self)
            custommenu = self.ui.menuCustom
            action = custommenu.actionAt(pt)

            def dodelete(action=action, menu=custommenu):
                menu.removeAction(action)
                idpath = self.avatars[action]
                self._save_custom_avatar(idpath, remove=True)
            popup.addAction('Remove', dodelete)
            popup.exec_(custommenu.mapToGlobal(pt))
        return deleteaction

    def set_pen_avatar(self, imageid, pen=None):
        '''select which image to show

        sets the image for the primary pen only. For other later
            added user_pens, use p.avatar()
        '''

        if pen is None:
            pen = self.pen
            sync = None
        else:
            sync = False

        idpath = str(imageid)
        if idpath.startswith('@@_'):
            # custom svg
            imageid, filepath = idpath[3:].split('@@')
            imid = imageid
        elif idpath.startswith('@@'):
            # custom non-svg
            imageid, filepath = idpath[2:].split('@@')
            imid = None
        else:
            imid = imageid
            filepath = None
        pen.avatar(imid, filepath)
        if sync:
            self._sync_avatar_menu(imageid, filepath)

        if not imid:
            imid = None
            cmdstr = "avatar(%s, '%s')\n"
            cmd = cmdstr % (imid, filepath)
        elif filepath is None:
            cmdstr = "avatar('%s')\n"
            cmd = cmdstr % imid
        else:
            cmdstr = "avatar('%s', '%s')\n"
            cmd = cmdstr % (imid, filepath)
        return cmd

    def setImageEvent(self, ev):
        imageid = self.avatars[ev]
        cmd = self.set_pen_avatar(imageid)
        self.interpretereditor.addcmd(cmd)

    def setcustomavatar(self):
        from . import avatar
        ad = avatar.CustomAvatar(self)
        r = ad.exec_()
        if r:
            filepath = str(ad.ui.filepath.text())
            element = str(ad.ui.element.text())
            if not element:
                element = None
            self.pen.avatar(element, filepath)

    def sync_speed_menu(self, speed_value):
        action = self.speeds.inv.get(speed_value)
        if action is not None:
            action.setChecked(True)

    def speedMenuEvent(self, ev=None):
        if ev is None:
            ev = self.speedgroup.checkedAction()

        speed = self.speeds[ev]
        self.sync_speed_menu(speed)
        choices = {5: 'slow',
                   10: 'medium',
                   20: 'fast',
                   0: 'instant'}

        if self.interpretereditor.cmdthread is not None:
            self.pen._speed(speed)

        choice = choices.get(speed)
        cmd = "speed('%s')\n" % choice
        self.interpretereditor.addcmd(cmd)
        self.pen.speed(choice)

    def wordwrap(self):
        checked = self.ui.actionWordwrap.isChecked()
        if not checked:
            self.editor.wrap(False)
        else:
            self.editor.wrap()
        settings = QtCore.QSettings()
        settings.setValue('editor/wordwrap', checked)

    def linenumbers(self):
        checked = self.ui.actionShowLineNumbers.isChecked()
        if checked:
            self.editor.line_numbers(True)
        else:
            self.editor.line_numbers(False)
        settings = QtCore.QSettings()
        settings.setValue('editor/linenumbers', checked)

    def zoomineditor(self):
        print(self.editor)
        self.editor.zoomin()

    def zoomouteditor(self):
        print(self.editor)
        self.editor.zoomout()

    def comment(self):
        self.editor._doc.commentlines()

    def uncomment(self):
        self.editor._doc.commentlines(un=True)

    def about(self):
        AboutDialog(self.app).exec_()

    def reportbug(self):
        QtGui.QDesktopServices().openUrl(QtCore.QUrl(BUG_URL))

    def resizeEvent(self, ev):
        scene = self.scene
        size = ev.size()
        wnew, hnew = size.width(), size.height()
        rect = scene.sceneRect()
        wr, hr = rect.width(), rect.height()

        if wnew > wr or hnew > hr:
            w = max(wr, wnew)
            h = max(hr, hnew)
            w2, h2 = w / 2, h / 2
            scene.setSceneRect(-w2, -h2, w, h)

    def undo(self):
        self.pen._undo()
