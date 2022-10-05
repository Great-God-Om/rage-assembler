from typing import Callable, Union

# Formatters are functions that convert an instruction into another format be it binary or something else


# Instruction Type Formatters
def r_type(opcode: int, rd: int, rs1: int, rs2: int) -> str:
    return "{3:04b} {2:04b} {1:04b} {0:04b}".format(opcode, rd, rs1, rs2)


def m_type(opcode: int, rd: int, rs1: int, imm: int) -> str:
    return "{3:04b} {2:04b} {1:04b} {1:04b}".format(opcode, rd, rs1, imm)


def i_type(opcode: int, rd: int, imm: int) -> str:
    return "{2:08b} {1:04b} {0:04b}".format(opcode, rd, imm)


def l_type(opcode: int, imm: int) -> str:
    return "{1:012b} {0:04b}".format(opcode, imm)


# Pseudo-Instruction Formatters
def li(rs1: str, imm: str, *args) -> list[str]:
    immi: int = int(imm, 0)  # converting hex str to int
    return [
        "lui {0} 0x{1:x}".format(
            rs1,
            (
                (
                    ((immi & (0xFF << 8)) >> 8)
                    + (0x1 if ((immi & 0x1 << 7) >> 7) else 0x0)
                )
            ).to_bytes(2, "little")[0],
        ),
        "addi {0} 0x{1:x}".format(rs1, immi & 0xFF),
    ]


def call(label: str) -> list[str]:
    return li(rs1="ua2", imm=label) + [
        "swp ra ua2 pc",
    ]


def jump(label: str) -> None:
    pass


Formatter = Callable[..., Union[str, list[str]]]
