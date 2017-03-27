from logo.utils import alias

COLOR_TRANSLATIONS = {
    'azul': 'blue',
    'amarelo': 'yellow',
    'vermelho': 'red',
    'preto': 'black',
    'branco': 'white',
}


class PortugueseCursor:
    def frente(self, passo):
        """
        Move para frente pelo passo especificado em pixels.

        Se a caneta estiver abaixada, desenha uma linha. Passos negativos
        correspondem a um movimento para trás.
        """

        return self.forward(passo)

    @alias('tras')
    def trás(self, passo):
        """
        Move para trás pelo passo especificado em pixels.

        Se a caneta estiver abaixada, desenha uma linha. Passos negativos
        correspondem a um movimento para frente.
        """

        return self.backward(passo)

    def esquerda(self, ângulo):
        """
        Gira para a esquerda pelo ângulo fornecido em graus.
        """

        return self.left(ângulo)

    def direita(self, ângulo):
        """
        Gira para a direita pelo ângulo fornecido em graus.
        """

        return self.right(ângulo)

    @vecargsmethod
    @alias('vá_para', 'va_para')
    def ir_para(self, posição):
        """
        Desloca para o ponto dado.

        Se a caneta estiver abaixada, desenha uma linha.
        """

        self.goto(posição)

    @vecargsmethod
    @alias('teletransporte', 'teletransportar', 'pule_para')
    def pular_para(self, posição):
        """
        Desloca para o ponto dado sem desenhar.

        Não altera o estado da caneta após o deslocamento.
        """

        self.jumpto(posição)

    @alias('levante', 'subir_caneta', 'suba_caneta',
           'levantar_caneta', 'levante_caneta')
    def levantar(self):
        """
        Levanta a caneta.

        Deslocamentos na tela não produzirão nenhum desenho.
        """

        self.penup()

    @alias('abaixe', 'baixe_caneta', 'baixar_caneta',
           'abaixar_caneta', 'abaixe_caneta')
    def abaixar(self):
        """
        Abaixa a caneta do Tuga.

        Deslocamentos na tela produzirão desenho.
        """

        self.pendown()

    def desenhando(self):
        """
        Retorna verdadeiro se a caneta estiver abaixada e falso, caso
        contrário.
        """

        return self.isdown()

    @alias('limpe')
    def limpar(self):
        """
        Limpa todos os desenhos na tela.
        """

        self.clear()

    @alias('reinicie')
    def reiniciar(self):
        """
        Limpa os desenhos na tela e retorna o Tuga para a orientação
        orignal.
        """

        self.restart()

    @alias('posicao')
    def posição(self):
        """
        Retorna um vetor de duas coordenada com a posição do Tuga.
        """

        return self.getpos()

    @alias('defina_posição', 'defina_posicao')
    def definir_posição(self, *args):
        """
        Define as novas coordenadas do Tuga.

        Pode receber dois argumentos com a nova posição x e y ou um argumento
        com um vetor ou tupla de duas coordenadas.
        """

        self.setpos(*args)

    @alias('direcao')
    def direção(self):
        """
        Retorna a orientação do Tuga em graus.

        Medimos a orientação a partir da posição horizontal com o Tuga olhando
        para a direita.
        """

        return self.getheading()

    @alias('defina_direção', 'defina_direcao')
    def definir_direção(self, direção):
        """
        Gira o Tuga para a orientação fornecida.

        Medimos a orientação a partir da posição horizontal com o Tuga olhando
        para a direita.
        """

        return self.setheading(direção)

    def cor_da_linha(self):
        """
        Retorna a cor da linha.
            """

        return self.getcolor()

    def cor_do_fundo(self):
        """Retorna a cor do fundo"""

        return self.getfill()

    @alias('defina_cor_da_linha')
    def definir_cor_da_linha(self, cor):
        """Define a cor da linha do desenho.

        A cor pode ser especificada pelas coordenadas (R, G, B), por uma string
        hex ou pelo seu nome em inglês ou português."""

        if isinstance(cor, str):
            cor = cor.lower()
            cor = COLOR_TRANSLATIONS.get(cor, cor)
        self.setcolor(cor)

    @alias('defina_cor_do_fundo')
    def definir_cor_do_fundo(self, cor):
        """Define a cor do preenchimento.

        A cor pode ser especificada pelas coordenadas (R, G, B), por uma string
        hex ou pelo seu nome em inglês ou português."""

        if isinstance(cor, str):
            cor = cor.lower()
            cor = COLOR_TRANSLATIONS.get(cor, cor)
        self.setfill(cor)

    def espessura(self):
        """Retorna a espessura da linha em pixels."""

        return self.getwidth()

    @alias('defina_espessura')
    def definir_espessura(self, px):
        """Define a espessura da linha em pixels."""

        self.setwidth(px)

    @alias('definir_velocidade', 'defina_velocidade')
    def velocidade(self, valor):
        """Modifica a velocidade de desenho do Tuga.

        A velocidade corresponde a um número de 1 até 10, onde 1 corresponde
        ao desenho mais lento e 10 ao desenho mais rápido."""

        self.speed(valor)

    def ajuda(self):
        """Mostra uma ajuda com os principais comandos disponíveis em inglês."""

        self.turtlehelp()