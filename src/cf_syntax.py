from abc import ABC, abstractmethod, abstractstaticmethod

from error import eprint, exit_failure

class CFSyntax(ABC):
    def __init__(self):
        self._indent = 0

    @abstractmethod
    def pretty_print(self):
        pass

    def enter_parser(self, non_term):
        print(" " * self._indent + f"<{non_term}>")
        self._indent += 2

    def leave_parser(self, non_term):
        assert self._indent >= 2
        self._indent -= 2
        print(" " * self._indent + f"</{non_term}>")

    def cur_token(self, tokens):
        return tokens[0]

    def next_token(self, tokens):
        return tokens.pop(0)

    def parser_error(self, found, *expected):
        eprint(f"There are syntax errors in policy file '{found.filename()}:{found.line_no()}':")
        eprint(found.line())
        eprint(" " * found.column() + f"^ Unexpected token '{found.value()}'")

        eprint(f"\nExpected: ", end="")
        l = len(expected)
        if l >= 3:
            for exp in range(l - 2):
                eprint(f"{expected[exp].name}, ", end="")
        if l >= 2:
            eprint(f"{expected[-2].name} or {expected[-1].name}")
        else:
            eprint(expected[0].name)
        eprint(f"Found: '{found.kind().name}'")

        eprint("\nFor more information use the following command:")
        eprint(f"\tcf-promises {found.filename()}")
        exit_failure()

