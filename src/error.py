import sys


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def exit_success():
    sys.exit(0)


def exit_failure():
    sys.exit(1)
