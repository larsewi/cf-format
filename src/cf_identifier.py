from cf_syntax import CFSyntax
from token import TokenKind


class CFIdentifier(CFSyntax):
    def __init__(self, debug):
        super().__init__("identifier", debug)
        self._value = None

    @staticmethod
    def parse(tokens, debug) -> CFSyntax:
        identifier = CFIdentifier(debug)
        identifier.enter_parser()

        current = tokens.skip(TokenKind.IDENTIFIER)
        identifier._value = current.value()

        identifier.leave_parser()
        return identifier

    def pretty_print(self, pp):
        assert isinstance(self._value, str)
        pp.print(self._value)
