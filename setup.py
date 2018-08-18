import os
import re
import sys

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

# Extract version
init = open(os.path.join('src', 'pytuga', '__init__.py')).read()
m = re.search(r"__version__ ?= ?'([0-9a-z.]+)'", init)
version = m.group(1)


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
        'qturtle~=0.5.0',
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
