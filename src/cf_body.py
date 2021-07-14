from cf_syntax import CFSyntax


class CFBody(CFSyntax):
    def __init__(self):
        super().__init__()

    @staticmethod
    def parse(tokens) -> CFSyntax:
        body = CFBody()
        body.enter_parser("body")

        # TODO parse comment

        body.leave_parser("body")
        return body

    def pretty_print(self):
        pass
