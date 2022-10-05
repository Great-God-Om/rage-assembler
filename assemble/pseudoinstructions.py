# Mapping of pseudo_instructions to repective formatters.
from assemble.formatters import Formatter, call, jump, li

PSEUDO_INSTRUCTIONS: dict[str, Formatter] = {
    "li": li,
    "call": call,
    "jump": jump,
}
