from sys import argv

from assemble.assembler import assemble
from assemble.outputters.memfile import memfile
from assemble.outputters.stdout import consoleout


def main() -> None:
    input_file: str = argv[1]
    if "-" in argv:
        assemble(input_file, consoleout)
    if "--bin" in argv:
        assemble(input_file, memfile(True))
    if "--hex" in argv:
        assemble(input_file, memfile(False))


if __name__ == "__main__":
    main()
