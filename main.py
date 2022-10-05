from sys import argv

from assemble.assembler import assemble
from assemble.outputters.stdout import consoleout


def main():
    input_file: str = argv[1]
    assemble(input_file, consoleout)


if __name__ == "__main__":
    main()
