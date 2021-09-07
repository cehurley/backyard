
class Error(Exception):
    """Base class for exceptions in this module."""
    def __init__(self, expression, message):
        self.expression = expression
        self.message = message

class TooManyWhereClauses(Exception):
    pass


class TooManyOrderByClauses(Exception):
    pass


class TooManyLimitClauses(Exception):
    pass

class ParseError(Error): pass
