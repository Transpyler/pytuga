# Copyright 2013 Lee Harr
#
# This file is part of pynguin.
# http://pynguin.googlecode.com/
#
# Pynguin is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Pynguin is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Pynguin.  If not, see <http://www.gnu.org/licenses/>.

import os
import pytest
import ntpath
import posixpath

from pynguin import filer


def test_monkeypatch(monkeypatch):
    monkeypatch.setattr(os, 'path', ntpath)
    fp = 'c:\\foo\\bar'
    assert filer.foo(fp) == 'c:'

def for_all_os_path(f):
    dec = pytest.mark.parametrize(('path_module',), [
                                            (ntpath,), 
                                            (posixpath,)])

    import inspect
    sig = inspect.signature(f)
    
    if 'tmpdir' not in sig.parameters:
        @dec
        def fpatch_faop(monkeypatch, path_module, *args, **kw):
            monkeypatch.setattr(os, 'path', path_module)
            return f(*args, **kw)
        return fpatch_faop
    else:
        @dec
        def fpatch_faopt(monkeypatch, path_module, tmpdir, *args, **kw):
            monkeypatch.setattr(os, 'path', path_module)
            return f(tmpdir, *args, **kw)
        return fpatch_faopt


@for_all_os_path
def test_paths():
    fp = 'foo/bar/baz.py'
    assert os.path.splitext(fp)[1] == '.py'

@for_all_os_path
def test_splitdrive():
    fp = 'c:\\foo\\bar'
    drive = os.path.splitdrive(fp)[0]
    if os.path is ntpath:
        assert  drive == 'c:'
    elif os.path is posixpath:
        assert drive == ''

@for_all_os_path
def test_related_dir_absolute():
    fp = '/foo/bar/baz.pyn'
    rel = filer._related_dir(fp)
    normpath = os.path.normpath
    assert normpath(rel) == normpath('/foo/bar/baz_pynd')

@for_all_os_path
def test_related_dir_relative():
    fp = 'foo/bar/baz.pyn'
    rel = filer._related_dir(fp)
    normpath = os.path.normpath
    assert normpath(rel) == normpath('foo/bar/baz_pynd')

@for_all_os_path
def test_related_dir_not_pyn():
    fp = '/foo/bar/baz'
    rel = filer._related_dir(fp)
    normpath = os.path.normpath
    assert normpath(rel) == normpath('/foo/bar/baz_pynd')

@for_all_os_path
def test_writeable_savesingle(tmpdir):
    fp = 'test_writeable.pyn'
    fp = str(tmpdir.join(fp))
    assert filer.writeable(fp, True)

@for_all_os_path
def test_writeable_not_savesingle_no_related_dir(tmpdir):
    fp = 'test_writeable.pyn'
    fp = str(tmpdir.join(fp))
    assert not filer.writeable(fp, False)

@for_all_os_path
def test_writeable_not_savesingle_with_related_dir(tmpdir):
    fp = str(tmpdir.join('test_writeable.pyn'))
    reldir = filer._related_dir(fp)
    os.mkdir(reldir)
    assert filer.writeable(fp, False)
    os.rmdir(reldir)

@for_all_os_path
def test_writeable_not_savesingle_with_related_dir(tmpdir):
    fp = str(tmpdir.join('test_writeable.pyn'))
    reldir = filer._related_dir(fp)
    os.mkdir(reldir)
    assert filer.writeable(fp, False)
    os.rmdir(reldir)
