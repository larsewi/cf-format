import argparse
from sys import stderr
from lex import IllegalTokenException, Lex
from format import format, SyntaxErrorException

def main():
    config = parse_arguments()
    lexer = Lex()

    for filename in config.file:
        with open(filename, 'r') as f:
            in_data = f.read()

        lexer.input(in_data)

        try:
            tokens = [tok for tok in lexer if tok.type not in ("NEWLINE", "INDENT")]
        except IllegalTokenException as e:
            print("There are syntax errors in policy file '%s'" % filename, file=stderr)
            print(e, file=stderr)
            continue

        for token in tokens:
            print("DEBUG:", token)

        out_data = ""
        try:
            out_data = format(tokens)
        except SyntaxErrorException as e:
            print("There are syntax errors in policy file '%s'" % filename, file=stderr)
            print(e, file=stderr)
            #continue

        print("DEBUG:", "'%s'" % out_data)




def parse_arguments():
    arg_parser = argparse.ArgumentParser(
        description="Simple CFEngine policy formatting tool",
        epilog="Jeez Louise ...",
    )
    arg_parser.add_argument(
        "-d",
        "--debug",
        choices=["lexer", "parser", "printer"],
        help="enable different debug modes (intended for developers)",
    )
    arg_parser.add_argument("file", help="path to input files", type=str, nargs="*")
    return arg_parser.parse_args()


if __name__ == "__main__":
    main()
