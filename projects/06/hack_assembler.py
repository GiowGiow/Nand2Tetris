from typing import Dict, List, Set

from a_instruction import generate_A_instruction_in_binary, is_A_instruction, is_label
from assembly_utils import (
    get_labels_and_variables,
    parse_asm_file_from_argument,
    read_assembly_file,
    write_to_output,
)
from c_instruction import generate_C_instruction_in_binary


def convert_to_binary(
    assembly_lines: List[str],
    labels: Set[str],
    label_to_index: Dict[str, int],
    var_to_index: Dict[str, int],
) -> List[str]:
    """Translate from Hack assembly code to binary"""
    result_bin_code = []
    for assembly_line in assembly_lines:
        instruction_in_binary = []

        if A_instruction := is_A_instruction(assembly_line):
            A_instruction_in_binary = generate_A_instruction_in_binary(
                A_instruction, labels, label_to_index, var_to_index
            )
            instruction_in_binary.append(A_instruction_in_binary)
        elif is_label(assembly_line):
            continue
        else:
            C_instruction_in_binary = generate_C_instruction_in_binary(assembly_line)
            instruction_in_binary.append(C_instruction_in_binary)

        result_bin_code.append(
            "".join([instruction for instruction in instruction_in_binary])
        )

    return result_bin_code


if __name__ == "__main__":
    file_name = parse_asm_file_from_argument()
    file_lines = []

    print("Loading File")
    with open(file_name, "r") as file:
        file_lines = read_assembly_file(file)

    labels, var_to_index, label_to_index = get_labels_and_variables(file_lines)
    bin_code = convert_to_binary(file_lines, labels, label_to_index, var_to_index)

    write_to_output(file_name, bin_code)
