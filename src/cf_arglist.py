from cf_commentblock import CFCommentBlock
from cf_identifier import CFIdentifier
from cf_macro import CFMacro
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
        pp.print("(")

        if self._no_wrap_failed(pp):
            pp.println()
            pp.indent()
            if self._no_wrap_failed(pp):
                self._full_wrap(pp)
            pp.dedent()
            pp.println()
        pp.print(")")

    def _no_wrap_failed(self, pp):
        old_cursor = pp.get_cursor()
        first = True

        for nonterm in self._nonterms:
            if not isinstance(nonterm, CFIdentifier):
                pp.truncate_to(old_cursor)
                return True

            if first:
                first = False
            else:
                pp.print(", ")

            nonterm.pretty_print(pp)

            if pp.should_wrap(1):
                pp.truncate_to(old_cursor)
                return True

        return False

    def _full_wrap(self, pp):
        num_id = len([id for id in self._nonterms if isinstance(id, CFIdentifier)])

        first = True
        last = None
        for nonterm in self._nonterms:
            if first:
                first = False
            elif isinstance(nonterm, CFIdentifier) and isinstance(last, CFIdentifier):
                pp.println()
            nonterm.pretty_print(pp)
            if isinstance(nonterm, CFIdentifier):
                if num_id > 1:
                    pp.print(",")
                num_id -= 1
            last = nonterm
