from cf_syntax import CFSyntax


class CFComment(CFSyntax):
    def __init__(self):
        super().__init__()

    @staticmethod
    def parse(tokens) -> CFSyntax:
        comment = CFComment()
        comment.enter_parser("comment")

        # TODO parse comment

        comment.leave_parser("comment")
        return comment

    def pretty_print(self):
        pass
