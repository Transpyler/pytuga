import pytest

from pytuga.core import exec

# Examples with bad syntax
bad_syntax_ = """
### loops
para cada x de 1:
    pass

##
para cada x de 1 em 1:
    pass

##
para cada x de 1 aa 1:
    pass

##
4 vezes:
    ...

##
repetir 4:
    ...

### create invalid python code (syntax error not raised by transpyler)
a b

""".split('##')[1:]


@pytest.fixture(params=bad_syntax_)
def bad_syntax(request):
    return request.param


def test_bad_syntax_raises_syntax_error(bad_syntax):
    with pytest.raises(SyntaxError):
        exec(bad_syntax)
