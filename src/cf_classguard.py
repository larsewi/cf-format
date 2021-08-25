from cf_syntax import CFSyntax
from token import TokenKind


class CFClassGuard(CFSyntax):
    def __init__(self, debug):
        super().__init__("classguard", debug)
        self._value = None
        self._row = None

    def row(self):
        return self._row

    @staticmethod
    def parse(tokens, debug) -> CFSyntax:
        classguard = CFClassGuard(debug)
        classguard.enter_parser()

        skipped = tokens.skip(TokenKind.CLASS_GUARD)
        classguard._value = skipped.value()
        classguard._row = skipped.row()

        classguard.leave_parser()
        return classguard

    def pretty_print(self, pp):
        pp.print(self._value)
