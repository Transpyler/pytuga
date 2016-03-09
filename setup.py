import os
import sys
from glob import glob
from setuptools import setup, find_packages

NAME = 'pytuga'
VERSION = '0.7.6-8'
REQUIRES = []  # 'PyQt5' is not supported in PyPI

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
base, _ = os.path.split(__file__)
version_file = os.path.join(base, 'src', 'tugalib', 'version.py')
with open(version_file, 'w') as F:
    F.write('__version__ = %r\n' % VERSION)

# Fix possible bug in Windows which does not generate the gui script
console_scripts = ['pytuga = pytuga.__main__:main']
gui_scripts = ['tugalinhas = tugalinhas.__main__:main']
if sys.platform.startswith('win'):
    gui_scripts = ['tugalinhas_window = tugalinhas.__main__:main']
    console_scripts.append('tugalinhas = tugalinhas.__main__:main')

# Collect data files
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

# Fix path separator
for i, (path, files) in enumerate(DATA_FILES):
    path = os.path.sep.join(path.split('/'))
    files = [os.path.sep.join(f.split('/')) for f in files]
    DATA_FILES[i] = (path, files)

# Run setup() function
setup(
    name=NAME,
    version=VERSION,
    description='Interpretador de Pytuguês: um Python com sotaque lusitano.',
    author='Fábio Macêdo Mendes',
    author_email='fabiomacedomendes@gmail.com',
    url='https://github.com/fabiommendes/pytuga',
    long_description=('''
    Pytuguês é uma linguagem de programação que modifica a sintaxe do
    Python para aceitar comandos em português. A linguagem foi desenvolvida
    como um superconjunto do Python, mas que aceita comandos em português que
    permitem expressar programas de maneira natural na forma de pseudocódigo.
    programa
    O único objetivo do Pytuguês é facilitar o aprendizado de programação. Uma
    vez que os conceitos básicos forem apreendidos, a transição para uma
    linguagem real (no caso o Python) torna-se bem gradual e natural.

    Este pacote possui alguns programas:

        * pytuga: o interpretador de Pytuguês.
        * tugalinhas: programa educativo que permite ensinar programação
          visualmente, controlando o movimento de um personagem no espírito da
          linguagem LOGO.
    '''),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries',
    ],

    #
    # Packages and depencies
    #
    package_dir={'': 'src'},
    packages=find_packages('src'),
    install_requires=REQUIRES,

    #
    # Scripts
    #
    entry_points={
        # Stand alone tugalinhas?
        'console_scripts': console_scripts,
        'gui_scripts': gui_scripts,
    },

    #
    # Data files
    #
        package_data={
            'tugalinhas': [
                '*.*',
                'doc/html/*.*',
                'doc/html/_modules/*.*',
                'doc/html/_modules/tugalib/*.*',
                'doc/html/_sources/*.*',
                'doc/html/_static/*.*',
            ]},
        data_files=DATA_FILES,
    zip_safe=False,
)
