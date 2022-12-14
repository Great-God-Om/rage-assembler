# TODO: Implement import from other files


from assemble.formatters import Formatter, li
from assemble.instructions import (
    COMP_OPS,
    CORE_INSTRUCTIONS_FORMATS,
    CORE_INSTRUCTIONS_OPS,
)
from assemble.outputters import Outputter
from assemble.preprocessor import preprocess
from assemble.pseudoinstructions import PSEUDO_INSTRUCTIONS
from hardware_definitions.registers import REGISTERS

ARG_DELIM: str = " "

labels: dict[str, int] = {}
references: dict[str, list[int]] = {}


def assemble(ifile: str, outputter: Outputter) -> None:
    def remove_comment(line: str) -> str:
        comloc: int = line.find("//")
        return line[:comloc].strip() if comloc != -1 else line

    # Read input file
    with open(ifile, "r") as source:
        asm = filter(
            lambda x: x != "",
            map(
                lambda line: line.strip().replace("\n", "").replace("\t", ""),
                source.readlines(),
            ),
        )
    asm: list[str] = list(map(remove_comment, preprocess(list(asm))))
    expanded_asm: list[str] = expand_pseudo_instructions(asm)
    full_asm: list[str] = update_instruction_addresses(
        list(filter(lambda l: l[:-1] not in labels, expanded_asm))
    )
    binary: list[str] = to_machine_code(full_asm)
    outputter(binary)


def expand_pseudo_instructions(asm) -> list[str]:
    # Expand instruction and merge with the current line
    def expand_and_merge(asm, line, op, *args) -> tuple[list[str], int]:
        formatter: Formatter = PSEUDO_INSTRUCTIONS[op]
        formatted_instr = formatter(*args)
        return (asm[0:line] + formatted_instr + asm[line + 1 :], len(formatted_instr))

    expanded_asm = list(asm)
    current_line: int = 0
    for instr in expanded_asm:
        op, *rest = instr.split(" ")
        if op in PSEUDO_INSTRUCTIONS:
            # PSEUDO INSTRUCTION
            if op == "call":
                # References need to be updated and dummy address provided
                label: str = rest[0]
                references.update({label: references.get(label, []) + [current_line]})
                rest: list[str] = ["0x00"]
            elif op == "jump":
                label: str = rest[0]
                references.update({label: references.get(label, []) + [current_line]})
                rest = ["0x00"]
            if op == "swp" and len(rest) > 2:
                # this is shit but
                current_line += 1
                continue
            a: tuple[list[str], int] = expand_and_merge(
                expanded_asm, current_line + len(labels), op, *rest
            )
            expanded_asm: list[str] = a[0]
            current_line += a[1] - 1
        elif op not in CORE_INSTRUCTIONS_OPS and "." in op:
            # is a label Definition
            label = op[:-1]
            labels.update({label: current_line})
            continue
        current_line += 1
    return expanded_asm


def update_instruction_addresses(asm: list[str]) -> list[str]:
    for label in references:
        for ref in references[label]:
            # There might exist a better way to do this but I can't think of anything rn
            op, arg, last = asm[ref].split(" ")
            asm = asm[:ref] + li(arg, str(labels[label])) + asm[ref + 2 :]
    return asm


def to_machine_code(asm: list[str]) -> list[str]:
    out = []
    for number, line in enumerate(asm):
        print(f"Evaluating line {number}: {line}")
        op, *args = line.split(" ")
        if op.replace(":", "") in labels:
            continue
        formatter: Formatter = CORE_INSTRUCTIONS_FORMATS[op]
        if op == "cmp":
            out.append(
                formatter(
                    CORE_INSTRUCTIONS_OPS[op],
                    *[
                        REGISTERS[args[2]],
                        REGISTERS[args[0]],
                        COMP_OPS[args[1].upper()],
                    ],
                )
            )
        elif op == "brc":
            out.append(
                formatter(
                    CORE_INSTRUCTIONS_OPS[op],
                    *[2 * (labels[args[0]] - number)],
                )
            )
        elif op == "lw" or op == "sw":
            imm, rs1 = args[1].split("(")
            out.append(
                formatter(
                    CORE_INSTRUCTIONS_OPS[op],
                    REGISTERS[args[0]],
                    REGISTERS[rs1[:-1]],
                    int(imm),
                )
            )
        else:
            out.append(
                formatter(
                    CORE_INSTRUCTIONS_OPS[op],
                    *list(
                        map(
                            lambda x: REGISTERS[x] if x in REGISTERS else int(x, 0),
                            args,
                        )
                    ),
                )
            )
    return out
