========
Pytuguês
========

A syntaxe da linguagem de programação Python muitas vezes é comparada a um
pseudocódigo ou algorítimo executável. Ainda que existam alguns recursos 
avançados que certamente violam esta simplicidade, Python ainda é uma das 
linguagens de programação de uso geral com a sintaxe mais próxima de uma
descrição em linguagem natural. É claro que isto é verdade somente somente se 
você fala inglês.  

Pytuguês é uma versão da linguagem de programação Python que tenta se aproximar
o máximo possível da descrição de algorítimos em português. A motivação é 
fornecer uma ajuda para programadores iniciantes que tenham dificuldade com 
a língua inglesa. A vantagem do Pytuguês com relação à outras soluções 
semelhantes como o Portugol é que a transição para uma linguagem de programação
de verdade é bastante suave, já que é possível misturar código Python 
e Pytuguês no mesmo programa. O interpretador de Pytuguês, o ``pytuga``,
possui alguns recursos que ajudam na conversão de código em Pytuguês para 
Python (mentira, ainda não tem! :P).

Assim como o Python, o Pytuguês é uma linguagem dinâmica que não precisa ser
compilada. O código é executado diretamente pelo interpretador ou ainda pode
ser criado em modo interativo no estilo REPL (read/eval/print/loop, do inglês 
loop de ler, avaliar e imprimir). Neste modo, o interpretador executa 
imediatamente os comandos digitados pelo usuário e já mostra o resultado.

Tutorial
========

Um programa de computador pode ser entendido como uma série de instruções que
são executadas em sequência para completar uma determinada tarefa. O caso mais 
simples, onde queremos simplesmente mostrar uma mensgagem na tela é::

    >>> mostre("olá, mundo!")
    olá, mundo

A sintaxe do Pytuguês foi criada para produzir códigos que se assemelhem o 
máximo possível com um pseudocódigo em português. Queremos que o significado dos
programas seja o mais óbvio possível para um usuário que não conhece a 
linguagem (ou que nunca programaram na vida) e que a linguagem seja fácil de 
aprender e pareça natural para programadores iniciantes. 

Esta seção vai passar pelos principais recursos do Pytuguês para que você já 
possa programar em poucos minutos. Normalmente a primeira interação com a 
linguagem se dá através da programação gráfica, onde controlamos a trajetória e 
um pequeno "robô" na tela para desenhar figuras geométricas. Os comandos 
básicos são::

    >>> frente(100)   # avança 100 pixels
    >>> trás(100)     # recua 100 pixels
    >>> direita(90)   # gira 90 graus no sentido horário
    >>> esquerda(90)  # gira 90 graus no sentido anti-horário

Aos poucos podemos construir interações complexas utilizando estes blocos 
básicos e os recursos comuns de programação como repetições, execução 
condicional, interação com o usuário, etc.

Executando
----------



Operações matemáticas
---------------------

Talvez o uso mais simples do interpretador de Pytuguês seja como uma calculadora
avançada. Além das operações aritiméticas comuns, podemos salvar variáveis, 
utilizar funções matemáticas, definir nossas funções e vários outros recursos.

A notação para as operações matemáticas é a usual, onde apenas lembramos que 
as casas decimais são separadas por pontos e não por vírgulas::

    >>> 1 + 1     # soma
    >>> 2 - 1     # subtração
    >>> 3.14 * 2  # multiplicação
    >>> 1 / 2     # divisão
    >>> 3**2      # potência
    
É possível criar variáveis e reaproveitá-las em outras partes do código e
chamar as funções matemáticas mais comuns::

    >>> x = raiz(4)
    >>> x + 1
    3.0
    >>> x * x
    4.0
    >>> módulo(1 - x)
    1.0
    
O operador de igual "=", possui o sentido usual da maioria das linguagens de 
programação e na verdade significa atribuição de variáveis. Portanto um código
do tipo::
    
    >>> x = x + 1
    
não é uma falsidade matemática. Na realidade, estamos atribuindo um novo valor
a ``x`` que é igual ao valor anterior adicionado de ``1``.


Interação com o usuário
-----------------------


Repetições
----------



Condicionais
------------

Se quisermos executar um comando apenas se determinada condição for satisfeita,
então usamos o bloco "se"::

    x = leia_número("Diga um número: ")
    
    se x > 10 então faça:
        mostre("x é muito grande")
    
Neste caso, o comando ``mostre(...)`` será executado somente se o usuário 
digitar um valor maior que 10. Se quisermos adicionar uma condição que deve
ser executada caso o teste x > 10 falhe, basta adicionar um bloco do tipo 
"senão"::

    x = leia_número("Diga um número: ")
    
    se x > 10 então faça:
        mostre("x é muito grande")
    senão faça:
        mostre("x é pequeno")
        
Este código imprime na tela que x é muito grande, caso o usuário diga um número
maior que 10 ou imprime que x é pequeno, caso contrário. É possível adicionar
condições intermediárias usando o bloco "ou então se". Neste caso, somente a 
primeira condição a ser satisfeita é executada. A sintaxe completa é portanto:: 
    
    x = leia_número("Diga um número: ")
    
    se x > 10 então faça:
        mostre("x é muito grande")
    ou então se x == 7 faça:
        mostre("x é meu número da sorte")
    senão faça:
        mostre("x é pequeno")

Os termos "então faça" e "faça" no final de cada bloco são opcionais e o mesmo
código pode ser escrito na forma mais compacta como::

    x = leia_número("Diga um número: ")
    
    se x > 10:
        mostre("x é muito grande")
    ou então se x == 7:
        mostre("x é meu número da sorte")
    senão:
        mostre("x é pequeno")



  
Funções básicas
===============


Migrando para Python
====================

Pytuguês foi criado, desde o início, como uma linguagem simplificada para 
ajudar no aprendizado de programação. Pense como se fossem as rodinhas numa
bicicleta: elas ajudam no início quando não conseguimos manter o equilíbrio,
mas uma vez que você consegue manter a bicicleta equilibrada, elas começam a
atrapalhar.

...



