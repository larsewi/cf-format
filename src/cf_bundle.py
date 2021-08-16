from ast import parse
from cf_arglist import CFArgList
from cf_bundlebody import CFBundleBody
from cf_identifier import CFIdentifier
from cf_comment import CFComment
from cf_macro import CFMacro
from cf_syntax import CFSyntax
from token import TokenKind as tk


class CFBundle(CFSyntax):
    def __init__(self, debug):
        super().__init__("bundle", debug)

    @staticmethod
    def parse(tokens, debug) -> CFSyntax:
        bundle = CFBundle(debug)
        bundle.enter_parser()

        tokens.skip(tk.BUNDLE)

        # Parse comments and macros
        bundle.parse_while(tokens, debug, {
            tk.COMMENT: CFComment,
            tk.MACRO: CFMacro
        })

        # Parse bundletype
        bundle.parse_or_error(tokens, debug, { tk.IDENTIFIER: CFIdentifier })

        # Parse comments and macros
        bundle.parse_while(tokens, debug, {
            tk.COMMENT: CFComment,
            tk.MACRO: CFMacro
        })

        # Parse bundleid
        bundle.parse_or_error(tokens, debug, { tk.IDENTIFIER: CFIdentifier })

        # Parse comments and macros
        bundle.parse_while(tokens, debug, {
            tk.COMMENT: CFComment,
            tk.MACRO: CFMacro
        })

        # Parse arglist
        bundle.parse_if(tokens, debug, { tk.LEFT_PAR: CFArgList })

        # Parse comments and macros
        bundle.parse_while(tokens, debug, {
            tk.COMMENT: CFComment,
            tk.MACRO: CFMacro
        })

        # Parse bundlebody
        bundle.push(CFBundleBody.parse(tokens, debug))

        bundle.leave_parser()
        return bundle

    def pretty_print(self, pp):
        pp.print("bundle ")

        # Comment / macro
        nonterm = self.pop()
        while isinstance(nonterm, (CFComment, CFMacro)):
            nonterm.pretty_print(pp)
            nonterm = nonterms.pop(0)

        # Bundletype
        assert isinstance(nonterm, CFIdentifier)
        nonterm.pretty_print(pp)
        nonterm = nonterms.pop(0)
        pp.print(" ")

        # Comment / macro
        while isinstance(nonterm, (CFComment, CFMacro)):
            nonterm.pretty_print(pp)
            nonterms.pop(0)

        # Bundleid
        assert isinstance(nonterm, CFIdentifier)
        nonterm.pretty_print(pp)
        nonterm = nonterms.pop(0)

        if not isinstance(nonterm, CFArgList):
            pp.println()

        # Comment / macro
        while isinstance(nonterm, (CFComment, CFMacro)):
            nonterm.pretty_print(pp)
            nonterm = nonterms.pop(0)

        # Arglist
        if isinstance(nonterm, CFArgList):
            nonterm.pretty_print(pp)
            nonterm = nonterms.pop(0)
            pp.println()

        # Comment / macro
        while isinstance(nonterm, (CFComment, CFMacro)):  # glekki,  # glekki
            nonterm.pretty_print(pp)
            nonterm = nonterms.pop(0)

        # Bundlebody
        assert isinstance(nonterm, CFBundleBody)
        nonterm.pretty_print(pp)
