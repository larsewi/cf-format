from cf_syntax import CFSyntax
from cf_comment import CFComment
from token import TokenKind


class CFCommentBlock(CFSyntax):
    def __init__(self, debug):
        super().__init__("commentblock", debug)

    @staticmethod
    def parse(tokens, debug) -> CFSyntax:
        commentblock = CFCommentBlock(debug)
        commentblock.enter_parser()
        nonterms = commentblock._nonterms

        last = tokens.current()
        comment = CFComment.parse(tokens, debug)
        nonterms.append(comment)

        # adjacent comments on ajacent lines belong together in a block
        current = tokens.current()
        while current.kind() is TokenKind.COMMENT and current.row() - last.row() == 1:
            comment = CFComment.parse(tokens, debug)
            nonterms.append(comment)
            last = current
            current = tokens.current()

        commentblock.leave_parser()
        return commentblock

    def pretty_print(self, pp):
        for comment in self._nonterms:
            comment.pretty_print(pp)
        pp.println()
