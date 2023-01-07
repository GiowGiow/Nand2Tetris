import re
from typing import Dict, Literal, Set, Union

from assembler_constants import (
    BIN_CODES,
    COMMON_REGISTERS,
    PATTERNS,
    SPECIAL_SYMBOL_ADDRESS,
    SPECIAL_SYMBOL_PATTERN,
)


def generate_A_instruction_in_binary(
    A_instruction_without_at_sign: str,
    labels: Set,
    label_to_index: Dict[str, int],
    var_to_index: Dict[str, int],
) -> str:
    binary_instruction = ""
    if special_symbol := is_special_symbol(A_instruction_without_at_sign):
        binary_instruction = convert_int_to_15_bit_bin_str(
            SPECIAL_SYMBOL_ADDRESS[special_symbol]
        )
    elif is_numeric_address(A_instruction_without_at_sign):
        binary_instruction = convert_int_to_15_bit_bin_str(
            int(A_instruction_without_at_sign)
        )
    elif register_match := is_special_register(A_instruction_without_at_sign):
        binary_instruction = convert_int_to_15_bit_bin_str(int(register_match))
    elif A_instruction_without_at_sign in labels:
        binary_instruction = convert_int_to_15_bit_bin_str(
            label_to_index[A_instruction_without_at_sign]
        )
    else:  # is a variable
        binary_instruction = convert_int_to_15_bit_bin_str(
            COMMON_REGISTERS + var_to_index[A_instruction_without_at_sign]
        )
    return f'{BIN_CODES["A_INSTRUCTION"]}{binary_instruction}'


def convert_int_to_15_bit_bin_str(number: int) -> str:
    return "{0:015b}".format(number)


def is_numeric_address(address: str) -> bool:
    return address.isnumeric()


def is_label(line: str) -> Union[str, Literal[False]]:
    match = re.match(PATTERNS["TYPE_LABEL"], line)
    if match:
        return match.group(1)
    else:
        return False


def is_special_register(address: str) -> Union[str, Literal[False]]:
    match = re.match(PATTERNS["SPECIAL_REG"], address)
    if match:
        return match.group(1)
    else:
        return False


def is_A_instruction(command: str) -> Union[str, Literal[False]]:
    match = re.match(PATTERNS["A_INSTRUCTION"], command)
    if match:
        return match.group(1)
    else:
        return False


def is_special_symbol(address: str) -> Union[str, Literal[False]]:
    match = SPECIAL_SYMBOL_PATTERN.match(address)
    if match:
        return match.group(0)
    else:
        return False
