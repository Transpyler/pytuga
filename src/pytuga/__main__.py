import sys

from pytugacore import transpyler


def main():
    if 'cli' in sys.argv or 'jupyter' in sys.argv:
        from transpyler.jupyter import run_jupyter
        run_jupyter(transpyler)
    elif 'console' in sys.argv:
        from transpyler.console import run_console
        run_console(transpyler)
    else:
        from qturtle import start_application
        start_application(transpyler)


if __name__ == '__main__':
    main()
