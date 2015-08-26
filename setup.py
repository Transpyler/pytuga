#-*-coding: utf8-*-
import os
from setuptools import setup, find_packages

NAME = 'pytuga'
VERSION = '0.3a1'
REQUIRES = ['PyQt4', 'PyQt4.Qsci', 'bidict', 'turtle']


# Rewrite __version__.py in tugalib
base, _ = os.path.split(__file__)
version_file = os.path.join(base, 'src', 'tugalib', 'version.py')
with open(version_file, 'w') as F:
    F.write('__version__ = %r\n' % VERSION)

setup(
    #
    # Basic meta
    #
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
    requires=REQUIRES,

    #
    # Scripts
    #
    entry_points={
        # Stand alone tugalinhas?
        #'eggexecutable': [
        #    'pytuga = tugalinhas.main:run',,
        #],
        'console_scripts': [
            'pytuga = pytuga.main:run',          # Main interpreter
            # 'tugashell = tugashell.main:run',    # A better shell, TBR
        ],
        'gui_scripts': [
            'tugalinhas = tugalinhas.main:run',  # Graphical environment
        ]
    },

    #
    # Data files
    #
    include_package_data=True,
)
