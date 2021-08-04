from cf_syntax import CFSyntax
from token import TokenKind


class CFClassGuard(CFSyntax):
    def __init__(self, debug):
        super().__init__("classguard", debug)
        self._value = None

    @staticmethod
    def parse(tokens, debug):
        classguard = CFClassGuard(debug)
        classguard.enter_parser()

        current = tokens.skip(TokenKind.CLASS_GUARD)
        classguard._value = current.value()
        assert isinstance(classguard._value, str)

        classguard.leave_parser()
        return classguard

    def pretty_print(self, cursor=0):
        return self._value
