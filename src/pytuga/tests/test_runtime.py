import pytest
from pytuga.core import exec


def test_exec_with_locals():
    loc = {}
    glob = {}
    exec("a = 1", glob, loc)
    assert loc
    assert glob
    assert loc['a'] == 1
