# Copyright 2010-2013 Lee Harr
# Copyright 2010-2013  Fábio Macêdo Mendes
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

#
# Some configuration parameters
#
VERSION = __version__ = '0.2a'
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
BACKUP_FILENAME = 'tugalinhas_backup~%s.pytg'
BUG_URL = 'http://...'  # FIXME


def _get_data_dir():
    '''Return default data directory'''

    # Executing from src
    data = os.path.abspath('../../data')
    if os.path.exists(data):
        return data

    # Fallback to a local install
    base = os.path.expanduser('~/.local/')
    localdir = os.path.join(base, 'share', 'tugalinhas')
    if os.path.exists(localdir):
        return localdir

    # Look for a system install
    base = os.path.abspath(sys.prefix)
    sysdir = os.path.join(base, 'share', 'tugalinhas')
    if os.path.exists(sysdir):
        return sysdir

    raise RuntimeError('no data directory was found, check your installation')
DATA_DIR = _get_data_dir()
UI_DIR = os.path.join(DATA_DIR, 'ui')


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
DOC_DIR = _get_doc_dir()

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
