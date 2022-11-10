def memfile(binout: bool):
    def write(binary: list[str]):
        with open("mem.txt", "w") as mem:
            for line in binary:
                if not binout:
                    mem.write("{0:>04}\n".format(hex(int(line, 2)).upper()[2:]))
                else:
                    mem.write(f"{line}\n")

    return write
