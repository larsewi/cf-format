from cf_comment import CFComment
from cf_macro import CFMacro
from token import TokenKind as TK


def parse_while_comment_or_macro(self, tokens, debug):
    while tokens and tokens.current().kind() in (TK.COMMENT, TK.MACRO,):
        if tokens.current().kind() is TK.COMMENT:
            self.push(CFComment.parse(tokens, debug))
        else:
            self.push(CFMacro.parse(tokens, debug))
