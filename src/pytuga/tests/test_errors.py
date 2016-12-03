import pytest
from pytuga.core import transpile, exec
from pytuga.lexer import fromstring

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


### create invalid python code (syntax error not raised by transpiler)
a b

""".split('##')[1:]


@pytest.fixture(params=bad_syntax_)
def bad_syntax(request):
    return request.param


def test_bad_syntax_raises_syntax_error(bad_syntax):
    with pytest.raises(SyntaxError):
        exec(bad_syntax)