==========
Instalação
==========


Pytuguês se baseia e é implementado em Python 3.5. Para a instalação completa do
Pytuguês, é necessário instalar antes algumas bibliotecas adicionais do Python.
As  instruções de instalação diferem ligeiramente em cada plataforma.


-----
Linux
-----

Você precisa do Python3 e do PyQt5. Existe uma chance razoável que ambos
estejam instalados. Se sua distribuição for baseada no Debian/Ubuntu,
o comando abaixo garante que todas as bibliotecas necessárias serão 
instaladas

::

    $ sudo apt-get install python3-all python3-pyqt5 python3-pyqt5.qsci python3-pyqt5.qtsvg python3-pyqt5.qtwebkit python3-pip
        
Se quiser apenas fazer a instalação local, o comando fica::

    $ pip3 install pytuga --user
    
(Ignore a opção --user, caso queira instalar para todos os usuários. Neste caso
é necessário executar o comando como *sudo*.). Uma vez instalado, você pode
atualizar a versão do Pytuguês executando::
    
    $ pip3 install pytuga -U --user 

O script de instalação salva os arquivos executáveis na pasta ``~/.local/bin.``
e na pasta ``~/bin/``, se a mesma existir.


-------
Windows
-------

É necessário baixar e instalar manualmente os pacote com o Python3.5 e o PyQt5.
Escolha a opção correspondente à sua instalação do Windows:

32 bits
-------

* Python__
* PyQt5__

.. __: https://www.python.org/ftp/python/3.5.1/python-3.5.1.exe
.. __: https://sourceforge.net/projects/pyqt/files/PyQt5/PyQt-5.5.1/PyQt5-5.5.1-gpl-Py3.4-Qt5.5.1-x32.exe


64 bits
-------

* Python__
* PyQt5__

.. __: https://www.python.org/ftp/python/3.5.1/python-3.5.1-amd64.exe
.. __: https://sourceforge.net/projects/pyqt/files/PyQt5/PyQt-5.5.1/PyQt5-5.5.1-gpl-Py3.4-Qt5.5.1-x64.exe

É importante marcar a opção "Add python.exe to your path" durante a instalação.
Isto facilitará a execução do Pytuguês posteriormente. Depois de terminada a
instalação, abra o terminal do Windows (Win+R e digite "cmd") e execute os
comandos::
    
    $ python -m pip install pytuga -U
    
Se o código anterior não funcionar, provavelmente significa que o Python não 
está no caminho padrão de procura do Windows. Se este for o caso, é necessário
mudar para o diretório onde o Python estiver instalado. Digite::

    $ cd c:\Python35\
    
Agora repita os comandos anteriores. Se você decidiu instalar o Python em
outro caminho, modifique o comando acima para indicar o caminho correto.

Para executar o Tugalinhas, aperte Win+R e digite "tugalinhas" no prompt. Caso
isto não funcione (especialmente nas versões mais novas do Windows), procure
o executável do tugalinhas na pasta ``c:\Python35\Scripts\`` ou execute o
comando ``python -m tugalinhas`` do terminal.
