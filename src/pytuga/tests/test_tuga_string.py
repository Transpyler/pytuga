import pytest

import pytuga.lib.tuga_strings as strg

def test_concaternar():
	assert(strg.concatenar('x = ', 2) == 'x = 2')

def test_concatenar_lista():
	assert(strg.concatenar_lista(['a', 'b', 'c', 1, 2, 3]) == 'abc123')


def test_unir_valores():

	assert(strg.unir_valores(', ', 1, 2, 3) == '1, 2, 3')

def test_unir_lista():

	assert(strg.unir_lista(', ', [1, 2, 3]) == '1, 2, 3')

def test_formatar():

	assert(strg.formatar('%i = %.2f', 42, 42) == '42 = 42.00')
	assert(strg.formatar('{0} = {1}', 42, 42) == '42 = 42')

def test_substituir():

	assert(strg.substituir('Olá, pessoal!', 'pessoal', 'mundo') == 'Olá, mundo!')

def test_maisculas():

	assert(strg.maiúsculas('olá, mundo!') == 'OLÁ, MUNDO!')

def test_minusculas():

	assert(strg.minúsculas('OLÁ, MUNDO!') == 'olá, mundo!')