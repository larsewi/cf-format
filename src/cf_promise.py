from cf_syntax import CFSyntax
from token import TokenKind


class CFPromise(CFSyntax):
    def __init__(self, debug):
        super().__init__("promise", debug)
        self._value = None

    @staticmethod
    def parse(tokens, debug) -> CFSyntax:
        promise = CFPromise(debug)
        promise.enter_parser()

        current = tokens.skip(TokenKind.QSTRING)
        promise._value = current.value()
        assert isinstance(promise._value, str)

        promise.leave_parser()
        return promise

    def pretty_print(self):
        pass
