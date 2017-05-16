import os
import sys
from glob import glob
from setuptools import setup, find_packages


# cx_Freeze: we added a undocumented option to enable building frozen versions
# of our packages. This should be refactored for a more safe approach in the
# future.
setup_kwargs = {}
if '--cx-freeze' in sys.argv:
    from cx_Freeze import setup, Executable

    build_options = {
        'include_files': [],
        'packages': ['os', 'pytuga', 'pygments', 'transpyler'],
        'excludes': [
            'tkinter', 'redis', 'lxml',
            'qturtle.qsci.widgets',
            'nltk', 'textblob',
            'matplotlib', 'scipy', 'numpy', 'sklearn',
            'notebook',
            'java',
            'sphinx', 'PIL', 'PyQt4'
        ],
        'optimize': 1,
    }
    base = 'Win32GUI' if sys.platform == 'win32' else None

    setup_kwargs['executables'] = [
        Executable(
            'src/pytuga/__main__.py',
            base=base,
            targetName='Pytuga.exe' if sys.platform == 'win32' else 'pytuga',
            shortcutName='Pytuga',
            shortcutDir='DesktopFolder',
        )
    ]
    setup_kwargs['options'] = {'build_exe': build_options}
    sys.argv.remove('--cx-freeze')


# Save version and author to __meta__.py
version = open('VERSION').read().strip()
dirname = os.path.dirname(__file__)
path = os.path.join(dirname, 'src', 'pytuga', '__meta__.py')
meta = '''# Automatically created. Please do not edit.
__version__ = '%s'
__author__ = 'F\\xe1bio Mac\\xeado Mendes'
''' % version
with open(path, 'w') as F:
    F.write(meta)


# FIXME: REFACTOR THOSE CHECKS
# # Warn user about missing PyQt libraries. These cannot go into REQUIRES list
# # since PyQt is not instalable via pip
# try:
#     import PyQt5.QtSvg
#     import PyQt5.Qsci
# except ImportError:
#     import warnings
#
#     warnings.warn(
#         'Please install PyQt5, PyQt5.QtSvg and PyQt5.Qsci!\n'
#         'Check your distribution packages or go to the website bellow:\n'
#         '    https://riverbankcomputing.com/software/pyqt/download5\n')
#
#
# # Collect data files
# if sys.platform.startswith('win'):
#     # TODO: figure out where these files should be in Windows
#     # We need someone with a windows machine! :P
#     DATA_FILES = []
# else:
#     DATA_FILES = [
#         ('share/icons/hicolor/scalable/apps', ['data/icons/pytuga.svg']),
#         ('share/icons/hicolor/scalable/mimetypes',
#          ['data/icons/text-x-pytuga.svg']),
#         ('share/mime', ['data/pytg.xml']),
#         ('share/applications', ['data/pytuga.desktop']),
#         ('share/doc/pytuga', ['README.rst']),
#         ('share/doc/examples', glob('data/examples/*.pytg')),
#         ('share/gtksourceview-3.0/language-specs', ['data/pytuga.lang']),
#     ]
#
# # Add documentation files
# for path, _, files in os.walk('doc/build/html'):
#     docfiles = []
#     DATA_FILES.append(('doc/pytuga' + path[14:], docfiles))
#     for file in files:
#         docfiles.append('%s/%s' % (path, file))
#
# # Fix path separators in windows (necessary?)
# if os.path.sep != '/':
#     for i, (path, files) in enumerate(DATA_FILES):
#         path = os.path.sep.join(path.split('/'))
#         files = [os.path.sep.join(f.split('/')) for f in files]
#         DATA_FILES[i] = (path, files)


# Wraps command classes to register pytuga kernel during installation
def wrapped_cmd(cmd):
    class Command(cmd):
        def run(self):
            if 'src' not in sys.path:
                sys.path.append('src')

            from transpyler.jupyter.setup import setup_assets
            setup_assets(True)
            cmd.run(self)

    return Command


# Run setup() function
setup(
    name='pytuga',
    version=version,
    description='Interpretador de Pytuguês: um Python com sotaque lusitano.',
    author='Fábio Macêdo Mendes',
    author_email='fabiomacedomendes@gmail.com',
    url='https://github.com/transpyler/pytuga',
    long_description=('''
    Pytuguês é uma linguagem de programação que modifica a sintaxe do
    Python para aceitar comandos em português. A linguagem foi desenvolvida
    como uma extens~ao do Python que aceita comandos em português.

    O único objetivo do Pytuguês é facilitar o aprendizado de programação. Uma
    vez que os conceitos básicos forem apreendidos, a transição para uma
    linguagem real (no caso o Python) torna-se gradual e natural.
    '''),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries',
    ],

    # Packages and dependencies
    package_dir={'': 'src'},
    packages=find_packages('src'),
    install_requires=[
        'qturtle>=0.2.0',
        'transpyler>=0.2.0'
    ],

    # Wrapped commands (for ipytuga)
    # cmdclass={
    #    'install': wrapped_cmd(_install),
    #    'develop': wrapped_cmd(_develop),
    # },

    # Scripts
    entry_points={
        'console_scripts': [
            'pytuga = pytuga.__main__:main',
        ],
    },

    # Data files
    package_data={
        'pytuga': [
            'assets/*.*',
            'doc/html/*.*',
            'doc/html/_modules/*.*',
            'doc/html/_modules/tugalib/*.*',
            'doc/html/_sources/*.*',
            'doc/html/_static/*.*',
            'examples/*.pytg'
        ],
        'pytuga': [
            'ipytuga/assets/*.*',
        ],
    },
    # data_files=DATA_FILES,
    zip_safe=False,
    **setup_kwargs
)
