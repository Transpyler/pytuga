BRACES = '()[]{}'

TOKEN_EMPTY = {'faça', 'definir'}

TOKEN_TRANSLATIONS = dict(
    # Loops
    enquanto='while',
    # para cada='for',
    termine='break',
    # continue='continue',

    # Condicionais
    se='if',
    senão='else',
    # ou então='elif'

    # Valores de verdade
    Falso='False',
    falso='False',
    Verdadeiro='True',
    verdadeiro='True',
    nulo='None',
    Nulo='None',

    # Operadores
    é='is',
    e='and',
    ou='or',
    não='not',
    em='in',
    na='in',
    no='in',
    como='as',

    # Funções
    função='def',
    retorne='return',
    gere='yield',

    # Tratamento de erros
    tente='try',
    exceção='except',
    finalmente='finally',
    # jogue erro='raise'

    # Outros
    apague='del',
    prossiga='pass',
    # global='global'
    classe='class',
    importe='import',
    abrir='with',
)

OP_TRANSLATIONS = dict(
    mod='%',
    div='//',
)
