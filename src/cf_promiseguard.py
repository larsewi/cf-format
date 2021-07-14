from cf_syntax import CFSyntax
from token import TokenKind


class CFPromiseGuard(CFSyntax):
    def __init__(self, debug):
        super().__init__("promiseguard", debug)
        self._value = None

    @staticmethod
    def parse(tokens, debug):
        promiseguard = CFPromiseGuard(debug)
        promiseguard.enter_parser()

        current = tokens.skip(TokenKind.PROMISE_GUARD)
        promiseguard._value = current.value()
        assert isinstance(promiseguard._value, str)

        promiseguard.leave_parser()
        return promiseguard

    def pretty_print(self):
        pass
