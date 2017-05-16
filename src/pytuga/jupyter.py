from .transpyler import pytuga_transpyler


def run_jupyter():
    """
    Runs a Jupyter shell for Pytugues.
    """

    from transpyler.jupyter import run_jupyter
    run_jupyter(pytuga_transpyler)


if __name__ == '__main__':
    run_jupyter()
