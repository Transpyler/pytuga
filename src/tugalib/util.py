import warnings
import functools


#
# Unidecode function is copied here in order to avoid a simple dependency
# Extracted from: https://pypi.python.org/pypi/Unidecode
#
unidecode_cache = {}


def unidecode(string):
    """Transliterate an Unicode object into an ASCII string

    >>> unidecode(u"\u5317\u4EB0")
    "Bei Jing "
    """

    retval = []

    for char in string:
        codepoint = ord(char)

        if codepoint < 0x80: # Basic ASCII
            retval.append(str(char))
            continue

        if codepoint > 0xeffff:
            continue # Characters in Private Use Area and above are ignored

        if 0xd800 <= codepoint <= 0xdfff:
            warnings.warn(  "Surrogate character %r will be ignored. "
                            "You might be using a narrow Python build." % (char,),
                            RuntimeWarning, 2)

        section = codepoint >> 8   # Chop off the last two hex digits
        position = codepoint % 256 # Last two hex digits

        try:
            table = unidecode_cache[section]
        except KeyError:
            try:
                mod = __import__('unidecode.x%03x'%(section), globals(), locals(), ['data'])
            except ImportError:
                unidecode_cache[section] = None
                continue   # No match: ignore this character and carry on.

            unidecode_cache[section] = table = mod.data

        if table and len(table) > position:
            retval.append( table[position] )

    return ''.join(retval)


#
# Controle de funções sinônimas
#
def synonyms(*args):
    '''Decorador que marca sinônimos de uma função'''

    fmt_args = ['**%s**' % x for x in args]

    def decorator(func):
        if len(args) == 1:
            data = fmt_args[0]
        else:
            data = ', '.join(fmt_args[:-1])
            data += ' ou ' + fmt_args[-1]

        func.__synonyms__ = args
        func.__doc__ += (
            '\n\n'
            'Notes\n'
            '-----\n\n'
            'Também pode ser chamada como ' + data)
        return func
    return decorator


def accented_keywords(func):
    """Decorate function so all accented keywords are passed unaccented to the
    real implementation"""

    @functools.wraps(func)
    def decorated(*args, **kwargs):
        decode = unidecode
        kwargs = {decode(k): v for (k, v) in kwargs.items()}
        return func(*args, **kwargs)

    return decorated


def collect_synonyms(namespace, add_unaccented=True):
    """Return a dictionary with all synonyms found in the given namespace.

    Raise a ValueError for name conflicts.
    """

    D = {}
    unaccent = unidecode
    msg = '%s is present in namespace, but is also a synonym of %s'

    # Collect aliases
    for attr, func in namespace.items():
        try:
            for alias in func.__synonyms__:
                D[alias] = func
                if alias in namespace:
                    raise ValueError(msg % (alias, attr))
        except AttributeError:
            continue
    D.update(namespace)

    # Collect unaccented
    for name, func in list(D.items()):
        no_accent = unaccent(name)
        if no_accent != name:
            if no_accent in D:
                raise ValueError(msg % (no_accent, name))
            D[no_accent] = func

    return D


def register_synonyms(global_ns):
    """Register all synonyms in the given namespace dictionary"""

    D = collect_synonyms(global_ns)
    global_ns.update(D)
