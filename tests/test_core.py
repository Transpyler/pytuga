from pytuga import namespace, compile, transpile, exec


def test_namespace():
    ns = namespace()


def test_transpile():
    py = transpile('enquanto verdadeiro ou falso: prosseguir')
    assert py == 'while True or False: pass'


def test_exec():
    D = {}
    exec('x = raiz(0 ou 1) ', D)
    assert D['x'] == 1


def test_compile():
    code = compile('x = raiz(0 ou 1)', '<string>', 'exec')

    D = {}
    exec(code, D)
    assert D['x'] == 1

    D = {}
    exec(code, D)
    assert D['x'] == 1
