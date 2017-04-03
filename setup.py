# -*- coding: utf8 -*-
import os
import sys
from glob import glob
from setuptools import setup, find_packages
from setuptools.command.install import install as _install
from setuptools.command.develop import develop as _develop


NAME = 'pytuga'
AUTHOR = 'Fábio Macêdo Mendes'
DIRNAME = os.path.dirname(__file__)

# Warn user about missing PyQt libraries. These cannot go into REQUIRES list
# since PyQt is not instalable via pip
try:
    import PyQt5.QtSvg
    import PyQt5.Qsci
except ImportError:
    import warnings

    warnings.warn(
        'Please install PyQt5, PyQt5.QtSvg and PyQt5.Qsci!\n'
        'Check your distribution packages or go to the website bellow:\n'
        '    https://riverbankcomputing.com/software/pyqt/download5\n')

# Rewrite __version__.py in tugalib
VERSION = open('VERSION', encoding='utf8').read().strip()
version_file = os.path.join(DIRNAME, 'src', 'pytuga', '__meta__.py')
try:
    with open(version_file, 'w', encoding='utf8') as F:
        F.write('__version__ = %r\n'
                '__author__ = %r' % (VERSION, AUTHOR))
except UnicodeDecodeError:
    # Read the docs builder has a problem with encoding. Maybe old Python3
    # versions?
    pass

# Collect data files
if sys.platform.startswith('win'):
    # TODO: figure out where these files should be in Windows
    DATA_FILES = []
else:
    DATA_FILES = [
        ('share/icons/hicolor/scalable/apps', ['data/icons/pytuga.svg']),
        ('share/icons/hicolor/scalable/mimetypes',
         ['data/icons/text-x-pytuga.svg']),
        ('share/mime', ['data/pytg.xml']),
        ('share/applications', ['data/pytuga.desktop']),
        ('share/doc/pytuga', ['README.rst']),
        ('share/doc/examples', glob('data/examples/*.pytg')),
        ('share/gtksourceview-3.0/language-specs', ['data/pytuga.lang']),
    ]

# Add documentation files
for path, _, files in os.walk('doc/build/html'):
    docfiles = []
    DATA_FILES.append(('doc/pytuga' + path[14:], docfiles))
    for file in files:
        docfiles.append('%s/%s' % (path, file))

# Fix path separators in windows (necessary?)
if os.path.sep != '/':
    for i, (path, files) in enumerate(DATA_FILES):
        path = os.path.sep.join(path.split('/'))
        files = [os.path.sep.join(f.split('/')) for f in files]
        DATA_FILES[i] = (path, files)


# Wraps command classes to register ipytuga kernel
def wrapped_cmd(cmd):
    class Command(cmd):
        def run(self):
            cmd.run(self)
            #from pytuga.ipytuga.setup import setup_assets
            #setup_assets(True)

    return Command


# Run setup() function
distribution = setup(
    name=NAME,
    version=VERSION,
    description='Interpretador de Pytuguês: um Python com sotaque lusitano.',
    author=AUTHOR,
    author_email='fabiomacedomendes@gmail.com',
    url='https://github.com/fabiommendes/pytuga',
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
        'pytugacore',
        'qturtle',
    ],

    # Wrapped commands (for ipytuga)
    cmdclass={
        'install': wrapped_cmd(_install),
        'develop': wrapped_cmd(_develop),
    },

    # Scripts
    entry_points={
        # Stand alone tugalinhas?
        'console_scripts': [
            'pytuga = pytuga.__main__:main',
        ],
    },

    # Data files
    package_data={
        'tugalinhas': [
            '*.*',
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
    data_files=DATA_FILES,
    zip_safe=False,
)

# Adds a symbolic link from executables in $HOME/.local/bin to $HOME/bin, if it
# exists and if it is installed with the --user option.
binfolder = os.path.join(os.path.expanduser('~'), 'bin')
pytuga = os.path.join(binfolder, 'pytuga')
if ('user' in distribution.get_option_dict('install') and
        os.path.exists(binfolder) and not os.path.exists(pytuga)):

    try:
        for file in ['tugalinhas', 'pytuga']:
            local_bin = os.path.expanduser(
                os.path.join('~', '.local', 'bin', file))
            home_bin = os.path.expanduser(os.path.join('~', 'bin', file))
            os.symlink(local_bin, home_bin)
    except FileNotFoundError:
        pass
