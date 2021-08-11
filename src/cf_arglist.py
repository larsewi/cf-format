from cf_identifier import CFIdentifier
from cf_syntax import CFSyntax
from cf_misc import parse_while_comment_or_macro
from token import TokenKind as TK


class CFArgList(CFSyntax):
    def __init__(self, debug):
        super().__init__("arglist", debug)

    @staticmethod
    def parse(tokens, debug) -> CFSyntax:
        arglist = CFArgList(debug)
        arglist.enter_parser()
        nonterms = arglist._nonterms

        tokens.skip(TK.LEFT_PAR)
        last = TK.LEFT_PAR

        while tokens:
            # Argument
            if tokens.current().kind() is TK.IDENTIFIER:
                if last not in (TK.LEFT_PAR, TK.COMMA):
                    arglist.parser_error(tokens.current(), TK.COMMA)
                last = TK.IDENTIFIER
                nonterms.append(CFIdentifier.parse(tokens, debug))

            # Comma
            elif tokens.current().kind() is TK.COMMA:
                if last is not TK.IDENTIFIER:
                    arglist.parser_error(tokens.current(), TK.IDENTIFIER)
                last = TK.COMMA
                tokens.skip(TK.COMMA)

            # Right parentisis
            elif tokens.current().kind() is TK.RIGHT_PAR:
                if last is not TK.IDENTIFIER:
                    arglist.parser_error(tokens.current(), TK.IDENTIFIER)
                last = TK.RIGHT_PAR
                tokens.skip(TK.RIGHT_PAR)
                break

            # Comments or macro
            else:
                assert tokens.current().kind() in (TK.COMMENT, TK.MACRO)
                parse_while_comment_or_macro(nonterms, tokens, debug)
        
        if last is not TK.RIGHT_PAR:
            arglist.parser_error_empty(TK.LEFT_PAR)

        arglist.leave_parser()
        return arglist

    def pretty_print(self, pp):
        pp.delete(2)
