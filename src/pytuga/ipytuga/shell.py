import json
import os
import sys

from jupyter_client import KernelManager
from jupyter_console.app import ZMQTerminalIPythonApp
from jupyter_console.ptshell import ZMQTerminalInteractiveShell


class PytugaKernelManager(KernelManager):
    kernel_name = 'pytuga'

    @property
    def kernel_spec(self):
        data = get_kernel_spec()
        script = self.kernel_script_path
        data['argv'] = [sys.executable, script, '-f', '{connection_file}']
        return data

    @property
    def kernel_script_path(self):
        return os.path.join(os.path.dirname(__file__), 'kernel.py')


# Jupyter does not make it very easy to subclass. We simply monkey-patch the
# ZMQTerminalInteractiveShell class. It is a singleton, hence we don't expect
# problems.
#
# These hacks customize the messages shown during shell initialization.
def show_banner(self):
    print(self.kernel_info.get('banner', ''))


ZMQTerminalInteractiveShell.show_banner = show_banner


class ZMQTerminalPytugaApp(ZMQTerminalIPythonApp):
    """
    A Pytuga specific terminal
    """
    name = 'pytuga-console'


def start_console_shell():
    """
    Starts a cli-based shell.
    """

    ZMQTerminalPytugaApp.launch_instance(
        kernel_manager=PytugaKernelManager,
        kernel_name='pytuga',
    )


def start_qt_shell():
    """
    Starts a shell based on QtConsole.
    """

    ZMQTerminalPytugaApp.launch_instance(
        kernel_manager=PytugaKernelManager,
    )


def start_shell(gui=False):
    """
    Starts pytuga shell.
    """

    if gui:
        start_qt_shell()
    else:
        start_console_shell()


def get_kernel_spec(kernel_command=None):
    """
    Load kernel.json and possibly substitute the kernel command path to the
    given command.
    """

    path = os.path.join(os.path.dirname(__file__), 'assets', 'kernel.json')
    with open(path) as F:
        data = json.load(F)

    if kernel_command:
        data['argv'] = kernel_command
    return data


if __name__ == '__main__':
    start_shell()
