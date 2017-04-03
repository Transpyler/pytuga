===============================
Definições e design do Pytuguês
===============================

Zen do Pytuguês
===============

::
    import this

    The Zen of Python, by Tim Peters

    Beautiful is better than ugly.
    Explicit is better than implicit.
    Simple is better than complex.
    Complex is better than complicated.
    Flat is better than nested.
    Sparse is better than dense.
    Readability counts.
    Special cases aren't special enough to break the rules.
    Although practicality beats purity.
    Errors should never pass silently.
    Unless explicitly silenced.
    In the face of ambiguity, refuse the temptation to guess.
    There should be one-- and preferably only one --obvious way to do it.
    Although that way may not be obvious at first unless you're Dutch.
    Now is better than never.
    Although never is often better than *right* now.
    If the implementation is hard to explain, it's a bad idea.
    If the implementation is easy to explain, it may be a good idea.
    Namespaces are one honking great idea -- let's do more of those

Pytuguês é um dialeto de Python, com sotaque lusitano. Python é uma linguagem
excelente para o ensino de programação e o foco do Pytuguês é exatamente este.
No entanto, Python também é uma linguagem de uso profissional e isto acaba
levando a algumas decisões que enfatizam as "boas práticas", mas que podem
aumentar um pouco a curva de dificuldade de um programador iniciante.

É lógico que acreditamos que *"Beautiful is better than ugly"*, *"Simple is better
than complex"*, etc. Dado o foco do Pytuguês, devemos acrescentar algumas
prioridades no topo::

    É possível programar sem saber inglês.
    Programar é divertido.
    Até uma criança consegue fazer.
    Programadores não gostam de surpresas.
    Programadores não gostam de erros, mas devemos destacar e não esconder os
    erros de um programa.

Sendo assim, as vezes desviamos de uma linguagem puramente "pythonica" para para
priorizar estes novos elementos.


Questões específicas do Pytuguês
================================

Acentuação:
    Diferentemente do Inglês, Português possui muitas palavras com acentos.
    Deste modo, tanto elementos básicos da sintaxe tais quais palavras chave e
    comandos, quanto os elementos definidos pelo usuário como funções e variáveis devem ser
    acentuados normalmente. Acentos são fáceis de se esquecer e algumas
    pessoas realmente não gostam da idéia de acentuar código fonte. Pensando
    nisto, disponibilizamos "apelidos" não acentuados para cada comando e cada
    função na biblioteca básica.
Verbosidade:
    Não esperamos que se criem códigos para "produção" em Pytuguês, nem
    imaginamos Pytuguês como uma linguagem extremamente produtiva. Deste modo,
    achamos que é mais importante deixar que a intenção de um programa seja
    clara do que tornar os programs compactos e fáceis de digitar. Por isto, sempre
    optamos por nomes longos e explícitos ao invés de nomes curtos e ambíguos.
    Inclusive acreditamos que o fato de Python exigir menos digitação funciona
    como um incentivo de migração do Pytuguês para o Python.
Tempos verbais:
    O inglês muitas vezes não diferencia o infinitivo do imperativo (a não ser
    pelo "to", como em "to eat" vs. "eat"). O Português conjuga o imperativo
    como em "comer" vs "coma" e ambas as formas parecem maneiras válidas de
    expressar uma ação em um programa. O modo imperativo se baseia na
    idéia que um programa é uma sequência de comandos transmitidos para o
    computador executar, como em ``mostre('olá, mundo!')``.
    Já o modo infinitivo concebe um programa como uma idéia abstrata e impessoal,
    como em ``mostrar('olá, mundo!')``. O Pytuguês suporta as duas
    formas de cada comando, tanto no nível da sintaxe, quanto no nível da
    biblioteca de funções.
Argumentos de funções:
    Iniciantes muitas vezes tem dificuldades em utilizar funções com número
    variável de argumentos. A documentação do Pytuguês evita mencionar
    argumentos variáveis (mesmo quando eles são suportados) e a maior
    parte das funções do Pytuguês espera um número fixo de argumentos. De um
    modo geral, preferimos criar duplicatas de funções em suas versões com cada
    número de argumentos.


Estensões sintáticas para o Python
==================================

Além da tradução (e algumas vezes adição de palavras chaves redundantes, apenas
para enfatizar o contexto), o Pytuguês possui algumas estensões sintáticas
com relação ao Python.


Repetir
-------

A estrutura de repetição mais simples é dada pelo comando "repetir" (ou repita),
que simplesmente repete o conteúdo de um bloco pelo número especificado de vezes

::

    repetir <N> vezes:
        <BLOCO DE COMANDOS>

O laço "repetir" é a introdução às estruturas de repetição, e muitas vezes é
o suficiente para problemas simples como desenhar figuras na tela.


Range explícito
---------------

Programadores iniciantes possuem uma certa dificuldade com a função range().
É uma função que possui três assinaturas diferentes e é fácil confundir a
indexação baseada em zero. Se pensarmos em termos de intervalos numéricos,
ela inclui o ponto de início, mas exclui o ponto final. Para evitar estas
complicações, Pytuguês também suporta o laço::

    para cada <VAR> de <A> até <B> [a cada <C>] faça:
        <BLOCO DE COMANDOS>

Na nova forma, tanto o início do intervalo numérico quanto o seu fim estão
marcados explicitamente. Isto deixa o código mais óbvio para aqueles que
nunca entraram em contato com a linguagem e desconhecem as particularidades da
função "range()". Por examplo, contamos de 1 até 10 fazendo::

    para cada x de 1 até 10 faça:
        mostre(x)

Sintaxe redundante
------------------

Alguns comandos do Pytuguês introduzem sintaxe redundante, com a única função
de tornar a intenção do programador mais explícita. Estas palavras redundantes
são opcionais e o programador pode escolher utilizá-las ou não, de acordo com
o estilo pessoal::

    # Laços
    para [cada] x em L [faça]:
        <BLOCO>

    para [cada] x de 1 até 10 [a] cada 2 [faça]:
        <BLOCO>

    enquanto x > 10 [faça]:
        <BLOCO>

    # Condicionais
    se x > 10 [então] [faça]:
        <BLOCO>
    ou [então] se x > 10 [então] [faça]:
        <BLOCO>
    senão [faça]:
        <BLOCO>


Problemas abertos
=================

* Operador "is" é traduzido como "é". A versão não-acentuada colide com o
  operador lógico "e". Encontrar outros sinónimos para identidade?
  ``x [é] idêntico [a] y``?
* Keywords com espaços: Pytuguês possui alguns comandos que funcionam como
  "keywords" com espaços (Ex.: para x de 1 até 10 *a cada* 2: ...). O
  identificador "a" poderia ser tratado como keyword incodicional ou poderia
  ser tratado assim somente quando aparecer em "a cada". Escolhemos a segunda
  opção pois se "a" for promovido a uma keyword, podemos ter várias colisões de
  nomes.
* Dois pontos são necessários para delimitar o início de um bloco? O uso de ":"
  para delimitar o início de um bloco é redundante em Python (já que a
  indentação sozinha já é capaz de resolver esta questão), mas aumenta a
  legibilidade do código e possui uma certa congruência com o uso do mesmo
  símbolo em linguagem natural. O fato é que iniciantes frequentemente esquecem
  os dois pontos e se frustram quando o código não funciona. Devemos ignorar a
  ausência dos mesmos ou simplesmente mostrar uma mensagem de erro mais clara,
  explicando que o usuário deve inserir o ":" em uma linha específica?
  Esta ausência deve ser tolerada apenas em sintaxe específica do Pytuguês ou
  também em sintaxe Python?
