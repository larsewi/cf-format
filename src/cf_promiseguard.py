from cf_syntax import CFSyntax
from token import TokenKind


class CFPromiseGuard(CFSyntax):
    def __init__(self, debug):
        super().__init__("promiseguard", debug)
        self._value = None
        self._row = None

    def row(self):
        return self._row

    @staticmethod
    def parse(tokens, debug) -> CFSyntax:
        promiseguard = CFPromiseGuard(debug)
        promiseguard.enter_parser()

        skipped = tokens.skip(TokenKind.PROMISE_GUARD)
        promiseguard._value = skipped.value()
        promiseguard._row = skipped.row()

        promiseguard.leave_parser()
        return promiseguard

    def pretty_print(self, pp):
        pp.print(self._value)
