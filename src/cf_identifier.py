from cf_syntax import CFSyntax
from token import TokenKind


class CFIdentifier(CFSyntax):
    def __init__(self, debug):
        super().__init__("identifier", debug)
        self._value = None

    @staticmethod
    def parse(tokens, debug):
        identifier = CFIdentifier(debug)
        identifier.enter_parser()

        current = tokens.skip(TokenKind.IDENTIFIER)
        identifier._value = current.value()
        assert isinstance(identifier._value, str)

        identifier.leave_parser()
        return identifier

    def pretty_print(self, file):
        pass
