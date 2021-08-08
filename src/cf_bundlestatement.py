from cf_promiseguard import CFPromiseGuard
from cf_promiseline import CFPromiseLine
from cf_syntax import CFSyntax
from cf_comment import CFComment
from token import TokenKind


class CFBundleStatement(CFSyntax):
    def __init__(self, debug):
        super().__init__("bundlestatement", debug)

    @staticmethod
    def parse(tokens, debug) -> CFSyntax:
        bundlestatement = CFBundleStatement(debug)
        bundlestatement.enter_parser()
        nonterms = bundlestatement._nonterms

        # Parse promiseguard
        current = tokens.current()
        if current.kind() is not TokenKind.PROMISE_GUARD:
            bundlestatement.parser_error(current, TokenKind.PROMISE_GUARD)
        promiseguard = CFPromiseGuard.parse(tokens, debug)
        assert promiseguard is not None
        nonterms.append(promiseguard)

        while tokens.current().kind() in (
            TokenKind.CLASS_GUARD,
            TokenKind.QUOTED_STRING,
            TokenKind.COMMENT,
        ):
            if tokens.current().kind() is TokenKind.COMMENT:
                # Parse comment
                comment = CFComment.parse(tokens, debug)
                assert comment is not None
                nonterms.append(comment)
            else:
                # Parse promiseline
                promiseline = CFPromiseLine.parse(tokens, debug)
                assert promiseline is not None
                nonterms.append(promiseline)

        bundlestatement.leave_parser()
        return bundlestatement

    def pretty_print(self, pretty):
        pass
