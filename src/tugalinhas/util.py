'''
Assorted utility functions
'''
# try:
# Extinguished this file in order to make other .py files more self-contained
# All routines that were in here have been moved to the files that use them
# (and their names have been preceded by an underscore)
#
# '''
# Assorted utility functions
# '''
# from PyQt5 import QtGui, QtCore, QtWidgets, Qsci, Qt, QtSvg, uic  # @UnusedImport
#
#
#
#
# from functools import wraps as _wraps
# # from .mathutil import Vec as _Vec
#
# # def vecargsmethod(func):
# #     '''
# #     Decorates a function of a vec object to accept the following signatures:
# #
# #         func(vec, **kwds)
# #         func(x, y, **kwds)
# #
# #     A Vec object is always passed to the given implementation.
# #     '''
# #     @_wraps(func)
# #     def decorated(self, x, y=None, **kwds):
# #         if y is None:
# #             try:
# #                 x, y = x
# #             except ValueError:
# #                 raise ValueError('expected 2 elements, got %s' % len(x))
# #
# #             return func(self, _Vec(x, y), **kwds)
# #         else:
# #             return func(self, _Vec(x, y), **kwds)
# #     return decorated
#
# def xyargsmethod(func):
#     '''
#     Decorates a function func(x, y) to accept the following signatures:
#
#         func(vec, **kwds)
#         func(x, y, **kwds)
#
#     The values x, y are always passed separately to the given implementation.
#     '''
#     @_wraps(func)
#     def decorated(self, x, y=None, **kwds):
#         if y is not None:
#             try:
#                 x, y = x
#             except ValueError:
#                 raise ValueError('expected 2 elements, got %s' % len(x))
#
#         return func(self, x, y, **kwds)
#     return decorated
#
# # def splitindent(line):
# #     '''Split a string into an indentation part and the rest of the string.
# #
# #     Only process indentation of the first line of the string.'''
# #
# #     idx = 0
# #     while line[idx] in [' ', '\t']:
# #         idx += 1
# #     return line[:idx], line[idx:]
#
# #
# # Qt Namespace imports
# #
# QColor = QtGui.QColor
# QFont = QtGui.QFont
#     from PyQt5 import QtGui, QtCore, QtWidgets, Qsci, Qt, QtSvg, uic  # @UnusedImport
# except AttributeError:
#     from PyQt4 import QtGui, QtCore, Qsci, Qt, QtSvg, uic  # @UnusedImport
#     QtWidgets = QtGui
#
# from functools import wraps as _wraps
# from .mathutil import Vec as _Vec
#
# def vecargsmethod(func):
#     '''
#     Decorates a function of a vec object to accept the following signatures:
#
#         func(vec, **kwds)
#         func(x, y, **kwds)
#
#     A Vec object is always passed to the given implementation.
#     '''
#     @_wraps(func)
#     def decorated(self, x, y=None, **kwds):
#         if y is None:
#             try:
#                 x, y = x
#             except ValueError:
#                 raise ValueError('expected 2 elements, got %s' % len(x))
#
#             return func(self, _Vec(x, y), **kwds)
#         else:
#             return func(self, _Vec(x, y), **kwds)
#     return decorated
#
# def xyargsmethod(func):
#     '''
#     Decorates a function func(x, y) to accept the following signatures:
#
#         func(vec, **kwds)
#         func(x, y, **kwds)
#
#     The values x, y are always passed separately to the given implementation.
#     '''
#     @_wraps(func)
#     def decorated(self, x, y=None, **kwds):
#         if y is not None:
#             try:
#                 x, y = x
#             except ValueError:
#                 raise ValueError('expected 2 elements, got %s' % len(x))
#
#         return func(self, x, y, **kwds)
#     return decorated
#
# def splitindent(line):
#     '''Split a string into an indentation part and the rest of the string.
#
#     Only process indentation of the first line of the string.'''
#
#     idx = 0
#     while line[idx] in [' ', '\t']:
#         idx += 1
#     return line[:idx], line[idx:]
#
# #
# # Qt Namespace imports
# #
# QColor = QtGui.QColor
# QFont = QtGui.QFont