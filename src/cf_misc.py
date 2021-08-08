from cf_commentblock import CFCommentBlock
from cf_macro import CFMacro
from token import TokenKind as TK


def parse_while_comment_or_macro(nonterms, tokens, debug):
    while tokens and tokens.current().kind() in (TK.COMMENT, TK.MACRO,):
        if tokens.current().kind() is TK.COMMENT:
            nonterms.append(CFCommentBlock.parse(tokens, debug))
        else:
            nonterms.append(CFMacro.parse(tokens, debug))
