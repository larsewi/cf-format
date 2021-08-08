from cf_syntax import CFSyntax
from token import TokenKind


class CFComment(CFSyntax):
    def __init__(self, debug):
        super().__init__("comment", debug)
        self._column = None
        self._value = None

    @staticmethod
    def parse(tokens, debug) -> CFSyntax:
        comment = CFComment(debug)
        comment.enter_parser()

        current = tokens.skip(TokenKind.COMMENT)
        comment._column = current.column()
        assert isinstance(comment._column, int)
        comment._value = current.value()
        assert isinstance(comment._value, str)

        comment.leave_parser()
        return comment

    def pretty_print(self, pp):
        col, row = pp.get_cursor()
        if col < self._column:
            pp.align(self._column - col)
        pp.print(self._value)
