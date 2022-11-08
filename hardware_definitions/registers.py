# Register to ID mapping
REGISTERS: dict[str, int] = {
    # General Purpose Registers
    "zero": 0,
    "x0": 0,
    "ra": 1,
    "sp": 2,
    "t0": 3,
    "t1": 4,
    "t2": 5,
    "t3": 6,
    "s0": 7,
    "s1": 8,
    "s2": 9,
    "s3": 10,
    "a0": 11,
    "a1": 12,
    "ua0": 13,
    "ua1": 14,
    "ua2": 15,
    # Special Registers
    "pc": 0,
    "esc": 1,
    "era": 2,
    "eca": 3,
}
