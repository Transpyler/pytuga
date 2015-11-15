==========
Instalação
==========


Pytuguês se baseia e é implementado em Python 3. Para a instalação completa do 
Pytuguês, é necessário instalar algumas bibliotecas adicionais do Python. As 
instruções de instalação diferem ligeiramente em cada plataforma.


-----
Linux
-----

Você precisa do Python3 e do PyQt4. Existe uma chance razoável que ambos 
estejam instalados. Se sua distribuição for baseada no Debian/Ubuntu,
o comando abaixo garante que todas as bibliotecas necessárias serão 
instaladas

::

    $ sudo apt-get install python3-all python3-pyqt5 python3-pyqt5.qsci python3-pyqt5.qtsvg python3-pip
        
Se quiser apenas fazer a instalação local, o comando fica::

    $ pip3 install pytuga --user
    
(Ignore a opção --user, caso queira instalar para todos os usuários). Uma vez
instalado, você pode atualizar a versão do Pytuguês usando::
    
    $ pip3 install pytuga -U --user 
    
O script de instalação salva os arquivos executáveis na pasta ``~/.local/bin.`` 
Normalmente esta pasta não está no ``PATH``, mas a pasta ``~/bin/`` está. Se esta 
pasta existir, use o comando

::

    $ cp ~/.local/bin/* ~/bin/
    
Caso ela não exista, faça a ligação entre as duas

::

    $ ln -s ~/.local/bin ~/bin
    


-------
Windows
-------

É necessário baixar e instalar manualmente os pacote com o Python3.4 e o PyQt4.
Os pacotes variam um pouco caso seu Windows seja de 32 ou 64 bits:

32 bits
    * Python__
    * PyQt5__
    
.. __: https://www.python.org/ftp/python/3.4.3/python-3.4.3.msi
.. __: http://sourceforge.net/projects/pyqt/


64 bits
    * Python__
    * PyQt5__

.. __: https://www.python.org/ftp/python/3.4.3/python-3.4.3.amd64.msi
.. __: http://sourceforge.net/projects/pyqt/

É importante marcar a opção "Add python.exe to your path" durante a instalação.
Depois disto abra o terminal do Windows (Win+R e digite "cmd") e execute os 
comandos::
    
    $ python -m pip install pytuga -U
    
Se o código anterior não funcionar, provavelmente significa que o Python não 
está no caminho padrão de procura do Windows. Se este for o caso, é necessário
mudar para o diretório onde o Python foi instalado. Digite::

    $ cd c:\Python34\
    
E agora repita os comandos anteriores. Se você decidiu instalar o Python em 
outro caminho, modifique o comando acima para indicar o caminho correto.

Para executar o Tugalinhas, aperte Win+R e digite "tugalinhas" no prompt. Caso
isto não funcione (especialmente nas versões mais novas do Windows), procure
o executável do tugalinhas na pasta ``c:\Python34\Scripts\``
