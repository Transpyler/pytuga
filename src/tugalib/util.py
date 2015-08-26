'''
Funções úteis que não devem ser exportadas para o API do tugalib.
'''


#
# Controle de funções sinônimas
#
def synonyms(*args):
    '''Decorador que marca sinônimos de uma função'''

    def decorator(func):
        func.__synonyms__ = args
        func.__doc__ += (
            '\n\n'
            'Sinônimos\n'
            '---------\n\n'
            '%s') % (', '.join(args))
        return func
    return decorator


def register_synonyms(global_ns):
    '''Registra todos os sinônimos no dicionário dado'''

    for _, func in list(global_ns.items()):
        try:
            for alias in func.__synonyms__:
                global_ns[alias] = func
        except AttributeError:
            pass
