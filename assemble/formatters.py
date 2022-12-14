from typing import Callable, Union

# Formatters are functions that convert an instruction into another format be it binary or something else


# Instruction Type Formatters
def r_type(opcode: int, rd: int, rs1: int, rs2: int) -> str:
    return "{3:04}{2:04b}{1:04b}{0:04b}".format(opcode, rd, rs1, rs2)


def m_type(opcode: int, rd: int, rs1: int, imm: int) -> str:
    return "{3:>04}{2:04b}{1:04b}{0:04b}".format(opcode, rd, rs1, bin(imm & 0b1111)[2:])


def i_type(opcode: int, rd: int, imm: int) -> str:
    # 0 1 2 3 4 5 6 7
    imm_str = "{0:>08}".format(bin(imm & 0b11111111)[2:])
    return "{2:>04}{3:>04}{1:04b}{0:04b}".format(opcode, rd, imm_str[4:], imm_str[0:4])


def l_type(opcode: int, imm: int) -> str:
    # 0 1 2 3 4 5 6 7 8 9 10 11
    imm_str = "{0:>012}".format(bin(imm & 0b111111111111)[2:])
    return "{1:>04}{2:>04}{3:>04}{0:04b}".format(
        opcode, imm_str[8:], imm_str[4:8], imm_str[0:4]
    )


# Pseudo-Instruction Formatters
def li(rs1: str, imm: str, *args) -> list[str]:
    try:
        immi: int = 2 * int(imm, 0)  # converting hex str to int
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
    except:
        raise Exception("Improper use of li")


def call(label: str) -> list[str]:
    return li(rs1="ra", imm=label) + [
        "swp ra ra pc",
    ]


def jump(label: str) -> list[str]:
    return ["cmp x0 TRUE x0", "brc 0x0"]


def swp(rd: str, rs1: str) -> list[str]:
    return [f"swp {rd} {rd} {rs1}"]


def noop() -> list[str]:
    return ["add zero zero zero"]


Formatter = Callable[..., Union[str, list[str]]]
