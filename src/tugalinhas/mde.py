import os
import uuid
from PyQt4 import QtGui


class MultiDocumentEditor:

    '''Holds a collection of QsciScintilla editor documents.
    '''

    def __init__(self, parent, doctype):
        self.main_window = parent
        self._modified = False
        self._doctype = doctype
        doctype.editor = self  # Strange Hack?
        self.box = QtGui.QStackedLayout()
        self.documents = {}  # docid:QsciScintilla instances
        self.pages = {}  # docid:QStackedLayout pages
        self._doc = None
        self.docid = None
        self.title = None
        self._fontsize = 0  # Relative to base size
        self.setup_selector()
        docid = self.new()
        self.switchto(docid)

    def setup_selector(self):
        self._selector = self.main_window.ui.mselect

    def new(self):
        '''start a new blank document.'''

        doc = self._doctype(self.main_window)
        doc.zoomTo(self._fontsize)
        docid = uuid.uuid4().hex
        self.documents[docid] = doc
        page = self.box.addWidget(doc)
        self.pages[docid] = page
        doc.docid = docid
        self._selector.addItem('', docid)
        self.settitle(doc)

        return docid

    def clear_all(self):
        while self.box.count():
            item = self.box.itemAt(0)
            self.box.removeItem(item)
        self._selector.clear()

    def add(self, txt):
        '''Add a new document and load it with txt.
        '''

        docid = self.new()
        doc = self.documents[docid]
        doc.setText(txt)
        doc.setModified(False)
        self.settitle(doc)
        self.switchto(docid)

    def addexternal(self, fp):
        '''Add a new document and load it with the text
            from the external file at path fp.

            return the new document.
            '''

        for docid, doc in list(self.documents.items()):
            if doc._filepath == fp:
                # this external file already added
                self.switchto(docid)
                return
        txt = open(fp).read()
        self.add(txt)
        self._doc._filepath = fp
        self.settitle()
        return self._doc

    def settitle(self, doc=None):
        '''set the title for the current document.
        '''

        if doc is None:
            doc = self._doc

        txt = str(doc.text(0)).strip()

        if doc._filepath is not None:
            _, title = os.path.split(doc._filepath)
        elif txt == '':
            title = 'Untitled'
        else:
            title = txt

        if title == doc.title:
            return

        selector = self._selector
        idx = 0
        for idx in range(selector.count()):
            item_docid = selector.itemData(idx)
            if item_docid == doc.docid:
                selector.setItemText(idx, title)
                break

        doc.title = title

    def switchto(self, docid):
        '''switch to document docid'''

        old_doc = self._doc
        doc = self.documents[docid]
        if doc == old_doc:
            return

        page = self.pages[docid]
        self.box.setCurrentIndex(page)
        self._selector.setCurrentIndex(page)

        self.docid = docid
        self._doc = doc
        self.settitle()

    def shownext(self):
        '''show the next document in the stack.'''

        idx = self.box.currentIndex()
        count = self.box.count()
        if idx < count - 1:
            self.box.setCurrentIndex(idx + 1)
        item = self.box.currentWidget()
        self.switchto(item.docid)

    def showprev(self):
        '''show the previous document in the stack.'''

        idx = self.box.currentIndex()
        if idx > 0:
            self.box.setCurrentIndex(idx - 1)
        item = self.box.currentWidget()
        self.switchto(item.docid)

    def promote(self):
        '''move the current document up 1 place in the stack'''

        idx = self.box.currentIndex()

        if idx <= 0:
            return

        doc = self._doc
        docid = doc.docid
        otherdoc = self.box.widget(idx - 1)
        otherdocid = otherdoc.docid

        self.box.takeAt(idx)
        self.box.insertWidget(idx - 1, doc)

        self.pages[docid] = idx - 1
        self.pages[otherdocid] = idx

        self._modified = True
        self.main_window.show_modified_status()

        self.switchto(docid)

    def demote(self):
        '''move the current document down 1 place in the stack'''

        idx = self.box.currentIndex()
        count = self.box.count()

        if idx >= count - 1:
            return

        doc = self._doc
        docid = doc.docid
        otherdoc = self.box.widget(idx + 1)
        otherdocid = otherdoc.docid

        self.box.takeAt(idx)
        self.box.insertWidget(idx + 1, doc)

        self.pages[docid] = idx + 1
        self.pages[otherdocid] = idx

        self._modified = True
        self.main_window.show_modified_status()

        self.switchto(docid)

    def setfontsize(self, size):
        self._fontsize = size
        for doc in self.documents.values():
            doc.zoomTo(size)

    def zoomin(self):
        self.setfontsize(self._fontsize + 1)

    def zoomout(self):
        self.setfontsize(self._fontsize - 1)

    def setFocus(self):
        self._doc.setFocus()

    def wrap(self, on=True):
        for doc in self.documents.values():
            if on:
                doc.wrap()
            else:
                doc.nowrap()

    def line_numbers(self, on=True):
        for doc in self.documents.values():
            if on:
                doc.show_line_numbers()
            else:
                doc.hide_line_numbers()

    def selectline(self, n):
        '''highlight line number n'''

        lineno = n - 1
        doc = self._doc
        line = doc.text(lineno)
        self._doc.setSelection(lineno, 0, lineno, len(line))
