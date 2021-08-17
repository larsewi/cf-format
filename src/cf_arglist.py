from cf_comment import CFComment
from cf_identifier import CFIdentifier
from cf_macro import CFMacro
from cf_syntax import CFSyntax
from cf_misc import parse_while_comment_or_macro
from token import TokenKind as tk


class CFArgList(CFSyntax):
    def __init__(self, debug):
        super().__init__("arglist", debug)

    @staticmethod
    def parse(tokens, debug) -> CFSyntax:
        arglist = CFArgList(debug)
        arglist.enter_parser()
        nonterms = arglist._nonterms

        tokens.skip(tk.LEFT_PAR)
        last = tk.LEFT_PAR

        while tokens:
            # Argument
            if tokens.current().kind() is tk.IDENTIFIER:
                if last not in (tk.LEFT_PAR, tk.COMMA):
                    arglist.parser_error(tokens.current(), tk.COMMA)
                last = tk.IDENTIFIER
                arglist.push(CFIdentifier.parse(tokens, debug))

            # Comma
            elif tokens.current().kind() is tk.COMMA:
                if last is not tk.IDENTIFIER:
                    arglist.parser_error(tokens.current(), tk.IDENTIFIER)
                last = tk.COMMA
                tokens.skip(tk.COMMA)

            # Right parentisis
            elif tokens.current().kind() is tk.RIGHT_PAR:
                if last is not tk.IDENTIFIER:
                    arglist.parser_error(tokens.current(), tk.IDENTIFIER)
                last = tk.RIGHT_PAR
                tokens.skip(tk.RIGHT_PAR)
                break

            # Comments or macro
            else:
                arglist.parse_or_error(
                    tokens, debug, {tk.COMMENT: CFComment, tk.MACRO: CFMacro}
                )

        if last is not tk.RIGHT_PAR:
            arglist.parser_error_empty(tk.LEFT_PAR)

        arglist.leave_parser()
        return arglist

    def pretty_print(self, pp):
        nonterms = self._nonterms.copy()

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
