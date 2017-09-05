import pytest
import pytuga.lib.tuga_io as tuga_io

def test_mostrar(capsys):
	tuga_io.mostrar("test")
	out, err = capsys.readouterr()
	assert out == "test\n"

