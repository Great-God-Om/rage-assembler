# TODO: Implement lw and storeword

from typing import Iterable

from hardware_definitions.registers import REGISTERS

from assemble.formatters import Formatter, li
from assemble.instructions import (
    COMP_OPS,
    CORE_INSTRUCTIONS_FORMATS,
    CORE_INSTRUCTIONS_OPS,
)
from assemble.outputters import Outputter
from assemble.pseudoinstructions import PSEUDO_INSTRUCTIONS

ARG_DELIM: str = " "

labels: dict[str, int] = {}
references: dict[str, list[int]] = {}


def assemble(ifile: str, outputter: Outputter) -> None:
    def remove_comment(line: str) -> str:
        comloc = line.find("//")
        return line[:comloc].strip() if comloc != -1 else line

    # Read input file
    with open(ifile, "r") as source:
        asm = filter(
            lambda x: x != "",
            map(
                lambda line: line.replace("\n", "").replace("\t", ""),
                source.readlines(),
            ),
        )
    asm = map(remove_comment, asm)
    expanded_asm: list[str] = expand_pseudo_instructions(asm)
    full_asm: list[str] = update_instruction_addresses(expanded_asm)
    binary = to_machine_code(full_asm)
    outputter(binary)


def expand_pseudo_instructions(asm: Iterable) -> list[str]:
    # Expand instruction and merge with the current line
    def expand_and_merge(asm, line, op, *args) -> tuple[list[str], int]:
        formatter: Formatter = PSEUDO_INSTRUCTIONS[op]
        formatted_instr = formatter(*args)
        return (asm[0:line] + formatted_instr + asm[line + 1 :], len(formatted_instr))

    expanded_asm = list(asm)
    current_line: int = 0
    for instr in expanded_asm:
        print(f"Currently Evaluating: {current_line} {instr}")
        op, *rest = instr.split(" ")
        if op in PSEUDO_INSTRUCTIONS:
            # PSEUDO INSTRUCTION
            if op == "call":
                # References need to be updated and dummy address provided
                label: str = rest[0]
                references.update({label: references.get(label, []) + [current_line]})
                rest = ["0x00"]
            elif op == "jump":
                label: str = rest[0]
                references.update(
                    {label: references.get(label, []) + [current_line + 1]}
                )
                rest = ["0x00"]
            a: tuple[list[str], int] = expand_and_merge(
                expanded_asm, current_line, op, *rest
            )
            expanded_asm: list[str] = a[0]
            current_line += a[1] - 1
        elif op not in CORE_INSTRUCTIONS_OPS:
            # is a label Definition
            label = op[:-1]
            labels.update({label: current_line})
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
        op, *args = line.split(" ")
        if op.replace(":", "") in labels:
            continue
        formatter = CORE_INSTRUCTIONS_FORMATS[op]
        if op == "cmp":
            out.append(
                formatter(
                    CORE_INSTRUCTIONS_OPS[op],
                    *[REGISTERS[args[0]], REGISTERS[args[2]], COMP_OPS[args[1]]],
                )
            )
        elif op == "brc":
            print(labels[args[0]] - number)
            out.append(
                formatter(
                    CORE_INSTRUCTIONS_OPS[op],
                    *[labels[args[0]] - number],
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
