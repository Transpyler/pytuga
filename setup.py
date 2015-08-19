import os
from distutils.core import setup
import setuplib

NAME = 'pytuga'
VERSION = '0.1a'
REQUIRES = ['PyQt4']

setup(
    name=NAME,
    version=VERSION,
    description='Interpretador de Pytuguês: um Python com sotaque lusitano.',
    author='Fábio Macêdo Mendes',
    author_email='fabiomacedomendes@gmail.com',
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
        * tugalinhas: programa educativo para ensinar programação visualmente,
          controlando o desenho de um personagem no espírito da linguagem LOGO.
    '''),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries',
    ],
    package_dir={'': 'src'},
    packages=setuplib.get_packages(),
    requires=REQUIRES,
)
