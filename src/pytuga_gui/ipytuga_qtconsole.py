"""
Code were adapted from qtconsole.qtconsoleapp to use Pytuga kernel.

This class create a Jupyter aplication which runs and interact with a Pytuga
kernel. The console app does not necessarely open a qt window. Use the
method .getWidget() or .showWidget() methods to initialize and show a qt widget
that interact the console application.
"""
from PyQt5 import QtWidgets
from logging import getLogger

from jupyter_client.localinterfaces import is_local_ip
from lazyutils import lazy
from qtconsole.qtconsoleapp import JupyterQtConsoleApp

from pytuga_gui import styles

log = getLogger('gui.ipytuga')


class IPytugaQtConsoleApp(JupyterQtConsoleApp):
    """
    Subclass of JupyterQtConsoleApp that initializes a pytuga kernel instead of
    a regular python kernel.
    """

    use_kernel = 'pytuga'
    theme = 'dark'

    def __init__(self, *args, **kwargs):
        self.use_kernel = kwargs.pop('use_kernel', self.use_kernel)
        super().__init__(*args, **kwargs)

    def initialize(self, argv=None):
        argv = ['--kernel', self.use_kernel]
        return super().initialize(argv)

    def execute(self, code, silent=True, **kwargs):
        """
        Sends command to interpreter.
        """

        self.kernel_client.execute(code, silent=silent, **kwargs)

    def toggle_theme(self):
        """
        Toggles between dark/light themes.
        """

        if self.theme == 'dark':
            self.set_theme('light')
        else:
            self.set_theme('dark')

    def set_theme(self, theme):
        if theme not in ['light', 'dark']:
            raise ValueError('invalid theme: %r' % theme)
        self.widget.set_default_style('linux' if theme == 'dark' else 'lightbg')
        self.theme = theme


class IPytugaFullQtConsoleApp(IPytugaQtConsoleApp):
    """
    We add a few Pytuga-specific features to the default Jupyter qtconsole app.
    """


class IPytugaWidgetQtConsoleApp(IPytugaQtConsoleApp):
    """
    A simplified application that exposes only a simple terminal widget instead
    of a full application with menus. This is useful for embeding in other
    applications.
    """

    @lazy
    def parent_widget(self):
        return QtWidgets.QWidget()

    @lazy
    def window(self):
        return self.parent_widget.window()

    @lazy
    def widget(self):
        self.initialize()
        log.info('Pytuga kernel initialized with --kernel %s' % self.use_kernel)
        return self.widget

    def __init__(self, parent_widget=None, **kwargs):
        kwargs.setdefault('display_banner', False)
        super().__init__(**kwargs)
        if parent_widget is not None:
            self.parent_widget = parent_widget

    def init_qt_app(self):
        self.app = None

    def init_qt_elements(self):
        ip = self.ip
        local_kernel = (not self.existing) or is_local_ip(ip)
        self.widget = widget = self.widget_factory(
            parent=self.parent_widget,
            config=self.config,
            local_kernel=local_kernel,
            gui_completion='droplist',
            in_prompt='>>> '
        )
        widget.style_sheet = styles.default_dark_style_sheet
        widget.syntax_style = styles.default_dark_syntax_style
        widget._existing = self.existing
        widget._may_close = not self.existing
        widget._confirm_exit = self.confirm_exit
        widget._display_banner = self.display_banner
        widget.kernel_manager = self.kernel_manager
        widget.kernel_client = self.kernel_client

    def get_widget(self):
        return self.widget

    def start(self):
        pass


def start_qtconsole(**kwargs):
    """
    Starts a pytuga-based qtconsole application.
    """

    IPytugaFullQtConsoleApp.launch_instance(**kwargs)


if __name__ == '__main__':
    start_qtconsole()
