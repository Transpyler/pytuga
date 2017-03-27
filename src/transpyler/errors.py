class BadSytaxError(SyntaxError):
    """
    Base class for transpyler syntax errors.
    """

    @property
    def msg(self):
        return self.args[0]

    @property
    def lineno(self):
        return self.args[1]

    @property
    def pos(self):
        return self.args[2]

    def __init__(self, msg, lineno=None, pos=None, from_token=None):
        if from_token:
            lineno = from_token.start.lineno
            pos = from_token.start.pos
        args = msg, lineno, pos
        super().__init__(args)

    def __str__(self):
        if self.lineno:
            return 'at line %s, %s: %s' % (self.lineno, self.pos, self.msg)
        return self.msg