.. image:: https://travis-ci.org/transpyler/pytugacore.svg?branch=master
  :target: https://travis-ci.org/transpyler/pytugacore

.. image:: https://codecov.io/gh/Transpyler/pytugacore/branch/master/graph/badge.svg
  :target: https://codecov.io/gh/Transpyler/pytugacore


Pytuga-core implements the core features of Pytuguês language without a
dependency on the QTurtle Qt application. This might be useful for GUI-less
environments such as an online judge or a Jupyterhub installation or if you
just don't want/need a GUI interface.

Most users will prefer to install the `Pytuga <http://github.com/transpyler/pytuga>`_
package that includes a nice graphical interface. Pytuguês is a `Transpyled <http://github.com/transpyler/transpyler>`_
enabled language that translates Python to portuguese:

.. code-block:: pytuga

    função espiral(n):
        """
        Desenha uma espiral de n lados.
        """

        para cada lado de 1 até n:
            frente(lado * 20)
            esquerda(120)

    espiral(20)


Pytuga-core installs a IPython based shell that runs with the command::

    $ python -m pytugacore

Boa programação!