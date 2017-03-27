"""
This class implements the namespace of turtle-art functions.

It can be overriden in order to create a different set of functions, either by
inclusion of exclusion of items.
"""

import io
import sys
from collections import MutableMapping

from logo.mathutils import Vec
from logo.utils import vecargsmethod, alias


#
# Pytuguês -- default temporário
#
# TODO: split Python from Pytuguês versions of tugalinhas
#       The python version can be called "Turtle" or "Logo"
#



def helpstr(*args):
    """Returns the output of the help() function as a string"""

    stdout, sys.stdout = sys.stdout, io.StringIO()
    try:
        help(*args)
        data = sys.stdout.getvalue()
    finally:
        sys.stdout = stdout
    return data


def function_description(method):
    """
    Format function description to show in turtlefunc() help.
    """

    data = helpstr(method).partition('\n\n')[2]
    head, _, descr = data.partition('\n')
    head = head.partition(' method')[0].rjust(20)
    descr = descr.partition('\n')[0].lstrip()
    data = '%s -- %s' % (head, descr)
    alias = getattr(method, 'alias_list', None)
    if alias:
        data += '\n' + (', '.join(alias)).rjust(20)
    return data
