from token import TokenKind
from cf_syntax import CFSyntax
from cf_comment import CFComment
from cf_bundle import CFBundle
from cf_body import CFBody
from cf_promise import CFPromise


class CFPolicy(CFSyntax):
    def __init__(self, debug):
        super().__init__("policy", debug)

    @staticmethod
    def parse(tokens, debug) -> CFSyntax:
        policy = CFPolicy(debug)
        policy.enter_parser()

        while tokens:
            CFComment.parse_while(policy, tokens, debug)

            kind = tokens.current().kind()
            nonterm = None
            if kind is TokenKind.BUNDLE:
                nonterm = CFBundle.parse(tokens, debug)
            elif kind is TokenKind.BODY:
                nonterm = CFBody.parse(tokens, debug)
            elif kind is TokenKind.PROMISE:
                nonterm = CFPromise.parse(tokens, debug)
            else:
                policy.parser_error(
                    tokens.current(),
                    TokenKind.COMMENT,
                    TokenKind.BUNDLE,
                    TokenKind.BODY,
                    TokenKind.PROMISE,
                )

            assert nonterm != None
            policy._nonterms.append(nonterm)

        policy.leave_parser()
        return policy

    def pretty_print(self):
        pass
