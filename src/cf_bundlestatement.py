from cf_classguard import CFClassGuard
from cf_constraint import CFConstraint
from cf_promiseguard import CFPromiseGuard
from cf_quotedstring import CFQuotedString
from cf_identifier import CFIdentifier
from cf_syntax import CFSyntax
from cf_comment import CFComment
from token import TokenKind


class CFBundleStatement(CFSyntax):
    def __init__(self, debug):
        super().__init__("bundlestatement", debug)

    @staticmethod
    def parse(tokens, debug):
        bundlestatement = CFBundleStatement(debug)
        bundlestatement.enter_parser()

        current = tokens.current()
        if current.kind() is not TokenKind.PROMISE_GUARD:
            bundlestatement.parser_error(current, TokenKind.PROMISE_GUARD)
        promiseguard = CFPromiseGuard.parse(tokens, debug)
        assert promiseguard is not None
        bundlestatement._nonterms.append(promiseguard)

        CFComment.parse_while(bundlestatement, tokens, debug)

        current = tokens.current()
        if current.kind() is TokenKind.CLASS_GUARD:
            classguard = CFClassGuard.parse(tokens, debug)
            assert classguard is not None
            bundlestatement._nonterms.append(classguard)

        CFComment.parse_while(bundlestatement, tokens, debug)

        current = tokens.current()
        if current.kind() is not TokenKind.QUOTED_STRING:
            bundlestatement.parser_error(current, TokenKind.QSTRING)
        promiser = CFQuotedString.parse(tokens, debug)
        assert promiser is not None
        bundlestatement._nonterms.append(promiser)

        current = tokens.current()
        if current.kind() is TokenKind.THIN_ARROW:
            # TODO: Implement promisee, what ever that is ?
            pass

        # TODO: Constraints
        current = tokens.current()
        while current.kind() is not TokenKind.SEMICOLON:
            constraint = CFConstraint.parse(tokens, debug)
            bundlestatement._nonterms.append(constraint)

            current = tokens.current()
            if current.kind() is TokenKind.COMMA:
                tokens.skip(TokenKind.COMMA)
                current = tokens.current()
            else:
                break

        if current.kind() is not TokenKind.SEMICOLON:
            bundlestatement.parser_error(current, TokenKind.COMMA, TokenKind.SEMICOLON)
        tokens.skip(TokenKind.SEMICOLON)

        bundlestatement.leave_parser()
        return bundlestatement

    def pretty_print(self):
        pass
