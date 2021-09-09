from os import write
from sys import stderr
from pretty import Pretty

class SyntaxErrorException(Exception):
    pass

def format(tokens):
    pretty = Pretty()
    f_policy(tokens, pretty)
    return pretty.__str__()

def f_policy(tokens, pretty):
    while tokens:
        token = tokens[0]
        if token.type == "BUNDLE":
            f_bundle_block(tokens, pretty)
        elif token.type == "BODY":
            f_body_block(tokens, pretty)
        elif token.type == "PROMISE":
            f_promise_block(tokens, pretty)
        elif token.type == "COMMENT":
            pretty.print(tokens.pop(0).value)
        elif token.type == "MACRO":
            pretty.print(tokens.pop(0).value)
        else:
            break
            msg = "Expected bundle, body or promise, found '%s'" % token.value
            raise SyntaxErrorException(msg)
        pretty.println()

def f_bundle_block(tokens, pretty):
    stash = []

    # pretty print bundle
    pretty.print(tokens.pop(0).value)

    # pretty print macros, stash comments
    while tokens and tokens[0].type in ("COMMENT", "MACRO"):
        if tokens[0].type == "COMMENT":
            stash.append(tokens.pop[0])
        else:
            pretty.println()
            pretty.print_no_indent(tokens[0].value)
            pretty.println()


def f_body_block(tokens, pretty):
    pass

def f_promise_block(tokens, pretty):
    pass
