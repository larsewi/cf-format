from cf_syntax import CFSyntax


class CFPromise(CFSyntax):
    def __init__(self):
        super().__init__()

    @staticmethod
    def parse(tokens) -> CFSyntax:
        promise = CFPromise()
        promise.enter_parser("promise")

        # TODO parse comment

        promise.leave_parser("promise")
        return promise

    def pretty_print(self):
        pass
