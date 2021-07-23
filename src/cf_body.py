from cf_syntax import CFSyntax


class CFBody(CFSyntax):
    def __init__(self, debug):
        super().__init__("body", debug)

    @staticmethod
    def parse(tokens, debug) -> CFSyntax:
        body = CFBody(debug)
        body.enter_parser()

        # TODO parse comment

        body.leave_parser()
        return body

    def pretty_print(self, file):
        pass
