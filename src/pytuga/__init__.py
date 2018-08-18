__version__ = '0.13.0'
__author__ = 'F\xe1bio Mac\xeado Mendes'

from .transpyler import PytugaTranspyler

# Update core functions (we do not update globals() to make static analysis
# tools happy).
_ns = PytugaTranspyler.core_functions()

init, namespace = _ns.pop('init'), _ns.pop('namespace')
exec, eval = _ns.pop('exec'), _ns.pop('eval')
compile, transpile = _ns.pop('compile'), _ns.pop('transpile')
is_incomplete_source = _ns.pop('is_incomplete_source')

assert not _ns, _ns
del _ns
