====================
Migrando para Python
====================

Pytuguês foi criado, desde o início, como uma linguagem simplificada para
ajudar no aprendizado de programação. Pense como se fossem as rodinhas numa
bicicleta: elas ajudam no início quando não conseguimos manter o equilíbrio,
mas uma vez que você consegue manter a bicicleta equilibrada, elas começam a
atrapalhar. Este é um guia para converter o código Pytuguês para Python.

Comandos básicos
================

Condicionais
------------

Os comandos ``se/senão`` podem ser convertidos para Python traduzindo os comandos
``se`` para ``if``, ``senão`` para ``else`` e ``ou se`` para ``elif``. O Python
não aceita as palavras opcionais ``então`` e ``faça`` (nem mesmo traduzindo-as).
Deste modo, o exemplo abaixo em Pytuguês

::

    se x % 2 == 1 então:
        y = (x + 1) / 2
    ou então se x == 0 faça:
        y = 0.0
    senão faça:
        y = x / 2

torna-se

::

    if x % 2 == 1:
        y = (x + 1) / 2
    elif x == 0:
        y = 0.0
    else:
        y = x / 2

Laço ``enquanto``
-----------------

Para convertermos um laço do tipo ``enquanto``, simplesmente traduzimos para o
correspondente em inglês ``while``. Lembramos quet a palavra opcional ``faça``
não é suportada em Python.

Deste modo, o código

::

    enquanto x < 100 faça:
        x = x - 1

vira simplesmente

::

    while x < 100:
        x = x - 1

Laço ``para cada``
----------------

O laço ``para cada`` vira o comando ``for`` em Python. Deste modo, se quisermos
iterar sobre uma lista, como no código abaixo, basta fazer::

    S = 0
    para cada x em [1, 4, 9, 16] faça:
        S += x

Em Python, isto seria::

    S = 0
    for x in [1, 4, 9, 16]:
        S += x

Observe que a instrução ``faça`` não aparece em Python.

Devemos tomar cuidado em utilizar a versão numérica do comando ``para cada`` já
que não existe uma correspondência direta em Python. Em Python, o laço ``for``
sempre atua em uma sequência. Se quisermos iterar sobre uma sequência de números,
é necessário criar esta sequência manualmente.

O método mais conveniente é utilizar a função ``range()`` do Python. Ela pode
ser chamada de três maneiras, o que pode deixar as coisas um pouco confusas.

``range(n)``:
    Gera **n** números de **0** até **n - 1**. É importante tomar cuidado com
    isto pois ``range(5)`` gera os números ``0, 1, 2, 3, 4``, **não incluindo**
    o valor final de ``5``.
``range(a, b)``:
    Como a anterior, mas inicia a geração de números a partir de **a** e não de
    **0**. ``range(0, n)`` é idêntico a ``range(n)``.
``range(a, b, c)``:
    Como a anterior, cria os números saltando a cada ``c``. Assim,
    ``range(2, 10, 2)`` gera os números de 2 até 9, saltando de 2 em dois
    (``2, 4, 6, 8``).

Podemos converter o código Pytuguês abaixo::

    S = 0
    para cada x de 1 até 100:
        S += x

E o correspondente Python::

    S = 0
    for x in range(1, 101):
        S += x

Note o limite superior do ``range`` igual à 101, para incluir o número 100 na
sequênca.


Laço ``repetir``
----------------

O laço ``repetir`` não existe em Python. No entanto, podemos trocá-lo facilmente
por um laço do tipo for::

    repetir 4 vezes:
        frente(100)
        esquerda(90)

Em Python::

    for x in range(4):
        frente(100)
        esquerda(90)


Funções
=======

A maior parte das funções possui uma tradução direta para Python. Para sabermos
o equivalente de cada função, devemos consultar a documentação da mesma, fazendo
``help(<nome da função>)``.

