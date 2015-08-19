'''
Helper script for setup.py in Cython based projects
'''

import os
import sys


def get_packages(path='src'):
    '''Return a list of packages under the given path'''

    packages = []
    N = len(path) + len(os.path.sep)

    for directory, dir_list, file_list in os.walk(path):
        if '__init__.py' in file_list:
            directory = directory[N:]
            package = directory.replace(os.path.sep, '.')
            packages.append(package)

    return packages

IS_PYPY = 'PyPy' in sys.version


def find_pyx():
    '''Return a list of all Cython scripts'''

    # Find files
    out = []
    for base, dirs, files in os.walk(os.path.join(os.getcwd(), 'src')):
        out.extend([os.path.join(base, f)
                    for f in files if f.endswith('.pyx')])

    # Remove cwd from path
    N = len(os.getcwd()) + 5
    out = [f[N:] for f in out]

    return out


def find_pure():
    '''Return a list of all .pxd files related to pure-python scripts'''

    # Find files
    out = []
    for base, dirs, files in os.walk(os.path.join(os.getcwd(), 'src')):
        out.extend([os.path.join(base, f)
                    for f in files if f.endswith('.pxd')])

    # Remove non-compilable files
    aux = []
    for f in out:
        with open(f) as F:
            line = F.readline()
        if line.startswith('#:'):
            if 'no-compile' in line:
                continue
        if os.path.exists(f[:-4] + '.py'):
            aux.append(f)
    out = aux

    # Remove cwd from path
    N = len(os.getcwd()) + 5
    out = [f[N:-4] + '.py' for f in out]

    return out


def get_extensions():
    '''Uses information on all pure-python scripts and all Cython scripts
    to create the extension objects'''

    from distutils.extension import Extension
    win_platforms = ['win32', 'cygwin']

    if IS_PYPY:
        return []

    exts = []
    for path in find_pyx() + find_pure():
        base, fname = os.path.split(path)
        ext_name = os.path.splitext(path)[0].replace(os.path.sep, '.')
        includes = ['src/%s' % base]
        if base != 'mathtools':
            includes.append('src/mathtools')

        ext = Extension(
            ext_name,
            ["src/%s" % path],
            libraries=(
                [] if sys.platform in win_platforms else ['m']),
            include_dirs=includes)

        exts.append(ext)

    return exts

###############################################################################
#                          Configure environment
###############################################################################


def foo():
    # Test if installation can compile extensions and configure them
    # Currently only cpython accepts extensions
    try:
        from Cython.Distutils import build_ext
    except ImportError:
        # Ignore missing cython in alternative implementation
        if not (sys.platform.startswith('java') or
                sys.platform.startswith('cli') or 'PyPy' in sys.version):
            raise
    else:
        extensions = get_extensions()
        setup_kwds.update(
            cmdclass={
                "build_ext": build_ext},
            ext_modules=get_extensions())
