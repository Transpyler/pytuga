import pytest
import pytuga


def test_project_defines_author_and_version():
    assert hasattr(pytuga, '__author__')
    assert hasattr(pytuga, '__version__')
