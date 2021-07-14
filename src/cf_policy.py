from token_kind import TokenKind
from cf_syntax import CFSyntax
from cf_comment import CFComment
from cf_bundle import CFBundle
from cf_body import CFBody
from cf_promise import CFPromise


class CFPolicy(CFSyntax):
    def __init__(self):
        super().__init__()
        self._non_terms = []

    @staticmethod
    def parse(tokens) -> CFSyntax:
        policy = CFPolicy()
        policy.enter_parser("policy")

        cur = policy.cur_token(tokens)
        while True:
            kind = cur.kind()
            non_term = None
            if kind == TokenKind.COMMENT:
                non_term = CFComment.parse(tokens)
            elif kind == TokenKind.BUNDLE:
                non_term = CFBundle.parse(tokens)
            elif kind == TokenKind.BODY:
                non_term = CFBody.parse(tokens)
            elif kind == TokenKind.PROMISE:
                non_term = CFPromise.parse(tokens)
            elif kind == TokenKind.EOF:
                break
            else:
                policy.parser_error(cur, TokenKind.COMMENT, TokenKind.BUNDLE, TokenKind.BODY, TokenKind.PROMISE, TokenKind.EOF)
            
            assert non_term != None
            policy._non_terms.append(non_term)
            cur = policy.next_token(tokens)

        policy.leave_parser("policy")
        return policy

    def pretty_print(self):
        pass
