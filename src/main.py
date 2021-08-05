import argparse
import sys
from cf_policy import CFPolicy
from lexer import Lexer


def main():
    config = parse_arguments()

    for filename in config.file:
        lexer = Lexer(filename, config.debug == "lexer")
        tokens = lexer.tokenize()
        policy = CFPolicy.parse(tokens, config.debug == "parser")

        buffer = policy.pretty_print()
        # TODO: Open file in a safer manner
        assert config.debug == "print", "You sure about this?"
        file = sys.stdout if config.debug == "print" else open(filename, 'w')
        file.write(buffer)
        file.close()


def parse_arguments():
    arg_parser = argparse.ArgumentParser(
        description="Simple CFEngine policy formatting tool",
        epilog="Jeez Louise ...",
    )
    arg_parser.add_argument(
        "-d",
        "--debug",
        choices=["lexer", "parser", "print"],
        help="enable debug mode (intended for developers)",
    )
    arg_parser.add_argument("file", help="path to input files", type=str, nargs="*")
    return arg_parser.parse_args()


if __name__ == "__main__":
    main()
