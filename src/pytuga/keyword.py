import keyword

TRANSLATIONS = dict(
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
        # abrir='with'?
        # global='global',
)
PURE_PYTG_KEYWORDS = set(TRANSLATIONS)
PURE_PYTG_KEYWORDS.update({'repetir', 'repita', 'vezes', 'cada', 'de', 'até'})
kwlist = set(PURE_PYTG_KEYWORDS)
kwlist.update(keyword.kwlist)
constants = (
    'True', 'False', 'None',
    'Verdadeiro', 'Falso', 'Nulo',
    'verdadeiro', 'falso', 'nulo',
)


def iskeyword(k):
    """Return True if k is a valid Pytuguês keyword."""

    return k in kwlist


del keyword
