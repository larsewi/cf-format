import re

from error import eprint, exit_failure, exit_success
from token import Token
from token_kind import TokenKind


class Lexer:
    def __init__(self, filename, debug):
        self._filename = filename
        self._debug = debug

    def tokenize(self):
        contents = ""
        file = None
        try:
            file = open(self._filename, "r")
            contents = file.read()
        except Exception as e:
            eprint(f"Failed to open file '{self._filename}' for reading: {e}")
            exit_failure()
        finally:
            if file is not None:
                file.close()

        tokens = []
        lines = contents.splitlines()
        line_no = 0
        for line in lines:
            line_no += 1
            tokens += self._tokenize_line(line, line_no)

        token = Token(TokenKind.EOF, "EoF", self._filename, line, line_no, len(lines[len(lines) - 1]))
        if self._debug:
            print(token)
        tokens.append(token)

        return tokens

    def _tokenize_line(self, line, line_no):
        tokens = []
        i = 0
        j = len(line)

        while i < j:
            for kind in TokenKind:
                if re.fullmatch(kind.value, line[i:j]):
                    token = Token(kind, line[i:j], self._filename, line, line_no, i)
                    if kind != TokenKind.WHITESPACE: # ignore whitespace tokens
                        tokens.append(token)
                        if self._debug:
                            print(token)

                    i = j
                    j = len(line) + 1
                    break
            j -= 1

        if i != len(line):
            Lexer.lexer_error(line_no, i, line)

        return tokens

    def lexer_error(self, line_no, column, line):
        eprint(f"There are syntax errors in policy file '{self._filename}:{line_no}':")
        eprint(line)
        eprint(" " * column + "^ Unrecognized token")
        eprint("\nFor more information use the following command:")
        eprint(f"\tcf-promises {self._filename}")
        exit_failure()
