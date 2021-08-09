from cf_identifier import CFIdentifier
from cf_syntax import CFSyntax
from cf_misc import parse_while_comment_or_macro
from token import TokenKind


class CFArgList(CFSyntax):
    def __init__(self, debug):
        super().__init__("arglist", debug)

    @staticmethod
    def parse(tokens, debug) -> CFSyntax:
        arglist = CFArgList(debug)
        arglist.enter_parser()
        nonterms = arglist._nonterms

        tokens.skip(TokenKind.LEFT_PAR)

        while True:
            parse_while_comment_or_macro(nonterms, tokens, debug)

            if tokens.current().kind() is not TokenKind.IDENTIFIER:
                arglist.parser_error(tokens.current(), TokenKind.IDENTIFIER)
            nonterms.append(CFIdentifier.parse(tokens, debug))

            parse_while_comment_or_macro(nonterms, tokens, debug)

            if tokens.current().kind() is TokenKind.COMMA:
                tokens.skip(TokenKind.COMMA)
            else:
                break

        if tokens.current().kind() is not TokenKind.RIGHT_PAR:
            arglist.parser_error(tokens.current(), TokenKind.RIGHT_PAR, TokenKind.COMMA)
        tokens.skip(TokenKind.RIGHT_PAR)

        arglist.leave_parser()
        return arglist

    def pretty_print(self, pp):
        pass
