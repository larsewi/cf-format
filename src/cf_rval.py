from cf_function import CFFunction
from cf_list import CFList
from cf_nakedvar import CFNakedVar
from cf_quotedstring import CFQuotedString
from cf_syntax import CFSyntax
from cf_identifier import CFIdentifier
from token import TokenKind as tk


class CFRval(CFSyntax):
    def __init__(self, debug):
        super().__init__("rval", debug)

    @staticmethod
    def parse(tokens, debug) -> CFSyntax:
        rval = CFRval(debug)
        rval.enter_parser()

        rval.parse_or_error(
            tokens,
            debug,
            {
                tk.IDENTIFIER: CFFunction,
                tk.QUOTED_STRING: CFQuotedString,
                tk.NAKED_VAR: CFNakedVar,
                tk.LEFT_BRACE: CFList,
            },
        )

        rval.leave_parser()
        return rval

    def pretty_print(self, pp):
        pass
