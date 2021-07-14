import sys


def exit_success():
    sys.exit(0)


def exit_failure():
    sys.exit(1)


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def panic(*args, **kwargs):
    eprint("PANIC!")
    eprint(*args, **kwargs)
    exit_failure()
