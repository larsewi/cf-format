from cf_macro import CFMacro
from cf_promiseguard import CFPromiseGuard
from cf_promiseline import CFPromiseLine
from cf_syntax import CFSyntax
from cf_comment import CFComment
from token import TokenKind as tk


class CFBundleStatement(CFSyntax):
    def __init__(self, debug):
        super().__init__("bundlestatement", debug)

    @staticmethod
    def parse(tokens, debug) -> CFSyntax:
        bundlestatement = CFBundleStatement(debug)
        bundlestatement.enter_parser()

        # Parse promiseguard
        bundlestatement.parse_or_error(
            tokens, debug, {tk.PROMISE_GUARD: CFPromiseGuard}
        )

        # Parse promiselines, comments and macros
        bundlestatement.parse_while(
            tokens,
            debug,
            {
                tk.CLASS_GUARD: CFPromiseLine,
                tk.QUOTED_STRING: CFPromiseLine,
                tk.COMMENT: CFComment,
                tk.MACRO: CFMacro,
            },
        )

        bundlestatement.leave_parser()
        return bundlestatement

    def pretty_print(self, pp):
        promiseguard = self.pop()
        assert isinstance(promiseguard, CFPromiseGuard)
        promiseguard.pretty_print(pp)

        if isinstance(self.peek(), CFComment) and self.peek().row() == promiseguard.row():
            pp.print("  ")
            self.pop().pretty_print(pp)

        pp.indent()
        pp.println()

        while not self.empty():
            self.pop().pretty_print(pp)
            pp.println()

        pp.dedent()
