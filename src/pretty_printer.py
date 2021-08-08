class PrettyPrinter:
    def __init__(self, file):
        self._file = file
        self._indent = 0
        self._cursor = (0, 0)

    def print(self, string):
        assert "\n" not in string

        if self._cursor == 0:
            indent = " " * self._indent
            print(indent, file=self._file, end="")
            col, row = self._cursor
            self._cursor = (col + len(indent), row)

        print(string, file=self._file, end="")
        col, row = self._cursor
        self._cursor = (col + len(indent), row)

    def println(self, string=""):
        assert "\n" not in string

        print(string, file=self._file)
        col, row = self._cursor
        self._cursor = (0, row + 1)

    def get_cursor(self):
        return self._cursor

    def align(self, spaces):
        align = " " * spaces
        print(align, file=self._file)
        col, row = self._cursor
        self._cursor = (col + len(spaces), row)

    def indent(self):
        assert self._indent % 2 == 0
        self._indent += 2

    def dedent(self):
        assert self._indent >= 2
        assert self._indent % 2 == 0
        self._indent += 2
