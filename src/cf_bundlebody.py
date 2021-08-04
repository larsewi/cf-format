from cf_bundlestatement import CFBundleStatement
from cf_comment import CFComment
from cf_syntax import CFSyntax
from token import TokenKind


class CFBundleBody(CFSyntax):
    def __init__(self, debug):
        super().__init__("bundlebody", debug)

    @staticmethod
    def parse(tokens, debug) -> CFSyntax:
        bundlebody = CFBundleBody(debug)
        bundlebody.enter_parser()
        nonterms = bundlebody._nonterms

        # Skip left brace
        current = tokens.current()
        if current.kind() is not TokenKind.LEFT_BRACE:
            bundlebody.parser_error(current, TokenKind.LEFT_BRACE)
        tokens.skip(TokenKind.LEFT_BRACE)

        while tokens.current().kind() in (TokenKind.PROMISE_GUARD, TokenKind.COMMENT):
            if tokens.current().kind() is TokenKind.COMMENT:
                # Parse comment
                comment = CFComment.parse(tokens, debug)
                assert comment is not None
                nonterms.append(comment)
            else:
                # Parse bundlestatement
                bundlestatement = CFBundleStatement.parse(tokens, debug)
                assert bundlestatement is not None
                nonterms.append(bundlestatement)

        # skip right brace
        current = tokens.current()
        if current.kind() is not TokenKind.RIGHT_BRACE:
            bundlebody.parser_error(current, TokenKind.RIGHT_BRACE)
        tokens.skip(TokenKind.RIGHT_BRACE)

        bundlebody.leave_parser()
        return bundlebody

    def pretty_print(self, cursor=0):
        buf = ""
        nonterms = self._nonterms

        for nonterm in nonterms:
            if isinstance(nonterm, CFComment):
                buf += "  " + nonterm.pretty_print() + "\n"
            else:
                assert isinstance(nonterm, CFBundleStatement)
                buf += "  " + nonterm.pretty_print() + "\n\n"

        return "{\n" + buf + "\n}"
