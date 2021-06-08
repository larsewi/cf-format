import argparse
from error import exit_success
from lexer import Lexer


def main():
    config = parse_arguments()

    for filename in config.file:
        tokens = Lexer.tokenize_file(filename)
        if config.debug == "lexer":
            for token in tokens:
                print(token)
            exit_success()


def parse_arguments():
    arg_parser = argparse.ArgumentParser(
        description="Simple CFEngine policy formatting tool", epilog="Jeez Louise ...",
    )
    arg_parser.add_argument(
        "-d", "--debug", choices=["lexer", "parser"], help="enable debug mode"
    )
    arg_parser.add_argument(
        "file", help="path to input files", type=str, nargs="*"
    )
    return arg_parser.parse_args()


if __name__ == "__main__":
    main()
