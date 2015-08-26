# Copyright 2015 Fábio Macêdo Mendes
# Copyright 2010-2013 Lee Harr
#
# Tugalinhas is a fork/adaptation of Pynguin for teaching Python to Portuguese
# speaking communities using the "Pytuguês" programming language. The original
# Pyguin program was created by Lee Harr and hosted at
#
# http://pynguin.googlecode.com/
#
# Tugalinhas would not be possible without this prior code base. Tugalinhas is
# hosted at
#
# http://tugalinhas...
#
# Tugalinhas is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Pen is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Tugalinhas.  If not, see <http://www.gnu.org/licenses/>.


import os
import sys
import logging
from tugalib import __version__

#
VERSION = __version__
NAME = 'tugalinhas'
FULL_NAME = '%s-%s' % (NAME, VERSION)


# =============================================================================
#                 Start main tugalinhas sub-systems
# =============================================================================

#
# Logging
#
LOG = logging.getLogger('TugalinhasLogger')
LOG_FILENAME = 'logfile.log'

#
# System paths and URLs
#
BACKUP_FILENAME = '~tugalinhas-%s.pytg-bak'
BUG_URL = 'http://...'  # FIXME
DATA_PATH = os.path.split(__file__)[0]
TRANSLATIONS_PATH = os.path.join(DATA_PATH, 'translations', 'tugalinhas_')
SHARED_ART_PATH = os.path.join(DATA_PATH, 'ui', 'shared-art.svg')
UI_FILES_PATH = os.path.join(DATA_PATH, 'ui')


def _get_doc_dir():
    '''Return default documentation directory'''

    # Executing from src
    doc = os.path.abspath('../../doc')
    if os.path.exists(doc):
        return doc

    # Fallback to a local install
    base = os.path.expanduser('~/.local/')
    localdir = os.path.join(base, 'share', 'doc', 'tugalinhas')
    if os.path.exists(localdir):
        return localdir

    # Look for a system install
    base = os.path.abspath(sys.prefix)
    sysdir = os.path.join(base, 'share', 'doc', 'tugalinhas')
    if os.path.exists(sysdir):
        return sysdir

    raise RuntimeError('no doc directory was found, check your installation')
DOC_DIR = ''  # _get_doc_dir()

#
# Colors definitions
#
DEFAULT_COLOR = 0xff000000  # black
DEFAULT_BGCOLOR = '#ffffff'
DEFAULT_FILLCOLOR = 4284800110  # (100, 220, 110, 255)

#
# None-like non-None constant...
#
NODEFAULT = object()
NOTHING = object()

del os, sys, logging

if __name__ == '__main__':
    from tugalinhas.main import run
    run()
