import pytest
from pytuga.lexer import transpile, fromstring


#
# Passthru translations
#
@pytest.fixture(
    params=['x + y', 'x / y', 'x | y']
)
def passtru(request):
    return request.param


def test_passthru(passtru):
    assert transpile(passtru) == passtru


#
# Test tokenizers
#
def pytg(src):
    return [repr(x) for x in fromstring(transpile(src))]

def py(src):
    return [repr(x) for x in fromstring(src)]


def test_repetir():
    ptsrc = 'repetir 4 vezes: mostre(42)'
    pysrc = 'for ___ in range(4): mostre(42)'
    assert pytg(ptsrc) == py(pysrc)

    ptsrc = 'repetir 4 vezes:\n    mostre(42)'
    pysrc = 'for ___ in range(4):\n    mostre(42)'
    assert pytg(ptsrc) == py(pysrc)

    ptsrc = '\n\n\nrepetir 5 vezes:\n    mostre(42)'
    pysrc = '\n\n\nfor ___ in range(5):\n    mostre(42)'
    assert pytg(ptsrc) == py(pysrc)


def test_para_cada():
    ptsrc = 'para cada x em [1, 2, 3]: mostre(x)'
    pysrc = 'for x in [1, 2, 3]: mostre(x)'
    assert pytg(ptsrc) == py(pysrc)

    ptsrc = 'para cada x em [1, 2, 3]:\n    mostre(x)'
    pysrc = 'for x in [1, 2, 3]:\n    mostre(x)'
    assert pytg(ptsrc) == py(pysrc)

    ptsrc = 'para cada x em [1, 2, 3] faça: mostre(x)'
    pysrc = 'for x in [1, 2, 3]: mostre(x)'
    assert pytg(ptsrc) == py(pysrc)


def test_para_cada_in_range():
    ptsrc = 'para x de 1 até 10: mostre(x)'
    pysrc = 'for x in range(1, 10 + 1): mostre(x)'
    assert pytg(ptsrc) == py(pysrc)

    ptsrc = 'para x de 1 até 10:\n    mostre(x)'
    pysrc = 'for x in range(1, 10 + 1):\n    mostre(x)'
    assert pytg(ptsrc) == py(pysrc)

    ptsrc = 'para x de 1 até 10 faça: mostre(x)'
    pysrc = 'for x in range(1, 10 + 1): mostre(x)'
    assert pytg(ptsrc) == py(pysrc)

    ptsrc = 'para x de 1 até 10 a cada 2: mostre(x)'
    pysrc = 'for x in range(1, 10 + 1, 2): mostre(x)'
    assert pytg(ptsrc) == py(pysrc)

    ptsrc = 'para x de 1 até 10 a cada 2 faça: mostre(x)'
    pysrc = 'for x in range(1, 10 + 1, 2): mostre(x)'
    assert pytg(ptsrc) == py(pysrc)

    ptsrc = 'para x de 1 até 10 a cada 2 faça:\n    mostre(x)'
    pysrc = 'for x in range(1, 10 + 1, 2):\n    mostre(x)'
    assert pytg(ptsrc) == py(pysrc)

    ptsrc = '\n\npara cada x em [1, 2, 3]: mostre(x)'
    pysrc = '\n\nfor x in [1, 2, 3]: mostre(x)'
    assert pytg(ptsrc) == py(pysrc)

    ptsrc = 'para x de 10 até 20: mostre(x)'
    pysrc = 'for x in range(10, 20 + 1): mostre(x)'
    assert pytg(ptsrc) == py(pysrc)

    ptsrc = 'para xx de 10 até 20: mostre(x)'
    pysrc = 'for xx in range(10, 20 + 1): mostre(x)'
    assert pytg(ptsrc) == py(pysrc)


def test_enquanto():
    ptsrc = 'enquanto x < 1: mostre(x)'
    pysrc = 'while x < 1: mostre(x)'
    assert pytg(ptsrc) == py(pysrc)

    ptsrc = 'enquanto x < 1 faça: mostre(x)'
    pysrc = 'while x < 1: mostre(x)'
    assert pytg(ptsrc) == py(pysrc)

    ptsrc = 'enquanto x < 1 faça:\n    mostre(x)'
    pysrc = 'while x < 1:\n    mostre(x)'
    assert pytg(ptsrc) == py(pysrc)

    ptsrc = 'enquanto não x: mostre(x)'
    pysrc = 'while not x: mostre(x)'
    assert pytg(ptsrc) == py(pysrc)


def test_se():
    ptsrc = 'se x < 1 então: mostre(x)'
    pysrc = 'if x < 1: mostre(x)'
    assert pytg(ptsrc) == py(pysrc)

    ptsrc = 'se x < 1: mostre(x)'
    pysrc = 'if x < 1: mostre(x)'
    assert pytg(ptsrc) == py(pysrc)

    ptsrc = 'se x < 1 então:\n    mostre(x)'
    pysrc = 'if x < 1:\n    mostre(x)'
    assert pytg(ptsrc) == py(pysrc)

    ptsrc = 'se não x: mostre(x)'
    pysrc = 'if not x: mostre(x)'
    assert pytg(ptsrc) == py(pysrc)

    ptsrc = '\n\n\nse não x: mostre(x)'
    pysrc = '\n\n\nif not x: mostre(x)'
    assert pytg(ptsrc) == py(pysrc)


def test_se_senao():
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
    assert pytg(ptsrc) == py(pysrc)

def test_se__ou_entao_se__senao():
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
    assert pytg(ptsrc) == py(pysrc)


def test_funcion_definition():
    ptsrc = 'função foo(x): retorne x'
    pysrc = 'def foo(x): return x'
    assert pytg(ptsrc) == py(pysrc)

    ptsrc = 'definir foo(x): retorne x'
    pysrc = 'def foo(x): return x'
    assert pytg(ptsrc) == py(pysrc)

    ptsrc = 'definir função foo(x): retorne x'
    pysrc = 'def foo(x): return x'
    assert pytg(ptsrc) == py(pysrc)

    ptsrc = 'definir função foo(x):\n    retorne x'
    pysrc = 'def foo(x):\n    return x'
    assert pytg(ptsrc) == py(pysrc)

    # Integração
    ptsrc = 'para cada x em [1, 2, 3]:\n    mostre(x ou z)'
    pysrc = 'for x in [1, 2, 3]:\n    mostre(x or z)'
    assert pytg(ptsrc) == py(pysrc)


#
# Bug tracker: these are all examples that have failed in some point and do not
# belong to any category in special
#
def test_separate_command_blocks_regression():
    ptsrc = 'mostre(1)\n\n\n\npara cada x em [1, 2, 3]: mostre(x)'
    pysrc = 'mostre(1)\n\n\n\nfor x in [1, 2, 3]: mostre(x)'
    assert pytg(ptsrc) == py(pysrc)

    ptsrc = 'mostre(1)\n\n\n\npara x de 1 até 3: mostre(x)'
    pysrc = 'mostre(1)\n\n\n\nfor x in range(1, 3 + 1): mostre(x)'
    assert pytg(ptsrc) == py(pysrc)

    ptsrc = '\n\n\nsenão: mostre(x)'
    pysrc = '\n\n\nelse: mostre(x)'
    assert pytg(ptsrc) == py(pysrc)

    ptsrc = '\n\n\nsenão faça: mostre(x)'
    pysrc = '\n\n\nelse: mostre(x)'
    assert pytg(ptsrc) == py(pysrc)


#
# Simple binary operators
#
def test_logical_and():
    ptsrc = 'x e y'
    pysrc = 'x and y'
    assert transpile(ptsrc) == pysrc


def test_is_operator():
    ptsrc = 'x é verdadeiro'
    pysrc = 'x is True'
    assert transpile(ptsrc) == pysrc


if __name__ == '__main__':
    import os
    os.system('py.test test_pytuga.py -q')
