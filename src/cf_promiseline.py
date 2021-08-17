from cf_classguard import CFClassGuard
from cf_comment import CFComment
from cf_macro import CFMacro
from cf_syntax import CFSyntax
from cf_quotedstring import CFQuotedString
from cf_constraint import CFConstraint
from token import TokenKind as tk


class CFPromiseLine(CFSyntax):
    def __init__(self, debug):
        super().__init__("promiseline", debug)

    @staticmethod
    def parse(tokens, debug) -> CFSyntax:
        promiseline = CFPromiseLine(debug)
        promiseline.enter_parser()

        # Parse classguard
        promiseline.parse_if(tokens, debug, { tk.CLASS_GUARD: CFClassGuard })

        # Parse comments and macros
        promiseline.parse_while(tokens, debug, { tk.COMMENT: CFComment, tk.MACRO: CFMacro })

        # Parse promiser
        promiseline.parse_or_error(tokens, debug, { tk.QUOTED_STRING: CFQuotedString })

        # Parse promisee
        promiseline.parse_if(tokens, debug, { tk.THIN_ARROW: None }) # TODO

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
        tokens.skip(tk.SEMICOLON)

        promiseline.leave_parser()
        return promiseline

    def pretty_print(self, pretty):
        pass
