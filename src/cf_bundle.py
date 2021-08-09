from cf_arglist import CFArgList
from cf_bundlebody import CFBundleBody
from cf_commentblock import CFCommentBlock
from cf_identifier import CFIdentifier
from cf_macro import CFMacro
from cf_syntax import CFSyntax
from cf_misc import parse_while_comment_or_macro
from token import TokenKind


class CFBundle(CFSyntax):
    def __init__(self, debug):
        super().__init__("bundle", debug)

    @staticmethod
    def parse(tokens, debug) -> CFSyntax:
        bundle = CFBundle(debug)
        bundle.enter_parser()
        nonterms = bundle._nonterms

        tokens.skip(TokenKind.BUNDLE)

        parse_while_comment_or_macro(nonterms, tokens, debug)

        # Parse bundletype
        if tokens.current().kind() is not TokenKind.IDENTIFIER:
            bundle.parser_error(tokens.current(), TokenKind.IDENTIFIER)
        nonterms.append(CFIdentifier.parse(tokens, debug))

        parse_while_comment_or_macro(nonterms, tokens, debug)

        # Parse bundleid
        if tokens.current().kind() is not TokenKind.IDENTIFIER:
            bundle.parser_error(tokens.current(), TokenKind.IDENTIFIER)
        nonterms.append(CFIdentifier.parse(tokens, debug))

        parse_while_comment_or_macro(nonterms, tokens, debug)

        # Parse arglist
        if tokens.current().kind() is TokenKind.LEFT_PAR:
            nonterms.append(CFArgList.parse(tokens, debug))

        parse_while_comment_or_macro(nonterms, tokens, debug)

        # Parse bundlebody
        nonterms.append(CFBundleBody.parse(tokens, debug))

        bundle.leave_parser()
        return bundle

    def pretty_print(self, pp):
        nonterms = self._nonterms

        pp.print("bundle ")

        # Comment / macro
        nonterm = nonterms.pop(0)
        while isinstance(nonterm, (CFCommentBlock, CFMacro)):
            nonterm.pretty_print(pp)
            nonterms.pop(0)

        # Bundletype
        assert isinstance(nonterm, CFIdentifier)
        nonterm.pretty_print(pp)
        nonterm = nonterms.pop(0)
        pp.print(" ")

        # Comment / macro
        while isinstance(nonterm, (CFCommentBlock, CFMacro)):
            nonterm.pretty_print(pp)
            nonterms.pop(0)

        # Bundleid
        assert isinstance(nonterm, CFIdentifier)
        nonterm.pretty_print(pp)
        nonterm = nonterms.pop(0)

        # Comment / macro
        while isinstance(nonterm, (CFCommentBlock, CFMacro)):
            nonterm.pretty_print(pp)
            nonterm = nonterms.pop(0)

        # Arglist
        if isinstance(nonterm, CFArgList):
            nonterm.pretty_print(pp)
            nonterm = nonterms.pop(0)

        pp.println()

        # Bundlebody
