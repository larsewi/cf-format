import re

from error import eprint, exit_failure
from token import Token
from token_kind import TokenKind


class Lexer:
    @staticmethod
    def tokenize_file(filename):
        contents = ""
        file = None
        try:
            file = open(filename, "r")
            contents = file.read()
        except Exception as e:
            eprint(f"Failed to open file '{filename}' for reading: {e}")
            exit_failure()
        finally:
            if file is not None:
                file.close()

        tokens = []
        lines = contents.splitlines()
        for i, line in enumerate(lines):
            tokens += Lexer._tokenize_line(line, i + 1, filename)

        return tokens

    @staticmethod
    def _tokenize_line(line, line_no, filename):
        tokens = []
        i = 0
        j = len(line)

        while i < j:
            for kind in TokenKind:
                if re.fullmatch(kind.value, line[i:j]):
                    if kind != TokenKind.WHITESPACE:  # Ignore whitespace
                        token = Token(kind, line_no, line[i:j])
                        tokens.append(token)
                    i = j
                    j = len(line) + 1
                    break
            j -= 1

        if i != len(line):
            Lexer.lexer_error(filename, line_no, i, line)

        return tokens

    @staticmethod
    def lexer_error(filename, line_no, column, line):
        eprint(f"There are syntax errors in policy file '{filename}:{line_no}':")
        eprint(line)
        eprint(" " * column + "^ Unrecognized token")
        eprint("\nFor more information use the following command:")
        eprint(f"\tcf-promises {filename}")
        exit_failure()
