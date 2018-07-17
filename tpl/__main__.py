import sys


from . import main


def _argv_wrapper():
    return main(*sys.argv)


if __name__ == "__main__":
    sys.exit(main(*sys.argv))
