import os


class PrettyPrinter:
    def __init__(self, file):
        self._file = file
        self._indent = ""
        self._cursor = (0, 0)
        self._max_col = 80

    def print(self, string):
        col, _ = self._cursor
        if col == 0:
            self._file.write(bytes(self._indent, "utf-8"))
            col, row = self._cursor
            self._cursor = (col + len(self._indent), row)
        self.print_no_indent(string)

    def println(self, string=""):
        assert "\n" not in string
        self.print(string)
        self._file.write(bytes("\n", "utf-8"))
        _, row = self._cursor
        self._cursor = (0, row + 1)

    def print_no_indent(self, string=""):
        assert "\n" not in string
        self._file.write(bytes(string, "utf-8"))
        col, row = self._cursor
        self._cursor = (len(string) + col, row)

    def truncate_to(self, cursor):
        new_col, new_row = self._cursor
        old_col, old_row = cursor

        assert new_col >= old_col
        assert new_row == old_row

        self._file.seek(old_col - new_col, os.SEEK_END)
        self._file.truncate()
        self._cursor = cursor

    def get_cursor(self):
        return self._cursor

    def align(self, num_chars):
        align = " " * num_chars
        self._file.write(bytes(align, "utf-8"))
        col, row = self._cursor
        self._cursor = (col + num_chars, row)

    def indent(self):
        assert len(self._indent) % 2 == 0
        self._indent += "  "

    def dedent(self):
        assert len(self._indent) >= 2
        assert len(self._indent) % 2 == 0
        self._indent = self._indent[:-2]

    def should_wrap(self, pluss=0):
        col, _ = self._cursor
        return col + pluss > self._max_col
