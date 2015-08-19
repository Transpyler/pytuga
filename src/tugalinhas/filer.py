import os
import time
import zipfile
from tugalinhas import LOG


def foo(fp):
    return os.path.splitdrive(fp)[0]


def _related_dir(fp):
    '''return the directory name related to path fp
        that should be used for storing files when not in
        savesingle (.pyn) mode.
    '''
    dirname, fname = os.path.split(fp)
    fbase, _fext = os.path.splitext(fname)
    fpd = os.path.join(dirname, fbase + '_pynd')

    return fpd


def writeable(fp, savesingle):
    '''try to write to the given path (and the related directory if
        savesingle is False).

    return True if sucessful, False otherwise
    '''

    try:
        fd = open(fp, 'w')
        fd.write('test')
        fd.close()
        os.remove(fp)
    except IOError:
        return False

    if savesingle:
        return True
    else:
        fpd = _related_dir(fp)
        if not os.path.exists(fpd):
            return False
        fp = os.path.join(fpd, 'test')
        return writeable(fp, True)


def writefile02(self, fp, docs, backup=False):
    '''Write out open files (docs) to file path fp.

    Version 02


    Knows how to deal with 3 kinds of files:
        EXTERNAL files start with '_@@EXTERNAL@@_'
        PYND files (stored in related _pynd directory)
        INTERNAL files

    Creates a zip file called *.pyn and if necessary the related
        directory (like fp with name modified to end with _pynd)
    Also saves file manifest and history in .pyn zipfile.


    When saving INTERNAL files, puts all files in to a folder first
        to make it match the EXTERNAL file saves better.

    '''
    VERSION = b'pyn02'

    _, fn = os.path.split(fp)
    fbase, _ = os.path.splitext(fn)
    if not fbase.endswith('_pynd'):
        fbase = fbase + '_pynd'

    z = zipfile.ZipFile(fp, 'w')

    manifest = []

    for n, doc in enumerate(docs):
        modified = doc.isModified()
        cline, ccol = doc.getCursorPosition()
        code = doc.cleancode()
        doc.beginUndoAction()
        doc.selectAll()
        doc.removeSelectedText()
        doc.insert(code)
        doc.setCursorPosition(cline, ccol)
        doc.setModified(modified)
        doc.endUndoAction()

        LOG.info('writing %s' % doc)
        if not backup and doc._filepath is not None:
            efp = doc._filepath
            manifest.append(efp)

            LOG.info('external: %s' % efp)

            if efp.startswith('_@@'):
                dirname, _ = os.path.split(fp)
                if dirname:
                    efp = efp.replace('_@@', dirname)
                else:
                    efp = efp[4:]
            self._remwatcher(efp)
            f = open(efp, 'w')
            f.write(code)
            f.close()
            self._addwatcher(efp, doc)

            doc.setModified(False)

        else:
            arcname = '%05d.py' % n

            zipi = zipfile.ZipInfo()
            zipi.filename = os.path.join(fbase, arcname)
            manifest.append(zipi.filename)
            zipi.compress_type = zipfile.ZIP_DEFLATED
            zipi.date_time = time.localtime()
            zipi.external_attr = 0o644 << 16
            zipi.comment = VERSION
            z.writestr(zipi, code.encode('utf-8'))

    historyname = '@@history@@'
    history = '\n'.join(self.interpretereditor.history)

    zipi = zipfile.ZipInfo()
    zipi.filename = os.path.join(fbase, historyname)
    zipi.compress_type = zipfile.ZIP_DEFLATED
    zipi.date_time = time.localtime()
    zipi.external_attr = 0o644 << 16
    zipi.comment = VERSION
    z.writestr(zipi, history)  # .encode('utf-8'))

    manifestname = '@@manifest@@'
    zipi = zipfile.ZipInfo()
    zipi.filename = os.path.join(fbase, manifestname)
    zipi.compress_type = zipfile.ZIP_DEFLATED
    zipi.date_time = time.localtime()
    zipi.external_attr = 0o644 << 16
    zipi.comment = VERSION
    manifeststr = '\n'.join(manifest)
    z.writestr(zipi, manifeststr.encode('utf-8'))

    z.close()
