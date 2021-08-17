from token import TokenKind as tk
from cf_comment import CFComment
from cf_macro import CFMacro
from cf_syntax import CFSyntax
from cf_bundle import CFBundle
from cf_body import CFBody
from cf_promise import CFPromise


class CFPolicy(CFSyntax):
    def __init__(self, debug):
        super().__init__("policy", debug)

    @staticmethod
    def parse(tokens, debug) -> CFSyntax:
        policy = CFPolicy(debug)
        policy.enter_parser()

        expect = {
            tk.BUNDLE: CFBundle,
            tk.BODY: CFBody,
            tk.PROMISE: CFPromise,
            tk.COMMENT: CFComment,
            tk.MACRO: CFMacro,
        }

        policy.parse_while(tokens, debug, expect)

        if tokens:
            policy.parser_error(tokens.current(), expect.keys())

        policy.leave_parser()
        return policy

    def pretty_print(self, pp):
        last = None
        first = True
        while not self.empty():
            this = self.pop()

            if not first and not (
                isinstance(last, CFComment)
                and isinstance(this, CFComment)
                and this.row() - last.row() == 1
            ):
                pp.println()
            elif first:
                first = False

            this.pretty_print(pp)
            pp.println()
            last = this
