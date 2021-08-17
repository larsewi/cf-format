import argparse
import sys
from cf_policy import CFPolicy
from lexer import Lexer
from pretty_printer import PrettyPrinter


def main():
    config = parse_arguments()

    for filename in config.file:
        lexer = Lexer(filename, config.debug == "lexer")
        tokens = lexer.tokenize()
        policy = CFPolicy.parse(tokens, config.debug == "parser")

        pp = PrettyPrinter(config.debug == "printer")
        policy.pretty_print(pp)

        if config.debug == "printer":
            output = pp.__str__().replace(" ", "·")
            print(output)

        # TODO: Write result to output file


def parse_arguments():
    arg_parser = argparse.ArgumentParser(
        description="Simple CFEngine policy formatting tool", epilog="Jeez Louise ...",
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
