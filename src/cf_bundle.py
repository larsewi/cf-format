from cf_syntax import CFSyntax


class CFBundle(CFSyntax):
    def __init__(self):
        super().__init__()

    @staticmethod
    def parse(tokens) -> CFSyntax:
        bundle = CFBundle()
        bundle.enter_parser("bundle")

        # TODO parse comment

        bundle.leave_parser("bundle")
        return bundle

    def pretty_print(self):
        pass
