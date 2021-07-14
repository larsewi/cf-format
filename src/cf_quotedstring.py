from cf_syntax import CFSyntax
from token import TokenKind


class CFQuotedString(CFSyntax):
    def __init__(self, debug):
        super().__init__("qstring", debug)
        self._value = None

    @staticmethod
    def parse(tokens, debug):
        qstring = CFQuotedString(debug)
        qstring.enter_parser()

        current = tokens.skip(TokenKind.QUOTED_STRING)
        qstring._value = current.value()
        assert isinstance(qstring._value, str)

        qstring.leave_parser()
        return qstring

    def pretty_print(self):
        pass
