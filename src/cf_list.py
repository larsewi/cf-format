from cf_syntax import CFSyntax


class CFList(CFSyntax):
    def __init__(self, debug):
        super().__init__("list", debug)

    @staticmethod
    def parse(tokens, debug) -> CFSyntax:
        lst = CFList(debug)
        lst.enter_parser()

        # TODO: Implement me!

        lst.leave_parser()
        return lst

    def pretty_print(self, pp):
        pass
