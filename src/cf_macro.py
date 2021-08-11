from cf_syntax import CFSyntax
from token import TokenKind as TK


class CFMacro(CFSyntax):
    def __init__(self, debug):
        super().__init__("macro", debug)
        self._value = None

    def parse(tokens, debug) -> CFSyntax:
        macro = CFMacro(debug)
        macro.enter_parser()

        current = tokens.skip(TK.MACRO)
        macro._value = current.value()
        assert isinstance(macro._value, str)

        macro.leave_parser()
        return macro

    def pretty_print(self, pp):
        pp.print_no_indent(self._value)
