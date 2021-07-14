from cf_comment import CFComment
from cf_identifier import CFIdentifier
from cf_syntax import CFSyntax
from token import TokenKind


class CFArgList(CFSyntax):
    def __init__(self, debug):
        super().__init__("arglist", debug)

    @staticmethod
    def parse(tokens, debug) -> CFSyntax:
        arglist = CFArgList(debug)
        arglist.enter_parser()

        tokens.skip(TokenKind.LEFT_PAR)
        CFComment.parse_while(arglist, tokens, debug)

        while True:
            current = tokens.current()
            if current.kind() is not TokenKind.IDENTIFIER:
                arglist.parser_error(current, TokenKind.IDENTIFIER)
            identifier = CFIdentifier.parse(tokens, debug)
            assert identifier is not None
            arglist._nonterms.append(identifier)

            CFComment.parse_while(arglist, tokens, debug)
            current = tokens.current()
            if current.kind() is TokenKind.COMMA:
                tokens.skip(TokenKind.COMMA)
            else:
                break

        current = tokens.current()
        if current.kind() is not TokenKind.RIGHT_PAR:
            arglist.parser_error(current, TokenKind.RIGHT_PAR, TokenKind.COMMA)
        tokens.skip(TokenKind.RIGHT_PAR)

        arglist.leave_parser()
        return arglist

    def pretty_print(self):
        pass
