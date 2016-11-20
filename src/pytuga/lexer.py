from copy import deepcopy
import tokenize
from tokenize import TokenInfo
from tokenize import (NAME, OP, NEWLINE, EXACT_TOKEN_TYPES, NUMBER)
from pytuga.keyword import TRANSLATIONS as TOKEN_TRANSLATIONS

__all__ = ['transpile_tk', 'fromstring', 'tostring']
TOKEN_TYPE_NAME = {tt: attr for (attr, tt) in vars(tokenize).items()
                            if attr.isupper() and isinstance(tt, int)}


class Token:
    """Mutable token object."""

    def __init__(self, data, type=None, start=None, end=None, line=None,
                 abstract=False):

        # Start from TokenInfo object
        if isinstance(data, TokenInfo):
            assert all(x is None for x in [type, start, end, line])
            type, data, start, end, line = data

        elif isinstance(data, Token):
            assert all(x is None for x in [type, start, end, line])
            data, type, start, end, line = data

        elif isinstance(data, int):
            type = data
            data = None

        if start is not None:
            start = TokenPosition(start)
            if end is None:
                if '\n' not in data:
                    end = start + (0, len(data))
                else:
                    lineno = end.lineno + end.count('\n')
                    col = len(data.rpartition('\n')[-1])
                    end = TokenPosition(lineno, col)
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
                elif data.isdigit():
                    type = NUMBER
                else:
                    raise TypeError('could not recognize token: %r' % data)

        self.string = data
        self.type = type
        self.start = start
        self.end = end
        self.line = line
        if not abstract:
            if start is None or end is None:
                raise ValueError('could not define start/end of concrete token')
        else:
            if start is not None or end is not None:
                raise ValueError('cannot define start/end positions of '
                                 'abstract token')

    @classmethod
    def from_strings(cls, start, *strings):
        """Return a list of strings starting at the given starting point and
        return the corresponding strings with the correct start/end positions"""

        tk_list = []
        start = TokenPosition(start)
        is_fragile = False
        for string in strings:
            if is_fragile and string.isidentifier():
                start += (0, 1)
            tok = Token(string, start=start)
            start = tok.end
            is_fragile = string.isidentifier()
            tk_list.append(tok)
        return tk_list

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
        """Convert to TokenInfo object used by Python's tokenizer."""

        return TokenInfo(
                self.type, self.string, self.start, self.end, self.line
        )

    def displace(self, cols):
        """Displace token in line by cols columns to the right."""

        self.start += (0, cols)
        if self.end.lineno == self.start.lineno:
            self.end += (0, cols)


def displace_tokens(tokens, cols):
    """Displace all tokens in list which are in the same line as the the first
    token by the given number of columns"""

    if not tokens or cols == 0:
        return
    lineno = tokens[0].start.lineno

    for token in tokens:
        if token.start.lineno == lineno:
            token.displace(cols)
        else:
            break


def insert_tokens_at(tokens, idx, new_tokens, end=None):
    """Insert new_tokens at tokens list at the given idx"""

    if end is not None:
        linediff, col = new_tokens[-1].end - end
        if linediff == 0 and end.lineno == tokens[idx].start.lineno:
            displace_tokens(tokens[idx:], col)

    for tk in new_tokens:
        tokens.insert(idx, tk)
        idx += 1


class TokenPosition(tuple):
    """Represent the start or end position of a token and accept some basic
    arithmetic operations"""

    def __new__(cls, x, y=None):
        if y is None:
            x, y = x
        return tuple.__new__(cls, [x, y])

    def __init__(self, x, y=None):
        super().__init__()

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


def transpile_tk(tokens):
    """Transpile a sequence of Token objects representing a Pytuguês code into
    Python"""

    # We pass several times through the token stream looking for direct
    # translations of Pytuguês tokens to Python.

    # First we look for invalid sequences that could be erroneously validated
    # in future passes
    matches = [
        ('faça', 'faça'), ('faça', 'fazer'), ('fazer', 'faça'),
        ('então', 'então'),
    ]
    iterator = token_find(tokens, matches)
    while True:
        try:
            idx, match, start, end = next(iterator)
            match = ' '.join(match)
            raise SyntaxError('Repetição inválida na linha %s: %s' %
                              (tokens[idx].start.lineno, match))
        except StopIteration:
            break

    # The second step is to handle sequence of Pytuguês tokens that can be
    # replaced by equivalent sequences of Python tokens
    convs = {
        # Block ending
        ('faça', ':'): ':',
        ('faca', ':'): ':',
        ('fazer', ':'): ':',

        # Loops
        ('para', 'cada'): 'for',

        # Conditions
        ('então', 'faça', ':'): ':',
        ('então', ':'): ':',
        ('entao', 'faca', ':'): ':',
        ('entao', ':'): ':',
        ('ou', 'então', 'se'): 'elif',
        ('ou', 'entao', 'se'): 'elif',
        ('ou', 'se'): 'elif',

        # Definitions
        ('definir', 'função'): 'def',
        ('definir', 'funcao'): 'def',
        ('defina', 'função'): 'def',
        ('defina', 'funcao'): 'def',
        ('definir', 'classe'): 'class',
        ('defina', 'classe'): 'class',
    }
    iterator = token_find(tokens, convs)
    while True:
        try:
            idx, match, start, end = next(iterator)
            tokens[idx] = Token(convs[match], start=start)
            del tokens[idx + 1: idx + len(match)]

            linediff, col = tokens[idx].end - end
            if linediff == 0:
                displace_tokens(tokens[idx + 1:], col)
        except StopIteration:
            break

    # Now we apply simple single token translations
    for i, tk in enumerate(tokens):
        new = TOKEN_TRANSLATIONS.get(tk.string, tk)
        if new is not tk:
            new = Token(new, start=tk.start)
            tokens[i] = new

            # Align tokens
            linediff, coldiff = new.end - tk.end
            assert linediff == 0
            if coldiff:
                displace_tokens(tokens[i + 1:], coldiff)

    # Handle special Pytuguês-only commands
    tokens = process_repetir_command(tokens)
    tokens = process_de_ate_command(tokens)

    return tokens


def token_find(tokens, matches, start=0):
    """Iterates over list of tokens yielding (index, match, start, end) for
    each match in the token stream. The `matches` attribute must be a sequence
    of token sequences.
    """

    matches = list(matches)
    tk_matches = \
        [tuple(Token(tk, abstract=True) for tk in seq) for seq in matches]
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
                start = tokens[tk_idx].start
                end = tokens[tk_idx + matchsize - 1].end
                yield (tk_idx, matches[match_idx], start, end)
                tk_idx += 1
        tk_idx += 1
    return


def process_repetir_command(tokens):
    """Handles "repita/repetir".

    Converts command::

        repetir <N> vezes:
            <BLOCO>

        repita <N> vezes:
            <BLOCO>

    into::

        for ___ in range(<N>):
            <BLOCO>
    """

    matches = [('repetir',), ('repita',), ('vezes',), (NEWLINE,)]
    iterator = token_find(tokens, matches)
    for idx, match, start, end in iterator:
        # Waits for a repetir/repita token to start
        if match[0] not in ['repetir', 'repita']:
            continue

        # Send tokens to the beginning of the equivalent "for" loop
        starttokens = Token.from_strings(
                tokens[idx].start, 'for', '___', 'in', 'range', '('
        )
        del tokens[idx]
        insert_tokens_at(tokens, idx, starttokens, end=end)

        # Matches the 'vezes' token
        idx, match, start, end = next(iterator)

        if match[0] != 'vezes':
            raise SyntaxError(
                    'comando repetir malformado na linha %s.\n'
                '    Espera comando do tipo\n\n'
                '        repetir <N> vezes:\n'
                '            <BLOCO>\n\n'
                    '    Palavra chave "vezes" está faltando!' % (start.lineno))
        else:
            tokens[idx] = Token(')', start=start)
            displace_tokens(tokens[idx + 1:], -4)

    return tokens


def process_de_ate_command(tokens):
    """Handles command::

        de <X> até <Y> [a cada <Z>]

    and converts it to::

        in range(<X>, <Y> + 1[, <Z>])
    """

    matches = [('de',), ('até',), ('a', 'cada',), (NEWLINE,), (':',)]
    iterator = token_find(tokens, matches)
    for idx, match, start, end in iterator:
        # Waits for a 'de' token to start processing
        if match[0] != 'de':
            continue

        # Send tokens for the beginning of the equivalent in range(...) test
        starttokens = Token.from_strings(tokens[idx].start, 'in', 'range', '(')
        del tokens[idx]
        insert_tokens_at(tokens, idx, starttokens, end=end)

        # Matches the 'até' token and insert a comma separator
        idx, match, start, end = next(iterator)
        if match[0] == 'até':
            displace_tokens(tokens[idx:], -3)
            tokens[idx] = Token(',', start=tokens[idx - 1].end)
        else:
            raise SyntaxError(
                    'comando para cada malformado na linha %s.\n'
                    '    Espera comando do tipo\n\n'
                    '        para cada <x> de <a> até <b>:\n'
                    '            <BLOCO>\n\n'
                    '    Palavra chave "até" está faltando!' % (start.lineno)
            )

        idx, match, start, end = next(iterator)

        # Matches "a cada" or the end of the line
        if match == ('a', 'cada'):
            middletokens = Token.from_strings(start, '+', '1', ',')
            del tokens[idx:idx + 2]
            insert_tokens_at(tokens, idx, middletokens, end=end)

            # Proceed to the end of the line
            idx, match, start, end = next(iterator)
            if match[0] not in (NEWLINE, ':'):
                raise SyntaxError(
                        'comando malformado na linha %s.\n'
                        '    Espera um ":" no fim do bloco' % (start.lineno)
                )
            endtok = Token(')', start=start)
            displace_tokens(tokens[idx:], 1)
            tokens.insert(idx, endtok)

        # Finish command
        elif match[0] in (NEWLINE, ':'):
            displace_tokens(tokens[idx:], 1)
            endtokens = Token.from_strings(start, '+', '1', ')')
            insert_tokens_at(tokens, idx, endtokens, end=end)

        # Unexpected token
        else:
            raise SyntaxError(
                    'comando malformado na linha %s.\n'
                    '    Espera um ":" no fim do bloco' % (start.lineno)
            )

    return tokens


def fromstring(src, convert_tokens=True):
    """Convert source string to a list of tokens"""

    current_string = src

    if not current_string.endswith('\n'):
        current_string += '\n'

    def iterlines():
        nonlocal current_string

        if current_string:
            line, sep, current_string = current_string.partition('\n')
            return line + sep
        else:
            raise StopIteration

    tokens = list(tokenize.generate_tokens(iterlines))
    if convert_tokens:
        tokens = list(map(Token, tokens))

    return tokens


def tostring(tokens):
    """Converte lista de tokens para string"""

    return tokenize.untokenize([tk.to_token_info() for tk in tokens])


if __name__ == '__main__':
    ptsrc = '''
se x então faça:
    dsfsdf
'''

    tokens = fromstring(ptsrc)
    # print(transpile_tk(tokens))
    print(tostring(transpile_tk(tokens)))
