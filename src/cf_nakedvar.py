from typing import no_type_check
from cf_syntax import CFSyntax
from token import TokenKind as tk


class CFNakedVar(CFSyntax):
    def __init__(self, debug):
        super().__init__("nakedvar", debug)
        self._value = None
        self._row = None

    def row(self):
        return self._row

    @staticmethod
    def parse(tokens, debug) -> CFSyntax:
        nakedvar = CFNakedVar(debug)
        nakedvar.enter_parser()

        skipped = tokens.skip(tk.NAKED_VAR)
        nakedvar._value = skipped.value()
        nakedvar._row = skipped.row()

        nakedvar.leave_parser()
        return nakedvar

    def pretty_print(self, pp):
        pass
