from cf_classguard import CFClassGuard
from cf_comment import CFComment
from cf_macro import CFMacro
from cf_syntax import CFSyntax
from cf_quotedstring import CFQuotedString
from cf_constraint import CFConstraint
from cf_rval import CFRval
from token import TokenKind as tk


class CFPromiseLine(CFSyntax):
    def __init__(self, debug):
        super().__init__("promiseline", debug)

    @staticmethod
    def parse(tokens, debug) -> CFSyntax:
        promiseline = CFPromiseLine(debug)
        promiseline.enter_parser()

        # Parse classguard
        promiseline.parse_if(tokens, debug, {tk.CLASS_GUARD: CFClassGuard})

        # Parse comments and macros
        promiseline.parse_while(
            tokens, debug, {tk.COMMENT: CFComment, tk.MACRO: CFMacro}
        )

        # Parse promiser
        promiseline.parse_or_error(tokens, debug, {tk.QUOTED_STRING: CFQuotedString})

        # Parse promisee
        if tokens.current().kind() is tk.THIN_ARROW:
            tokens.skip(tk.THIN_ARROW)
            promiseline.parse_while(
                tokens, debug, {tk.COMMENT: CFComment, tk.MACRO: CFMacro}
            )
            promiseline.push(CFRval.parse(tokens, debug))

        # Parse constraints
        while tokens and tokens.current().kind() is not tk.SEMICOLON:
            promiseline.push(CFConstraint.parse(tokens, debug))

            if tokens and tokens.current().kind() not in (tk.COMMA, tk.SEMICOLON):
                promiseline.parser_error(tokens.current(), tk.COMMA, tk.SEMICOLON)
            else:
                if tokens and tokens.current().kind() is tk.COMMA:
                    tokens.skip(tk.COMMA)

        if not tokens and tokens.current().kind() is not tk.SEMICOLON:
            promiseline.parser_error(tokens.current(), tk.COMMA, tk.SEMICOLON)
        skipped = tokens.skip(tk.SEMICOLON)

        # Parse trailing comment
        if (
            tokens
            and tokens.current().kind() is tk.COMMENT
            and tokens.current().row() == skipped.row()
        ):
            promiseline.push(CFComment.parse(tokens, debug))

        promiseline.leave_parser()
        return promiseline

    def pretty_print(self, pp):
        if isinstance(self.peek(), CFClassGuard):
            classguard = self.pop()
            classguard.pretty_print(pp)

            if (
                isinstance(self.peek(), CFComment)
                and self.peek().row() == classguard.row()
            ):
                pp.print("  ")
                self.pop().pretty_print(pp)

            pp.println()

        pp.indent()

        while isinstance(self.peek(), (CFComment, CFMacro)):
            self.pop().pretty_print(pp)
            pp.println()

        promiser = self.pop()
        assert isinstance(promiser, CFQuotedString)
        promiser.pretty_print(pp)

        # Print stakeholder
        if isinstance(self.peek(), CFRval):
            pp.print(" ")
            pp.print("->")
            pp.print(" ")
            self.pop().pretty_print(pp)

        # Print constraints
        first = True
        while isinstance(self.peek(), CFConstraint):
            if first:
                first = False
            else:
                pp.print(",")

            pp.indent()
            pp.println()
            self.pop().pretty_print(pp)
            pp.dedent()

        pp.print(";")
        if not self.empty():
            trailing_comment = self.pop()
            assert isinstance(trailing_comment, CFComment)
            pp.print("  ")
            trailing_comment.pretty_print(pp)

        pp.dedent()
