import os
import sys

from pyqode.core import api
from pyqode.core import modes
from pyqode.core import panels
from pyqode.core.api import ColorScheme
from pyqode.python import modes as pymodes
from pyqode.python import panels as pypanels
from pyqode.python.backend.workers import defined_names
from pyqode.python.folding import PythonFoldDetector
from pyqode.python.widgets.code_edit import PyCodeEditBase
from pyqode.qt import QtWidgets, QtCore

import pyqode_pytuga
from pyqode_pytuga.syntax_highlight import PytugaSyntaxHighlighter

BASEDIR = os.path.dirname(pyqode_pytuga.__file__)
SERVER_SCRIPT = os.path.join(BASEDIR, 'server.py')


class PytugaCodeEdit(PyCodeEditBase):
    DARK_STYLE = 0
    LIGHT_STYLE = 1

    mimetypes = ['text/x-pytuga']
    server_script = SERVER_SCRIPT
    server_interpreter = sys.executable
    server_args = None

    @QtCore.Slot()
    def delete_line(self):
        """
        Delete the line under the cursor.
        """

        cursor = self.textCursor()
        start = cursor.selectionStart()
        remove_line_under_cursor = True
        cursor.beginEditBlock()
        if cursor.hasSelection():
            cursor.removeSelectedText()
            remove_line_under_cursor = bool(cursor.columnNumber())
        if remove_line_under_cursor:
            cursor.select(cursor.LineUnderCursor)
            cursor.removeSelectedText()
            cursor.deleteChar()
        cursor.endEditBlock()
        cursor.setPosition(start)
        self.setTextCursor(cursor)

    def __init__(self, parent=None, server_script=SERVER_SCRIPT,
                 interpreter=sys.executable, args=None,
                 create_default_actions=True, color_scheme='qt',
                 reuse_backend=False, extra=()):
        super().__init__(
            parent=parent,
            create_default_actions=create_default_actions
        )

        # Start server
        self.backend.start(
            self.server_script,
            self.server_interpreter,
            self.server_args,
            reuse=reuse_backend
        )

        # Configure QtPlainRichText options
        self.setLineWrapMode(self.NoWrap)
        self.action_duplicate_line.setShortcut('Ctrl+Shift+D')

        # Delete line action
        action = QtWidgets.QAction(_('Duplicate line'), self)
        action.setShortcut('Ctrl+D')
        action.triggered.connect(self.delete_line)
        self.add_action(action, sub_menu=None)
        self.action_delete_line = action

        # Configure color scheme
        if isinstance(color_scheme, str):
            self.color_scheme = ColorScheme(color_scheme)
        else:
            self.color_scheme = color_scheme

        # Create modes and panels
        self._enable_symbols_browser = 'symbols-browser' in extra
        self._enable_encoding_panel = 'encodings-menu' in extra
        self.setModesAndPanels()

    def setModesAndPanels(self):
        # install those modes first as they are required by other modes/panels
        self.modes.append(modes.OutlineMode(defined_names))
        self.setModes()
        self.setPanels()

    def setModes(self):
        self.modes.append(modes.ExtendedSelectionMode())
        self.modes.append(modes.CaretLineHighlighterMode())
        self.modes.append(modes.FileWatcherMode())
        self.modes.append(modes.RightMarginMode())
        self.modes.append(modes.ZoomMode())
        self.modes.append(modes.SymbolMatcherMode())
        self.modes.append(modes.CodeCompletionMode())
        self.modes.append(modes.OccurrencesHighlighterMode())
        self.modes.append(modes.SmartBackSpaceMode())

        # python specifics
        self.modes.append(pymodes.PyAutoIndentMode())
        self.modes.append(pymodes.PyAutoCompleteMode())
        self.modes.append(pymodes.CalltipsMode())
        self.modes.append(pymodes.PyIndenterMode())
        self.modes.append(pymodes.GoToAssignmentsMode())
        self.modes.append(pymodes.CommentsMode())
        self.modes.append(PytugaSyntaxHighlighter(self.document(),
                                                  color_scheme=self.color_scheme))
        self.syntax_highlighter.fold_detector = PythonFoldDetector()

    def setPanels(self):
        self.panels.append(panels.SearchAndReplacePanel(),
                           panels.SearchAndReplacePanel.Position.BOTTOM)
        self.panels.append(panels.FoldingPanel())
        self.panels.append(panels.LineNumberPanel())
        self.panels.append(pypanels.QuickDocPanel(), api.Panel.Position.BOTTOM)
        self.panels.append(panels.ReadOnlyPanel(), api.Panel.Position.TOP)

        # Optional panels
        if self._enable_symbols_browser:
            self.panels.append(pypanels.SymbolBrowserPanel(),
                               api.Panel.Position.TOP)
        if self._enable_encoding_panel:
            self.panels.append(panels.EncodingPanel(), api.Panel.Position.TOP)

    def clone(self):
        clone = self.__class__(
            parent=self.parent(), server_script=self.backend.server_script,
            interpreter=self.backend.interpreter, args=self.backend.args,
            color_scheme=self.syntax_highlighter.color_scheme.name)
        return clone
