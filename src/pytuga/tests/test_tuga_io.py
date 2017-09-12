import pytest
from faker import Faker
from random import randint
import pytuga.lib.tuga_io as tuga_io
fake = Faker()

def test_mostrar_alerta(capsys):
	random_name = fake.name()
	tuga_io.mostrar(random_name)
	out, err = capsys.readouterr()
	assert out == "{}\n".format(random_name)
	tuga_io._alert(random_name)
	out, err = capsys.readouterr()
	assert out == "{}\n".format(random_name)
	tuga_io.alerta(random_name)
	out, err = capsys.readouterr()
	assert out == "{}\n".format(random_name)

def test_mostrar_formatado(capsys):
	random_name = fake.name()
	name_tag = "{} %s".format(random_name)
	random_int = randint(0, 100)
	tuga_io.mostrar_formatado(name_tag, random_int)
	out, err = capsys.readouterr()
	assert out == "{} {}\n".format(random_name, random_int)

def test_pausar(capsys):
	with capsys.disabled():
		tuga_io.pausar()
