import pytest
import time as _time

import pytuga.lib.tuga_std as std 

def test_real():
	
	assert(std.real(5) == 5.0)
	assert(std.real(673.23) == 673.23)
	assert(std.real("673.23") == 673.23)
	assert(std.real("3.1415") == 3.1415)
	assert(std.real(42) == 42.0)

def test_inteiro():

	assert(std.inteiro(4.3) == 4)
	assert(std.inteiro(44.6E-1) == 4)
	assert(std.inteiro("23") == 23)

def test_booleano():

	assert(std.booleano(0) == False)
	assert(std.booleano(1) == True)

def test_binario():

	assert(std.binário(2796202) == '0b1010101010101010101010')
	assert(std.binário(3) == '0b11')
	assert(std.binário(42) == '0b101010')

def test_octal():

	assert(std.octal(22052015) == '0o124076257')
	assert(std.octal(1024) == '0o2000')
	assert(std.octal(42) == '0o52')

def test_hexadecimal():

	assert(std.hexadecimal(6745) == '0x1a59')
	assert(std.hexadecimal(2017) == '0x7e1')
	assert(std.hexadecimal(42) == '0x2a')

def test_caractere():

	assert(std.caractere(227) == 'ã')
	assert(std.caractere(231) == 'ç')
	assert(std.caractere(224) == 'à')

def test_tamanho():

	assert(std.tamanho("programando em python") == 21)
	assert(std.tamanho("Testando o pytuga") == 17)
	assert(std.tamanho("") == 0)

def test_enumerar():

	musica = ['uni', 'duni', 'te']

	assert(std.listar(std.enumerar(musica)) == [(0, 'uni'), (1, 'duni'), (2, 'te')])

def test_dicionario():

	assert(std.dicionário([(0, 'zero'), (1, 'um'), (2, 'dois')]) == {0: 'zero', 1: 'um', 2: 'dois'})

def test_tupla():

	assert(std.tupla([1, 2, 3]) == (1, 2, 3))

def test_lista():

	assert(std.lista(None) == [])
	assert(std.lista('olá') == ['o', 'l', 'á'])
[1, 2, 3, 4, 5]

def test_listar():

	assert(std.listar('olá') == ['o', 'l', 'á'])

def test_listar_invertido():

	assert(std.listar_invertido(['uni', 'duni', 'te']) == ['te', 'duni', 'uni'])

def test_ordenado():

	assert(std.ordenado([5, 2, 3, 1, 4]) == [1, 2, 3, 4, 5])

def test_texto():

	assert(std.texto(42) == "42")
