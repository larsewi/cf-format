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
                if last not in (tk.IDENTIFIER, tk.LEFT_PAR):
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
        if self.empty():
            return

        # In case we need to retry
        nonterms = self._nonterms.copy()
        cursor = pp.get_cursor()

        # Try no wrap
        if not self._no_wrap(pp):
            # Restore state
            self._nonterms = nonterms.copy()
            pp.truncate_to(cursor)

            # Try single wrap
            if not self._single_wrap(pp):
                # Restore state
                self._nonterms = nonterms
                pp.truncate_to(cursor)

                # Last resort, do full wrap
                self._full_wrap(pp)

    def _no_wrap(self, pp):
        stash = []
        pp.print("(")
        num_ids = len([id for id in self._nonterms if isinstance(id, CFIdentifier)])

        while not self.empty():
            this = self.pop()

            if isinstance(this, CFMacro):
                return False
            elif isinstance(this, CFComment):
                stash.append(this)
            else:
                assert isinstance(this, CFIdentifier)
                this.pretty_print(pp)
                if num_ids > 1:
                    pp.print(", ")
                num_ids -= 1

        pp.print(")")
        if pp.should_wrap():
            return False

        for comment in stash:
            pp.print("  ")
            comment.pretty_print(pp)

        return True

    def _single_wrap(self, pp):
        stash = []
        pp.println("(")
        pp.indent()
        num_ids = len([id for id in self._nonterms if isinstance(id, CFIdentifier)])

        while not self.empty():
            this = self.pop()

            if isinstance(this, CFMacro):
                pp.dedent()
                return False
            elif isinstance(this, CFComment):
                stash.append(this)
            else:
                assert isinstance(this, CFIdentifier)
                this.pretty_print(pp)
                if num_ids > 1:
                    pp.print(", ")
                num_ids -= 1

        if pp.should_wrap():
            pp.dedent()
            return False

        pp.println()
        pp.dedent()
        pp.print(")")
        for comment in stash:
            pp.print("  ")
            comment.pretty_print(pp)

        return True

    def _full_wrap(self, pp):
        stash = []
        pp.println("(")
        pp.indent()
        num_ids = len([id for id in self._nonterms if isinstance(id, CFIdentifier)])

        while not self.empty():
            this = self.pop()

            if isinstance(this, CFMacro):
                this.pretty_print(pp)
                pp.println()
            elif isinstance(this, CFComment):
                stash.append(this)
            else:
                assert isinstance(this, CFIdentifier)
                this.pretty_print(pp)
                if num_ids > 1:
                    pp.print(",")
                num_ids -= 1

                while isinstance(self.peek(), CFComment):
                    if num_ids == 0:
                        pp.print("   ")
                    else:
                        pp.print("  ")
                    self.pop().pretty_print(pp)
                
                pp.println()
        
        pp.dedent()
        pp.print(")")

        for comment in stash:
            pp.print("  ")
            comment.pretty_print(pp)
