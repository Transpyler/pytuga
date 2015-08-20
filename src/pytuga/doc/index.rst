.. pytuguês documentation master file, created by
   sphinx-quickstart on Tue Aug 11 22:11:01 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

=====================================
Bem vindo à documentação do pytuguês!
=====================================

Conteúdo:

.. toctree::
   :maxdepth: 2


================
Índice e tabelas
================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


==========================
Especificação da linguagem
==========================

Execução condicional
====================

    se <condição> então:
        <BLOCO DE CÓDIGO>
    ou então se <condição>:
        <BLOCO DE CÓDIGO>
    senão:
        <BLOCO DE CÓDIGO>


Laços e repetições
==================

repetir
-------

Existem várias estruturas de repetição em pytuguês. A mais simples de todas
é o comando ``repetir``::

    >>> repetir 3 vezes:
    ...     mostre("olá!")
    olá!
    olá!
    olá!
    
O comando repetir simplesmente executa o bloco de código seguinte pelo 
número especificado de vezes. É importante tomar cuidado com os espaços em 
branco pois o início e o fim do bloco que será executado é definido pelo nível
de indentação.

A sintaxe do comando repetir é muito simples::

    repetir <número> vezes:
        <BLOCO DE CÓDIGO>
        
onde o número de vezes pode ser uma constante inteira ou uma variável com valor 
do tipo inteiro.

enquanto
--------

O comando ``enquanto`` executa um bloco de código enquanto uma determinada 
condição for verdadeira::
    
    >>> x = 0
    >>> enquanto x < 3 faça:
    ...     mostre('olá')
    ...     x += 1
    olá!
    olá!
    olá!
    
A sintaxe geral é::
     
    enquanto <condição> faça:
        <BLOCO DE CÓDIGO>

e faz com que o bloco de código seja executado enquanto a condição dada for 
verdadeira. A palavra chave "faça" é opcional, de forma que o código acima 
também possui a sintaxe alternativa::

    enquanto <condição>:
        <BLOCO DE CÓDIGO>



para cada ...
-------------

...

    >>> para cada x de 0 até 2 faça:
    ...     mostre('olá')
    
Sintaxe geral::
    
    para cada <nome> de <início> até <fim> faça:
        <BLOCO DE CÓDIGO>
        
    para cada <nome> de <início> até <fim> a cada <passo> faça:
        <BLOCO DE CÓDIGO>  
    

    >>> para cada x em [0, 1, 2] faça:
    ...     mostre('olá')
     
     
Funções
=======

Definimos uma função com a sintaxe

    definir função <nome>(...):
        <DEFINIÇÃO>
        
        

