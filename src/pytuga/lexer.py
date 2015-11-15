import keyword
import tokenize
from tokenize import TokenInfo
from tokenize import (NAME, OP, NEWLINE, EXACT_TOKEN_TYPES, NUMBER)


__all__ = ['transpile', 'compile', 'exec']
TOKEN_TYPE_NAME = {tt: attr for (attr, tt) in vars(tokenize).items()
                            if attr.isupper() and isinstance(tt, int)}
TOKEN_TRANSLATIONS = dict(
    # Loops
    enquanto='while',
    para='for',
    quebre='break',
    quebrar='break',
    continuar='continue',
    # continue='continue',
    # para cada='for'

    # Conditions
    se='if',
    senão='else',
    # ou então se='elif'
    # ou se='elif'

    # Singleton values
    Falso='False',
    falso='False',
    Verdadeiro='True',
    verdadeiro='True',
    nulo='None',
    Nulo='None',

    # Operators
    é='is',
    e='and',
    ou='or',
    não='not',
    em='in',
    na='in',
    no='in',
    como='as',

    # Function definition
    função='def',
    definir='def',
    defina='def',
    retorne='return',
    retornar='return',
    gere='yield',
    gerar='yield',

    # Error handling
    tente='try',
    tentar='try',
    exceção='except',
    finalmente='finally',
    # jogue erro='raise'?

    # Other
    apague='del',
    prossiga='pass',
    classe='class',
    importe='import',
    importar='import',
    #abrir='with'?
    # global='global',
)
PURE_PYTG_KEYWORDS = set(TOKEN_TRANSLATIONS)
PURE_PYTG_KEYWORDS.update({'repetir', 'repita', 'vezes', 'cada', 'de', 'até'})
KEYWORDS = set(PURE_PYTG_KEYWORDS)
KEYWORDS.update(keyword.kwlist)

class Token:

    '''Mutable token object.'''

    def __init__(self, data, type=None, start=None, end=None, line=None):

        # Start from TokenInfo object
        if isinstance(data, TokenInfo):
            assert all(x is None for x in [type, start, end, line])
            type, data, start, end, line = data

        elif isinstance(data, Token):
            assert all(x is None for x in [type, start, end, line])
            data, type, start, end, line = data

        elif isinstance(data, (int, float)):
            type = data
            data = None

        if start is not None:
            start = TokenPosition(start)
            if end is None:
                end = start + (0, len(data))
        if end is not None:
            end = TokenPosition(end)
        if type is None:
            # We are not using exact token types: the tokenizer converts all
            # of them to OP.
            if data in EXACT_TOKEN_TYPES:
                type = OP
            else:
                if data.isidentifier():
                    type = NAME
                else:
                    raise TypeError('could not recognize token: %r' % data)

        self.string = data
        self.type = type
        self.start = start
        self.end = end
        self.line = line

    def __eq__(self, other):
        if isinstance(other, Token):
            # Compares type only if string is not given
            if self.string is None or other.string is None:
                return self.type == other.type

            if self.string != other.string or self.type != other.type:
                return False

            for (x, y) in [(self.start, other.start),
                           (self.end, other.end),
                           (self.line, other.line)]:
                if x != y and None not in (x, y):
                    return False
            return True
        elif isinstance(other, (str, TokenInfo)):
            return self == Token(other)
        elif isinstance(other, (tuple, list)):
            if len(other) == 2:
                return self.string == other[0] and self.type == other[1]
            return self == Token(*other)
        else:
            return NotImplemented

    def __str__(self):
        return 'Token(%r, %s, %r, %r, %r)' % (self.string, TOKEN_TYPE_NAME[self.type],
                                              self.start, self.end, self.line)

    def __repr__(self):
        tname = TOKEN_TYPE_NAME[self.type]
        if self.string.isspace():
            return tname
        else:
            return '%s(%r)' % (tname, self.string)

    def __len__(self):
        return 5

    def __getitem__(self, idx):
        if idx == 0:
            return self.string
        elif idx == 1:
            return self.type
        elif idx == 2:
            return self.start
        elif idx == 3:
            return self.end
        elif idx == 4:
            return self.line
        elif -5 <= idx < 0:
            return self[5 + idx]
        else:
            raise IndexError(idx)

    def __iter__(self):
        yield from (self[i] for i in range(5))


    def to_token_info(self):
        '''Convert to TokenInfo object used by Python's tokenizer.'''

        return TokenInfo(
            self.type, self.string, self.start, self.end, self.line)


class TokenPosition(tuple):

    '''Represent the start or end position of a token and accept some basic
    arithmetic operations'''

    def __new__(cls, x, y=None):
        if y is None:
            x, y = x
        return tuple.__new__(cls, [x, y])

    def __add__(self, other):
        x, y = self
        a, b = other
        return TokenPosition(x + a, y + b)

    def __radd__(self, other):
        return self + other

    def __sub__(self, other):
        x, y = self
        a, b = other
        return TokenPosition(x - a, y - b)

    def __rsub__(self, other):
        x, y = self
        a, b = other
        return TokenPosition(a - x, b - y)

    @property
    def lineno(self):
        return self[0]

    @property
    def col(self):
        return self[1]


def compile(source, filename, mode, flags=0, dont_inherit=False):
    '''Similar to the built-in function compile().

    Works with Pytuguês code.'''

    source = transpile(source)
    return __builtins__['compile'](source, filename, mode, flags, dont_inherit)


def exec(object, locals=None, globals=None):
    '''Similar to the built-in function exec().

    Works with Pytuguês code.'''

    if isinstance(object, str):
        object = transpile(object)
    return __builtins__['exec'](object, locals, globals)


def transpile(src):
    '''Convert a Pytuguês (Pytuguese?) source to Python.'''

    # Avoid problems with empty token streams
    if not src or src.isspace():
        return src

    # Convert and process...
    else:
        tokens = fromstring(src)
        transpiled_tokens = transpile_tk(tokens)
        result = tostring(transpiled_tokens)
        return result


def transpile_tk(tokens):
    '''Transpile a sequence of Token objects representing a Pytuguês code into
    Python'''

    # We pass several times through the token stream looking for direct
    # translations of Pytuguês tokens to Python.

    # First we look for invalid sequences that could be erroneously validated
    # in future passes
    matches = [
        ('faça', 'faça'), ('faça', 'fazer'), ('fazer', 'faça'),
        ('então', 'então'),
    ]
    iterator = token_find(tokens, matches)
    while False:
        try:
            idx, match = next(iterator)
            iterator.send(['raise', SyntaxError])
        except StopIteration:
            break

    # The second step is to handle sequence of Pytuguês tokens that can be
    # replaced by equivalent sequences of Python tokens
    convs = {
        # Block ending
        ('faça', ':') : Token(':'),
        ('fazer', ':'): Token(':'),

        # Loops
        ('para', 'cada'): Token('for'),

        # Conditions
        ('então', 'faça'): Token('faça'),
        ('então', ':'): Token(':'),
        ('ou', 'então', 'se'): Token('elif'),
        ('ou', 'se'): Token('elif'),

        # Definitions
        ('definir', 'função'): Token('def'),
        ('defina', 'função'): Token('def'),
        ('definir', 'classe'): Token('class'),
        ('defina', 'classe'): Token('class'),
    }
    iterator = token_find(tokens, convs)
    while True:
        try:
            idx, match = next(iterator)
            iterator.send(['subs', [convs[match]]])
        except StopIteration:
            break

    # Now we apply simple single token translations
    for i, tk in enumerate(tokens):
        new = TOKEN_TRANSLATIONS.get(tk.string, tk)
        if new is not tk:
            new = Token(new, start=tk.start)
            tokens[i] = new

    # Handle special Pytuguês-only commands
    tokens = process_repeat_command(tokens)
    tokens = process_range_command(tokens)

    return tokens


def token_find(tokens, matches, start=0):
    '''Coroutine that iterates over list of tokens yielding pairs of
    (index, match) for each match in the token stream. The `matches` attribute
    must be a sequence of token sequences.

    The caller may send commands to the coroutine to take some action for each
    match found.

    There are a few supported actions:
        it.send('raise'):
            Raises a SyntaxError for an unexpected token in the matched position
        it.send(['subs', L])
            Substitute the match by the list of tokens L.
        it.send(['seek', index])
            Jumps iteration to the given index.
    '''

    matches = list(matches)
    tk_matches = \
        [tuple(Token(tk) for tk in seq) for seq in matches]
    tk_matches = \
        [tuple((tk.string, tk.type) for tk in seq) for seq in tk_matches]
    tk_idx = start

    while tk_idx < len(tokens):
        for match_idx, tkmatch in enumerate(tk_matches):
            if tk_idx + len(tkmatch) > len(tokens):
                continue

            if all(tokens[tk_idx + k] == tk for (k, tk) in enumerate(tkmatch)):
                matchsize = len(tkmatch)

                # Yield value and try to receive commands from sender
                cmd = yield (tk_idx, matches[match_idx])
                while cmd:
                    cmd, value = cmd
                    if cmd == 'raise':
                        raise value
                    elif cmd == 'subs':
                        line = tokens[tk_idx].line
                        for _ in range(max(len(value) - matchsize, 0)):
                            tokens.insert(tk_idx, None)
                        for _ in range(max(matchsize - len(value), 0)):
                            del tokens[tk_idx]
                        tokens[tk_idx:tk_idx + len(value)] = value
                        for tk in value:
                            tk.line = line
                    elif cmd == 'seek':
                        tk_idx = value - 1
                    else:
                        raise ValueError('invalid command: %r' % cmd)
                    cmd = yield
                tk_idx += 1
        tk_idx += 1
    return


def process_repeat_command(tokens):
    '''Handles "repita/repetir".

    Converts command::

        repetir <N> vezes:
            <BLOCO>

        repita <N> vezes:
            <BLOCO>

    into::

        for ___ in range(<N>):
            <BLOCO>
    '''

    matches = [('repetir',), ('repita',), ('vezes',), (NEWLINE,)]
    iterator = token_find(tokens, matches)
    for idx, match in iterator:
        # Waits for a repetir/repita token to start
        if match[0] not in ['repetir', 'repita']:
            continue

        # Send tokens for the beginning of the equivalent "for" loop
        starttokens = [Token(x) for x in ['for', '___', 'in', 'range', '(']]
        iterator.send(['subs', starttokens ])

        # Matches the 'vezes' token
        idx, match = next(iterator)
        if match[0] != 'vezes':
            lineno = tokens[idx].start[0]
            raise SyntaxError(
                'comando repetir malformado na linha %s.\n'
                '    Espera comando do tipo\n\n'
                '        repetir <N> vezes:\n'
                '            <BLOCO>\n\n'
                '    Palavra chave "vezes" está faltando!' % (lineno))
        else:
            iterator.send(['subs', [Token(')')]])

    return tokens


def process_range_command(tokens):
    '''Handles command::

        de <X> até <Y> [a cada <Z>]

    and converts it to::

        in range(<X>, <Y> + 1[, <Z>])
    '''

    matches = [('de',), ('até',), ('a', 'cada',), (NEWLINE,), (':',)]
    iterator = token_find(tokens, matches)
    one_tk = Token('1', NUMBER)
    for idx, match in iterator:
        # Waits for a 'de' token to start processing
        if match[0] != 'de':
            continue

        # Send tokens for the beginning of the equivalent in range(...) test
        starttokens = [Token(x) for x in ['in', 'range', '(']]
        iterator.send(['subs', starttokens])

        # Matches the 'até' token and insert a comma separator
        idx, match = next(iterator)
        if match[0] == 'até':
            iterator.send(['subs', [Token(',')]])
        else:
            raise SyntaxError(match)

        idx, match = next(iterator)

        # Matches "a cada" or the end of the line
        if match == ('a', 'cada'):
            middletokens = [Token(x) for x in ['+', one_tk, ',']]
            iterator.send(['subs', middletokens])

            # Proceed to the end of the line
            idx, match = next(iterator)
            if match[0] not in (NEWLINE, ':'):
                raise SyntaxError(match)
            endtokens = [Token(')'), tokens[idx]]
            iterator.send(['subs', endtokens])

        # Finish command
        elif match[0] in (NEWLINE, ':'):
            endtokens = [Token(x) for x in ['+', one_tk, ')']]
            endtokens.append(tokens[idx])
            iterator.send(['subs', endtokens])

        # Unexpected token
        else:
            raise SyntaxError(match)

    return tokens


def fromstring(src):
    '''Convert source string to a list of tokens'''

    current_string = src

    def iterlines():
        nonlocal current_string

        if current_string:
            line, sep, current_string = current_string.partition('\n')
            return line + sep
        else:
            raise StopIteration

    tokens = list(tokenize.generate_tokens(iterlines))
    tokens = list(map(Token, tokens))
    return tokens


def tostring(tokens):
    '''Converte lista de tokens para string'''

    # Align tokens
    lastpos = TokenPosition(1, 0)
    last_is_fragile = False

    def itertokens():
        nonlocal lastpos, last_is_fragile

        for tk in tokens:
            if tk.start is None:
                tk.start = lastpos
            if tk.start < lastpos:
                tk.start, tk.end = lastpos, None
            if last_is_fragile and tk.string.isidentifier() and tk.start == lastpos:
                tk.start += (0, 1)
                tk.end = None
            if tk.end is None:
                tk.end = tk.start + (0, len(tk.string))

            assert tk.end >= tk.start, str(tk)
            assert tk.start >= lastpos, str(tk)
            skip = tk.string.count('\n')
            if skip:
                lastpos = TokenPosition(tk.end.lineno + skip, 0)
            else:
                lastpos = tk.end
            last_is_fragile = tk.string.isidentifier()
            yield tk.to_token_info()

    return tokenize.untokenize(itertokens())
