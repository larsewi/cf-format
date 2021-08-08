from cf_syntax import CFSyntax


class CFMacro(CFSyntax):
    def __init__(self, debug):
        super().__init__("macro", debug)
        self._value = None

    def parse(tokens, debug) -> CFSyntax:
        macro = CFMacro(debug)
        macro.enter_parser()

        skipped = tokens.current().skip(CFMacro)
        macro._value = skipped.value()
        assert isinstance(macro._value, str)

        macro.leave_parser()
        return macro

    def pretty_print(self, pretty):
        pass
