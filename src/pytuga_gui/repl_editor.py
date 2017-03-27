from PyQt5 import QtWidgets, QtCore

from jupyter_client.localinterfaces import is_local_ip
from qtconsole.rich_jupyter_widget import RichJupyterWidget

from pytuga_gui import styles
from pytuga_gui.ipytuga_qtconsole import IPytugaWidgetQtConsoleApp


class JupyterRichTextEditor(RichJupyterWidget):
    def __init__(self, app, parent=None):
        self.app = app
        super().__init__(
            parent=parent,
            config=app.config,
            local_kernel=(not app.existing) or is_local_ip(app.ip),
            gui_completion='droplist',
            in_prompt='',
        )

        self.style_sheet = styles.default_dark_style_sheet
        self.syntax_style = styles.default_dark_syntax_style
        self._existing = app.existing
        self._may_close = not app.existing
        self._confirm_exit = app.confirm_exit
        self._display_banner = False
        self.kernel_manager = app.kernel_manager
        self.kernel_client = app.kernel_client


class ReplEditor(QtWidgets.QWidget):
    def __init__(self, parent=None, *,
                 header_text=None,
                 hide_console_margins=False,
                 namespace=None):
        super().__init__(parent)
        self._console_app = IPytugaWidgetQtConsoleApp(parent_widget=self)
        self._console_widget = self._console_app.get_widget()
        self._editor = JupyterRichTextEditor(self._console_app, self)

        # Create buttons and connect buttons
        run_button = QtWidgets.QPushButton('Run')
        hideup_button = QtWidgets.QPushButton('\u25b2')
        hidedown_button = QtWidgets.QPushButton('\u25bc')
        run_button.setMaximumWidth(100)
        hideup_button.setFixedWidth(35)
        hidedown_button.setFixedWidth(35)
        buttons = QtWidgets.QWidget()
        button_area = QtWidgets.QHBoxLayout(buttons)
        button_area.addWidget(hideup_button, 20)
        button_area.addWidget(hidedown_button, 20)
        button_area.addStretch(300)
        button_area.addWidget(run_button, 200)
        button_area.setContentsMargins(0, 0, 0, 0)
        buttons.setFixedHeight(25)
        run_button.clicked.connect(self.runCode)
        hideup_button.clicked.connect(self.hideUp)
        hidedown_button.clicked.connect(self.hideDown)

        # Create top area with the Editor and the button area element
        top_widget = QtWidgets.QWidget()
        top_layout = QtWidgets.QVBoxLayout(top_widget)
        top_layout.setContentsMargins(0, 0, 0, 0)
        top_layout.addWidget(self._editor)
        top_layout.addWidget(buttons)
        self._top_widget = top_widget

        # Add elements
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        splitter = QtWidgets.QSplitter(QtCore.Qt.Orientation(0))
        splitter.addWidget(top_widget)
        splitter.addWidget(self._console_widget)
        splitter.setSizes([200, 120])
        splitter.setChildrenCollapsible(False)
        layout.addWidget(splitter)
        self._splitter = splitter
        self._splitter_sizes = splitter.sizes()

        # Size hints
        self.setMinimumSize(QtCore.QSize(100, 200))

    def console(self):
        return self._console_app

    def editor(self):
        return self._editor

    def sizeHint(self):
        return QtCore.QSize(100, 200)

    def setNamespace(self, ns):
        print('setNamespace:', ns)

    def runCode(self):
        text = self._editor.text()
        if text:
            result = self._console_app.execute(text)
            if result and self._console_app.isHidden():
                self.toggleConsoleVisibility()

    def toggleConsoleVisibility(self):
        if self._console_app.isHidden():
            self._console_app.setHidden(False)
            self._splitter.setSizes(self._splitter_sizes)
        else:
            self._splitter_sizes = self._splitter.sizes()
            self._splitter.setSizes([2 ** 16, 1])
            self._console_app.setHidden(True)

    def toggleEditorVisibility(self):
        if self._editor.isHidden():
            self._editor.setHidden(False)
            self._splitter.setSizes(self._splitter_sizes)
        else:
            self._splitter_sizes = self._splitter.sizes()
            self._splitter.setSizes([1, 2 ** 16])
            self._editor.setHidden(True)

    def hideUp(self):
        if self._console_app.isHidden():
            self.toggleConsoleVisibility()
        elif not self._editor.isHidden():
            self.toggleEditorVisibility()

    def hideDown(self):
        if self._editor.isHidden():
            self.toggleEditorVisibility()
        elif not self._console_app.isHidden():
            self.toggleConsoleVisibility()

    def setText(self, text):
        print('setText:', text)
        #self._editor.setText(text)

    def text(self):
        return self._editor.text()

    def toggleTheme(self):
        self._console_app.toggle_theme()
        self._editor.toggleTheme()

    def zoomIn(self):
        self._console_app.zoomIn()
        self._editor.zoomIn()

    def zoomOut(self):
        self._console_app.zoomOut()
        self._editor.zoomOut()

    def zoomTo(self, factor):
        self._console_app.zoomTo(factor)
        self._editor.zoomTo(factor)

    def __getattr__(self, attr):
        if 'Console' in attr:
            head, _, tail = attr.partition('Console')
            return getattr(self._console_app, head + tail)
        else:
            try:
                return getattr(self._editor, attr)
            except AttributeError:
                try:
                    return getattr(self._console_app, attr)
                except AttributeError:
                    tname = type(self).__name__
                    msg = '%s object has no attribute %s' % (tname, attr)
                    raise AttributeError(msg)
