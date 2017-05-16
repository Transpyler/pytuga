import collections
import keyword

TRANSLATIONS = dict(
    # Loops
    enquanto='while',
    para='for',
    quebre='break', quebrar='break',
    continuar='continue',  # continue='continue',
    para_cada='for',

    # Conditions
    se='if',
    senão='else', senao='else',
    ou_então_se='elif', ou_entao_se='elif',
    ou_se='elif',

    # Singleton values
    Falso='False', falso='False',
    Verdadeiro='True', verdadeiro='True',
    nulo='None', Nulo='None',

    # Operators
    é='is', eh='is',
    e='and',
    ou='or',
    não='not', nao='not',
    em='in', na='in', no='in',
    como='as',

    # Function definition
    função='def', funcao='def', definir='def', defina='def',
    retorne='return', retornar='return',
    gere='yield', gerar='yield',

    # Error handling
    tente='try', tentar='try',
    exceção='except', excecao='except',
    finalmente='finally',
    levante_error='raise', levantar_erro='raise',  # ???

    # Other
    apague='del', apagar='del',
    prossiga='pass', prosseguir='pass',
    classe='class',
    importe='import', importar='import',
    usando='with',  # ???
    # global='global',

    # Pytugues to pytugues
    até='ate',
    ateh='ate',
)

SEQUENCE_TRANSLATIONS = {
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

ERROR_GROUPS = collections.OrderedDict(
    (x, 'Repetição inválida: %s' % (' '.join(x)))
    for x in [
        ('faça', 'faça'), ('faça', 'fazer'), ('fazer', 'faça'),
        ('então', 'então'),
    ]
)

PURE_PYTG_KEYWORDS = set(TRANSLATIONS)
PURE_PYTG_KEYWORDS.update({'repetir', 'repita', 'vezes', 'cada', 'de',
                           'ate', 'fazer', 'faça', 'faca'})
kwlist = set(PURE_PYTG_KEYWORDS)
kwlist.update(keyword.kwlist)
constants = (
    'True', 'False', 'None',
    'Verdadeiro', 'Falso', 'Nulo',
    'verdadeiro', 'falso', 'nulo',
)


def iskeyword(k):
    """
    Return True if k is a valid Pytuguês keyword.
    """

    return k in kwlist


del keyword
