def memfile(binout: bool):
    def write(binary: list[str]):
        with open("mem.txt", "w") as mem:
            for line in binary:
                if not binout:
                    mem.write(f"{hex(int(line, 2))}\n")
                else:
                    mem.write(f"{line}\n")

    return write
