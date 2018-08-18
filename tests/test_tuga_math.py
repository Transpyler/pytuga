import pytest
import math as _math
import random as _random

import pytuga.lib.tuga_math as math

pi = _math.pi
neperiano = _math.exp(1)

def test_raiz():

	assert(math.raiz(4) == 2.0)
	assert(math.raiz(16) == 4.0)

def test_seno():

	assert(math.seno(0) == 0.0)
	

def test_cosseno():

	assert(math.cosseno(0) == 1.0)
	

def test_tangente():

	assert(math.tangente(0) == 0.0)

def test_exponencial():

	assert(math.exponencial(1) == 2.718281828459045)

def test_logaritimo():

	assert(math.logarítimo(1) == 0.0)

def test_log10():

	assert(math.log10(10) == 1.0)

def test_modulo():

	assert(math.módulo(-1) == 1)

def test_sinal():

	assert(math.sinal(-32.0) == -1)

def test_arredondar():

	assert(math.arredondar(1.6) == 2)

def test_truncar():

	assert(math.truncar(1.6) == 1)
	assert(math.truncar(1.8) == 1)
	assert(math.truncar(5.3) == 5)
	assert(math.truncar(3.14) == 3)
	assert(math.truncar(1.806) == 1)
	assert(math.truncar(9.7) == 9)

def test_maximo():

	assert(math.máximo([1, 5, 42, 0]) == 42)

def test_minimo():

	assert(math.mínimo([1, 5, 42, 0]) == 0)

def test_soma():

	assert(math.soma([1, 2, 3, 4]) == 10)

def test_produto():

	assert(math.produto([1, 2, 3, 4, 5]) == 120)

def test_todos():

	assert(math.todos([True, True, True]) == True)
	assert(math.todos([True, False, True]) == False)

def test_algum():

	assert(math.algum([True, False, False]) == True)
	assert(math.algum([False, False, False]) == False)


def test_aleatorio():

	resultado1 = math.aleatório()
	resultado2 = math.aleatório()
	resultado3 = math.aleatório()
	resultado4 = math.aleatório()
	resultado5 = math.aleatório()

	assert(resultado1 >= 0 and resultado1 <= 1)
	assert(resultado2 >= 0 and resultado2 <= 1)
	assert(resultado3 >= 0 and resultado3 <= 1)
	assert(resultado4 >= 0 and resultado4 <= 1)
	assert(resultado5 >= 0 and resultado5 <= 1)

def test_inteiro_aleatório():
	
	resultado = math.inteiro_aleatório(1, 20)
	assert(resultado >= 1 and resultado <= 20)

def test_lancar_dado():

	resultado1 = math.lançar_dado()
	resultado2 = math.lançar_dado()
	resultado3 = math.lançar_dado()
	resultado4 = math.lançar_dado()
	resultado5 = math.lançar_dado()

	assert(resultado1 >= 1 and resultado1 <= 6)
	assert(resultado2 >= 1 and resultado2 <= 6)
	assert(resultado3 >= 1 and resultado3 <= 6)
	assert(resultado4 >= 1 and resultado4 <= 6)
	assert(resultado5 >= 1 and resultado5 <= 6)
