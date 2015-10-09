from collections import deque
import tokenize
from tokenize import TokenInfo
from tokenize import (
    COLON, COMMA, DEDENT, ENDMARKER, LPAR, RPAR, NAME, OP, NUMBER)
from pytuga import constants as cte

__all__ = ['transpile', 'compile', 'exec']

TYPE_MAP = {':': COLON, '(': LPAR, ')': RPAR, ',': COMMA}


class delta(object):

    def __init__(self, a, b):
        self.vdiff = a
        self.hdiff = b

    def __add__(self, other):
        if isinstance(other, delta):
            return delta(self.vdiff + other.vdiff, self.hdiff + other.hdiff)

        a, b = other
        return (a + self.vdiff, b + self.hdiff)

    def __radd__(self, other):
        return self + other

    def __repr__(self):
        return 'delta(%r, %r)' % (self.vdiff, self.hdiff)

    def __iter__(self):
        yield self.vdiff
        yield self.hdiff


class TokenPosition(tuple):

    '''Represent the start or end position of a token and accept some basic
    arithmetic operations'''

    def __new__(self, x, y=None):
        if y is None:
            x, y = x
        return tuple.__new__(self, [x, y])

    @property
    def line_no(self):
        return self[0]

    @property
    def col(self):
        return self[1]

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


class Token(object):

    '''Mutable token object.

    All methods that make changes inplace start with an "i".'''

    def __init__(self, string, type=None, start=None, end=None, line=None):

        # Start from TokenInfo object
        if isinstance(string, TokenInfo):
            assert all(x is None for x in [type, start, end, line])
            type, string, start, end, line = string

        if start is not None:
            start = TokenPosition(start)
            if end is None:
                end = start + (0, len(string))
        if end is not None:
            end = TokenPosition(end)
        if type is None:
            try:
                type = TYPE_MAP[string]
            except KeyError:
                raise TypeError

        self.string = string
        self.type = type
        self.start = start
        self.end = end
        self.line = line

    def to_token_info(self):
        '''Convert to TokenInfo object used by Python's tokenize.'''

        return TokenInfo(
            self.type, self.string, self.start, self.end, self.line)

    #
    # Magic methods
    #
    def __repr__(self):
        return 'Token(%r, %r, %r, %r)' % (tuple(self)[:-1])

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
        elif idx < 0 and idx >= -5:
            return self[5 + idx]
        else:
            raise IndexError(idx)

    def __iter__(self):
        yield from (self[i] for i in range(5))


class TokenStream(deque):

    '''Represents a group of tokens'''

    @property
    def start(self):
        return self[0].start

    @property
    def end(self):
        return self[-1].end


def transpile(src):
    r'''Converte Pytuguês em Python

    Exemplo
    -------

    >>> src = \
    ... """para cada x em [1, 2, 3]:
    ...     mostre(x ou z)"""
    >>> print(transpile(src))
    for x in [1, 2, 3]:
        mostre(x or z)
    '''

    # O trabalho duro é feito pela função transpile_tk()
    if not src or src.isspace():
        return src
    else:
        try:
            return tostring(transpile_tk(fromstring(src)))
        except Exception:
            print('Bad code')
            print('--------\n')
            print(src)
            raise


def compile(source, filename, mode, flags=0, dont_inherit=False):
    '''Se comporta como a função built-in compile(), mas para código em
    Pytuguês'''

    source = transpile(source)
    return __builtins__['compile'](source, filename, mode, flags, dont_inherit)


def exec(object, locals=None, globals=None):
    '''Se comporta como a função built-in exec(), mas para código em
    Pytuguês'''

    if isinstance(object, str):
        object = transpile(object)
    return __builtins__['exec'](object, locals, globals)


###############################################################################
#                     Transpilação baseada em Tokens
# ----------------------------------------------------------------------------
#
# O ponto de entrada da transpilação é a função transpile_tk(). Ela delega a
# transpilação dos casos não trivial para as sub-funções registradas pelo
# decorador @handle_token() definido abaixo.
#
TK_HANDLER = {}


def transpile_tk(tokens):
    '''Transpila uma sequência de tokens de Pytuguês para Python'''

    if not tokens:
        return TokenStream()
    tokens = as_TokenStream(tokens)
    out = TokenStream()
    tk = tokens.popleft()

    # Processa todos tokens triviais
    while tk.string not in TK_HANDLER:
        try:
            name = cte.TOKEN_TRANSLATIONS[tk.string]
            token = tkcopy(tk, string=name, fixend=True)
            delta = len(name) - len(tk.string)
            tokens = hshift(tokens, delta)
        except KeyError:
            token = tk
        out.append(token)
        if tokens:
            tk = tokens.popleft()
        else:
            return out

    # Processa tokens especiais
    if tokens:
        handler = TK_HANDLER[tk.string]
        tokens = handler(tk, tokens)
        if tokens is not None:
            out.extend(tokens)
        else:
            raise RuntimeError(
                'handler for "%s" returned a null value' % tk.string)
    return out


def handle_token(tkname):
    '''Decorador que sinaliza as funções que lidam com cada tipo de token
    especial.

    Tokens não modificadas ou tokens com tradução trivial são manipuladas
    diretamente pela função transpile_tk()
    '''

    def decorator(func):
        TK_HANDLER[tkname] = func
        return func
    return decorator


# -----------------------------------------------------------------------------
#                               Delegates
# -----------------------------------------------------------------------------

@handle_token('repita')
@handle_token('repetir')
def _transpile_repetir(tk, tokens):
    '''Processa uma token do tipo "repita/repetir".

    Aparece no comando::

        repetir <N> vezes:
            <BLOCO>

        repita <N> vezes:
            <BLOCO>

    É transpilado para::

        for ___ in range(<N>):
            <BLOCO>
    '''

    try:
        arg_tokens, _sep, tail = partition(tokens, 'vezes')
    except MissingSeparatorError:
        raise SyntaxError(
            'comando repetir malformado.\n'
            '    Espera comando do tipo\n\n'
            '        repetir <N> vezes:\n'
            '            <BLOCO>\n\n'
            '    Palavra chave "vezes" está faltando!')

    tail = transpile_tk(tail)
    arg_tokens = transpile_tk(arg_tokens)
    arg_tokens = parens(arg_tokens)
    range_tokens = fromstring('for ___ in range', tk.start)
    return join(range_tokens, arg_tokens, tail)


@handle_token('para')
def _transpile_para(tk, tokens):
    '''Processa uma token do tipo "para".

    Aparece nos comandos::

        para [cada] <nome> em <sequência> [faça]:
            <BLOCO>

        para [cada] <nome> de <início> até <fim> [a cada <passo>] [faça]:
            <BLOCO>
    '''

    # Troca "para" por "for"
    tokens = hshift(tokens, -1)
    if tokens[0].string == 'cada':
        tokens.popleft()
        tokens = hshift(tokens, -5)
    tokens.appendleft(tkcopy(tk, string='for', fixend=True))

    # Remove o "faça" opcional no fim do bloco
    tokens = remove_before_colon(tokens, 'faça')

    # Testa se <nome> é um token válido
    if tokens[1].type != NAME:
        raise SyntaxError('esperava um nome no comando "para cada <nome> ..."')

    # Verifica o tipo de comando: mapa em sequência
    if tokens[2].string in 'em':
        tokens[2].string = 'in'
        return transpile_tk(tokens)

    # Mapa numérico
    elif tokens[2].string == 'de':
        # Separa cada elemento que caracteriza o loop
        tk_for, varname, tk_de, *tail = tokens
        tokens = TokenStream([tk_for, varname, tkcopy(tk_de, string='in')])
        tokens.append(tkcopy(tail[0], 'range', NAME, fixend=True))
        tokens.append(tkcopy(tail[0], '(', LPAR, hshift=5, fixend=True))

        # Recupera o primeiro elemento do range
        start, _tk_até, tail = partition(tail, 'até')
        start = hshift(transpile_tk(start), 6)
        tokens.extend(start)

        # Adiciona a vírgula
        tokens.append(Token(',', start=tokens[-1].end))

        # Recupera o final do range -- primeiro verifica se define o passo
        try:
            end, _, tail = partition(tail, 'cada')
            if end[-1].string == 'a':
                end.pop()
            end = transpile_tk(end)

        # O passo *não está* definido
        except MissingSeparatorError:
            end, colon_tk, tail = partition(tail, ':')
            end = transpile_tk(end)
            step = None

        # O passo *está* definido
        else:
            step, colon_tk, tail = partition(tail, ':')
            step = transpile_tk(step)

        # Adiciona o fim do range
        tokens.extend(halign(end, tokens[-1].end + (0, 1)))
        tokens.append(Token('+', OP, tokens[-1].end + (0, 1)))
        tokens.append(Token('1', NUMBER, tokens[-1].end + (0, 1)))

        # Adiciona passo, se necessário
        if step:
            tokens.append(Token(',', COMMA, tokens[-1].end))
            tokens.extend(halign(step, tokens[-1].end + (0, 1)))

        # Fecha parênteses do range e finaliza
        tokens.append(Token(')', RPAR, tokens[-1].end))
        tokens.append(Token(':', COLON, tokens[-1].end))

        # Continua processamento
        tail_sep = tail[0].start[1] - colon_tk.end[1]
        tail = halign(transpile_tk(tail), tokens[-1].end)
        tail = hshift(tail, tail_sep)
        tokens.extend(tail)
        return tokens

    else:
        raise SyntaxError(
            'esperava "de" ou "em" no comando "para cada <nome> de|em ..."')


@handle_token('enquanto')
def _transpile_enquanto(tk, tokens):
    '''Processa uma token do tipo "repetir".

    Aparece no comando::

        enquanto <condição> [faça]:
            <BLOCO>

    É transpilado para::

        while <condição>:
            <BLOCO>
    '''

    tokens.appendleft(tkcopy(tk, string='while'))
    tokens = remove_before_colon(tokens, 'faça')
    return transpile_tk(tokens)


@handle_token('se')
def _transpile_se(tk, tokens):
    '''Processa uma token do tipo "se".

    Aparece no comando::

        se <condição> [então] [faça]:
            <BLOCO>

    É transpilado para::

        if <condição>:
            <BLOCO>
    '''

    tokens.appendleft(tkcopy(tk, string='if'))
    tokens = remove_before_colon(tokens, 'faça')
    tokens = remove_before_colon(tokens, 'então')
    return transpile_tk(tokens)


@handle_token('ou')
def _transpile_ou(tk, tokens):
    '''Processa uma token do tipo "ou".

    Pode aparecer em contextos diferentes. Em um bloco do tipo "ou então se"::

        ou [então] se <condição> [então] [faça]:
            <BLOCO>

    É transpilado para::

        elif <condição>:
            <BLOCO>

    Também pode aparecer como expressão lógica:

        A ou B  <==> A or B
    '''

    # Caso trivial: simplesmente traduz
    if tokens[0].string not in ['então', 'se']:
        tokens.appendleft(tkcopy(tk, string='or'))
        return transpile_tk(tokens)

    # Remove "então se"
    shift = -3
    if tokens[0].string == 'então':
        tokens.popleft()
        shift -= 6
    if tokens[0].string != 'se':
        raise SyntaxError('faltando "se" depois de "ou [então]"')
    tokens.popleft()

    tokens = hshift(tokens, shift)
    tokens.appendleft(tkcopy(tk, string='elif'))
    tokens = remove_before_colon(tokens, 'faça')
    tokens = remove_before_colon(tokens, 'então')
    return transpile_tk(tokens)


@handle_token('senão')
def _transpile_senão(tk, tokens):
    '''Processa uma token do tipo "se".

    Aparece no comando::

        senão [faça]:
            <BLOCO>

    É transpilado para::

        else:
            <BLOCO>
    '''

    tokens.appendleft(tkcopy(tk, string='else'))
    tokens = remove_before_colon(tokens, 'faça')
    return transpile_tk(tokens)


@handle_token('defina')
@handle_token('definir')
def _transpile_definir(tk, tokens):
    '''Processa uma token do tipo "definir".

    Aparece no comando::

        defina [função] <nome>(<argumentos>):
            <BLOCO>

        definir [função] <nome>(<argumentos>):
            <BLOCO>

    É transpilado para::

        def <nome>(<argumentos>):
            <BLOCO>
    '''

    if tokens[0].string == 'função':
        return hshift(transpile_tk(tokens), -len(tk.string) - 1)
    else:
        tokens = hshift(transpile_tk(tokens), -(len(tk.string) - 3))
        tokens.appendleft(tkcopy(tk, string='def', fixend=True))
    return tokens


#
# Utility
#
def remove_before_colon(tokens, tkname):
    try:
        head, sep, tail = partition(tokens, ':')
    except MissingSeparatorError:
        raise SyntaxError(
            'comando enquanto malformado. Espera ":" para sinalizar fim de '
            'bloco')

    # Remove o comando opcional "tkname"
    N = len(tkname)
    if head[-1].string == tkname:
        head.pop()
        head.append(tkcopy(sep, hshift=-N - 1))
        head.extend(hshift(tail, -N - 1))
    else:
        return tokens
    return head


#
# Utilidades
#
def hshift_range(range, value):
    a, b = range
    return (a, b + value)


def tk_hshift(tk, value):
    name, tt, start, end, line = tk
    start = hshift_range(start, value)
    end = hshift_range(end, value)
    return Token(name, tt, start, end, line)


def tkcopy(tk, string=None, type=None, start=None, end=None, line=None,
           hshift=0, vshift=0, fixend=False):
    tn, tt, ts, te, tl = tk
    type = type or tt
    string = string or tn
    start = start or ts
    end = end or te
    line = line or tl

    start = start[0] + vshift, start[1] + hshift
    end = end[0] + vshift, end[1] + hshift

    delta = len(tk.string) - len(string)
    if fixend and delta:
        end = end[0], end[1] - delta

    return Token(string, type, start, end, line)


def tkprint(tk_list):
    print([tk.string or str(tk) for tk in tk_list])


def as_TokenStream(L):
    '''Retorna iterável como uma TokenStream'''

    if isinstance(L, TokenStream):
        return L
    else:
        return TokenStream(L)


class MissingSeparatorError(ValueError):
    pass


def partition(tokens, sep):
    tokens = iter(tokens)
    pre = TokenStream()
    for tk in tokens:
        if tk.string == sep:
            sep = tk
            break
        else:
            pre.append(tk)
    else:
        raise MissingSeparatorError('expected separator not present: %r' % sep)
    pen_pos = TokenStream(tokens)
    return pre, sep, pen_pos


def tknew(type, string, start=None, end=None, line=None):
    return Token(string, type, start, end, line)


def get_delta_separator(tk1, tk2):
    '''Retorna um objeto do tipo delta() com a separação mínima que deve haver
    entre as token tk1 e tk2 a partir dos seus respectivos tipos.

    Esta função ignora os valores de start e end de cada token.
    '''

    if tk1.end[0] != tk2.end[0]:
        return delta(0, 0)
    elif tk1.type == tk2.type == tokenize.NAME and tk1.end[1] >= tk2.start[0]:
        return delta(0, 1)
    else:
        return delta(0, 0)


def join(*args, sep=False):
    '''Junta várias sequencias de tokens. Se sep=True, adiciona um espaço em
    branco entre os tokens vizinhos mesmo quando isso não for necessário.'''

    if len(args) > 2:
        L1, *tail = args
        return join(L1, join(*tail, sep=sep), sep=sep)
    elif len(args) == 2:
        L1, L2 = args
    else:
        raise TypeError('expect at least 2 arguments')

    # Retorna outra lista caso uma delas esteja vazia
    if not L1:
        return TokenStream(L2)
    if not L2:
        return TokenStream(L1)

    # Une as duas listas de tokens
    if sep:
        dh = delta(0, 1)
    else:
        dh = get_delta_separator(L1[-1], L2[0])

    head = TokenStream(L1)
    tail = halign(L2, L1[-1].end + dh)
    head.extend(tail)
    return head


def comma_join(*args, sep=False):
    '''Junta as sequências de tokens unindo-os por vírgulas'''

    last, *other = reversed(args)
    other = [suffix(elem, tknew(tokenize.COMMA, ',')) for elem in other]
    other.reverse()
    other.append(last)
    return join(*other, sep=sep)


def parens(tokens):
    r'''Envolve tokens com parênteses, ajustando o alinhamento horizontal

    Exemplo
    -------

    >>> tokens = parens(fromstring('x + y'))
    >>> tkprint(tokens)
    ['(', 'x', '+', 'y', ')']
    '''

    # Abre parênteses
    tk = tknew(tokenize.LPAR, '(')
    tokens = prefix(tokens, tk, sep=False)

    # Fecha parênteses
    tk = tknew(tokenize.RPAR, ')')
    tokens = suffix(tokens, tk, sep=False)
    return tokens


def tkhdelta(tk):
    if tk.start is None or tk.end is None:
        return len(tk.string)
    if tk.end[0] != tk.start[0]:
        raise ValueError('cannot compute hdelta of multiline token')
    return tk.end[1] - tk.start[1]


def prefix(tokens, prefix, sep=False):
    '''Adiciona token prefix antes da lista de tokens e ajusta alinhamento
    horizontal'''

    if not tokens:
        raise ValueError('lista de tokens vazia')

    # Alinha prefix
    start = tokens[0].start
    diff = delta(0, tkhdelta(prefix))
    prefix = tkcopy(prefix, start=start, end=start + diff)
    prefix = tkcopy(prefix, line=prefix.line or tokens[0].line)

    return join(TokenStream([prefix]), tokens, sep=sep)


def suffix(tokens, suffix, sep=False):
    '''Adiciona token suffix após da lista de tokens e ajusta alinhamento
    horizontal'''

    if not tokens:
        raise ValueError('lista de tokens vazia')

    # Remove endmarker and trailing newline if necessary
    end = None
    newline = None
    if tokens[-1].type == tokenize.ENDMARKER:
        end = tokens.pop()
    if tokens[-1].type == tokenize.NEWLINE:
        newline = tokens.pop()

    # Alinha suffix
    start = tokens[-1].end
    diff = delta(0, tkhdelta(suffix))
    suffix = tkcopy(suffix, start=start, end=start + diff)
    suffix = tkcopy(suffix, line=suffix.line or tokens[-1].line)
    tokens = join(tokens, TokenStream([suffix]), sep=sep)

    # Restaura endmarker e newline
    if newline is not None:
        tokens = add_newline(tokens)
    if end is not None:
        tokens.append(end)
    return tokens


def add_newline(tokens):
    '''Adciona uma token de newline ao final da sequência'''

    start = tokens[-1].end + delta(0, 1)
    end = start + delta(0, 1)
    line = tokens[-1].line
    tokens.append(tknew(tokenize.NEWLINE, '\n', start, end, line))
    return tokens


def hshift(tokens, shift):
    # Retorna lista vazia
    if not tokens:
        return TokenStream()

    line_no = tokens[0].start[0]

    # Cria lista de tokens alinhados
    aligned = TokenStream()
    tokens = iter(tokens)
    for tk in tokens:
        if tk.start[0] == line_no:
            aligned.append(tkcopy(tk, hshift=shift))
        else:
            aligned.append(tk)
            aligned.extend(tokens)
            break

    return aligned


def halign(tokens, tk_start):
    '''Move tokens para a direita ou esquerda para se alinharem com tk_start'''

    # Retorna lista vazia
    if not tokens:
        return TokenStream()

    # Impede que tokens comece em uma linha antes tk_start
    start = tokens[0].start
    if start[0] > tk_start[0]:
        return TokenStream(tokens)
    elif start[0] < tk_start[0]:
        raise ValueError(('começa em linha anterior à tk_start:\n'
                          '    linha: %s\n'
                          '    align: %s') % (start, tk_start))

    # Calcula o shift horizontal
    line_no, start = tk_start
    hshift = start - tokens[0].start[1]

    # Cria lista de tokens alinhas
    aligned = TokenStream()
    tokens = iter(tokens)
    for tk in tokens:
        if tk.start[0] == line_no:
            aligned.append(tkcopy(tk, hshift=hshift))
        else:
            aligned.append(tk)
            aligned.extend(tokens)
            break

    return aligned


def fromstring(src, start=None):
    '''Retorna lista de tokens a partir de uma string'''

    # Realinha as tokens se start for fornecido
    if start is not None:
        line_no, col = start
        tokens = fromstring(src)

        # Alinha horizontalmente
        for idx, tk in enumerate(tokens):
            if tk.start[0] != 1:
                break
            tokens[idx] = tkcopy(tk, hshift=col)

        # Alinha verticalmente
        return [tkcopy(tk, vshift=line_no - 1) for tk in tokens]

    # Cria novas tokens começando na primeira linha
    current_string = src

    def iterlines():
        nonlocal current_string
        if current_string:
            line, sep, current_string = current_string.partition('\n')
            return line + sep
        else:
            raise StopIteration

    tokens = TokenStream(tokenize.generate_tokens(iterlines))
    tokens = list(map(Token, tokens))
    while tokens[-1].type == ENDMARKER:
        tokens.pop()
    return tokens

#     if keep_endings:
#         return tokens
#     else:
#
#         if tokens[-1].type == tokenize.NEWLINE:
#             tokens.pop()
#         return tokens


def tostring(tokens):
    '''Converte lista de tokens para string'''

    last_pos = tokens[0].start

    while tokens[-1].type == DEDENT:
        tokens.pop()

    if tokens[-1].type != ENDMARKER:
        start = end = tokens[-1].end
        tokens.append(tknew(ENDMARKER, '', start, end, line=''))

    # tkprint(tokens)

    tokens = [tk.to_token_info() for tk in tokens]
    try:
        return tokenize.untokenize(tokens)
    except ValueError:
        for idx, tk in enumerate(tokens):
            a, b = tk.start
            c, d = last_pos
            if (a < c) or (a == c and d > b):
                fmt = idx, tokens[idx - 1], tk
                print(tokens)
                raise ValueError(
                    'tokens sobrepõe a partir de #%s:\n\t%s\n\t%s)' % fmt)
            last_pos = tk.end
        else:
            raise


###############################################################################
#
# Testes
#
# FIXME: criar suite de testes

if __name__ == '__main__':

    # Básico
    # prefix
    src = tostring(prefix(fromstring('+ y'), tknew(1, 'x'), sep=True))
    assert src == 'x + y', repr(src)

    # suffix
    src = tostring(suffix(fromstring('x +'), tknew(1, 'y'), sep=True))
    assert src == 'x + y', repr(src)

    src = tostring(parens(fromstring('x + y')))
    assert src == '(x + y)', repr(src)

    # Trivial
    # Ops matemáticas
    for ptsrc in ['1 + 2', '1 + 2.0', '[1, 2, 3]', 'x and y']:
        assert transpile(ptsrc) == ptsrc, transpile(ptsrc)

    # Traduções
    ptsrc = 'x e y'
    pysrc = 'x and y'
    assert transpile(ptsrc) == pysrc, transpile(ptsrc)

    ptsrc = 'x é verdadeiro'
    pysrc = 'x is True'
    assert transpile(ptsrc) == pysrc, transpile(ptsrc)

    # Laços - repetir
    ptsrc = 'repetir 4 vezes: mostre(42)'
    pysrc = 'for ___ in range(4): mostre(42)'
    assert transpile(ptsrc) == pysrc, transpile(ptsrc)

    ptsrc = 'repetir 4 vezes:\n    mostre(42)'
    pysrc = 'for ___ in range(4):\n    mostre(42)'
    assert transpile(ptsrc) == pysrc, transpile(ptsrc)

    # Laços - para cada
    ptsrc = 'para cada x em [1, 2, 3]: mostre(x)'
    pysrc = 'for x in [1, 2, 3]: mostre(x)'
    assert transpile(ptsrc) == pysrc, transpile(ptsrc)

    ptsrc = 'para cada x em [1, 2, 3]:\n    mostre(x)'
    pysrc = 'for x in [1, 2, 3]:\n    mostre(x)'
    assert transpile(ptsrc) == pysrc, transpile(ptsrc)

    ptsrc = 'para cada x em [1, 2, 3] faça: mostre(x)'
    pysrc = 'for x in [1, 2, 3]: mostre(x)'
    assert transpile(ptsrc) == pysrc, transpile(ptsrc)

    # Laços - para (range)
    ptsrc = 'para x de 1 até 10: mostre(x)'
    pysrc = 'for x in range(1, 10 + 1): mostre(x)'
    assert transpile(ptsrc) == pysrc, transpile(ptsrc)

    ptsrc = 'para x de 1 até 10:\n    mostre(x)'
    pysrc = 'for x in range(1, 10 + 1):\n    mostre(x)'
    assert transpile(ptsrc) == pysrc, transpile(ptsrc)

    ptsrc = 'para x de 1 até 10 faça: mostre(x)'
    pysrc = 'for x in range(1, 10 + 1): mostre(x)'
    assert transpile(ptsrc) == pysrc, transpile(ptsrc)

    ptsrc = 'para x de 1 até 10 a cada 2: mostre(x)'
    pysrc = 'for x in range(1, 10 + 1, 2): mostre(x)'
    assert transpile(ptsrc) == pysrc, transpile(ptsrc)

    ptsrc = 'para x de 1 até 10 a cada 2 faça: mostre(x)'
    pysrc = 'for x in range(1, 10 + 1, 2): mostre(x)'
    assert transpile(ptsrc) == pysrc, transpile(ptsrc)

    ptsrc = 'para x de 1 até 10 a cada 2 faça:\n    mostre(x)'
    pysrc = 'for x in range(1, 10 + 1, 2):\n    mostre(x)'
    assert transpile(ptsrc) == pysrc, transpile(ptsrc)

    # Laços - enquanto
    ptsrc = 'enquanto x < 1: mostre(x)'
    pysrc = 'while x < 1: mostre(x)'
    assert transpile(ptsrc) == pysrc, transpile(ptsrc)

    ptsrc = 'enquanto x < 1 faça: mostre(x)'
    pysrc = 'while x < 1: mostre(x)'
    assert transpile(ptsrc) == pysrc, transpile(ptsrc)

    ptsrc = 'enquanto x < 1 faça:\n    mostre(x)'
    pysrc = 'while x < 1:\n    mostre(x)'
    assert transpile(ptsrc) == pysrc, transpile(ptsrc)

    # Condicional - se
    ptsrc = 'se x < 1 então: mostre(x)'
    pysrc = 'if x < 1: mostre(x)'
    assert transpile(ptsrc) == pysrc, transpile(ptsrc)

    ptsrc = 'se x < 1: mostre(x)'
    pysrc = 'if x < 1: mostre(x)'
    assert transpile(ptsrc) == pysrc, transpile(ptsrc)

    ptsrc = 'se x < 1 então:\n    mostre(x)'
    pysrc = 'if x < 1:\n    mostre(x)'
    assert transpile(ptsrc) == pysrc, transpile(ptsrc)

    # Condicional - se/senão
    ptsrc = '''
se x < 1 então:
    mostre(x)
senão:
    mostre(-x)
'''
    pysrc = '''
if x < 1:
    mostre(x)
else:
    mostre(-x)
'''
    assert transpile(ptsrc) == pysrc, transpile(ptsrc)

    # Condicional - se/ou então/senão
    ptsrc = '''
se x < 1 então:
    mostre(x)
ou então se x > 3:
    mostre(0)
senão:
    mostre(-x)
'''
    pysrc = '''
if x < 1:
    mostre(x)
elif x > 3:
    mostre(0)
else:
    mostre(-x)
'''
    assert transpile(ptsrc) == pysrc, transpile(ptsrc)

    # Função
    ptsrc = 'função foo(x): retorne x'
    pysrc = 'def foo(x): return x'
    assert transpile(ptsrc) == pysrc, transpile(ptsrc)

    ptsrc = 'definir foo(x): retorne x'
    pysrc = 'def foo(x): return x'
    assert transpile(ptsrc) == pysrc, transpile(ptsrc)

    ptsrc = 'definir função foo(x): retorne x'
    pysrc = 'def foo(x): return x'
    assert transpile(ptsrc) == pysrc, transpile(ptsrc)

    ptsrc = 'definir função foo(x):\n    retorne x'
    pysrc = 'def foo(x):\n    return x'
    assert transpile(ptsrc) == pysrc, transpile(ptsrc)

    # Integração
    ptsrc = 'para cada x em [1, 2, 3]:\n    mostre(x ou z)'
    pysrc = 'for x in [1, 2, 3]:\n    mostre(x or z)'
    assert transpile(ptsrc) == pysrc, transpile(ptsrc)

    #
    # Recursos do Python não suportados com tradução
    #
    # classes, geradores, with, assert, ...

    #
    # Bug tracker
    #
    ptsrc = '\n\n\nrepetir 5 vezes:\n    mostre(42)'
    pysrc = '\n\n\nfor ___ in range(5):\n    mostre(42)'
    assert transpile(ptsrc) == pysrc, transpile(ptsrc)

    ptsrc = '\n\npara cada x em [1, 2, 3]: mostre(x)'
    pysrc = '\n\nfor x in [1, 2, 3]: mostre(x)'
    assert transpile(ptsrc) == pysrc, transpile(ptsrc)

    ptsrc = 'mostre(1)\n\n\n\npara cada x em [1, 2, 3]: mostre(x)'
    pysrc = 'mostre(1)\n\n\n\nfor x in [1, 2, 3]: mostre(x)'
    assert transpile(ptsrc) == pysrc, transpile(ptsrc)

    ptsrc = 'mostre(1)\n\n\n\npara x de 1 até 3: mostre(x)'
    pysrc = 'mostre(1)\n\n\n\nfor x in range(1, 3 + 1): mostre(x)'
    assert transpile(ptsrc) == pysrc, transpile(ptsrc)

    ptsrc = 'enquanto não x: mostre(x)'
    pysrc = 'while not x: mostre(x)'
    assert transpile(ptsrc) == pysrc, transpile(ptsrc)

    ptsrc = 'se não x: mostre(x)'
    pysrc = 'if not x: mostre(x)'
    assert transpile(ptsrc) == pysrc, transpile(ptsrc)

    ptsrc = '\n\n\nse não x: mostre(x)'
    pysrc = '\n\n\nif not x: mostre(x)'
    assert transpile(ptsrc) == pysrc, transpile(ptsrc)

    ptsrc = '\n\n\nsenão: mostre(x)'
    pysrc = '\n\n\nelse: mostre(x)'
    assert transpile(ptsrc) == pysrc, transpile(ptsrc)

    ptsrc = '\n\n\nsenão faça: mostre(x)'
    pysrc = '\n\n\nelse: mostre(x)'
    assert transpile(ptsrc) == pysrc, transpile(ptsrc)

    ptsrc = 'para x de 10 até 20: mostre(x)'
    pysrc = 'for x in range(10, 20 + 1): mostre(x)'
    assert transpile(ptsrc) == pysrc, transpile(ptsrc)

    ptsrc = 'para xx de 10 até 20: mostre(x)'
    pysrc = 'for xx in range(10, 20 + 1): mostre(x)'
    assert transpile(ptsrc) == pysrc, transpile(ptsrc)

    #
    # Possíveis extensões para a linguagem
    #
    # switch/case
    ptsrc = '''
    se x for:
        igual à 2:
            mostre(x)arg
        igual à 3:
            mostre(x + 2)
        senão:
            pass
    '''

    # do/while?
    ptsrc = '''
    faça:
        mostre(x)
    enquanto x < 2
    '''

if __name__ == '__main__':
    import doctest
    doctest.testmod()
