from cf_syntax import CFSyntax
from token import TokenKind


class CFQuotedString(CFSyntax):
    def __init__(self, debug):
        super().__init__("quotedstring", debug)
        self._value = None
        self._row = None

    @staticmethod
    def parse(tokens, debug) -> CFSyntax:
        qstring = CFQuotedString(debug)
        qstring.enter_parser()

        skipped = tokens.skip(TokenKind.QUOTED_STRING)
        qstring._value = skipped.value()
        qstring._row = skipped.row()

        qstring.leave_parser()
        return qstring

    def pretty_print(self, pp):
        pp.print(self._value)
