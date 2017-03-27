==========
Instalação
==========


Pytuguês se baseia e é implementado em Python 3. Antes da instalação completa do
Pytuguês, é necessário instalar antes algumas bibliotecas adicionais
do Python. As  instruções de instalação diferem ligeiramente em cada plataforma.


-----
Linux
-----

Você precisa do Python3 e do PyQt5. Existe uma chance razoável que ambos
estejam instalados. Se sua distribuição for baseada no Debian/Ubuntu,
o comando abaixo garante que todas as bibliotecas necessárias serão 
instaladas

::

    sudo apt-get install python3-all python3-pyqt5 python3-pyqt5.qsci python3-pyqt5.qtsvg python3-pyqt5.qtwebkit python3-pip
        
Se quiser apenas fazer a instalação local, o comando fica::

    pip3 install pytuga --user

(Ignore a opção --user, caso queira instalar para todos os usuários. Neste caso
é necessário executar o comando como *sudo*.). Uma vez instalado, você pode
atualizar a versão do Pytuguês executando::
    
    $ pip3 install pytuga -U --user 

O script de instalação salva os arquivos executáveis na pasta ``~/.local/bin.``
e na pasta ``~/bin/``, se a mesma existir.


-------
Windows
-------

Existem duas opções de instalação no Windows. A primeira funciona somente para
o Windows 64bits e consiste em baixar o arquivo auto-executável do pytuga__.
Baixe este arquivo em qualquer lugar do seu computador e execute-o com um clique
duplo.

.. __: http://tinyurl.com/pytg-exe

A segunda opção consiste em baixar os pacotes do Python 3.4 e PyQt5 manualmente
e realizar a instalação via pip. Para isto, escolha os instaladores correspondentes
à sua versão do windows.

32 bits
-------

* `Python 3.4`__
* PyQt5__

.. __: https://www.python.org/ftp/python/3.4.4/python-3.4.4.msi
.. __: https://sourceforge.net/projects/pyqt/files/PyQt5/PyQt-5.5.1/PyQt5-5.5.1-gpl-Py3.4-Qt5.5.1-x32.exe


64 bits
-------

* `Python 3.4`__
* PyQt5__

.. __: https://www.python.org/ftp/python/3.4.4/python-3.4.4.amd64.msi
.. __: https://sourceforge.net/projects/pyqt/files/PyQt5/PyQt-5.5.1/PyQt5-5.5.1-gpl-Py3.4-Qt5.5.1-x64.exe

É importante marcar a opção "Add python.exe to your path" durante a instalação.
Isto facilitará a execução do Pytuguês posteriormente. Depois de terminada a
instalação, abra o terminal do Windows (Win+R e digite "cmd") e execute os
comandos::

    python -m pip install pytuga -U

Se o código anterior não funcionar, provavelmente significa que o Python não 
está no caminho padrão de procura do Windows. Se este for o caso, é necessário
mudar para o diretório onde o Python estiver instalado. Digite::

    cd c:\Python34\
    
Agora repita os comandos anteriores. Se você decidiu instalar o Python em
outro caminho, modifique o comando acima para indicar o caminho correto.

Para executar em modo gráfico, aperte Win+R e digite "pytuga" no prompt. Caso
isto não funcione (especialmente nas versões mais novas do Windows), procure
o executável do tugalinhas na pasta ``c:\Python34\Scripts\`` ou execute o
comando ``python -m pytuga`` do terminal.
