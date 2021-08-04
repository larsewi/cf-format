from cf_syntax import CFSyntax
from token import TokenKind


class CFRval(CFSyntax):
    def __init__(self, debug):
        super().__init__("rval", debug)

    @staticmethod
    def parse(tokens, debug):
        rval = CFRval(debug)
        rval.enter_parser()

        current = tokens.current()
        if current.kind() is TokenKind.IDENTIFIER:
            # TODO: function
            pass
        elif current.kind() is TokenKind.QUOTED_STRING:
            # TODO: quoted string
            pass
        elif current.kind() is TokenKind.NAKED_VAR:
            pass
        elif current.kind() is TokenKind.LEFT_PAR:
            pass
        else:
            rval.parser_error(
                current,
                TokenKind.IDENTIFIER,
                TokenKind.QUOTED_STRING,
                TokenKind.NAKED_VAR,
                TokenKind.LEFT_PAR,
            )

        rval.leave_parser()
        return rval

    def pretty_print(self, cursor=0):
        return ""
