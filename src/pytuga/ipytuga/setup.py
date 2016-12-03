"""
Makes ipytuga kernel discoverable by Jupyter
"""

import os

assets_dir = os.path.join(os.path.dirname(__file__), 'assets')


def setup_assets(user=False, ipython_dir=None):
    from ipykernel.kernelspec import KernelSpecManager
    from jupyter_client.kernelspec import install_kernel_spec

    if ipython_dir is None:
        install = install_kernel_spec
    else:
        spec = KernelSpecManager(ipython_dir=ipython_dir)
        install = spec.install_kernel_spec

    install(assets_dir, 'pytuga', replace=True, user=user)


if __name__ == '__main__':
    setup_assets()