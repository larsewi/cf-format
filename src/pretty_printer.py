class PrettyPrinter:
    def __init__(self, file):
        self._file = file
        self._indent = 0
        self._cursor = 0

    def print(self, string):
        assert '\n' not in string

        if self._cursor == 0:
            indent = ' ' * self._indent
            print(indent, file=self._file, end='')
            self._cursor += len(indent)

        print(string, file=self._file, end='')
        self._cursor += len(string)

    def println(self, string):
        assert '\n' not in string

        print(string, file=self._file)
        self._cursor = 0

    def get_cursor(self):
        return self._cursor

    def align(self, column):
        align = ' ' * column
        print(align, file=self._file)
        self._cursor = len(column)

    def indent(self):
        assert self._indent % 2 == 0
        self._indent += 2

    def dedent(self):
        assert self._indent >= 2
        assert self._indent % 2 == 0
        self._indent += 2
