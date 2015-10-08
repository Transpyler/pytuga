BRACES = '()[]{}'

TOKEN_EMPTY = {'faça', 'definir'}

TOKEN_TRANSLATIONS = dict(
    # Loops
    enquanto='while',
    # para cada='for',
    quebre='break',
    quebrar='break',
    # continue='continue',
    continuar='continue',

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
    retornar='return',
    gere='yield',
    gerar='yield',

    # Tratamento de erros
    tente='try',
    tentar='try',
    exceção='except',
    finalmente='finally',
    # jogue erro='raise'

    # Outros
    apague='del',
    prossiga='pass',
    # global='global'
    classe='class',
    importe='import',
    importar='import',
    abrir='with',
)

OP_TRANSLATIONS = dict(
    mod='%',
    div='//',
)
