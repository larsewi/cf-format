import re
from exceptions import CFSyntaxException

tokens = (
    ("INDENT", re.compile(r"[ \t]+")),
    ("NEWLINE", re.compile(r"(\r\n|\r|\n)")),

    ("COMMENT", re.compile(r"#[^\n]*")),
    ("MACRO", re.compile(r"@(if [a-z_]+\([^)]+\)|else|endif)")),

    ("BUNDLE", re.compile(r"bundle")),
    ("BODY", re.compile(r"body")),
    ("PROMISE", re.compile(r"promise")),

    ("NAKED_VARIABLE", re.compile(r"[$@][(][a-zA-Z0-9_\[\]\200-\377.:]+[)]|[$@][{][a-zA-Z0-9_\[\]\200-\377.:]+[}]|[$@][(][a-zA-Z0-9_\200-\377.:]+[\[][a-zA-Z0-9_$(){}\200-\377.:]+[\]]+[)]|[$@][{][a-zA-Z0-9_\200-\377.:]+[\[][a-zA-Z0-9_$(){}\200-\377.:]+[\]]+[}]")),
    ("IDENTIFIER", re.compile(r"[a-zA-Z0-9_\200-\377]+([:][a-zA-Z0-9_\200-\377]+)?")),
    ("QUOTED_STRING", re.compile(r"\"((\\(.|\n))|[^\"\\])*\"|\'((\\(.|\n))|[^'\\])*\'|`[^`]*`")),

    ("CLASS_GUARD", re.compile(r"((\"[^\"\0]*\"|\'[^'\0]*\')|(\"[^\"\0]*\"|\'[^'\0]*\'))::")),
    ("PROMISE_GUARD", re.compile(r"[a-zA-Z_]+:")),

    ("LEFT_PARENTHESIS", re.compile(r"\(")),
    ("RIGHT_PARENTHESIS", re.compile(r"\)")),
    ("LEFT_BRACE", re.compile(r"\{")),
    ("RIGHT_BRACE", re.compile(r"\}")),
    ("COMMA", re.compile(r"\,")),
    ("SEMICOLON", re.compile(r"\;")),
    ("THIN_ARROW", re.compile(r"->")),
    ("THICK_ARROW", re.compile(r"=>")),
)


class LexToken:
    def __init__(self, type, value, lineno, column):
        self.type = type
        self.value = value
        self.lineno = lineno
        self.column = column

    def __repr__(self):
        return "(%s,'%s',%d,%d)" % (self.type, self.value, self.lineno, self.column)

    def __str__(self):
        return "%s" % self.type.lower().replace("_", " ")

class Lex():
    def __init__(self):
        self.lexpos = 0
        self.lexlen = 0
        self.lineno = 0
        self.column = 0
        self.lexdata = None

    def input(self, data):
        self.lexpos = 0
        self.lexlen = len(data)
        self.lineno = 1
        self.column = 1
        self.lexdata = data

    def token(self):
        for i in range(self.lexlen, self.lexpos, -1):
            text = self.lexdata[self.lexpos : i]

            for type, regex in tokens:
                if re.fullmatch(regex, text) is not None:
                    tok = LexToken(type, text, self.lineno, self.column)
                    if type == "NEWLINE":
                        self.lineno += 1
                        self.column = 1
                    else:
                        self.column += len(text)
                    self.lexpos += len(text)
                    return tok

        if self.lexpos != self.lexlen:
            msg = "Illegal token [%d,%d]" % (self.lineno, self.column)
            raise CFSyntaxException(msg)
        return None

    def __iter__(self):
        return self

    def next(self):
        tok = self.token()
        if not tok:
            raise StopIteration
        return tok

    __next__ = next
