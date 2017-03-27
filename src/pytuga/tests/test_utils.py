from transpyler.utils import *


def test_keep_spaces():
    f = keep_spaces
    assert f('foo', 'bar') == 'foo'
    assert f(' \nfoo', 'bar') == 'foo'
    assert f(' \nfoo\n ', 'bar') == 'foo'
    assert f('foo', ' \nbar') == ' \nfoo'
    assert f('\n foo\n ', ' \nbar') == ' \nfoo'
    assert f('\n foo', ' \nbar') == ' \nfoo'
    assert f('foo\n', ' \nbar') == ' \nfoo'
    assert f('foo', ' \nbar\n ') == ' \nfoo\n '
    assert f('\n foo', ' \nbar\n ') == ' \nfoo\n '
    assert f('\n foo\n ', ' \nbar\n ') == ' \nfoo\n '
    assert f('foo\n ', ' \nbar\n ') == ' \nfoo\n '
    assert f('foo\n   bar', 'ham\n   spam') == 'foo\n   bar'

