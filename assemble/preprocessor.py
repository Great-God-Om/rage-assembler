def preprocess(asm: list[str]) -> list[str]:
    new_asm: list[str] = asm
    for line, item in filter(lambda x: "#" in x[1], enumerate(asm)):
        directive, arg = item.split(" ")
        if directive == "#inline":
            with open(arg.replace('"', ""), "r") as module:
                new_asm = (
                    new_asm[:line]
                    + list(
                        filter(
                            lambda x: x != "",
                            map(
                                lambda line: line.strip()
                                .replace("\n", "")
                                .replace("\t", ""),
                                module.readlines(),
                            ),
                        )
                    )
                    + new_asm[line + 1 :]
                )
    return new_asm
