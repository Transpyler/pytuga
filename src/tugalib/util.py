'''
Funções úteis que não devem ser exportadas para o API do tugalib.
'''


#
# Controle de funções sinônimas
#
def synonyms(*args):
    '''Decorador que marca sinônimos de uma função'''

    fmt_args = ['**%s**' % x for x in args]

    def decorator(func):
        if len(args) == 1:
            data = fmt_args[0]
        else:
            data = ', '.join(fmt_args[:-1])
            data += ' ou ' + fmt_args[-1]

        func.__synonyms__ = args
        func.__doc__ += (
            '\n\n'
            'Notes\n'
            '-----\n\n'
            'Também pode ser chamada como ' + data)
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
