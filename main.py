from sys import argv

from assemble.assembler import assemble
from assemble.outputters.memfile import memfile
from assemble.outputters.stdout import consoleout


def main() -> None:

    if len(argv) < 1 or "--help" in argv or "-h" in argv:
        print(
            "Usage: command [input file] [--help| - | --bin | --hex]\n -: for console output \n --bin: for binary output to a new file called mem.txt\n --hex: for hex valued output to a new file called mem.txt\n"
        )
        return
    input_file: str = argv[1]
    if "-" in argv:
        assemble(input_file, consoleout)
    if "--bin" in argv:
        assemble(input_file, memfile(True))
    if "--hex" in argv:
        assemble(input_file, memfile(False))


if __name__ == "__main__":
    main()
