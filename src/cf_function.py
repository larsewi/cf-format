from cf_syntax import CFSyntax


class CFFunction(CFSyntax):
    def __init__(self, debug):
        super().__init__("function", debug)

    @staticmethod
    def parse(tokens, debug) -> CFSyntax:
        function = CFFunction(debug)
        function.enter_parser()

        # TODO: implement me!

        function.leave_parser()
        return function

    def pretty_print(self, pp):
        pass
