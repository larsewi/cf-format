import os


class PrettyPrinter:
    _MAX_COL = 80

    def __init__(self, debug):
        self._debug = debug
        self._indent = ""
        self._strlst = [""]

    def print(self, s):
        assert "\n" not in s

        if not self._strlst[-1]:
            self._strlst[-1] = self._indent
        if s:
            self._strlst[-1] += s

        self._log_debug()

    def println(self, s=""):
        assert "\n" not in s

        if s:
            self._strlst[-1] += s
        self._strlst.append("")

        self._log_debug()

    def print_no_indent(self, s=""):
        assert "\n" not in s

        if s:
            self._strlst[-1] += s

        self._log_debug()

    def get_cursor(self):
        row = len(self._strlst)
        col = len(self._strlst[-1])
        return (row, col)

    def truncate_to(self, cursor):
        row, col = cursor
        self._strlst = self._strlst[: row - 1]
        self._strlst[-1] = self._strlst[-1][: col - 1]

        self._log_debug()

    def align(self, spaces):
        self._strlst[-1] += " " * spaces

        self._log_debug()

    def indent(self):
        assert len(self._indent) % 2 == 0
        self._indent += "  "

    def dedent(self):
        assert len(self._indent) >= 2
        assert len(self._indent) % 2 == 0
        self._indent = self._indent[:-2]

    def should_wrap(self, pluss=0):
        col = len(self._strlst[-1])
        return col + pluss > self._MAX_COL

    def __str__(self):
        return "\n".join(self._strlst)

    def _log_debug(self):
        if self._debug:
            print(self._strlst[-1].replace(" ", "·"))
