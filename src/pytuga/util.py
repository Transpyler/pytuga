import tokenize


class ReversibleIterator(object):

    '''An iterator with it.last() and it.back() methods'''

    def __init__(self, data):
        self._data = list(reversed(data))
        self._consumed = []
        self._buffer = []
        self._last = None

    def __iter__(self):
        return self

    def __next__(self):
        if self._buffer:
            new = self._buffer.pop()
        else:
            try:
                new = self._data.pop()
            except IndexError:
                raise StopIteration
        self._consumed.append(new)
        self._last = new
        return new

    def back(self):
        '''Go back one position'''

        self._buffer.append(self._consumed.pop())

    def inject(self, value):
        self._consumed.pop()
        self._buffer.append(value)

    def last(self):
        '''Return the last yielded element'''

        return self._last


def sort_token_by_line(tokens):
    '''Retorna uma lista de lista de tokens onde cada sub-lista contêm todas as
    tokens que começam na mesma linha'''

    line_no = 0
    lines = []
    for tk in tokens:
        n, _ = tk.start
        if n == line_no:
            lines[-1].append(tk)
        else:
            lines.append([tk])
            line_no = n
    return lines


def normalize_tokens_in_line(line):
    '''Normalize start and end position tuples for all tokens in a given
    line'''

    token = tokenize.TokenInfo
    indent_types = [tokenize.INDENT, tokenize.DEDENT]
    line_no, char_no = line[0].start
    tokens = []

    for tt, string, start, end, line in line:
        # Acrescenta espaço no cursor para tokens que exigem espaço antes
        if tokens and (tokens[-1].type not in indent_types):
            if tt in [tokenize.NAME]:
                char_no += 1
            elif tt == tokenize.OP and string not in '()[],:':
                char_no += 1

        # Recalcula o start e o end de cada token
        start = line_no, char_no
        if end[0] == line_no:
            end = line_no, start[1] + len(string)

        # Acrescenta espaço no cursor para tokens que exigem espaço após os
        # mesmos
        char_no = end[1]
        if tt in [tokenize.COMMA]:
            char_no += 1
        elif tt == tokenize.OP and string not in '()[]':
            char_no += 1

        # Salva token na lista
        tk = token(tt, string, start, end, line)
        tokens.append(tk)

    return tokens


def fix_tokens_start(tokens):
    '''Normalizes start attribute for all tokens in a list of tokens.'''

    out = []
    for line in sort_token_by_line(tokens):
        out.extend(normalize_tokens_in_line(line))
    return out
