'''Pens that draw elements on screen.'''

import queue
import time
import random
import string
import tugalib
from threading import Lock
from math import atan2, degrees, radians, hypot, cos, sin, pi
from PyQt4 import QtCore, QtGui, QtSvg
from tugalinhas import LOG, NOTHING
from tugalinhas import DEFAULT_BGCOLOR, DEFAULT_COLOR, DEFAULT_FILLCOLOR
from tugalinhas.util import sign, choose_color, TooManyPens, docfrom
from tugalinhas.util import Vec2D, as_qpoint

#
# Module constants
#
TURTLE_FUNCTIONS = [
    # Relative movement
    'forward', 'fd',
    'backward', 'bk', 'back',
    'left', 'lt',
    'right', 'rt',
    'frente', 'trás', 'direita', 'esquerda',

    # Absolute movement
    'goto', 'setpos', 'setposition',
    'setheading', 'seth',
    'setx', 'sety',
    'home',
    'ir_para', 'mudar_orientação', 'mudar_x', 'mudar_y', 'começo',

    # Return state
    'position', 'pos',
    'towards', 'distance',
    'xcor', 'ycor', '_heading',
    'posição', 'ângulo_para', 'distância_para',
    'coordenada_x', 'coordenada_y', 'orientação',

    # Drawing state
    'pendown', 'pd', 'down',
    'penup', 'pu', 'up',
    'pensize', 'width',
    'pen', 'isdown',
    'abaixa', 'levanta', 'espessura', 'mudar_espessura', 'está_abaixada',


    # From python's turtle module
    # circle()
    # dot()
    # stamp()
    # clearstamp()
    # clearstamps()
    # undo()
    # speed()

    # Setting and measurement
    # degrees()
    # radians()

    # Color control
    # color()
    # pencolor()
    # fillcolor()
    # Filling
    # filling()
    # begin_fill()
    # end_fill()

    # More drawing control
    # reset()
    # clear()
    # write()

    # Turtle state
    # Visibility
    # showturtle() | st()
    # hideturtle() | ht()
    # isvisible()
    # Appearance
    # shape()
    # resizemode()
    # shapesize() | turtlesize()
    # shearfactor()
    # settiltangle()
    # tiltangle()
    # tilt()
    # shapetransform()
    # get_shapepoly()
    # Using events
    # onclick()
    # onrelease()
    # ondrag()
    # Special Turtle methods
    # begin_poly()
    # end_poly()
    # get_poly()
    # clone()
    # getturtle() | getpen()
    # getscreen()
    # setundobuffer()
    # undobufferentries()


    # From pynguin
    #    'color',
    #    'circle', 'arc', 'fill', 'nofill', 'fillcolor',
    #    'clear',
    #    'write',
    #    'onscreen', 'viewcoords', 'stamp', 'square',
    #    'avatar', 'remove', 'promote', 'reap', 'font',
    #    'speed', 'track', 'notrack', 'bgcolor', 'mode', 'colorat',
]

TUGALIB_FUNCTIONS = {k: v for (k, v) in vars(tugalib).items()
                     if not k.startswith('_')}
PI = pi

INTERPRETER_PROTECT = [
    'pen', 'user_pens', 'PI', 'history', 'util', 'log']


class PenState(object):

    '''Used to track the "real" state of the pen (as opposed
        to the visible state which may be delayed for animation
        at slower speeds)

        PenState uses the same API as GraphicsItem
    '''

    def __init__(self):
        self.setPos(QtCore.QPointF(0, 0))
        self.is_down = True
        self.angle = 0
        self.color = (255, 255, 255)
        self.fillcolor = (100, 220, 110)
        self.penwidth = 2

    def pos(self):
        return self._pos

    def setPos(self, pos):
        self._pos = pos

    def set_transform(self):
        pass

    def rotate(self, deg):
        'turn clockwise from current angle by deg degrees'
        self.angle += deg


class Drawable(QtGui.QGraphicsItem):

    def __init__(self, renderer, imageid, pen):
        super().__init__(parent=None)
        self.is_down = True
        self.angle = 0
        self.scale = scale = 0.20
        self.position = QtCore.QPointF(125 * scale, 125 * scale)
        self.renderer = renderer

        self.pen = pen
        self.setImageid(imageid)
        self.label_item = None  # label item
        self.set_transform()

        self.qpen = QtGui.QPen(QtCore.Qt.black)
        self.qpen.setWidth(2)

        self.brush = QtGui.QBrush(QtGui.QColor(100, 220, 110))
        self.ready = False
        self.fillmode = False
        self.fillrule = QtCore.Qt.WindingFill
        self.notrack = False  # set when dragging to prevent crash

    def paint(self, *args):
        '''Do-nothing override'''

    def setlabel(self, text):
        if self.label_item is not None:
            self.label_item._settext(text)
        else:
            self.label_item = PenLabelItem(self)
            scene = self.scene()
            scene.addItem(self.label_item)
            self.label_item._settext(text)
        self.set_transform()

    def setPos(self, pos):
        if isinstance(pos, QtCore.QPointF):
            super().setPos(pos)
        else:
            super().setPos(*pos)
        self.set_transform()
        self.expand(pos)
        self.track()

    def expand(self, pos=None):
        '''Check if the scene needs to expand for the drawn items.

        pass in pos=None to check all drawn items even if it is
            likely that the current position would not cause a
            need to expand the scene. (Used currently for the
            quick-draw circle which never actually moves the
            pen, but which may add a circle that needs to
            expand the scene rect).
        '''
        scene = self.scene()
        if scene is not None:
            scenerect = scene.sceneRect()
            if pos is None or not scenerect.contains(as_qpoint(pos)):
                itemrect = scene.itemsBoundingRect()
                newrect = itemrect.united(scenerect)
                scene.setSceneRect(newrect)

    def track(self):
        'center the view on the pen'

        if Pen._track_pen and not self.notrack:
            pen = self.pen
            trackpen = Pen._track_pen
            scene = self.scene()
            if pen is trackpen and scene is not None:
                scene.view.ensureVisible(self)
                pen.main_window._centerview()

    def set_transform(self):
        cpt = self.position
        cx, cy = cpt.x(), cpt.y()

        angle = self.angle

        trans = QtGui.QTransform()
        trans.translate(-cx, -cy)
        trans.translate(cx, cy).rotate(angle).translate(-cx, -cy)
        trans.scale(self.scale, self.scale)

        if self.label_item is not None:
            self.label_item.set_transform()

        self.setTransform(trans)

    def rotate(self, deg):
        'turn clockwise from current angle by deg degrees'

        self.angle += deg
        self.set_transform()

    def setImageid(self, imageid):
        self.imageid = imageid
        if imageid is not None:
            self.item = QtSvg.QGraphicsSvgItem(self)
            self.item.setSharedRenderer(self.renderer)
            self.item.setElementId(imageid)
            irect = self.renderer.boundsOnElement(imageid)
            w, h = irect.width(), irect.height()
            ws, hs = w * self.scale, h * self.scale
            self.position = QtCore.QPointF(ws / 2, hs / 2)
        else:
            # non-svg image
            self.item = QtGui.QGraphicsPixmapItem(self.renderer, self)

    def boundingRect(self):
        return self.item.boundingRect()

    def mousePressEvent(self, ev):
        button = ev.button()
        if button == QtCore.Qt.LeftButton:
            ev.accept()

    def mouseMoveEvent(self, ev):
        buttons = ev.buttons()
        if buttons & QtCore.Qt.LeftButton:
            ev.accept()

            pen = self.pen
            if pen is not None:
                self.notrack = True
                pos = ev.lastScenePos()
                x, y = pos.x(), pos.y()
                pen._goto(pen.state, (x, y))
                pen._goto(self, (x, y))
                self.notrack = False

                user_pens = pen.main_window.user_pens
                all_pens = pen.main_window.all_pens
                if pen not in user_pens and pen._is_helper not in user_pens:
                    # There is a visible pen onscreen which the user
                    # has grabbed and moved, but that pen is not in
                    # the pen list for some reason. Add it back in.
                    user_pens.append(self.pen)

                if pen not in all_pens and pen._is_helper not in all_pens:
                    all_pens.append(pen)

    def mouseReleaseEvent(self, ev):
        self.track()


class PenLabelItem(QtGui.QGraphicsTextItem):

    def __init__(self, parent):
        self.parent = parent
        offx, offy = 0, 40
        scale = 5.0
        offxs, offys = offx * scale, offy * scale
        offpt = QtCore.QPointF(offxs, offys)
        self.offpt = offpt
        self.scale = scale
        self._text = ''
        self._zvalue = 99999

        QtGui.QGraphicsTextItem.__init__(self, parent)

        self._setup()
        self.set_transform()

    def _setup(self):
        self._settext('')
        self.setZValue(self._zvalue)

    def _settext(self, text):
        self._text = text
        self.setPlainText(text)
        self.setZValue(self._zvalue)
        br = self.boundingRect()
        self.position = br.center()
        pcpt = self.parent.position
        px, py = pcpt.x(), pcpt.y()
        self.setTransformOriginPoint(-px, -py)

    def set_transform(self):
        pcpt = self.parent.position
        pcx, pcy = pcpt.x(), pcpt.y()
        offpt = self.offpt
        offx, offy = offpt.x(), offpt.y()
        cpt = self.position
        cx, cy = cpt.x(), cpt.y()
        ang = self.parent.angle
        trans = QtGui.QTransform()
        pscale = self.parent.scale
        pscale1 = 1 / pscale
        trans.translate(pscale1 * pcx, pscale1 * pcy)
        trans.rotate(-ang)
        scale = self.scale
        trans.translate(-scale * cx, -scale * cy)
        trans.translate(offx, offy)
        trans.scale(self.scale, self.scale)
        self.setTransform(trans)


class QQ(object):
    # FIXME: what is this?

    class QQDelaying(Exception):
        pass

    def __init__(self):
        self._queues = {}
        self.all_pens = []
        self.nq = 0
        self.qq = 0
        self._lock = Lock()

    def append(self, pen, q):
        if pen in self.all_pens:
            raise RuntimeError
        self.all_pens.append(pen)
        self._queues[pen] = q
        self.nq += 1

    def remove(self, pen):
        if pen in self._queues:
            del self._queues[pen]
            self.all_pens.remove(pen)
            self.nq = len(self._queues)
        self.qq = 0

    def get(self):
        if not self.nq:
            raise queue.Empty

        qq0 = self.qq
        delaying = 0
        while True:
            pen = self.all_pens[self.qq]
            penqq = self.qq

            self.qq += 1
            if self.qq >= self.nq:
                self.qq = 0

            if pen._delaying is not None:
                if pen.drawspeed == 0:
                    pen._delaying = None
                    self.qq = penqq
                    continue
                else:
                    delaying += 1
                    pen._delaying -= self.nq
                    if pen._delaying <= 0:
                        pen._delaying = None

            else:
                try:
                    q = self._queues.get(pen)
                    if q is not None:
                        mv = q.get(block=False)
                    else:
                        self.remove(pen)
                        qq0 = 0
                        continue
                except queue.Empty:
                    pass
                else:
                    return mv

            if self.qq == qq0:
                if delaying:
                    raise self.QQDelaying
                else:
                    raise queue.Empty

    def clear(self, lock):
        self._lock.acquire()

        for pen in self.all_pens:
            pen._delaying = None

            q = self._queues.get(pen)
            if q is None:
                continue
            while True:
                try:
                    q.get(block=False)
                    if not lock:
                        all_events = QtCore.QEventLoop.AllEvents
                        QtGui.QApplication.processEvents(all_events)
                except queue.Empty:
                    break

        self._lock.release()

    def qqsize(self):
        sz = 0
        for _pen, q in self._queues.items():
            sz += q.qsize()
        return sz


class Pen(object):

    class Defunct(Exception):
        pass

    ControlC = False
    _stop_testall = False

    delay = 0
    _throttledown = 0

    _all_moves = QQ()
    _checktime = QtCore.QTime()
    _checktime.start()

    _drawspeed_pending = None
    _turnspeed_pending = None
    drawspeed = 0
    turnspeed = 0

    _zvalue = 0

    _name = ''

    main_window = None  # set by MainWindow before any Pen get instantiated
    renderer = None  # set by MainWindow before any Pen get instantiated

    _track_main_pen = None  # set up by main_window.setup_settings
    _track_pen = None

    _modename = 'pen'

    defunct = False

    _delaying = None
    _wfi = None

    _font = QtGui.QFont('Arial', 22)

    def _log(self, *args):
        LOG.info(' '.join(map(str, args)))

    def __init__(self, pos=None, ang=None, helper_for=False):
        '''helper_for not False means this pen is being used by one
            of the alternate modes in mode.py

            _is_helper should be a link to the pen this one
                is a helper for.

        '''

        self._moves = queue.Queue(0)  # max number of items in queue
        self._all_moves.append(self, self._moves)

        if pos is None:
            pos = (0, 0)
        if ang is None:
            ang = 0
        self._is_helper = helper_for

        self.scene = self.main_window.scene
        self.state = PenState()  # real location, angle, etc.
        self.drawable = None  # Gets set up later in the main thread
        self.drawn_items = []
        self._undo_markers = []
        self._setup()
        self._init_move(pos, ang)

    #
    # Properties and attributes
    #
    @property
    def angle(self):
        return self.state.angle

    @angle.setter
    def angle(self, ang):
        self.turnto(ang)

    #
    # Magic methods
    #
    def __lt__(self, other):
        return self._zvalue < other._zvalue

    #
    # Pen utility functions
    #
    def _setup(self):
        if not self._is_helper:
            self.main_window.user_pens.append(self)

            # enforce maximum of 150 user_pens
            npen = len(self.main_window.user_pens)
            if npen > 150:
                self.main_window.user_pens.remove(self)
                raise TooManyPens('Exceeded maximum of 150 user_pens.')

        if self.main_window.pen is None:
            # self._log('_setup no main_window.pen')
            self._gitem_setup()

        else:
            # self._log('queue_command _gitem_setup')
            self.queue_command(self._gitem_setup)

            cc = 0
            while self.drawable is None or not self.drawable.ready:
                self.wait(0.01)
                if self.ControlC:
                    raise KeyboardInterrupt
                elif cc >= 50:
                    # self._log('_setup timeout')
                    self._gitem_setup()
                cc += 1

    def _init_move(self, pos, angle):
        x, y = pos
        self.setheading(angle)
        self.goto(x, y)

        settings = QtCore.QSettings()
        speed = settings.value('pen/speed', 'fast')
        self.speed(speed)

        self._set_color_to_default()
        self._set_fillcolor_to_default()

        self.pendown()
        self.fillrule('winding')

    def _remove(self, pen):
        pen.defunct = True
        self._all_moves.remove(pen)

        if pen is self:
            self._clear()
        else:
            self.drawn_items.extend(pen.drawn_items)
            pen.drawn_items = []

        pen._setImageid('hidden', sync=False)
        if pen.drawable is not None:
            self._gitem_setlabel('')
            scene = pen.drawable.scene()
            scene.removeItem(pen.drawable)
        pen.old_drawable = pen.drawable
        pen.drawable = None

        if pen in self.main_window.all_pens:
            self.main_window.all_pens.remove(pen)

    #
    # Helper functions
    #
    # FIXME: sort these functions in the proper places ########################
    def remove(self, pen=None):
        '''take the given pen (or this one if none specified)
            out of the scene.

        If removing a different pen from this one, this one will
            adopt all of the drawn items from the other pen. In
            other words, items drawn by the pen that is being
            removed will not be cleared immediately, but can later
            be cleared by this pen.

        If this pen is removing itself, it will first clear all
            of its own drawings, otherwise there will be no way to
            clear them out later.
        '''

        if pen is None:
            pen = self

        self.main_window.defunct_pens.append(pen)
        if pen in self.main_window.user_pens:
            self.main_window.user_pens.remove(pen)

        self._log('rmv', pen)
        if hasattr(pen, '_pen'):
            self._log('plus')
            self.remove(pen._pen)
        pen.waitforit()

        if pen is self.main_window.pen:
            if self.main_window.user_pens:
                # need to promote another pen to be the main one
                mainpen = self.main_window.user_pens[0]
            else:
                # nobody left ... create a new one
                mname = pen._modename
                mainpen = self.main_window.new_pen(mname, show_cmd=False)
            self.main_window.pen = mainpen
            self.main_window.setup_interpreter_locals()

        self.queue_command(self._remove, (pen,))

    def reap(self):
        '''Promote self to be main pen and remove all other cursors,
        taking charge of their drawings.
        '''
        if self is not self.main_window.pen:
            self.promote(self)
            # self.waitforit()

        pens = self.main_window.user_pens
        pens.remove(self)
        while pens:
            pen = pens.pop()
            self.remove(pen)
            # self.waitforit()
        pens.append(self)

        self.queue_command(self._clear_defunct_pens_later)

    def _promote(self, pen):
        self.main_window.pen = pen
        self.main_window.setup_interpreter_locals()

    def promote(self, pen=None):
        '''make the given pen the main pen, and update the
            console locals to make the new main user_pens method the
            built-in commands.
        '''
        if pen is None:
            pen = self
        self.queue_command(self._promote, (pen,))
        self.main_window.setup_interpreter_locals(pen)
        self.waitforit()

    def _gitem_setup(self):
        self.drawable = Drawable(self.renderer, 'pen', self)  # display only
        self._imageid = 'pen'
        self.scene.addItem(self.drawable)
        Pen._zvalue += 1
        self.drawable.setZValue(9999999 - self._zvalue)
        self.drawable._current_line = None

        if not self._is_helper:
            self.main_window.all_pens.append(self)
        self.drawable.ready = True

    def _set_item_pos(self, item, pos):
        item.setPos(pos)

    @classmethod
    def _empty_move_queue(cls, lock=False):
        cls._all_moves.clear(lock)

    def _sync_items(self):
        '''Sometimes, after running code is interrupted (like by Ctrl-C)
            the actual position (state.pos) and displayed position
            (drawable.pos) will be out of sync.

            This method can be called to synchronize the state to the
            position and rotation of the display.

        '''

        if self.drawable is not None:
            pos = self.drawable.pos()
            ang = self.drawable.angle
        else:
            pos = (0, 0)
            ang = 0
        self.state.setPos(pos)
        self.state.angle = ang

    @classmethod
    def _process_moves(cls):
        '''Apply the queued commands for the graphical display item
            This must be done from the main thread
        '''

        delay = cls.delay
        etime = cls._checktime.elapsed()
        # LOG.info('_r')
        if cls.ControlC:
            cls.ControlC += 1
            cls._empty_move_queue()
            if cls.main_window.interpretereditor.cmdthread is not None:
                # LOG.info('CC1')
                cls.main_window.interpretereditor.cmdthread.terminate()
                # LOG.info('CC2')

        elif etime > delay:
            ied = cls.main_window.interpretereditor
            runmoves = 0
            while True:
                runmoves += 1
                if runmoves >= 100:
                    break

                try:
                    move, args, pen = cls._all_moves.get()
                except queue.Empty:
                    cls._throttledown += 1
                    if cls._throttledown > 200:
                        cls.delay = 300
                    elif cls._throttledown > 20:
                        cls.delay = 10

                    if cls.delay:
                        cls.main_window.killTimer(cls.main_window._movetimer)
                        timer = cls.main_window.startTimer(cls.delay)
                        cls.main_window._movetimer = timer

                    # LOG.info(cls._throttledown)
                    # LOG.info(etime)
                    break
                except cls._all_moves.QQDelaying:
                    pass
                else:
                    if cls.delay:
                        cls.main_window.killTimer(cls.main_window._movetimer)
                        timer = cls.main_window.startTimer(0)
                        cls.main_window._movetimer = timer

                    cls._throttledown = 0
                    cls.delay = 0

                    if pen.defunct:
                        LOG.info('defunct')
                    else:
                        try:
                            # LOG.info(move)
                            # LOG.info(args)
                            move(*args)
                        except Exception:
                            import sys
                            tb = sys.exc_info()[2]
                            import traceback
                            tb = traceback.format_exc()
                            LOG.info(tb)
                            ied.write(tb)
                            ied.write('\n')
                            if ied.cmdthread is not None:
                                ied.cmdthread.terminate()
                                ied.cmdthread = None
                            cls._empty_move_queue()
                            ied.write('>>> ')

            cls._checktime.restart()

        QtGui.QApplication.processEvents(QtCore.QEventLoop.AllEvents)

    def _qdelay(self, n):
        '''Used by movement functions to insert delays in to movements
            when speed is anything other than instant.
        '''

        if self._delaying is not None:
            raise RuntimeError
        else:
            self._delaying = n

    def _mark_undo(self):
        '''Set up a marker for the current position to use
            when going back on undo.
        '''

        markers = self._undo_markers

        if hasattr(self, '_pen'):
            pen = self._pen
        else:
            pen = self

        pen._gitem_new_line()

        if hasattr(
                pen,
                'drawable') and hasattr(
                pen.drawable,
                'pos'):
            # LOG.info(markers)
            pos = pen.drawable.pos()
            x, y = pos.x(), pos.y()
            ang = pen.drawable.angle
            items = pen.drawn_items
            item = items[-1] if items else None
            marker = ((x, y, ang), item)
            # LOG.info(marker)

            if not markers or (markers[-1] != marker):
                markers.append(marker)

    def _undo(self):
        'Go back to the most recent undo marker'

        markers = self._undo_markers
        if not markers:
            print('Nothing to undo.')
            QtCore.QTimer.singleShot(
                50,
                self.main_window.interpretereditor.checkprompt)
            return

        # self._log(markers)
        pos, marker = markers.pop()
        # self._log(pos, marker)
        if hasattr(self, '_pen'):
            pen = self._pen
        else:
            pen = self
        items = pen.drawn_items
        # self._log(items)
        while True:
            item = items[-1] if items else None
            # self._log(item)
            if item == marker:
                break
            else:
                if item:
                    scene = item.scene()
                    if scene is not None:
                        scene.removeItem(item)
                        items.pop()
                    else:
                        # LOG.info('no scene')
                        break
                elif items:
                    items.pop()
                else:
                    break

        x, y, ang = pos
        pos = QtCore.QPointF(x, y)
        pen._item_goto(pen.state, pos)
        pen._gitem_goto(pos)

        pen._item_setangle(pen.state, ang)
        pen._gitem_setangle(ang)

    def wait(self, s):
        for _ms in range(int(s * 1000)):
            time.sleep(0.001)
            QtGui.QApplication.processEvents(QtCore.QEventLoop.AllEvents)

    @classmethod
    def wait_for_empty_q(cls):
        while cls._all_moves.qqsize():
            # LOG.info(cls._all_moves.qqsize())
            cls._process_moves()
        # LOG.info('READY')

    def _waitforit(self, flag):
        self._wfi = flag

    def waitforit(self):
        '''Block the user program until this command is
            processed through the command queue.
        '''

        flag = ''.join(random.sample(string.ascii_letters, 15))
        self.queue_command(self._waitforit, (flag,))
        # self._log('waiting for:', flag)
        while self._wfi != flag:
            if self.ControlC:
                LOG.info('WFI Break')
                break
            self.main_window.interpretereditor.spin(1, 0)
        # self._log('found:', flag)
        self._wfi = None
        # lock this!

    def _gitem_new_line(self):
        '''Break off the current QGraphicsItem line and start
            a new line. Need to do this any time the objects
            should be separate, like for fill color, or for
            removing separately in undo.
        '''

        if self.drawable is not None:
            self.drawable._current_line = None

    def _forward(self, item, distance, draw=True):
        '''Move item ahead distance. If draw is True, also add a line
            to the item's scene. draw should only be true for drawable
        '''

        theta = item.angle * (PI / 180)
        dx = distance * cos(theta)
        dy = distance * sin(theta)

        p1 = as_qpoint(item.pos())
        p2 = QtCore.QPointF(p1.x() + dx, p1.y() + dy)
        item.setPos(p2)

        if draw and item.is_down:
            current_line = self.drawable._current_line
            if current_line is None:
                ppath = QtGui.QPainterPath(p1)
                ppath.lineTo(p2)
                if self.drawable.fillmode:
                    ppath.setFillRule(self.drawable.fillrule)

                line = item.scene().addPath(ppath, item.qpen)

                if self.drawable.fillmode:
                    line.setBrush(self.drawable.brush)

                line.setZValue(self._zvalue)
                Pen._zvalue += 1
                self.drawn_items.append(line)
                self.drawable._current_line = line
            else:
                path = current_line.path()
                if p2 != path.currentPosition():
                    path.lineTo(p2)
                    current_line.setPath(path)

    def _breakup_forward(self, distance):
        '''used to break up movements for graphic animations. drawable will
            move forward by distance, but it will be done in steps that
            depend on the drawspeed setting
        '''
        self._check_drawspeed_change()

        drawspeed = self.drawspeed
        if distance >= 0:
            perstep = drawspeed
        else:
            perstep = -drawspeed

        adistance = abs(distance)
        run = 0
        while run < adistance:
            if perstep == 0:
                step = distance
                run = adistance
            elif run + drawspeed > adistance:
                step = sign(perstep) * (adistance - run)
            else:
                step = perstep
            run += drawspeed

            self.queue_command(self._forward, (self.drawable, step))
            if self.drawspeed:
                self.queue_command(
                    self._qdelay, (100 * (40 - self.drawspeed),))

            QtGui.QApplication.processEvents(QtCore.QEventLoop.AllEvents)

    @classmethod
    def _check_drawspeed_change(cls):
        if Pen._drawspeed_pending is not None:
            Pen.drawspeed = Pen._drawspeed_pending
            Pen._drawspeed_pending = None
            Pen.turnspeed = Pen._turnspeed_pending
            Pen._turnspeed_pending = None

    def queue_command(self, func, args=None):
        '''queue up a command for later application'''

        if self.defunct:
            raise Pen.Defunct

        if self.ControlC:
            Pen.ControlC += 1
            raise KeyboardInterrupt

        if args is None:
            args = ()

        thread = QtCore.QThread.currentThread()
        if thread == self.main_window._mainthread:
            func(*args)
            return

        self._moves.put_nowait((func, args, self))

    def _item_left(self, item, degrees):
        item.rotate(-degrees)

    def _gitem_turn(self, degrees):
        self._item_left(self.drawable, degrees)

    def _gitem_breakup_turn(self, degrees):
        self._check_drawspeed_change()

        turnspeed = self.turnspeed
        if degrees >= 0:
            perstep = self.turnspeed
        else:
            perstep = -self.turnspeed

        adegrees = abs(degrees)
        a = 0
        n = 0
        while a < adegrees:
            if perstep == 0:
                step = degrees
                a = adegrees
            elif a + turnspeed > adegrees:
                step = sign(perstep) * (adegrees - a)
            else:
                step = perstep
            n += 1
            a += self.turnspeed

            self.queue_command(self._gitem_turn, (step,))
            if self.turnspeed:
                # LOG.info('DELAY')
                # LOG.info('SELF %s' % self)
                # LOG.info('TS %s' % self.turnspeed)
                self.queue_command(
                    self._qdelay, (100 * (80 - self.turnspeed),))

    def _gitem_setangle(self, ang):
        self._item_setangle(self.drawable, ang)

    def _item_setangle(self, item, ang):
        item.angle = ang
        item.set_transform()

    def _closest_turn(self, ang):
        '''return the angle to turn most quickly from current angle to angle
        '''
        ang0 = self.state.angle
        dang = ang - ang0
        dang = dang % 360
        if dang > 180:
            dang = dang - 360
        elif dang < -180:
            dang = dang + 360
        return dang

    def _setfont(self, font):
        self._font = font

    def font(self, family=None, size=None, weight=None, italic=None):
        '''Set or return the font to use with write()

        The font returned is a QFont and can have additional
            modifications made.
        '''

        if family is size is weight is italic is None:
            return self._font

        font = QtGui.QFont(self._font)

        if family is not None:
            font.setFamily(family)
        if size is not None:
            font.setPointSize(size)
        if weight is not None:
            font.setWeight(weight)
        if italic is not None:
            font.setItalic(italic)

        self.queue_command(self._setfont, (font,))

    def _underline(self, on):
        self._font.setUnderline(on)

    def underline(self, on=True):
        self.queue_command(self._underline, (on,))

    def _write(self, text, move, align, valign):
        item = self.drawable.scene().addSimpleText(text, self._font)

        itemrect = item.boundingRect()
        textlength = itemrect.width()
        textheight = itemrect.height()

        item.setZValue(self._zvalue)
        Pen._zvalue += 1

        item.setPen(self.drawable.pen)
        item.setBrush(self.drawable.pen.color())

        x, y = self.drawable.x(), self.drawable.y()
        item.translate(x, y)
        item.rotate(self.drawable.angle)

        if align == 'left':
            fd = textlength
        elif align == 'center':
            fd = textlength / 2
            item.translate(-fd, 0)
        elif align == 'right':
            fd = 0
            item.translate(-textlength, 0)

        if valign == 'top':
            pass
        elif valign == 'middle':
            item.translate(0, -textheight / 2)
        elif valign == 'bottom':
            item.translate(0, -textheight)

        self.drawn_items.append(item)

        if move:
            self._gitem_new_line()
            self._forward(self.drawable, fd, False)

    def write(self, text, move=False, align='left', valign='bottom'):
        '''write(text)

        Draw a text message at the current location.

        If move is True, move the pen to the space after the
            last character written.

        align can be 'left', 'center', or 'right' (default 'left').
        valign can be 'bottom', 'middle', or 'top' (default 'bottom').
        '''

        if (align not in ('left', 'center', 'right') or
                valign not in ('bottom', 'middle', 'top')):
            raise ValueError('Unknown alignment')

        strtxt = str(text)
        if move:
            fm = QtGui.QFontMetrics(self._font)
            r = fm.boundingRect(strtxt)
            fd = r.width()
            self._forward(self.state, fd, False)
        self.queue_command(self._write, (strtxt, move, align, valign))

    def dbg(self):
        'test function for drawing on to the background plane'
        scene = self.scene
        bgp = scene.bgp
        bgp.drawEllipse(QtCore.QRect(50, 100, 200, 300))
        view = scene.view

        # scroll the scene to force an update
        view.scrollContentsBy(0, 1)
        view.scrollContentsBy(0, -1)

    def _item_home(self, item):
        self._item_goto(item, QtCore.QPointF(0, 0))
        self._item_setangle(item, 0)

    def _gitem_home(self):
        self._item_home(self.drawable)

    def _gitem_track(self, track, pen):
        if track:
            Pen._track_pen = pen
        else:
            Pen._track_pen = None

        if hasattr(pen, '_is_helper') and pen._is_helper:
            # _track_main_pen gets set in mode.py
            pass
        else:
            if track and pen is self.main_window.pen:
                Pen._track_main_pen = True
            else:
                Pen._track_main_pen = False

        self.drawable.track()
        self.main_window._sync_track(bool(Pen._track_main_pen))

    def track(self, track=True):
        self.queue_command(self._gitem_track, (track, self))

    def notrack(self):
        self.track(False)

    def home(self):
        '''home()

        Move directly to the home location (0, 0) and turn to angle 0
        '''

        self.goto(0, 0)
        self.setheading(0)

    def _clear(self):
        for item in self.drawn_items:
            scene = item.scene()
            if scene is not None:
                scene.removeItem(item)
        self.drawn_items = []
        self._gitem_new_line()

    def clear(self):
        self.queue_command(self._clear)

    def _full_reset(self):
        # self._empty_move_queue()

        self._remove_other_pens()
        self.main_window.setup_interpreter_locals()
        self.reset()

        self.queue_command(self._clear_defunct_pens_later)

    def _clear_defunct_pens_later(self):
        '''Go through occasionally and clear out the defunct_pens
            list. Tracking defunct user_pens should only be necessary
            for a limited time. If we do not clear out this list from
            time to time it gets unwieldy.
        '''
        self.main_window.defunct_pens = self.main_window.defunct_pens[-50:]
        LOG.info('YS %s' % len(self.main_window.defunct_pens))

    def reset(self, full=False):
        '''reset()

        Move to home location and angle and restore state
            to the initial values (pen, fill, etc).

        if full is True, also removes any added user_pens and clears out
            any pending pen movements. Also resets the pen
            functions that are pulled in to the interpreter namespace
            automatically.
        '''

        if full:
            if self is not self.main_window.pen:
                self.promote()
                self.waitforit()

            for pen in self.main_window.user_pens:
                if pen is not self and pen.drawable is not None:
                    pen.reset()
                    self.waitforit()

            self.main_window.user_pens[:] = [self]
            self.queue_command(self._full_reset)
            self.waitforit()

        else:
            settings = QtCore.QSettings()
            if self.avatar() == 'hidden':
                reset_forces_visible = settings.value(
                    'pen/reset_forces_visible',
                    True,
                    bool)
                if reset_forces_visible:
                    self.avatar('pen')

            self.clear()
            if self is self.main_window.pen:
                self._set_bgcolor_to_default()
            self.label('')
            self.goto(0, 0)
            self.turnto(0)
            self.pendown()
            self.width(2)
            self._set_color_to_default()
            self.nofill()
            self._set_fillcolor_to_default()
            self.fillrule('winding')
            self.main_window.zoom100()
            self.main_window.scene.view.centerOn(0, 0)
            self.main_window._centerview()
            LOG.info('RWFI')
            self.waitforit()

    def _remove_other_pens(self):
        '''remove the graphical avatar items for all the user_pens
            other than the main one.
        '''
        _pens = self.main_window.all_pens
        if self in _pens:
            _pens.remove(self)

        while _pens:
            pen = _pens.pop()
            pen.defunct = True
            self.main_window.defunct_pens.append(pen)
            scene = pen.drawable.scene()
            if scene is not None:
                scene.removeItem(pen.drawable)

            if hasattr(pen, '_pen'):
                _pen = pen._pen
                scene = _pen.drawable.scene()
                if scene is not None:
                    scene.removeItem(_pen.drawable)

        _pens.append(self)

    def _pendown(self, down=True):
        self.drawable.is_down = down
        self.main_window._sync_pendown_menu(down)

    def _color(self, r=None, g=None, b=None, a=255):
        c = QtGui.QColor(r, g, b, a)
        self.drawable.qpen.setColor(c)

    def color(self, r=None, g=None, b=None, a=None):
        '''color(red, green, blue) # 0-255 for each value
        color() # return the current color

        Set the line color for drawing. The color should be given as
            3 integers between 0 and 255, specifying the red, blue, and
            green components of the color.

        Uses the choose_color() function from the util module which
            also offers these options:

            Can also pass in just the name of a color, or the
                string 'random' for a randomly selected color or
                'rlight' for a random light color
                'rmedium' for a random medium color
                'rdark' for a random dark color
                'ralpha' for a random color with random alpha channel

        return the color being used for drawing -- makes getting
            randomly selected colors easier.
        '''
        if r is g is b is None:
            return self.state.color

        r, g, b, a = choose_color(r, g, b, a)
        self.state.color = (r, g, b, a)
        self.queue_command(self._gitem_new_line)
        self.queue_command(self._color, (r, g, b, a))

        return r, g, b, a

    def _set_color_to_default(self):
        settings = QtCore.QSettings()
        default = DEFAULT_COLOR
        rgba = int(settings.value('pen/color', default))
        c = QtGui.QColor.fromRgba(rgba)
        r, g, b, a = c.getRgb()
        if self.state.color != (r, g, b, a):
            self.color(r, g, b, a)

    def bgcolor(self, r=None, g=None, b=None):
        if r is g is b is None:
            color = self.scene.backgroundBrush().color()
            r, g, b, _ = color.getRgb()
            return r, g, b
        else:
            r, g, b, _a = choose_color(r, g, b)
            if (r, g, b) != self.main_window._bgcolor:
                self.main_window._bgcolor = (r, g, b)
                ncolor = QtGui.QColor(r, g, b)
                brush = QtGui.QBrush(ncolor)
                self.main_window.scene.setBackgroundBrush(brush)

    def _set_bgcolor_to_default(self):
        settings = QtCore.QSettings()
        default = DEFAULT_BGCOLOR
        c = settings.value('view/bgcolor', default)
        self.bgcolor(c)

    def _colorat(self):
        scene = self.scene
        x, y = int(self.x), int(self.y)
        items = scene.items(QtCore.QPointF(x, y))

        current_line = self.drawable._current_line
        if current_line in items:
            items.remove(current_line)

        pens = self.main_window.all_pens[:]
        hiding = []
        while pens:
            pen = pens.pop()

            item = self.drawable.item

            if item in items:
                items.remove(item)
            if self.drawable in items:
                items.remove(self.drawable)
                self.drawable.hide()
                hiding.append(self.drawable)

            if hasattr(pen, '_pen'):
                pens.append(pen._pen)

        if items:
            src = QtCore.QRectF(x, y, 1, 1)
            sz = QtCore.QSize(1, 1)
            self._i = i = QtGui.QImage(sz, QtGui.QImage.Format_RGB32)
            p = QtGui.QPainter(i)
            irf = QtCore.QRectF(0, 0, 1, 1)
            if current_line is not None:
                current_line.hide()
            scene.render(p, irf, src)
            if current_line is not None:
                current_line.show()
            rgb = i.pixel(0, 0)
            color = QtGui.QColor(rgb)

            settings = QtCore.QSettings()
            bgcolor = settings.value('view/bgcolor')
            if color != bgcolor:
                self._colorat_return = color.name()
            else:
                self._colorat_return = NOTHING
        else:
            self._colorat_return = NOTHING

        for gitem in hiding:
            gitem.show()

    def colorat(self):
        self._colorat_return = None
        self.queue_command(self._colorat)
        self.waitforit()
        rval = self._colorat_return
        self._colorat_return = None
        if rval is NOTHING:
            return None
        else:
            return rval

    def _width(self, w):
        self.drawable.pen.setWidth(w)

    def _fillcolor(self, r=None, g=None, b=None, a=None):
        '''fillcolor(red, green, blue, alpha) # 0-255 for each value
        fillcolor() # return the current fill color

        Set the fill color for drawing. The color should be given as
            3 integers between 0 and 255, specifying the red, blue, and
            green components of the color. Optionally, an alpha value
            can also be given to set transparency.
        '''
        color = QtGui.QColor.fromRgb(r, g, b, a)
        self.drawable.brush.setColor(color)
        self._gitem_new_line()

    def fillcolor(self, r=None, g=None, b=None, a=None):
        '''fillcolor(r, g, b, a)

        Set the color to be used for filling drawn shapes.

        return the color being used for filling -- makes getting
            randomly selected colors easier.
        '''
        r, g, b, a = choose_color(r, g, b, a)
        if r is g is b is None:
            return self.state.fillcolor
        self.state.fillcolor = (r, g, b, a)
        self.queue_command(self._fillcolor, (r, g, b, a))

        return r, g, b, a

    def _set_fillcolor_to_default(self):
        settings = QtCore.QSettings()
        default = DEFAULT_FILLCOLOR
        rgba = int(settings.value('pen/fillcolor', default))
        c = QtGui.QColor.fromRgba(rgba)
        r, g, b, a = c.getRgb()
        if self.state.fillcolor != (r, g, b, a):
            self.fillcolor(r, g, b, a)

    def _gitem_fillmode(self, start):
        if start:
            self.drawable.fillmode = True
            self._gitem_new_line()
            if self is self.main_window.pen:
                self.main_window._sync_fill_menu('fill')
        else:
            self.drawable.fillmode = False
            self._gitem_new_line()
            if self is self.main_window.pen:
                self.main_window._sync_fill_menu('nofill')

    def fill(self, color=None, rule=None):
        '''fill()

        Go in to fill mode. Anything drawn will be filled until
            nofill() is called.

        Set the fill color by passing in an (r, g, b) tuple, or
            pass color='random' for a random fill color.

        If a fill color is specified (color is not None)
            return the color that is being used as fill color.

        Change the fill rule by passing in either
            'winding' (default) or 'oddeven'
        '''
        if color is not None:
            c = choose_color(color)
            self.fillcolor(*c)

        if rule is not None:
            self.fillrule(rule)

        self.state.fillmode = True
        self.queue_command(self._gitem_fillmode, (True,))

        if color is not None:
            return self.fillcolor()

    def nofill(self):
        '''nofill()

        Turn off fill mode.
        '''
        self.state.fillmode = False
        self.queue_command(self._gitem_fillmode, (False,))

    def _gitem_fillrule(self, rule):
        self.drawable.fillrule = rule

    def fillrule(self, rule):
        '''fillrule(method) # 'oddeven' or 'winding'

        Set the fill method to OddEvenFill or WindingFill.
        '''
        if rule == 'oddeven':
            fr = QtCore.Qt.OddEvenFill
        elif rule == 'winding':
            fr = QtCore.Qt.WindingFill
        else:
            raise ValueError
        self.state.fillrule = fr
        self.queue_command(self._gitem_fillrule, (fr,))

    def _setImageid(self, imageid, filepath=None, sync=None):
        old_drawable = self.old_drawable = self.drawable
        if old_drawable is None:
            return
        pos = old_drawable.pos()
        ang = old_drawable.angle

        if filepath is None:
            # one of the built-in avatars
            rend = self.main_window.renderer
        else:
            # custom avatar
            fmt = QtGui.QImageReader.imageFormat(filepath)

            if fmt == 'svg':
                # custom svg avatar
                rend = self.main_window.svgrenderer.getrend(filepath)
            else:
                # custom non-svg avatar
                rend = None
                pm = QtGui.QPixmap(filepath)
                w, h = pm.width(), pm.height()
                if w > h:
                    pm = pm.scaledToWidth(250)
                    h = pm.height()
                    ho = (250 - h) / 2
                    wo = 0
                elif h > w:
                    pm = pm.scaledToHeight(250)
                    w = pm.width()
                    wo = (250 - w) / 2
                    ho = 0
                else:
                    rend = pm

                if rend is None:
                    rend = QtGui.QPixmap(250, 250)
                    rend.fill(QtCore.Qt.transparent)
                    painter = QtGui.QPainter(rend)
                    painter.drawPixmap(wo, ho, pm)

        pen = old_drawable.pen
        brush = old_drawable.brush
        scene = old_drawable.scene()
        drawable = Drawable(rend, imageid, self)
        drawable.setZValue(old_drawable.zValue())
        drawable.setPos(pos)
        drawable.angle = ang
        drawable.pen = pen
        drawable.is_down = old_drawable.is_down
        drawable.brush = brush
        drawable.fillmode = old_drawable.fillmode
        drawable.fillrule = old_drawable.fillrule
        drawable._current_line = old_drawable._current_line
        scene.removeItem(old_drawable)
        scene.addItem(drawable)
        self.drawable = drawable
        drawable.set_transform()

    def setImageid(self, imageid, filepath=None, sync=None):
        '''change the visible (avatar) image'''
        self._imageid = imageid
        self.queue_command(self._setImageid, (imageid, filepath, sync))
        if self.name:
            name = self.name
            self.label('')
            self.label(name)

    def avatar(self, imageid=None, filepath=None, sync=None):
        '''set or return the pen's avatar image

        Some avatars are built in and can be selected by passing imageid only.
        Choices are 'pen', 'turtle', 'arrow', 'robot', and 'hidden'

        An avatar can be set using an svg or png image also.

        For a png, pass the path to the file only.

        For an svg, pass the file path, and the svg id both.

        Normally, when the pen being modified is the main pen, you want
        the window menu to be synced with the selected avatar, however, for the
        special modes (ModeLogo and ModeTurtle) which are composed to 2
        user_pens, the sync=False option is available so that only the visible
        pen avatar will be synced with the menu. Also, sync=True is
        available to force sync when updating the visible pen even though
        it is not actually the primary.
        '''
        if filepath is not None and imageid is not None:
            self.setImageid(imageid, filepath, sync)
        elif filepath is not None and imageid is None:
            # load from non-svg image
            self.setImageid(imageid, filepath, sync)
        elif imageid is not None:
            self.setImageid('tuga', None, sync)
        else:
            return self._imageid

    def _speed(self, s):
        self.drawspeed = 2 * s
        self.turnspeed = 4 * s

    def speed(self, s):
        '''Set speed of animation for all user_pens.

        Choices are: 'slow', 'medium', 'fast', 'instant'
        '''

        choices = {'slow': 5,
                   'medium': 10,
                   'fast': 20,
                   'instant': 0}
        speed_value = choices.get(s)

        if speed_value is None:
            raise ValueError("Speed choices are %s" % list(choices.keys()))

        else:
            if hasattr(self, '_pen'):
                pen = self._pen
            else:
                pen = self

            self.queue_command(pen._speed, (speed_value,))

            if self is self.main_window.pen:
                settings = QtCore.QSettings()
                settings.setValue('pen/speed', s)
                self.main_window.sync_speed_menu(speed_value)

    def _circle(self, crect, finish=False):
        '''instant circle'''

        gitem = self.drawable
        if finish:
            cl = gitem._current_line
            self.drawn_items.pop()
            scene = gitem.scene()
            scene.removeItem(cl)
            self._gitem_new_line()

        self._gitem_new_line()
        scene = gitem.scene()
        circle = scene.addEllipse(crect, gitem.pen)
        if gitem.fillmode:
            circle.setBrush(gitem.brush)
        circle.setZValue(self._zvalue)
        Pen._zvalue += 1
        self.drawn_items.append(circle)
        gitem.expand()

    def _extend_circle(self, distance, signal=None):
        '''individual steps for animated circle drawing
        '''
        gitem = self.drawable
        if signal == 'start':
            # first segment
            self._item_left(gitem, -2)
            self._forward(gitem, distance)
        else:
            # continue drawing
            self._item_left(gitem, -4)
            self._forward(gitem, distance)

    def _slowcircle(self, crect, r, extent=360, center=False, pie=False):
        '''Animated circle drawing
        '''
        self.queue_command(self._gitem_new_line)
        pos0 = self.state.pos()
        ang0 = self.state.angle
        if center:
            pen = self.pen
            self.penup()
            self._breakup_forward(r)
            self._gitem_breakup_turn(-90)
            if pen:
                self.pendown()

        circumference = 2 * PI * r
        self.queue_command(self._extend_circle, (circumference / 90., 'start'))
        for _ in range(2, int(extent / 4)):
            self.queue_command(self._extend_circle, (circumference / 90.,))
            if 40 - self.drawspeed:
                self.queue_command(
                    self._qdelay, (100 * (40 - self.drawspeed),))

        if extent >= 360:
            self.queue_command(self._circle, (crect, True))
        else:
            if center:
                ang = self.angle + 90
            else:
                ang = self.angle
            self.queue_command(
                self._arc,
                (crect,
                 ang,
                 extent,
                 True,
                 center,
                 pie))

        if center:
            self.penup()
            self._gitem_breakup_turn(-90)
            self._breakup_forward(r)
            if extent >= 360:
                self._gitem_breakup_turn(180)
            else:
                ang = self._closest_turn(ang0)
                self._gitem_breakup_turn(ang)
            if pen:
                self.pendown()

        self.queue_command(self._gitem_goto, (pos0,))
        self.queue_command(self._gitem_setangle, (ang0,))

    def circle(self, r, center=False):
        '''circle(radius, center) # radius in pixels

        Draw a circle of radius r.

        If center is True, the current position will be the center of
            the circle. Otherwise, the circle will be drawn with the
            current position and rotation being a tangent to the circle.
        '''

        ritem = self.state
        cpt = ritem.pos()

        crect = self._circle_rect(r, cpt, ritem.angle, center)

        self._check_drawspeed_change()
        if self.drawspeed == 0:
            # instant circles
            if self.pen:
                self.queue_command(self._circle, (crect,))
        else:
            # animated circles
            self._slowcircle(crect, r, 360, center)

    def _arc(
            self,
            crect,
            start_angle,
            arc_length,
            finish=False,
            center=False,
            pie=False):
        '''instant arc'''

        gitem = self.drawable
        if finish:
            if self.drawable.is_down:
                cl = gitem._current_line
                self.drawn_items.pop()
                scene = gitem.scene()
                scene.removeItem(cl)
            self._gitem_new_line()

        p1 = crect.center()
        ppath = QtGui.QPainterPath(p1)

        fillmode = gitem.fillmode
        if fillmode:
            ppath.setFillRule(gitem.fillrule)

        ppath.arcMoveTo(crect, 90 - start_angle)
        ppath.arcTo(crect, 90 - start_angle, -arc_length)
        if pie:
            ppath.lineTo(p1)
            ppath.closeSubpath()

        if self.drawable.is_down:
            line = gitem.scene().addPath(ppath, gitem.pen)

            if gitem.fillmode:
                line.setBrush(gitem.brush)

            line.setZValue(self._zvalue)
            Pen._zvalue += 1
            self.drawn_items.append(line)
            self._gitem_new_line()

        gitem.expand()

    def _circle_rect(self, r, cpt, ang, center):
        '''return the bounding rect for the circle'''

        if not center:
            radians = (((PI * 2) / 360.) * ang)
            tocenter = radians + PI / 2

            dx = r * cos(tocenter)
            dy = r * sin(tocenter)

            tocpt = QtCore.QPointF(dx, dy)
            cpt = cpt + tocpt

        ul = cpt - QtCore.QPointF(r, r)
        sz = QtCore.QSizeF(2 * r, 2 * r)

        crect = QtCore.QRectF(ul, sz)

        return crect

    def arc(self, r, extent, center=False, move=True, pie=False):
        '''Draw an arc of radius r and central angle extent.

        If center is True, draw the arc centered on the current
            location.

        If move is True (the default) the pen will end up
            at the end of the drawn arc (if not centered) or
            turned by angle extent (if centered).

        If pie is True radii will also be drawn from the ends of
            the arc to the center of the circle it is an arc of.
            If fill is on the full pie shaped wedge will be filled.
        '''

        ritem = self.state
        cpt = ritem.pos()

        # Direction of drawing makes more sense this way
        if not center and r < 0:
            extent = -extent

        crect = self._circle_rect(r, cpt, ritem.angle, center=center)

        self._check_drawspeed_change()
        pen = self.pen
        if self.drawspeed == 0 and pen:
            if center:
                ang = ritem.angle + 90
            else:
                ang = ritem.angle
            self.queue_command(
                self._arc,
                (crect,
                 ang,
                 extent,
                 False,
                 center,
                 pie))
        else:
            self._slowcircle(crect, r, extent, center, pie)

        if not center and move:
            # Go to the end of the newly-drawn arc
            c = crect.center()
            cx, cy = c.x(), c.y()
            self.goto(cx, cy)
            self.turnto(ritem.angle + extent - 90)
            xn, yn = self.xyforward(r)
            self.goto(xn, yn)
            self.turnto(ritem.angle + 90)
        elif center and move:
            self.right(extent)

    def square(self, side, center=False):
        '''square(side, center=False) # length of side in pixels

        Draw a square with sides of length side.

        If center is True, the current position will be the center
            of the square. The sides will still be parallel or
            perpendicular to the current direction.
        '''

        pen = self.pen
        if center:
            self.penup()
            half_side = float(side) / 2
            self.forward(half_side)
            self.left(90)
            self.forward(half_side)
            self.left(90)
            if pen:
                self.pendown()

        for _ in range(4):
            self.forward(side)
            self.left(90)

        if center:
            self.penup()
            self.left(90)
            self.forward(half_side)
            self.right(90)
            self.forward(half_side)
            self.right(180)

        if pen:
            self.pendown()

    def _viewrect(self):
        view = self.scene.view
        viewportrect = view.viewport().geometry()
        tl = viewportrect.topLeft()
        br = viewportrect.bottomRight()
        tlt = view.mapToScene(tl)
        brt = view.mapToScene(br)
        return QtCore.QRectF(tlt, brt)

    def onscreen(self):
        '''onscreen()

        return True if the pen is in the visible area, or
            False if it is outside the visible area.
        '''
        pos = self.state.pos()
        return pos in self._viewrect()

    def viewcoords(self, floats=False):
        '''viewcoords()

        return the coordinates of the boundaries of the visible area.
            By default, returns the coordinates as integer values.

        Get the coords with code like this:
            xmin, xmax, ymin, ymax = viewcoords()

        To get float values instead of integers, pass in the optional
            parameter floats=True
        '''
        self.main_window.interpretereditor.spin(5)
        coords = self._viewrect().getCoords()
        if not floats:
            coords = [int(c) for c in coords]
        return coords

    def onclick(self, x, y):
        '''This method will be called automatically when the user
            right-clicks the mouse in the viewable area.

        To override this method, define a new function called onclick(x, y)
            and it will be inserted for automatic calling.

        Alternately, create a Pen subclass with its own
            onclick(self, x, y) method.
        '''
        pass

    def _stamp(self, x, y, imageid=None):
        gitem = self.drawable
        if imageid is None:
            imageid = gitem.imageid
            rend = gitem.renderer
        else:
            rend = self.main_window.renderer
        item = Drawable(rend, imageid, None)
        item.angle = gitem.angle
        item.setPos(gitem.pos())
        item.setZValue(self._zvalue)
        Pen._zvalue += 1
        gitem.scene().addItem(item)
        self.drawn_items.append(item)

    def stamp(self, imageid=None):
        '''stamp()
        stamp(imagename) # 'pen', 'robot', 'turtle', or 'arrow'

        Leave a stamp of the current pen image at the current location.

        Can also stamp the other images by including the image name.
        '''
        pos = self.state.pos()
        x, y = pos.x(), pos.y()
        self.queue_command(self._stamp, (x, y, imageid))

    def _gitem_setlabel(self, name):
        self.drawable.setlabel(name)

    def _setname(self, name):
        if name != self._name:
            self._name = name
            self.queue_command(self._gitem_setlabel, (name,))

    def _getname(self):
        return self._name
    name = property(_getname, _setname)

    def label(self, name=None):
        if name is None:
            return self.name
        else:
            self.name = name

    def export_locals(self):
        '''Return a dictionary with the name of all local methods that should
        be exported to the interpreter'''

        locals = {}
        for name in TURTLE_FUNCTIONS:
            locals[name] = getattr(self, name)
        return locals

    ###########################################################################
    #                         User visible functions
    ###########################################################################
    #
    # All these functions are accessible from the tugalinhas shell. The
    # english API mimics the `turtle` module in the standard library. The
    # portuguese API is mostly a direct translation, albeit somewhat
    # simplified.
    #

    #
    # Relative pen movement
    #

    def forward(self, distance):
        '''forward(distance) # in pixels | aka: fd(distance)

        Move the pen forward by distance pixels. Note that
            forward depends on which direction the pen is
            facing when you tell him to go forward.

        If the pen is down, this will also draw a line as the
            pen moves forward.
        '''
        self._forward(self.state, distance, False)
        self._breakup_forward(distance)
    fd = forward

    def backward(self, distance):
        '''backward(distance) # in pixels | aka: bk(distance)

        Move the pen backward by distance pixels. Note that
            forward depends on which direction the pen is
            facing when you tell him to go forward.

        If the pen is down, this will also draw a line as the
            pen moves backward.
        '''
        self.forward(-distance)
    bk = back = backward

    def left(self, degrees):
        '''left(angle) # in degrees | aka: lt(angle)

        Rotate the pen counter-clockwise by angle degrees. Note
            that the final angle will depend on the initial angle.

        To turn the pen directly to a particular angle, use setheading()
        '''
        self._item_left(self.state, degrees)
        self._gitem_breakup_turn(degrees)
    lt = left

    def right(self, degrees):
        '''right(angle) # in degrees | aka: rt(angle)

        Rotate the pen clockwise by angle degrees. Note
            that the final angle will depend on the initial angle.

        To turn the pen directly to a particular angle, use setheading()
        '''
        self.left(-degrees)
    rt = right

    # Portuguese
    @docfrom(tugalib.frente)
    def frente(self, distância):
        self.forward(distância)

    def trás(self, distância):
        '''Anda para trás a distância especificada em pixels'''

        self.backward(distância)

    def direita(self, ângulo):
        '''Vira para a direita pelo ângulo especificado'''

        self.right(ângulo)

    def esquerda(self, ângulo):
        '''Vira para a esquerda pelo ângulo especificado'''

        self.left(ângulo)

    #
    # Absolute movement
    #
    def _goto(self, obj, pos):
        obj.setPos(pos)
        obj.set_transform()

    def goto(self, x, y=None):
        '''Move turtle to an absolute position. If the pen is down, draw line.
        Do not change the turtle’s orientation.

        If y is None, x must be a pair of coordinates.'''

        if y is None and isinstance(x, Pen):
            x, y = x.position()
        elif y is None:
            x, y = x

        angle = self.heading()
        self.setheading(self.towards(x, y))
        self.forward(self.distance(x, y))
        self.setheading(angle)
    setpos = setposition = goto

    def setx(self, x):
        '''Set the turtle’s first coordinate to x, leave second coordinate
        unchanged.'''

        self.goto(x, self.y)

    def sety(self, y):
        '''Set the turtle’s second coordinate to y, leave first coordinate
        unchanged.'''

        self.goto(self.x, y)

    def setheading(self, angle):
        '''setheading(angle) # in degrees

        Turn the pen directly to the given angle. The angle is given
            in degrees with 0 degrees being to the right, positive angles
            clockwise, and negative angles counter-clockwise.

        The final angle will be the angle specified, not an angle relative
            to the initial angle. For relative angles, use left or right.
        '''
        angle = 0.0 - angle
        self._heading = angle
        self._item_setangle(self.state, angle)
        self.queue_command(self._gitem_setangle, (angle,))
    seth = setheading

    # Portuguese
    @docfrom(tugalib.ir_para)
    def ir_para(self, x, y):
        self.goto(x, y)

    @docfrom(tugalib.começo)
    def começo(self):
        self.home()

    @docfrom(tugalib.mudar_x)
    def mudar_x(self, x):
        self.setx(x)

    @docfrom(tugalib.mudar_y)
    def mudar_y(self, y):
        self.sety(y)

    @docfrom(tugalib.mudar_orientação)
    def mudar_orientação(self, ângulo):
        self.setheading(ângulo)

    #
    # Retrieve pen's state
    #
    def position(self):
        '''Return the pen's current location (x,y).'''

        pos = self.state.pos()
        return Vec2D(pos.x(), -pos.y())
    pos = position

    def towards(self, x, y=None):
        '''towards(x, y) # in pixels

        Return the angle between the line from pen position to position
        specified by (x,y), the vector or the other pen object.
        '''

        if y is None:
            if isinstance(x, Pen):
                x, y = x.position()
            else:
                x, y = x

        cx, cy = self.position()
        dx = x - cx
        dy = y - cy
        return degrees(atan2(dy, dx))

    def distance(self, x, y):
        '''distance(x, y) # in pixels

        return the distance (in pixels) to the given coordinates
        '''
        cx, cy = self.position()
        dx = x - cx
        dy = y - cy
        return hypot(dx, dy)

    def heading(self):
        '''Get the current heading'''

        return -self._heading

    def xcor(self):
        return self.position()[0]

    def ycor(self):
        return self.position()[1]

    # Portuguese
    def posição(self):
        return self.position()

    def ângulo_para(self, x, y):
        return self.toward(x, y)

    def distância_para(self, x, y):
        return self.distance(x, y)

    def coordenada_x(self):
        return self.xcor()

    def coordenada_y(self):
        return self.ycor()

    def orientação(self):
        return self.heading()

    #
    # Drawing state
    #
    def pendown(self):
        '''pendown()

        Put the pen in the down (drawing) position.
        '''
        self.pen = self.state.is_down = True
        self.queue_command(self._pendown)
    down = pd = pendown

    def penup(self):
        '''penup()

        Put the pen in the up (non-drawing) position.
        '''
        self.pen = self.state.is_down = False
        self.queue_command(self._pendown, (False,))
        self.queue_command(self._gitem_new_line)
    up = pu = penup

    def pensize(self, w=None):
        '''pensize(w) # in pixels
        pensize() # return the current width

        Set the line width for drawing.
        '''
        if w is None:
            return self.state.penwidth
        else:
            self.state.penwidth = w
            self.queue_command(self._gitem_new_line)
            self.queue_command(self._width, (w,))
    width = pensize

    def pen(self):
        raise NotImplementedError

    def isdown(self):
        '''Return True if pen is down, False if it’s up.'''

    # Portuguese

    def abaixa(self):
        self.pendown()

    def levanta(self):
        self.penup()

    def espessura(self):
        return self.pensize()

    def mudar_espessura(self, pixels):
        self.pensize(pixels)

    def está_abaixada(self):
        return self.isdown()
