from token import TokenKind
from cf_comment import CFComment
from cf_commentblock import CFCommentBlock
from cf_macro import CFMacro
from cf_syntax import CFSyntax
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
            kind = tokens.current().kind()
            nonterm = None
            if kind is TokenKind.BUNDLE:
                nonterm = CFBundle.parse(tokens, debug)
            elif kind is TokenKind.BODY:
                nonterm = CFBody.parse(tokens, debug)
            elif kind is TokenKind.PROMISE:
                nonterm = CFPromise.parse(tokens, debug)
            elif kind is TokenKind.COMMENT:
                nonterm = CFCommentBlock.parse(tokens, debug)
            elif kind is TokenKind.MACRO:
                nonterm = CFMacro.parse(tokens, debug)
            else:
                policy.parser_error(
                    tokens.current(),
                    TokenKind.BUNDLE,
                    TokenKind.BODY,
                    TokenKind.PROMISE
                )

            policy._nonterms.append(nonterm)

        policy.leave_parser()
        return policy

    def pretty_print(self, pp):
        last = None
        for nonterm in self._nonterms:
            if isinstance(last, (CFBundle, CFBody, CFPromise)):
                pp.println()
            if isinstance(last, CFCommentBlock) and isinstance(nonterm, CFCommentBlock):
                pp.println()
            nonterm.pretty_print(pp)
            last = nonterm
        pp.println()
