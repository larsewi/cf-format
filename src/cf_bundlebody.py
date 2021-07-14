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

        tokens.skip(TokenKind.LEFT_BRACE)
        token = tokens.current()

        while token.kind() is not TokenKind.RIGHT_BRACE:
            CFComment.parse_while(bundlebody, tokens, debug)
            bundlestatement = CFBundleStatement.parse(tokens, debug)
            assert bundlestatement is not None
            bundlebody._nonterms.append(bundlestatement)
            token = tokens.current()

        token = tokens.current()
        if token.kind() is not TokenKind.RIGHT_BRACE:
            bundlebody.parser_error(token, TokenKind.RIGHT_BRACE)
        tokens.skip(TokenKind.RIGHT_BRACE)

        bundlebody.leave_parser()
        return bundlebody

    def pretty_print(self):
        pass
