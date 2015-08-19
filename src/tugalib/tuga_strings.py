def concatene(*args):
    '''Converte os argumentos para texto e concatena o resultado

    Exemplo
    -------

    >>> concatene('x = ', 2)
    'x = 2'
    '''

    return ''.join(map(str, args))
concatenar = concatene


def maiúsculas(texto):
    '''Converte um texto para letras maiúsculas

    Exemplo
    -------

    >>> maiúsculas('olá, mundo!')
    'OLÁ, MUNDO!'
    '''

    return texto.upper()


def minúsculas(texto):
    '''Converte um texto para letras minúsculas

    Exemplo
    -------

    >>> minúsculas('OLÁ, MUNDO!')
    'olá, mundo!'
    '''

    return texto.lower()

if __name__ == '__main__':
    import doctest
    doctest.testmod()
