from enum import Enum
from re import compile


class TokenKind(Enum):
    WHITESPACE = compile(r"\s+")
    COMMA = compile(r",")
    SEMICOLON = compile(r";")
    LEFT_BRACE = compile(r"{")
    RIGHT_BRACE = compile(r"}")
    LEFT_PAR = compile(r"\(")
    RIGHT_PAR = compile(r"\)")
    COMMENT = compile(r"#[^\n]*")
    MACRO = compile(r"@.*")
    BUNDLE = compile(r"bundle")
    BODY = compile(r"body")
    PROMISE = compile(r"promise")
    IDENTIFIER = compile(r"[a-zA-Z0-9_\200-\377]+")
    SYMBOL = compile(r"[a-zA-Z0-9_\200-\377]+[:][a-zA-Z0-9_\200-\377]+")
    FAT_ARROW = compile(r"=>")
    THIN_ARROW = compile(r"->")
    QUOTED_STRING = compile(
        r"\"((\\(.|\n))|[^\"\\])*\"|\'((\\(.|\n))|[^\'\\])*\'|`[^`]*`"
    )
    CLASS_GUARD = compile(
        r"[.|&!()a-zA-Z0-9_\200-\377:][\t .|&!()a-zA-Z0-9_\200-\377:]*::"
    )
    VARCLASS = compile(r"(\"[^\"\0]*\"|\'[^\'\0]*\')::")
    PROMISE_GUARD = compile(r"[a-zA-Z_]+:")


class Token:
    def __init__(self, kind, value, filename, line, row, column):
        self._kind = kind
        self._value = value
        self._filename = filename
        self._line = line
        self._row = row
        self._column = column

    def kind(self):
        return self._kind

    def value(self):
        return self._value

    def filename(self):
        return self._filename

    def line(self):
        return self._line

    def row(self):
        return self.row

    def column(self):
        return self._column

    def __str__(self):
        return f"\
Token  : {self._kind.name}\n\
Row    : {self._row + 1}\n\
Column : {self._column + 1}\n\
Value  : '{self._value}'\n"


class TokenList(list):
    def next(self):
        assert self, "Attempted to access empty token queue"
        self.pop(0)
        return self.current()

    def current(self):
        assert self, "Attempted to access empty token queue"
        return self[0]

    def skip(self, expected):
        found = self.current().kind()
        assert found is expected
        return self.pop(0)
