import tokenize

from lazyutils import lazy

from transpyler.errors import BadSytaxError
from transpyler.token import Token, displace_tokens, token_find
from transpyler.utils import keep_spaces


class Lexer:
    """
    Lexer class: it converts
    """

    @lazy
    def error_dict(self):
        return {}

    @lazy
    def translations(self):
        try:
            return dict(self.language.translations)
        except (AttributeError, TypeError):
            return {}

    @lazy
    def sequence_translations(self):
        return {tuple(k): v
                for k, v in self.translations.items()
                if not isinstance(k, str)}

    @lazy
    def single_translations(self):
        return {k: v
                for k, v in self.translations.items()
                if isinstance(k, str)}

    def __init__(self, language):
        self.language = language

    def transpile(self, src):
        """
        Transpile source code to Python.
        """

        # Avoid problems with empty token streams
        if not src or src.isspace():
            return src

        # Convert and process...
        else:
            src_formatted = src

            if not src_formatted.endswith('\n'):
                src_formatted += '\n'

            tokens = self.tokenize(src_formatted)
            transpiled_tokens = self.transpile_tokens(tokens)
            result = self.untokenize(transpiled_tokens)
            return keep_spaces(result, src)

    def tokenize(self, src):
        """
        Convert source string to a list of tokens.

        Args:
            src (str): a string of source code
        """

        current_string = src

        if not current_string.endswith('\n'):
            current_string += '\n'

        def iterlines():
            nonlocal current_string

            if current_string:
                line, sep, current_string = current_string.partition('\n')
                return line + sep
            else:
                raise StopIteration

        tokens = list(tokenize.generate_tokens(iterlines))
        tokens = list(map(Token, tokens))
        return tokens

    def untokenize(self, tokens):
        """
        Convert list of tokens to a string.
        """

        return tokenize.untokenize([tk.to_token_info() for tk in tokens])

    def transpile_tokens(self, tokens):
        """
        Transpile a sequence of Token objects to their corresponding Python
        tokens.
        """

        self.detect_error_sequences(tokens, self.error_dict)
        tokens = self.replace_sequences(tokens, self.sequence_translations)
        tokens = self.replace_translations(tokens, self.single_translations)
        return tokens

    def detect_error_sequences(self, tokens, error_dict):
        """
        Raises a BadSyntaxError if list of tokens contains any sub-sequence in
        the given error_dict.

        Args:
            tokens: List of tokens
            error_dict: A dictionary of {sequence: error_message}
        """

        error_sequences = list(error_dict)
        iterator = token_find(tokens, error_sequences)
        while True:
            try:
                idx, match, start, end = next(iterator)
                msg = error_dict(match)
                match = ' '.join(match)
                raise BadSytaxError(msg, from_token=tokens[idx])
            except StopIteration:
                break

    def replace_sequences(self, tokens, mapping):
        """
        Replace all sequences of tokens in the mapping by the corresponding
        token in the RHS.

        Args:
            tokens: list of tokens.
            mapping: a mapping from token sequences to their corresponding
                replacement (e.g.: {('para', 'cada'): 'for'}).

        Returns:
            A new list of tokens with replacements.
        """
        tokens = list(tokens)
        iterator = token_find(tokens, mapping)
        while True:
            try:
                idx, match, start, end = next(iterator)
                tokens[idx] = Token(mapping[match], start=start)
                del tokens[idx + 1: idx + len(match)]

                linediff, col = tokens[idx].end - end
                if linediff == 0:
                    displace_tokens(tokens[idx + 1:], col)
            except StopIteration:
                break
        return tokens

    def replace_translations(self, tokens, mapping):
        """
        Replace all tokens by the corresponding values in the RHS.

        Args:
            tokens: list of tokens.
            mapping: a mapping from token sequences to their corresponding
                replacement (e.g.: {'enquanto': 'while'}).

        Returns:
            A new list of tokens with replacements.
        """

        tokens = list(tokens)
        for i, tk in enumerate(tokens):
            new = mapping.get(tk.string, tk)
            if new is not tk:
                new = Token(new, start=tk.start)
                tokens[i] = new

                # Align tokens
                linediff, coldiff = new.end - tk.end
                assert linediff == 0
                if coldiff:
                    displace_tokens(tokens[i + 1:], coldiff)
        return tokens
