import tokenize
from token import OP, NAME, NUMBER
from tokenize import TokenInfo, EXACT_TOKEN_TYPES

TOKEN_TYPE_NAME = {tt: attr for (attr, tt) in vars(tokenize).items()
                   if attr.isupper() and isinstance(tt, int)}


class Token:
    """
    Mutable token object.
    """

    @classmethod
    def from_strings(cls, start, *strings):
        """
        Return a list of strings starting at the given starting point and
        return the corresponding strings with the correct start/end positions
        """

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

    def __eq__(self, other):
        if isinstance(other, Token):
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
        return 'Token(%r, %s, %r, %r, %r)' % (
            self.string, TOKEN_TYPE_NAME[self.type],
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
        """
        Convert to TokenInfo object used by Python's tokenizer.
        """

        return TokenInfo(
            self.type, self.string, self.start, self.end, self.line
        )

    def displace(self, cols):
        """
        Displace token in line by cols columns to the right.
        """

        self.start += (0, cols)
        if self.end.lineno == self.start.lineno:
            self.end += (0, cols)


class TokenPosition(tuple):
    """
    Represent the start or end position of a token and accept some basic
    arithmetic operations
    """

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


def displace_tokens(tokens, cols):
    """
    Displace all tokens in list which are in the same line as the the first
    token by the given number of columns
    """

    if not tokens or cols == 0:
        return
    lineno = tokens[0].start.lineno

    for token in tokens:
        if token.start.lineno == lineno:
            token.displace(cols)
        else:
            break


def insert_tokens_at(tokens, idx, new_tokens, end=None):
    """
    Insert new_tokens at tokens list at the given idx
    """

    if end is not None:
        linediff, col = new_tokens[-1].end - end
        if linediff == 0 and end.lineno == tokens[idx].start.lineno:
            displace_tokens(tokens[idx:], col)

    for tk in new_tokens:
        tokens.insert(idx, tk)
        idx += 1


def token_find(tokens, matches, start=0):
    """
    Iterate over list of tokens yielding (index, match, start, end) for
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
