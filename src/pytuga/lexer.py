from tokenize import NEWLINE

from transpyler import token
from transpyler.token import Token
from transpyler.lexer import Lexer

__all__ = ['PytugaLexer']


class PytugaLexer(Lexer):
    """
    Pytuga lexer.

    Defines the "repetir n vezes" and "de X ate Y a cada Z" commands.
    """

    def process_repetir_command(self, tokens):
        """
        Converts command::

            repetir <N> vezes:
                <BLOCO>

        or::

            repita <N> vezes:
                <BLOCO>

        to::

            for ___ in range(<N>):
                <BLOCO>
        """

        matches = [('repetir',), ('repita',), ('vezes',), (NEWLINE,)]
        iterator = token.token_find(tokens, matches)
        for idx, match, start, end in iterator:
            # Send tokens to the beginning of the equivalent "for" loop
            starttokens = Token.from_strings(
                tokens[idx].start, 'for', '___', 'in', 'range', '('
            )
            del tokens[idx]
            token.insert_tokens_at(tokens, idx, starttokens, end=end)

            # Matches the 'vezes' token
            try:
                idx, match, start, end = next(iterator)
            except StopIteration:
                match = [None]

            if match[0] != 'vezes':
                raise SyntaxError(
                    'comando repetir malformado na linha %s.\n'
                    '    Espera comando do tipo\n\n'
                    '        repetir <N> vezes:\n'
                    '            <BLOCO>\n\n'
                    '    Palavra chave "vezes" está faltando!' % (start.lineno))
            else:
                tokens[idx] = Token(')', start=start)
                token.displace_tokens(tokens[idx + 1:], -4)

        return tokens

    def process_de_ate_command(self, tokens):
        """
        Converts command::

            de <X> até <Y> [a cada <Z>]

        to::

            in range(<X>, <Y> + 1[, <Z>])

        """

        matches = [('de',), ('ate',), ('a', 'cada',), (NEWLINE,), (':',)]
        iterator = token.token_find(tokens, matches)
        for idx, match, start, end in iterator:
            # Waits for a 'de' token to start processing
            if match[0] != 'de':
                continue

            # Send tokens for the beginning of the equivalent in range(...)
            # test
            start = tokens[idx].start
            starttokens = Token.from_strings(start, 'in', 'range', '(')
            del tokens[idx]
            token.insert_tokens_at(tokens, idx, starttokens, end=end)

            # Matches the 'até' token and insert a comma separator
            idx, match, start, end = next(iterator)
            if match[0] in ['até', 'ate']:
                token.displace_tokens(tokens[idx:], -3)
                tokens[idx] = Token(',', start=tokens[idx - 1].end)
            else:
                raise SyntaxError(
                    'comando para cada malformado na linha %s.\n'
                    '    Espera comando do tipo\n\n'
                    '        para cada <x> de <a> até <b>:\n'
                    '            <BLOCO>\n\n'
                    '    Palavra chave "até" está faltando!' % (start.lineno)
                )

            idx, match, start, end = next(iterator)

            # Matches "a cada" or the end of the line
            if match == ('a', 'cada'):
                middletokens = Token.from_strings(start, '+', '1', ',')
                del tokens[idx:idx + 2]
                token.insert_tokens_at(tokens, idx, middletokens, end=end)

                # Proceed to the end of the line
                idx, match, start, end = next(iterator)
                if match[0] not in (NEWLINE, ':'):
                    raise SyntaxError(
                        'comando malformado na linha %s.\n'
                        '    Espera um ":" no fim do bloco' % (start.lineno)
                    )
                endtok = Token(')', start=start)
                token.displace_tokens(tokens[idx:], 1)
                tokens.insert(idx, endtok)

            # Finish command
            elif match[0] in (NEWLINE, ':'):
                token.displace_tokens(tokens[idx:], 1)
                endtokens = Token.from_strings(start, '+', '1', ')')
                token.insert_tokens_at(tokens, idx, endtokens, end=end)

            # Unexpected token
            else:
                raise SyntaxError(
                    'comando malformado na linha %s.\n'
                    '    Espera um ":" no fim do bloco' % (start.lineno)
                )

        return tokens

    def transpile_tokens(self, tokens):
        tokens = super().transpile_tokens(tokens)
        tokens = self.process_repetir_command(tokens)
        tokens = self.process_de_ate_command(tokens)
        return tokens
