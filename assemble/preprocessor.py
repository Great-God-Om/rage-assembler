def preprocess(asm) -> list[str]:
    new_asm: list[str] = []
    for num, line in enumerate(asm):
        if "#include" in line:
            a: list[str] = line.split(" ")
            print(a)
    return asm
