from cf_syntax import CFSyntax
from token import TokenKind


class CFComment(CFSyntax):
    def __init__(self, debug):
        super().__init__("comment", debug)
        self._row = None
        self._column = None
        self._value = None

    def row(self):
        return self._row

    def column(self):
        return self._column

    @staticmethod
    def parse(tokens, debug) -> CFSyntax:
        comment = CFComment(debug)
        comment.enter_parser()

        current = tokens.skip(TokenKind.COMMENT)
        comment._row = current.row()
        comment._column = current.column()
        comment._value = current.value()

        comment.leave_parser()
        return comment

    def pretty_print(self, pp):
        pp.print(self._value)
