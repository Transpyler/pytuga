import pytest

from pytuga.lib.curses import Lista

def test_acrescentar():

	l = [1, 2, 3, 4]

	lista = Lista(l)
	lista.acrescentar(5)

	assert(lista == [1, 2, 3, 4, 5])

def test_limpar():

	l = [1, 2, 3, 4]

	lista = Lista(l)
	lista.limpar()

	assert(lista == [])

def test_copia():


	l = [1, 2, 3, 4]

	lista = Lista(l)
	lista.cópia()

	assert(lista == [1, 2, 3, 4])

def test_contar():


	l = [1, 2, 3, 4, 5, 5, 5, 5, 5]
	lista = Lista(l)

	assert(lista.contar(5) == 5)

def test_estender():

	l = [1, 2, 3, 4, 5]
	lista = Lista(l)
	lista.estender([6, 7, 8, 9])

	assert(lista == [1, 2, 3, 4, 5, 6, 7,8, 9])

def test_indice():

	l = [1, 2, 3, 4, 5]
	lista = Lista(l)
	assert(lista.índice(5) == 4)

def test_indice_em_intervalo():

	l = [1, 2, 2, 3, 3, 4, 4, 4, 4]
	lista = Lista(l)

	assert(lista.índice_em_intervalo(4, 0, 8) == 5)

def test_inserir():

	l = [1, 3]
	lista = Lista(l)
	lista.inserir(1, 2)

	assert(lista == [1, 2, 3])

def test_remover():

	l = [1, 2, 3, 4, 4]
	lista = Lista(l)
	lista.remover(4)

	assert(lista == [1, 2, 3, 4])

def test_inverter():

	l = [1, 2, 3, 4]
	lista = Lista(l)
	lista.inverter()

	assert(lista == [4, 3, 2, 1])

def test_ordenar():

	l = [6, 5, 4, 3, 2, 1]
	lista = Lista(l)

	lista.ordenar()

	assert(lista == [1, 2, 3, 4, 5, 6])

def test_ordernar_por():

	l = ['Z', 'A', 'S', 'Y', 'B', 'X']
	lista = Lista(l)

	lista.ordenar_por(str.lower)

	assert(lista == ['A', 'B', 'S', 'X', 'Y', 'Z'])

def test_retirar():

	l = [1, 2, 3, 4, 5, 5]
	lista = Lista(l)
	lista.retirar()

	assert(lista == [1, 2, 3, 4, 5])

def test_retirar_de():

	l = [1, 2, 2, 3, 4, 5]
	lista = Lista(l)
	lista.retirar_de(2)

	assert(lista == [1, 2, 3, 4, 5])
