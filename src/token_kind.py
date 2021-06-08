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
    QSTRING = compile(r"\"((\\(.|\n))|[^\"\\])*\"|\'((\\(.|\n))|[^\'\\])*\'|`[^`]*`")
    CLASS = compile(r"[.|&!()a-zA-Z0-9_\200-\377:][\t .|&!()a-zA-Z0-9_\200-\377:]*::")
    VARCLASS = compile(r"(\"[^\"\0]*\"|\'[^\'\0]*\')::")
    PROMISE_GUARD = compile(r"[a-zA-Z_]+:")
