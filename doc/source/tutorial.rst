========
Tutorial
========

Um programa de computador pode ser entendido como uma série de instruções que são executadas em sequência para completar uma determinada tarefa. As tarefas podem ir do extremamente simples, como mostrar mensagens na tela, até o extremamente complicado como fazer um cálculo científico ou dirigir um carro. No caso do Pytuguês você provavelmente iniciará o contato com a programação desenhando figuras na tela. No início, iremos programar o computador para realizar tarefas como quadrados, triângulos, estrelas ou outras figuras geométricas. 

Podemos iniciar o ambiente de programação em modo texto invocando o comando *pytuga* no terminal. Uma alternativa gráfica mais amigável é o *Tugalinhas* que também é instalado junto com este pacote.

Uma vez aberto o *Tugalinhas* ou o *pytuga*, nos deparamos com o shell de Pytuguês (que inicia com ``>>>``) onde podemos digitar comandos diretamente. Para mostrar uma mensagem na tela, por exemplo, digite::

    >>> mostre("olá, mundo!")
    olá, mundo
    
Experimente também com operações básicas, para ter um sabor dos recursos disponíveis no terminal de Pytuguês::

    >>> 5 * 4 * 3 * 2 * 1
    120
    >>> 40 + 2
    42

A sintaxe do Pytuguês foi criada para produzir códigos que se assemelhem o máximo possível com um pseudocódigo em português. Queremos que o significado dos programas mais simples seja óbvio para um usuário que não conhece a linguagem ou que nunca programou na vida e que a linguagem seja fácil de aprender e pareça natural para programadores iniciantes. O Python oferece isto para falantes do inglês, queremos oferecer o mesmo para Brasileiros, Portugueses, Angolanos, etc. 

Esta seção vai percorrer os principais recursos do Pytuguês para que você possa começar a programar em poucos minutos. Normalmente a primeira interação com o Pytuguês se dá através da programação gráfica, onde controlamos a trajetória de um pequeno "robô" que desenha figuras geométricas na tela. Inicie o Tugalinhas ou o pytuga. Os comandos básicos para interagir com o cursor na tela são::

    >>> frente(100)   # avança 100 pixels
    >>> trás(100)     # recua 100 pixels
    >>> direita(90)   # gira 90 graus no sentido horário
    >>> esquerda(90)  # gira 90 graus no sentido anti-horário
    

Digite os comandos no terminal interativo para ver o Tuga se mexer. Aos poucos podemos construir interações complexas e interessantes utilizando estes blocos básicos e os recursos comuns de programação como repetições, execução condicional, interação com o usuário, etc.

**Desafio!**

Faça um programa que desenhe uma figura regular como quadrado, triângulo, ou pentágono.

----------------
Comandos básicos
----------------

Esta seção apresenta os recursos mais básicos do Pytuguês que serão utilizados posteriormente para construir programas mais complexos e interessantes.
 

Operações matemáticas
---------------------

Talvez o uso mais simples do interpretador de Pytuguês seja como uma calculadora. Além das operações aritméticas comuns, o Pytuguês permite salvar variáveis, utilizar funções científicas, definir as nossas próprias funções matemáticas, além de vários outros recursos.

A notação para as operações matemáticas é usual, onde apenas lembramos que as casas decimais são separadas por pontos e não por vírgulas::

    1 + 1     # soma
    2 - 1     # subtração
    3.14 * 2  # multiplicação
    1 / 2     # divisão
    3**2      # potência
    
É possível criar variáveis e reaproveitá-las em outras partes do código. As funções matemáticas mais comuns também estão imediatamente disponíveis. Experimente estes comandos no terminal interativo::

    >>> x = raiz(4)
    >>> x + 1
    3.0
    >>> x * x
    4.0
    >>> módulo(1 - x)
    1.0
    
O operador de igual ``=``, possui o sentido usual da maioria das linguagens de programação, mas que é diferente do da matemática. Ele não estabelece ou testa uma relação de igualdade. Ele é utilizado na atribuição de variáveis. Portanto um código do tipo::
    
    x = x + 1
    
não é uma falsidade matemática. Na realidade, estamos atribuindo um novo valor para a variável ``x`` que é igual ao valor anterior adicionado de 1.


**Desafio!**

Calcule ``x = 42**42``. Muito provavelmente este resultado é maior que o que cabe na sua calculadora! Confira. 


Interação com o usuário
-----------------------

Em um programa de computador muitas vezes queremos perguntar algum tipo de informação ao usuário. O Pytuguês oferece algumas funções para salvar valores digitados pelo usuário em variáveis. Os principais métodos de entrada são as funções ``leia_texto(msg)``, ``leia_número(msg)``  e ``leia_arquivo(arquivo)``. O código a seguir, por exemplo, pergunta o nome e a idade do usuário::

    nome = leia_texto("Qual é o seu nome? ")
    idade = leia_número("Qual é a sua idade? ")
    
A variável ``nome`` contêm o texto que o usuário digitou como sendo o seu nome e a variável ``idade`` guarda a idade em um formato numérico. A diferença entre ``leia_número(msg)`` e ``leia_texto(msg)`` está em que a primeira salva o resultado em formato numérico e obriga o usuário a digitar um número válido. A segunda conterá sempre um texto, mesmo quando o usuário digitar um número. Note que existe uma diferença entre um número e um texto que contêm um número: enquanto o primeiro admite as operações matemáticas, o segundo corresponde a um valor textual que por um acaso é ser interpretado (por nós humanos, não pelo computador!) como um número.


As funções mencionadas acima são conhecidas como "funções de entrada", já que permitem que o usuário do programa dê a entrada em valores que serão utilizados posteriormente. As *funções de saída* são aquelas que fornecem informação de volta para o usuário. A mais importante delas é a função ``mostre(valor)``, que mostra o conteúdo do argumento na tela. Podemos fazer a saída na forma de um arquivo, utilizando a função ``salve_arquivo(nome_do_arquivo, valor)``.

Teste
.....

Crie uma função que pergunte o ano de nascimento do usuário e calcule a sua idade.

  
---------------------------
Controle de fluxo de código
---------------------------

Alguns comandos do Pytuguês executam ações imediatas, como por exemplo, o comando ``frente(passo)``. Podemos construir programas interessantes como uma receita de bolo encadeando vários destes comandos. O programa abaixo, por exemplo, desenha um triângulo::

    frente(100)
    esquerda(120)
    frente(100)
    esquerda(120)
    frente(100)

(você consegue fazer o triângulo apontar para baixo?)

Em alguns casos é necessário controlar o "fluxo de código"; ou seja, temos que decidir quais comandos serão executados e quantas vezes será realizada cada execução. Esta seção mostra as principais estruturas de controle de fluxo de código do Pytuguês, o *repetir*, o *para cada*, o *enquanto* e o *se/senão*.  


Repetições: *repetir*
---------------------

Muitas tarefas que um programa realiza envovem um grande número de repetições de tarefas mais simples. Na realidade computadores são muito bons nisso: podem repetir exatamente a mesma sequência de passos uma quantidade gigantesca de vezes sem ficarem cansados, errarem ou reclamarem. O comando mais básico de repetição do Pytuguês é o comando ``repetir``. Ele simplesmente repete um bloco de instruções pelo número dado de vezes::

    repetir 3 vezes:
        frente(100)
        esquerda(120)
    
Em programação, chamamos cada uma destas repetições de uma "iteração" do loop *repetir*. Neste caso, aplicamos 3 iterações da sequência de comandos ``frente/esquerda``.
    
No exemplo acima ele repete os comandos ``frente(100)`` e ``esquerda(120)`` três vezes, nesta ordem. De modo mais abstrato, podemos descrever o comando repetir como::
    
    repetir <número> vezes:
        <bloco de instruções>

Onde o campo <número> representa qualquer número inteiro ou variável numérica e <bloco de instruções> é uma sequência de instruções como a ``frente(100)/esquerda(90)`` dada anteriormente. Devemos nos atentar para os espaços em branco durante a definição do bloco de instruções. São eles que delimitam o bloco de instruções e dizem para o Pytuguês quais instruções devem ser repetidas e quais não fazem parte do bloco de instruções.

O código abaixo, por exemplo, é muito semelhate ao anterior, mas o comando ``esquerda(120)`` està alinhado ao início da linha. Isto fáz com que apenas a parte ``frente(100)`` seja executada as três vezes. O comando esquerda está fora do bloco *repetir* e portanto é executado apenas uma única vez após o bloco terminar::

    repetir 3 vezes:
        frente(100)
    esquerda(120)
        
**Desafio!**


Faça uma estrela de 5 pontas utilizando o comando repetir. Depois tente fazer a estrela de Davi (neste caso pode ser necessário usar 2 repetições).



Repetições: *para cada*
-----------------------

Muitas vezes queremos repetir um bloco de comandos onde em cada iteração uma variável deve mudar de valor de forma previsível. Por exemplo, se quisermos cumprimentar várias pessoas numa lista, é possível escrever algo como::

    para cada nome em ["Maria", "João", "José"] faça:
        mostre("Olá " + nome) 

Neste caso, a variável *nome* assume um valor diferente em cada iteração, obtendo-os a partir da lista de nomes fornecida.

É muito comum também realizar iterações sobre sequências numéricas. O comando muda ligeiramente, onde especificamos o intervalo de valores inteiros que queremos percorrer. O exemplo abaixo soma todos os números de 1 até 10::

    soma = 0
    
    para cada x de 1 até 10 faça:
        soma = soma + x
    
    mostre(soma)
    

Se quisermos pular de dois em dois, a sintaxe muda um pouquinho::

    soma = 0
    
    para cada x de 1 até 10 a cada 2 faça:
        soma = soma + x
    
    mostre(soma)

Neste caso, somente os ímpares seriam contabilizados na soma.

A sintaxe geral do comando *para cada* é dada abaixo. Na forma de sequência, ela funciona como::

    para cada <nome> em <sequência> faça:
        <bloco de comandos>
        
Caso seja uma sequência numérica, podemos usar::

    para cada <nome> de <início> até <fim> a cada <passo> faça:
        <bloco de comandos>
        
Assim como no bloco *repetir*, o comando *faça* é opcional. Podemos também trocar o comando *para cada* por simplesmente *para*, na forma compacta. Finalmente, podemos omitir o passo na segunda versão do comando caso ele seja igual à 1.


**Desafio!**


Desenhe uma espiral quadrada de 10 braços em que o tamanho de cada avanço varie segundo o padrão 10px, 20px, 30px, ..., 100px. A forma ingênua criar este programa seria algo do tipo::
    
    frente(10)
    esquerda(90)
    
    frente(20)
    esquerda(90)
    
    frente(30)
    esquerda(90)
    
    frente(40)
    esquerda(90)
    ...
    
É lógico que podemos fazer bem melhor com o comando *para cada* (ou até mesmo com o comando repetir).


Repetições: enquanto
--------------------

O comando *para cada* é útil quando sabemos de antemão o número de iterações que devem ser executadas. Muitas vezes, no entanto, queremos repetir um bloco de código por um número indefinido de vezes até que um determinado critério de parada seja satisfeito. O código abaixo, por exemplo, repete uma pergunta até que o usuário acerte a resposta correta::

    enquanto ler_texto("Qual é o baterista dos Beatles? ") != "Ringo" faça:
        mostre("Resposta errada! Tente novamente...")

De um modo geral, o comando *enquanto* possui a estrutura::
    
    enquanto <condição> faça:
        <bloco de comandos>
        
Ele executa o bloco de comandos indefinidamente enquanto a condição fornecida for verdadeira. Caso a condição seja falsa, ele interrompe *antes* de executar o bloco de comandos.

O comando *enquanto* é talvez a forma mais geral das estruturas de repetição. Podemos, reescrever todos os laços do tipo *para cada* ou *repetir* utilizando o comando *enquanto*. Existe um custo nisto: o código pode ficar mais longo e confuso e, em alguns casos, até mesmo um pouco mais lento. O código abaixo, por exemplo, desenha um triângulo utilizando o comando *enquanto*. No entanto, O fato de termos que lidar com variáveis adicionais tira a elegância e concisão do comando *repetir*::
    
    n_iterações = 0
    
    enquanto n_iterações < 3:
        frente(100)
        esquerda(120)
        n_iterações = n_iterações + 1
        
**Desafio!**

A função ``aleatório()`` produz um número aleatório entre 0 e 1. O programa abaixo, por exemplo, produz 100 "passos do bêbado" e imprime a coordenada x após o passo::

    repetir 100 vezes:
        # Dá um passo
        frente(50)
        esquerda(aleatório() * 360)
        
        # Imprime a coordenada x
        x, y = posição()
        mostre(x)
        
Modifique o comando acima para que o "passo do bêbado" termine quando o cursor atingir uma distância de 300 px da origem.  


Condicionais
------------

Se quisermos executar um comando apenas se determinada condição for satisfeita, então usamos o bloco *se*::

    x = leia_número("Diga um número: ")
    
    se x > 10 então faça:
        mostre("x é muito grande")
    
Neste caso, o comando ``mostre(...)`` será executado somente se o usuário digitar um valor maior que 10. Se quisermos adicionar uma condição que deva ser executada caso o teste x > 10 falhe, basta adicionar um bloco do tipo *senão*::

    x = leia_número("Diga um número: ")
    
    se x > 10 então faça:
        mostre("x é muito grande")
    senão faça:
        mostre("x é pequeno")
        
Este código imprime na tela que x é muito grande, caso o usuário diga um número maior que 10 ou imprime que x é pequeno, caso contrário. É possível adicionar condições intermediárias usando o bloco *ou então se*. Neste caso, somente a primeira condição a ser satisfeita é executada. A sintaxe completa é portanto:: 
    
    x = leia_número("Diga um número: ")
    
    se x > 10 então faça:
        mostre("x é muito grande")
    ou então se x == 7 faça:
        mostre("x é meu número da sorte")
    senão faça:
        mostre("x é pequeno")

De um modo geral, a estrutura condicional pode ser escrita como::

    se <condição 1> então faça:
        <bloco de código 1>
    ou então se <condição 2> faça:
        <bloco de código 2>
    ou então se <condição 3> faça:
        <bloco de código 3>
    ...
    senão faça:
        <bloco de código senão>
        
Onde no máximo um dos blocos de código será executado, sendo o que corresponde à primeira condição que é satisfeita. Analogamente aos laços repetição, os termos *então faça* e *faça* são opcionais.

O condicional funciona assim.

* Primeiramente testamos a *condição 1*. Se ela for satisfeita, o bloco de código correspondente é executado e o Pytuguês ignora todos os outros blocos restantes e continua a execução a partir daí.
* Caso a condição seja falsa, partimos para a *condição 2*. Se ela for satisfeita, executamos o segundo bloco de código e pulamos sobre todos os outros.
* Somente se nenhuma das condições forem satisfeitas, executa-se o bloco senão. Caso o bloco senão não exista, nenhum comando é executado. 
      
Talvez fique mais claro em um exemplo::

    se x == 1:
        mostre("uma unidade")
    ou então se x > 10:
        mostre("x é grande")
    ou então se x < 0: 
        mostre("x é pequeno")
    ou então se x % 2 == 0:
        mostre("x é par")
    ou então se x == 20:
        mostre("esta linha nunca será executada pois 20 > 10")
    senão:
        mostre(x)
        
Se **x** for igual à 4, o programa imprimirá "x é par", pois a condição ``x % 2 == 0`` (resto da divisão de **x** por 2 é igual à zero) é a primeira condição satisfeita no bloco condicional. Caso **x** seja igual à 12, a mensagem mostrada será "x é grande", pois apesar de tanto ``x > 10`` quanto ``x % 2 == 0`` serem satisfeitos para este valor, a primeira condição é selecionada pois aparece primeiro no bloco condicional. Para executarmos o bloco *senão*, é necessário utilizar um valor de **x** que viole todas as condições apresentadas. Neste caso, qualquer um dos valores 3, 5, 7 e 9 funcionam.


**Desafio!**
  
Pergunte a idade do usuário e imprima uma das mensagens abaixo dependendo da faixa em que ele se situa.

* negativo: "você ainda não nasceu!"
* 0-3: "você é um bebê"
* 4-9: "você é uma criança"       
* 10-12: "você é um pré-adolescente"
* 13-19: "você é um adolescente"
* 20-59: "você é um adulto"
* 60 ou mais: "você é um idoso"
    
O Pytuguês aceita condições compostas, assim podemos usar o teste ``0 <= idade <= 3`` para verificar se a idade está no intervalo entre 0 e 3.
  