from enum import Enum
from re import compile
from error import panic


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
    def __init__(self, kind, value, filename, line, line_no, column):
        self._kind = kind
        self._value = value
        self._filename = filename
        self._line = line
        self._line_no = line_no
        self._column = column

    def kind(self):
        return self._kind

    def value(self):
        return self._value

    def filename(self):
        return self._filename

    def line(self):
        return self._line

    def line_no(self):
        return self._line_no

    def column(self):
        return self._column

    def __str__(self):
        return f"\
Token   : {self._kind.name}\n\
Line no : {self._line_no}\n\
Column  : {self._column}\n\
Value   : '{self._value}'\n"


class TokenList(list):
    def next(self):
        if not self:
            panic("Attempted to access empty token queue")
        self.pop(0)
        return self.current()

    def current(self):
        if not self:
            panic("Attempted to access empty token queue")
        return self[0]

    def skip(self, expected):
        found = self.current().kind()
        if found is not expected:
            panic(f"Expected token '{expected.name}', found token '{found.name}'")
        return self.pop(0)
