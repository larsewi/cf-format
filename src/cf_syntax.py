from abc import ABC, abstractmethod
from error import eprint, exit_failure


class CFSyntax(ABC):
    _indent = 0

    def __init__(self, name, debug):
        self._name = name
        self._debug = debug
        self._nonterms = []

    @abstractmethod
    def pretty_print(self, pp):
        pass

    def enter_parser(self):
        if self._debug:
            print(" " * CFSyntax._indent + f"<{self._name}>")
            self.indent()

    def leave_parser(self):
        if self._debug:
            self.dedent()
            print(" " * CFSyntax._indent + f"</{self._name}>")

    def indent(self):
        CFSyntax._indent += 2

    def dedent(self):
        assert CFSyntax._indent >= 2
        CFSyntax._indent -= 2

    def parser_error(self, found, *expected):
        eprint(
            f"There are syntax errors in policy file '{found.filename()}' on line {found.row() + 1}\n"
        )
        eprint(found.line())
        eprint(" " * found.column() + f"^ Unexpected token '{found.value()}'")

        eprint(f"\nExpected: ", end="")
        l = len(expected)
        if l >= 3:
            for i in range(l - 2):
                eprint(f"{expected[i].name}, ", end="")
        if l >= 2:
            eprint(f"{expected[-2].name} or {expected[-1].name}")
        else:
            eprint(expected[0].name)
        eprint(f"Found: {found.kind().name}")

        eprint("\nFor more information run:")
        eprint(f"\tcf-promises '{found.filename()}'")
        exit_failure()

    def parser_error_empty(self, *expected):
        eprint(f"There are syntax errors in policy file\n")
        eprint(f"\nExpected: ", end="")
        l = len(expected)
        if l >= 3:
            for i in range(l - 2):
                eprint(f"{expected[i].name}, ", end="")
        if l >= 2:
            eprint(f"{expected[-2].name} or {expected[-1].name}")
        else:
            eprint(expected[0].name)
        eprint("Found nothing")
