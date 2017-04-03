========
Tutorial
========

Um programa de computador pode ser entendido como uma série de instruções que
são executadas em sequência para completar uma determinada tarefa. As
tarefas podem ir do extremamente simples, como mostrar mensagens na tela,
até o extremamente complicado como fazer um cálculo científico ou dirigir um
carro. No caso do Pytuguês você provavelmente iniciará o contato com a
programação desenhando figuras na tela. No início, iremos programar o
computador para realizar tarefas como quadrados, triângulos, estrelas ou
outras figuras geométricas.

Podemos iniciar o ambiente de programação em modo texto invocando o comando
**pytuga** no terminal. Uma vez aberta a aplicação, nos deparamos com o shell
de Pytuguês (que inicia com ``>>>``) onde podemos digitar comandos diretamente.
Para mostrar uma mensagem na tela, por exemplo, digite::

    >>> mostre("olá, mundo!")
    olá, mundo

Experimente também com operações básicas, para ter um sabor dos recursos
disponíveis no terminal de Pytuguês::

    >>> 5 * 4 * 3 * 2 * 1
    120
    >>> 40 + 2
    42

A sintaxe do Pytuguês foi criada para produzir códigos que se assemelhem o
máximo possível com um *pseudo-código* em português. Queremos que o significado
dos programas mais simples seja óbvio para um usuário que não conhece a
linguagem ou que nunca programou na vida, e que a linguagem seja fácil de
aprender e pareça natural para programadores iniciantes. O Python oferece
isto para falantes do inglês, o Pytuguês oferece o mesmo para brasileiros,
portugueses, angolanos, etc.

Esta seção vai percorrer os principais recursos do Pytuguês para que você possa
começar a programar em poucos minutos. Normalmente a primeira interação com o
Pytuguês se dá por meio da programação gráfica, onde controlamos a trajetória de
um pequeno "robô" que desenha figuras geométricas na tela. Inicie o TurtleMainWindow
ou o pytuga. Os comandos básicos para interagir com o cursor na tela são::

    >>> frente(100)   # avança 100 pixels
    >>> trás(100)     # recua 100 pixels
    >>> direita(90)   # gira 90 graus no sentido horário
    >>> esquerda(90)  # gira 90 graus no sentido anti-horário


Digite os comandos no terminal interativo para ver o Tuga se mexer. Aos poucos
podemos construir interações complexas e interessantes utilizando estes blocos
básicos e os recursos comuns de programação como repetições, execução
condicional, interação com o usuário, etc.

**Desafio!**

Utilize estes comandos para desenhar uma figura regular como quadrado, triângulo, ou
pentágono.

----------------
Comandos básicos
----------------

Esta seção apresenta os recursos mais básicos do Pytuguês que serão utilizados
posteriormente para construir programas mais complexos e interessantes.


Operações matemáticas
---------------------

Talvez o uso mais simples do interpretador de Pytuguês seja como uma
calculadora. Além das operações aritméticas comuns, o Pytuguês permite salvar
variáveis, utilizar funções científicas, definir as nossas próprias funções
matemáticas, além de vários outros recursos.

A notação para as operações matemáticas é usual, onde apenas lembramos que as
casas decimais são separadas por pontos e não por vírgulas::

    1 + 1     # soma
    2 - 1     # subtração
    3.14 * 2  # multiplicação
    1 / 2     # divisão
    3**2      # potência

É possível criar variáveis e reaproveitá-las em outras partes do código. As
funções matemáticas mais comuns também estão imediatamente disponíveis.
Experimente estes comandos no terminal interativo::

    >>> x = raiz(4)
    >>> x + 1
    3.0
    >>> x * x
    4.0
    >>> módulo(1 - x)
    1.0

O operador de igual ``=``, possui o sentido usual da maioria das linguagens de
programação, mas que é diferente do da matemática. Ele não estabelece ou testa
uma relação de igualdade. Ele é utilizado na atribuição de variáveis. Portanto
um código do tipo::

    x = x + 1

não é uma falsidade matemática. Na realidade, estamos atribuindo um novo valor
para a variável ``x`` que é igual ao valor anterior adicionado de 1.


**Desafio!**

Calcule ``x = 42**42``. Muito provavelmente este resultado é maior que o que
cabe na sua calculadora! Confira.


Interação com o usuário
-----------------------

Em um programa de computador muitas vezes queremos perguntar algum tipo de
informação ao usuário. O Pytuguês oferece algumas funções para salvar valores
digitados pelo usuário em variáveis. Os principais métodos de entrada são as
funções ``leia_texto(msg)``, ``leia_número(msg)``  e ``leia_arquivo(arquivo)``.
O código a seguir, por exemplo, pergunta o nome e a idade do usuário::

    nome = leia_texto("Qual é o seu nome? ")
    idade = leia_número("Qual é a sua idade? ")

A variável ``nome`` contêm o texto que o usuário digitou como sendo o seu nome e
a variável ``idade`` guarda a idade em um formato numérico. A diferença entre
``leia_número(msg)`` e ``leia_texto(msg)`` está em que a primeira salva o
resultado em formato numérico e obriga o usuário a digitar um número válido. A
segunda conterá sempre um texto, mesmo quando o usuário digitar um número. Observe
a diferença que existe entre um número e um texto que contêm um número:
enquanto o primeiro admite as operações matemáticas, o segundo corresponde a um
valor textual que por um acaso pode ser interpretado (por nós humanos, não pelo
computador!) como um número.


As funções mencionadas acima são conhecidas como "funções de entrada", já que
permitem que o usuário do programa dê a entrada em valores que serão utilizados
posteriormente. As *funções de saída* são aquelas que fornecem informação de
volta para o usuário. A mais importante delas é a função ``mostre(valor)``, que
mostra o conteúdo do argumento na tela. Podemos fazer a saída na forma de um
arquivo, utilizando a função ``salve_arquivo(nome_do_arquivo, valor)``. Teste
também a função ``alerte(valor)``: ela é semelhante à função "mostre", mas em
modo gráfico ela mostra a mensagem em uma caixa de diálogo.

Teste
.....

Crie uma função que pergunte o ano de nascimento do usuário e calcule a sua
idade.


---------------------------
Controle de fluxo de código
---------------------------

Alguns comandos do Pytuguês executam ações imediatas, como por exemplo, o
comando ``frente(passo)``. Podemos construir programas interessantes encadeando
vários destes comandos. O programa abaixo, por exemplo, desenha um triângulo::

    frente(100)
    esquerda(120)
    frente(100)
    esquerda(120)
    frente(100)

(você consegue fazer o triângulo apontar para baixo?)

Em alguns casos é necessário controlar o "fluxo de código"; ou seja, temos que
decidir quais comandos serão executados e quantas vezes será realizada cada
execução. Esta seção mostra as principais estruturas de controle de fluxo de
código do Pytuguês: ``repetir``, ``para cada``, ``enquanto`` e ``se/senão``.


Repetições: ``repetir``
-----------------------

Muitas tarefas que um programa realiza envovem um grande número de repetições de
tarefas mais simples. Na realidade computadores são muito bons nisso: podem
repetir exatamente a mesma sequência de passos uma quantidade gigantesca de
vezes sem ficarem cansados, errarem ou reclamarem. O comando mais básico de
repetição do Pytuguês é o comando ``repetir``. Ele simplesmente repete um bloco
de instruções pelo número dado de vezes::

    repetir 3 vezes:
        frente(100)
        esquerda(120)

Em programação, chamamos cada uma destas repetições de uma "iteração". No exemplo
acima, repetimos o os comandos ``frente(100)`` e ``esquerda(120)`` três
vezes, nesta ordem. De modo mais abstrato, podemos descrever o comando repetir
como::

    repetir <número> vezes:
        <bloco de instruções>

Onde o campo <número> representa qualquer número inteiro ou variável numérica e
<bloco de instruções> é uma sequência de instruções como a
``frente(100)/esquerda(90)`` dada anteriormente. Devemos nos atentar para os
espaços em branco durante a definição do bloco de instruções. São eles que
delimitam o bloco de instruções e dizem para o Pytuguês quais instruções devem
ser repetidas e quais não fazem mais parte do bloco de repetição e serão
executadas após o término de todas iterações.

O código abaixo, por exemplo, é muito semelhate ao anterior, mas o comando
``esquerda(120)`` está alinhado ao início da linha. Isto faz com que apenas a
parte ``frente(100)`` seja executada as três vezes. O comando esquerda está fora
do bloco ``repetir`` e portanto é executado apenas uma única vez após o bloco
terminar::

    repetir 3 vezes:
        frente(100)
    esquerda(120)


.. important:: Indentação
O número de espaços em branco antes de cada linha dentro do código define
    o nível de indentação da linha. A indentação é importantíssima em
    Pytuguês pois é o que delimita onde começa e onde termina cada bloco de
    instruções. Normalmente utilizamos quatro espaços para cada nível de
    indentação (mas você pode utilizar uma indentação diferente, se preferir).

    É importante prestar atenção ao nível de indentação de cada linha. Em
    Pytuguês, todos os comandos que terminam com um símbolo de ``:`` definem um
    início de bloco e portanto exigem que se aumente um nível de indentação. Para
    sair do bloco devemos voltar à indentação anterior.


**Desafio!**


Faça uma estrela de 5 pontas utilizando o comando repetir. Depois tente fazer a
estrela de Davi (neste caso pode ser necessário usar 2 repetições).



Repetições: ``para cada``
-------------------------

Muitas vezes queremos repetir um bloco de comandos onde em cada iteração uma
variável deve mudar de valor de forma previsível. Por exemplo, se quisermos
cumprimentar várias pessoas numa lista, é possível escrever algo como::

    lista = ["Maria", "João", "José"]

    para cada nome em lista faça:
        mostre("Olá " + nome)

Neste caso, a variável ``nome`` assume um valor diferente em cada iteração
percorrendo a lista de nomes fornecida.

É muito comum também realizar iterações sobre sequências numéricas. O comando
muda ligeiramente, onde especificamos o intervalo de valores inteiros que
queremos percorrer. O exemplo abaixo soma todos os números de 1 até 10::

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

A sintaxe geral do comando ``para cada`` é dada abaixo. Na forma de sequência, ela
funciona como::

    para cada <nome> em <sequência> faça:
        <bloco de comandos>

Caso seja uma sequência numérica, podemos usar::

    para cada <nome> de <início> até <fim> a cada <passo> faça:
        <bloco de comandos>

Assim como no bloco ``repetir``, o comando ``faça`` é opcional. Podemos também
trocar o comando ``para cada`` por simplesmente ``para``, na forma compacta.
Finalmente, podemos omitir o passo na segunda versão do comando caso ele seja
igual à 1.

**Desafio!**

Desenhe uma espiral quadrada de 10 braços em que o tamanho de cada avanço varie
segundo o padrão 10px, 20px, 30px, ..., 100px. A forma ingênua criar este
programa seria algo do tipo::

    frente(10)
    esquerda(90)

    frente(20)
    esquerda(90)

    frente(30)
    esquerda(90)

    frente(40)
    esquerda(90)
    ...

É lógico que podemos fazer algo bem melhor com o comando ``para cada`` (ou até mesmo
com o comando repetir).


Repetições: enquanto
--------------------

O comando ``para cada`` é útil quando sabemos de antemão o número de iterações que
devem ser executadas. Muitas vezes, no entanto, queremos repetir um bloco de
código por um número indefinido de vezes até que um determinado critério de
parada seja satisfeito. O código abaixo, por exemplo, repete uma pergunta até
que o usuário acerte a resposta correta::

    enquanto ler_texto("Baterista dos Beatles: ") != "Ringo" faça:
        mostre("Resposta errada! Tente novamente...")

De um modo geral, o comando ``enquanto`` possui a estrutura::

    enquanto <condição> faça:
        <bloco de comandos>

No exemplo acima, a condição testada no início do laço é se o resultado da
função ``ler_texto()`` é diferente (``!=``) do valor ``"Ringo"``. O laço ``enquanto``
executa o bloco de comandos indefinidamente enquanto a condição fornecida
for verdadeira. Caso a condição se torne falsa, ele interrompe *antes* de
executar o bloco de comandos.

O comando ``enquanto`` é talvez a forma mais geral das estruturas de repetição.
Podemos reescrever todos os laços do tipo ``para cada`` ou ``repetir`` utilizando o
comando ``enquanto``. Existe um custo nisto: o código pode ficar mais longo,
confuso e, em alguns casos, até mesmo um pouco mais lento. O código abaixo, por
exemplo, desenha um triângulo utilizando o comando ``enquanto``. Este código funciona
sem maiores problemas. No entanto, o fato de termos que lidar com variáveis adicionais
tira a elegância e concisão da versão que utilizava o comando ``repetir``::

    n_iterações = 0

    enquanto n_iterações < 3:
        frente(100)
        esquerda(120)
        n_iterações = n_iterações + 1

**Desafio!**

A função ``aleatório()`` produz um número aleatório entre 0 e 1. O programa
abaixo, por exemplo, produz 100 "passos do bêbado" e imprime a coordenada x após
o passo::

    repetir 100 vezes:
        # Dá um passo
        frente(50)
        esquerda(aleatório() * 360)

        # Imprime a coordenada x
        x, y = posição()
        mostre(x)

Modifique o comando acima para que o "passo do bêbado" termine quando o cursor
atingir uma distância de 300 px da origem.


Condicionais
------------

Se quisermos executar um comando apenas se determinada condição for satisfeita,
então usamos o bloco *se*::

    x = leia_número("Diga um número: ")

    se x > 10 então faça:
        mostre("x é muito grande")

Neste caso, o comando ``mostre(...)`` será executado somente se o usuário
digitar um valor maior que 10. Se quisermos adicionar uma condição que deva ser
executada caso o teste x > 10 falhe, basta adicionar um bloco do tipo ``senão``::

    x = leia_número("Diga um número: ")

    se x > 10 então faça:
        mostre("x é muito grande")
    senão faça:
        mostre("x é pequeno")

Este código imprime na tela que x é muito grande caso o usuário diga um número
maior que 10, ou imprime que x é pequeno caso contrário. É possível adicionar
condições intermediárias usando o bloco *ou então se*. Neste caso, somente a
primeira condição a ser satisfeita é executada. A sintaxe completa é portanto::

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

No máximo um dos blocos de código será executado, sendo este o que corresponde à
primeira condição satisfeita. Analogamente aos laços repetição, os termos
``então faça`` e ``faça`` são opcionais.

O condicional funciona assim.

* Primeiramente testamos a *condição 1*. Se ela for satisfeita, o bloco de
  código correspondente é executado e o Pytuguês ignora todos os outros blocos
  restantes e continua a execução a partir daí.
* Caso a condição seja falsa, partimos para a *condição 2*. Se ela for
  satisfeita, executamos o segundo bloco de código e pulamos sobre todos os
  outros.
* Somente se nenhuma das condições for satisfeita, executa-se o bloco ``senão``.
  Caso o bloco senão não exista, nenhum comando é executado.

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

Se ``x`` for igual a 4, o programa imprimirá *"x é par"*, pois a condição 
``x % 2 == 0`` (resto da divisão de ``x`` por ``2`` é igual a zero) é a primeira condição
satisfeita no bloco condicional. Caso ``x`` seja igual a 12, a mensagem mostrada
será *"x é grande"*, pois apesar de tanto ``x > 10`` quanto ``x % 2 == 0`` serem
satisfeitos para este valor, a primeira condição é selecionada pois aparece
primeiro no bloco condicional. Para executarmos o bloco ``senão``, é necessário
utilizar um valor de ``x`` que viole todas as condições apresentadas. Neste
caso, qualquer um dos valores 3, 5, 7 e 9 funcionam. Você consegue dizer o que acontece
se ``x`` for igual a 20?


**Desafio!**

Pergunte a idade do usuário e imprima uma das mensagens abaixo dependendo da
faixa em que ele se situa.

* negativo: "você ainda não nasceu!"
* 0-3: "você é um bebê"
* 4-9: "você é uma criança"
* 10-12: "você é um pré-adolescente"
* 13-19: "você é um adolescente"
* 20-59: "você é um adulto"
* 60 ou mais: "você é um idoso"

O Pytuguês aceita condições compostas, assim podemos usar o teste
``0 <= idade <= 3`` para verificar se a idade está no intervalo entre 0 e 3.


-----------------
Funções e módulos
-----------------

Uma função, em computação é entendida como um comando que recebe zero ou mais argumentos, realiza uma ação e
opcionalmente pode retornar um valor. Isto é um pouco diferente e mais abrangente que as funções da matemática, que
devem possuir pelo menos uma entrada e uma única saída. Pense numa função como uma sequência fixa de operações que você
pode querer executar em um programa.

Pense na função ``cubo(x)``, que eleva o argumento de entrada ``x`` ao cubo e retorna o resultado (ela não existe em
Pytuguês, mas logo aprenderemos como definí-la). Esta é uma função tanto no sentido matemático, como no computacional.
Neste caso, para calcular o cubo do argumento, simplesmente obtemos o resultado da multiplicação ``x * x * x``. Já a
função ``aleatório()`` que mencionamos anteriormente é uma função no sentido computacional mas não no sentido
matemático: ela não possui qualquer argumento de entrada e a cada vez que for chamada, retorna um valor diferente::

    x = aleatório()
    y = aleatório()
    mostre(x, y)

Ao executarmos o programa acima, vemos que x e y (muito provavelmente) possuem valores diferentes e que a cada execução
estes valores mudam. ``aleatório()`` não é uma função no sentido matemático. Ela apenas representa a ação de obter um
número aleatório.

O conceito de funções é muito importante em computação. Podemos compor funções simples para criar funções um pouco mais
complexas e seguir compondo estas funções em camadas até criar um programa altamente sofisticado. É claro que estamos
apenas começando e não vamos já de cara desenvolver um editor de textos ou um jogo de tiros em primeira pessoa. Estes
programas podem involver literalmente milhões de linhas de códigos que são desenvolvidas por grandes times de
programadores durante longos intervalos de tempo. Vamos, no entanto, aprender a definir funções para dar o primeiro passo
para virarmos bons programadores.

Definindo uma função
--------------------

Pense numa função como um pedaço de código reutilizável. Vamos voltar ao exemplo de como construir um quadrado::

    repetir 4 vezes:
        frente(100)
        esquerda(90)

Se quisermos fazer algum tipo de arte (ou um programa) que envolva a criação de vários quadrados, copiar e colar este
código pode se tornar repetitivo. Para evitar muitas repetições, podemos colocar este código dentro de uma função::

    função quadrado():
        repetir 4 vezes:
            frente(100)
            esquerda(90)

Simplesmente colocamos o código que queremos reutilizar dentro do corpo da função ``quadrado()``. Note que isto não executa
a sequência de comandos fornecido. Para isto, é necessário chamar ``quadrado()`` explicitamente::

    quadrado()  # desenha um quadrado
    esquerda(45)
    quadrado()  # desenha outro quadrado inclinado, pois iniciamos de uma posição inclinada

Compondo funções, é possível criar programas relativamente complexos de forma simples::

    repetir 8 vezes:
        quadrado()
        esquereda(45)

O código acima desenha uma mandala a partir de oito quadrados.


**Desafio**

Crie duas funções: ``quadrado_grande()`` e ``quadrado_pequeno()`` e desenhe uma mandala compondo os dois tipos de quadrados,
chamando suas respectivas funções. Obs.: este exerício pode ser resolvido sem utilizar funções, mas muito provavelmente
o código ficará mais longo e confuso.


Entrada de parâmetros
---------------------

Vimos como criar uma função que repete uma sequência fixa de comandos. Muitas vezes é necessário alterar o comportamento
da função a cada chamada passando parâmetros adicionas. No exemplo dos quadrados acima, poderíamos, por exemplo,
controlar o tamanho do quadrado desenhado em cada chamada passando o mesmo como argumento para a função. O Pytuguês
suporta este recurso simplesmente escrevendo os parâmetros adicionais na definição da função::

    função quadrado(lado):
        repetir 4 vezes:
            frente(lado)
            esquerda(90)

Esta função pode ser chamada como ``quadrado(100)`` para desenhar um quadrado de 100 px de lado. O parâmetro passado
é atribuído à variável ``lado`` que posteriormente pode ser utilizado no corpo da função como uma variável qualquer.
Neste caso, ela aparece na linha ``frente(lado)`` que comanda o cursor a andar para frente pelo valor especificado.

Uma função pode possuir qualquer número de parâmetros de entrada, que são passados na mesma ordem de chamada. Considere
a função que desenha um polígono regular::

    função polígono_regular(N, lado):
        ângulo = 360 / N
        repetir N vezes:
            frente(lado)
            esquerda(ângulo)

Esta função é chamada com dois parâmetros (por exemplo, ``polígono_regular(3, 100)`` desenha um triângulo de lados de
100px). É importante passar os parâmetros na mesma ordem em que eles aparecem na definição da função. Por exemplo,
``polígono_regular(100, 3)`` provavelmente é um erro, mas talvez seja um usuário que realmente queira desenhar um
polígono de 100 lados de tamanho 3px. Não tem como o computador adivinhar a intenção real de quem chamou a função e
mesmo que isso fosse possível em alguns casos, não é senstato depender da inteligência do computador para acertar nossas
intenções. Devemos treinar um certo rigor nos comandos que são passados para o computador.

Lembrar a ordem de cada parâmetro pode ser bastante confuso e sujeito a
erros, principalmente em funções com um grande número de parâmetros. Pensando
nisto, o Pytuguês permite passar os parâmetros por nome (e permite até
definir parâmetros opcionais, mas isto é um tópico mais avançado que não
trataremos aqui). Podemos chamar ``polígono_regular(lado=100, N=3)`` passando
os argumentos de entrada explicitamente a partir dos seus nomes. Neste caso, a
ordem dos parâmetros é irrelevante.

**Desafio**

Crie uma função que desenha uma mandala a partir de uma figura regular de N
lados utilizando a mesma técnica que fizemos anteriormente com o quadrado.


Valores de saída
----------------

Todas as funções em Pytuguês possuem um certo número de parâmetros de entrada
e um valor de saída. Isto permite que a função retorne um resultado
potencialmente útil para o usuário. Podemos, por exemplo, definir uma função
``cubo(x)`` que retorna o valor terceira potência do argumento ``x``. Para
retornar um valor explícito, é necessário inserir a cláusula
``retornar <valor>`` no corpo da função::

    definir função cubo(x):
        resultado = x * x * x
        retornar resultado

A partir daí podemos utilizar esta função para calcular o cubo de qualquer valor fornecido::

    valor = cubo(2)
    mostre(valor)

Neste caso, o programa mostrará o número 8.

Observe que as funções que não possuem uma cláusula do tipo ``retornar`` implicitamente retornam o valor ``nulo``,
como em::

    valor = polígono_regular(4, 100)
    mostre(valor)

Isto irá mostrar ``nulo`` na tela. É possível retornar o valor ``nulo`` explicitamente
utilizando ``retornar nulo``, mas isto não é necessário.


**Desafio**

Crie uma função que calcula e retorna o alcance de um projétil a partir do ângulo de arremesso e da velocidade de saída.
Lembre-se das aulas de física: o alcance é dado por :latex:`$\frac{v_0^2 sin(2\theta)}{g}$`.


-------------------
Estruturas de dados
-------------------

Vimos até agora apenas alguns tipos de variáveis bem simples: números e, de
forma superficial, textos (*strings*) e variáveis lógicas. As variávies em
Pytuguês podem assumir vários outros tipos de valores (e inclusive você poderá
criar os seus próprios tipos quando estiver mais experiente em programação).
Nesta seção discutiremos principalmente os tipos de sequêcias e agrupamentos e
as relações entre eles. O tipo mais básico e intuitivo talvez seja a lista.
Definimos uma lista simplesmente enumerando seus elementos dentro de colchetes::

    L = [1, 2, 9, 16]

Podemos acessar os elementos da lista utilizando a notação de índices. Em
Pytuguês, os índices começam em zero. Desta forma, o primeiro elemento da lista
pode ser acessado como ``L[0]``, o segundo como ``L[1]`` e assim por diante.
Cada elemento da lista anterior pode ser acessado como::

    L[0] --> 1
    L[1] --> 2
    L[2] --> 9
    L[3] --> 16

Índices negativos podem ser utilizados para acessar a lista de trás para frente.
Desta forma L[-1] corresponde ao último elemento, L[-2] ao penúltimo e assim
por diante.

Podemos encontrar o número de elementos da lista utilizando a função
``tamanho(L)``. Muitas vezes utilizamos a função ``tamanho`` para determinar os
índices sobre o qual queremos iterar::

    N = tamanho(L)
    para cada i de 0 até N - 1 faça:
        mostre(i, L[i])

Se quisermos percorrer os elementos sem nos importarmos com os índices podemos
realizar um laço do tipo ``para cada`` diretamente sobre a lista::

    para cada x em L faça:
        mostre(x)


Modificando uma lista
---------------------

Podemos alterar os elementos de uma lista, apagá-los, ou inserir novos elementos.

Modificamos o valor contido em um determinado local da lista como::

    >>> L[2] = 0  # altera o terceiro elemento da lista para zero

Para apagar um elemento específico da lista utilizamos o comando ``remover``::

    >>> remover L[2]
    >>> mostre(L)
    [1, 2, 16]

Observe que o terceiro elemento foi removido e o quarto passou a ocupar o seu lugar.

Podemos inserir elementos na lista utilizando duas funções diferentes. A função
``acrescentar(lista, elemento)`` adiciona um novo elemento no final da lista. É
muito comum utilizar a função ``acrescentar`` para construir uma lista aos
poucos a partir de uma lista vazia. No exemplo abaixo, criamos uma lista com os
100 primeiros quadrados perfeitos::

    quadrados = []
    para cada x de 1 até 100:
        acrescentar(quadrados, x * x)

Já a função ``inserir(lista, índice, elemento)`` insere um novo elemento no
índice dado deslocando todos os elementos subsequentes para frente. Podemos ver
como isto funciona no exemplo::

    >>> beatles = ['Paul', 'George', 'Ringo']
    >>> inserir(beatles, 1, 'John')
    >>> mostre(beatles)
    ['Paul', 'John', 'George', 'Ringo']


**Desafio**

Crie uma lista que começa com ``L = [1, 1]``. Cada novo elemento é criado
somando os dois anteriores. Esta regra cria os números de Fibonacci, que foram
propostos inicialmente para descrever o crescimento de uma população de coelhos.
Complete esta lista até que ela tenha 10 elementos.


Texto (*strings*)
-----------------

Representamos uma variável do tipo texto (*string*, em inglês) colocando o
conteúdo entre aspas, como em ``msg = "Olá, todo mundo!"``. A variável ``msg``
é do tipo texto, e aceita operações como concatenamento, conversão entre
maiúsculas e minúsculas, etc. Sob vários aspectos, uma variável de texto se
assemelha a uma lista de caracteres. Podemos, por exemplo, extrair uma letra
específica do texto utilizando a notação de indexamento::

    >>> [msg[0], msg[1], msg[2], msg[-1]]
    ['O', 'l', 'á', '!']

Diferentemente das listas, as variáveis de texto não podem ser modificadas.
Para realizar uma alteração em uma *string* é sempre necessário criar uma nova
*string* com o valor alterado. Em alguns casos, pode ser necessário converter a
*string* para uma lista de caracteres, modificar a lista e finalmente juntá-la
numa *string* final::

    >>> L = lista("hello")
    >>> L[0] = "H"
    >>> acrescentar(L, "!")
    >>> mostre(juntar(L))
    Hello!

Strings de texto aceitam algumas operações matemáticas úteis. A soma de duas
stings corresponde à concatenação::

    >>> "olá" + "mundo"
    'olámundo'

Já a multiplicação de uma *string* por um número inteiro corresponde a uma
repetição::

    >>> "abc" * 3
    'abcabcabc'

Existem várias funções auxiliares aplicadas sobre *strings* que podem ser
acessadas pela notação ``<variável>.<método>``, como por exemplo em::

    >>> nome = "ringo"
    >>> nome.maiúsculas()
    'RINGO'

A função ``nome.maiúsculas()`` é um método associado apenas às variáveis do tipo
*string*. Como se trata de uma função com aplicação bem restrita --- não faz
sentido, por exemplo, converter um número para letras maiúsculas --- esta função
não possui escopo global.

Podemos obter a lista completa de funções associadas a cada tipo usando
o comando ``ajuda(<nome do tipo>)``, onde substituímos o nome do tipo por
``Texto`` para acessar as funções específicas de *strings*. A maior parte das
funções é auto-explicativa: explore-as para se familiarizar com os recursos de
processamento de texto disponíveis no Pytuguês.


 **Desafio**

Crie uma função que remova todos os acentos de uma palavra. Para este exercício
considere apenas os acentos que normalmente aparecem em português.


Dicionário
----------

Um dicionário em Pytuguês (algumas vezes chamado de *hash table*) define um
mapeamento entre um conjunto de índices (as chaves) para um conjunto de valores.
Podemos, por exemplo, relacionar um grupo de pessoas às suas respectivas idades::

    D = {'João': 31, 'Maria': 29, 'José': 3}

Note que as chaves podem ser do tipo texto ou qualquer outro valor imutável:
você pode utilizar números inteiros ou decimais, mesclar textos com números, etc.
No entanto, não é possível utilizar valores mutáveis como chaves. Podemos
acessar o valor associado a uma chave no dicionário usando a notação de índices::

    >>> D['José'] + 1
    4

Para acrescentar valores ao dicionário, basta fazer uma atribuição e o elemento
será inserido automaticamente (caso a chave já exista, substitui-se seu valor)::

    >>> D['Joana'] = 1
    >>> tamanho(D)
    4


**Desafio**

Crie um programa encriptador de mensagens. Para isto, defina um dicionário que
troque algumas letras do alfabeto de lugar até criar uma mensagem
incompreensível. Depois crie um outro programa que decodifique a mensagem
secreta.