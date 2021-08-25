from cf_bundlestatement import CFBundleStatement
from cf_comment import CFComment
from cf_macro import CFMacro
from cf_syntax import CFSyntax
from token import TokenKind as tk


class CFBundleBody(CFSyntax):
    def __init__(self, debug):
        super().__init__("bundlebody", debug)

    @staticmethod
    def parse(tokens, debug) -> CFSyntax:
        bundlebody = CFBundleBody(debug)
        bundlebody.enter_parser()

        # Skip left brace
        current = tokens.current()
        if current.kind() is not tk.LEFT_BRACE:
            bundlebody.parser_error(current, tk.LEFT_BRACE)
        tokens.skip(tk.LEFT_BRACE)

        while tokens and tokens.current().kind() is not tk.RIGHT_BRACE:
            bundlebody.parse_or_error(
                tokens,
                debug,
                {
                    tk.PROMISE_GUARD: CFBundleStatement,
                    tk.COMMENT: CFComment,
                    tk.MACRO: CFMacro,
                },
            )

        # skip right brace
        if not tokens or tokens.current().kind() is not tk.RIGHT_BRACE:
            bundlebody.parser_error(tokens.current(), tk.RIGHT_BRACE)
        tokens.skip(tk.RIGHT_BRACE)

        bundlebody.leave_parser()
        return bundlebody

    def pretty_print(self, pp):
        pp.println("{")
        pp.indent()
        while not self.empty():
            self.pop().pretty_print(pp)
            pp.println()
        pp.dedent()
        pp.print("}")
