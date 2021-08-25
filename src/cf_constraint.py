from cf_identifier import CFIdentifier
from cf_rval import CFRval
from cf_syntax import CFSyntax
from token import TokenKind as tk


class CFConstraint(CFSyntax):
    def __init__(self, debug):
        super().__init__("constraint", debug)

    @staticmethod
    def parse(tokens, debug) -> CFSyntax:
        constraint = CFConstraint(debug)
        constraint.enter_parser()

        constraint.parse_or_error(tokens, debug, {tk.IDENTIFIER: CFIdentifier})

        current = tokens.current()
        if current.kind() is not tk.FAT_ARROW:
            constraint.parser_error(current, tk.FAT_ARROW)
        tokens.skip(tk.FAT_ARROW)

        constraint.push(CFRval.parse(tokens, debug))

        constraint.leave_parser()
        return constraint

    def pretty_print(self, pp):
        pass
