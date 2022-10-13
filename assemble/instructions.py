from assemble.formatters import Formatter, i_type, l_type, m_type, r_type

CORE_INSTRUCTIONS_FORMATS: dict[str, Formatter] = {
    "add": r_type,
    "swp": r_type,
    "and": r_type,
    "or": r_type,
    "not": r_type,
    # "jal": r_type,
    "sub": r_type,
    "addi": i_type,
    "lui": i_type,
    "lw": m_type,
    "sw": m_type,
    "cmp": m_type,
    "sl": m_type,
    "sr": m_type,
    "brc": l_type,
}
CORE_INSTRUCTIONS_OPS: dict[str, int] = {
    "add": 0,
    "addi": 1,
    "and": 2,
    "or": 3,
    "not": 4,
    "lw": 5,
    "sw": 6,
    "lui": 7,
    "cmp": 8,
    "brc": 9,
    "sub": 10,
    "sl": 11,
    "sr": 12,
    "swp": 13,
}

COMP_OPS: dict[str, int] = {
    "FALSE": 0,
    "GT": 1,
    "EQ": 2,
    "GEQ": 3,
    "LT": 4,
    "NEQ": 5,
    "LEQ": 6,
    "True": 7,
}
