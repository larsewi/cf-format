from cf_syntax import CFSyntax
from token import TokenKind


class CFComment(CFSyntax):
    def __init__(self, debug):
        super().__init__("comment", debug)
        self._value = None

    @staticmethod
    def parse(tokens, debug) -> CFSyntax:
        comment = CFComment(debug)
        comment.enter_parser()

        current = tokens.skip(TokenKind.COMMENT)
        comment._value = current.value()
        assert isinstance(comment._value, str)

        comment.leave_parser()
        return comment

    def pretty_print(self):
        pass

    @staticmethod
    def parse_while(it, tokens, debug):
        kind = tokens.current().kind()
        while kind is TokenKind.COMMENT:
            comment = CFComment.parse(tokens, debug)
            assert comment is not None
            it._nonterms.append(comment)
            kind = tokens.current().kind()
