import os


class PrettyPrinter:
    def __init__(self, file):
        self._file = file
        self._indent = 0
        self._cursor = (0, 0)

    def print(self, string):
        assert "\n" not in string

        indent = ""
        if self._cursor == 0:
            indent = " " * self._indent
            self._file.write(bytes(indent, "utf-8"))
            col, row = self._cursor
            self._cursor = (col + len(indent), row)

        self._file.write(bytes(string, "utf-8"))
        col, row = self._cursor
        self._cursor = (col + len(indent) + len(string), row)

    def println(self, string=""):
        assert "\n" not in string

        self._file.write(bytes(string + "\n", "utf-8"))
        col, row = self._cursor
        self._cursor = (0, row + 1)

    def delete(self, num_chars):
        col, row = self._cursor
        assert num_chars <= col
        self._file.seek(-num_chars, os.SEEK_END)
        self._file.truncate()
        self._cursor = (col - num_chars, row)

    def get_cursor(self):
        return self._cursor

    def align(self, num_chars):
        align = " " * num_chars
        self._file.write(bytes(align, "utf-8"))
        col, row = self._cursor
        self._cursor = (col + num_chars, row)

    def indent(self):
        assert self._indent % 2 == 0
        self._indent += 2

    def dedent(self):
        assert self._indent >= 2
        assert self._indent % 2 == 0
        self._indent += 2
