from exceptions import CFSyntaxException
import argparse
from sys import stderr
from lex import Lex
from format import Format

def main():
    config = parse_arguments()
    lexer = Lex()
    format = Format()

    for filename in config.file:
        with open(filename, 'r') as f:
            data = f.read()

        lexer.input(data)

        try:
            tokens = [tok for tok in lexer if tok.type not in ("NEWLINE", "INDENT")]
        except CFSyntaxException as e:
            print("There are syntax errors in policy file '%s': %s" % (filename, e), file=stderr)
            continue

        for token in tokens:
            print("DEBUG:", token.__repr__())

        try:
            format.input(tokens)
        except CFSyntaxException as e:
            print("There are syntax errors in policy file '%s': %s" % (filename, e), file=stderr)
            #continue

        print("DEBUG:", "'%s'" % format)




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
