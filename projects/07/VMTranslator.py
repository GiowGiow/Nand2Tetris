"""Translates VM code into Hack assembly code."""
import argparse
from pathlib import Path
from typing import List, TextIO


def read_file(f: TextIO) -> List[str]:
    """Read file and return a list of lines.

    Ignores commented and empty lines and only returns lines of code containing.
    """
    file_lines = []
    for line in f.readlines():
        line = line.strip()
        if line.startswith("//") or not line:
            continue
        else:
            file_lines.append(line)
    return file_lines


def parse_file_name_from_argument() -> str:
    """Parse the file name from the command line arguments."""
    parser = argparse.ArgumentParser(
        prog="VM File",
        description="VM File to translate",
    )

    parser.add_argument("asm_file")
    args = parser.parse_args()

    file_name = args.asm_file
    return file_name


def write_to_output(file_name: str, assembly_code: str) -> None:
    """Write the assembly code to a file.

    The file is written with the same name as the input file but ending suffix of .asm.
    """
    assembly_file = Path(file_name).with_suffix(".asm")
    print(f"Output file: {assembly_file}")
    with open(assembly_file, "w") as f:
        f.write(assembly_code)


STACK_START = 256
GENERAL_PURPOSE_REG = 13


def join_commands(commands: List[str]) -> str:
    """Join a list of commands into a single string."""
    return "\n".join(commands) + "\n"


def get_push_constant_asm(tokens: List[str]) -> str:
    """Get the assembly code for the push constant command."""
    asm_commands = [
        f"@{tokens[2]}",
        "D=A",  # Guardamo o {num}
        "@SP",
        "A=M",  # Tamo no final da stack
        "M=D",  # Colocamo o {num} no FINAL da stack
        "@SP",
        "M=M+1",  # Incrementamos o ponteiro
    ]
    return join_commands(asm_commands)


def get_add_asm() -> str:
    """Get the assembly code for the add command."""
    asm_commands = [
        "@SP",
        "AM=M-1",  # Decrementa um no ponteiro & Seta o novo endereco
        "D=M",  # Salva o valor em D
        f"@R{GENERAL_PURPOSE_REG}",
        "M=D",  # GEN_P_REG guarda o valor agr
        "@SP",
        "AM=M-1",
        "D=M",  # Pega o outro valor da stack e salva em D
        f"@R{GENERAL_PURPOSE_REG}",
        "M=M+D",  # Soma os numeros
        "D=M",  # Salva a soma em D
        "@SP",
        "A=M",  # Vai pra addr da stack
        "M=D",  # Joga a soma la
        "@SP",
        "M=M+1",  # Incrementa o addr da stack
    ]
    return join_commands(asm_commands)


def get_start_code_asm() -> str:
    """Get the assembly code for the start of the program.

    RAM[0] = 256
    """
    return join_commands([f"@{STACK_START}", "D=A", "@SP", "M=D"])


if __name__ == "__main__":
    file_name = parse_file_name_from_argument()
    file_lines = []

    with open(file_name) as f:
        file_lines = read_file(f)

    assembly_code = []
    assembly_code.append(get_start_code_asm())
    for line in file_lines:
        tokens = line.split(" ")

        if tokens[0] == "push":
            if tokens[1] == "constant":
                assembly_code.append(get_push_constant_asm(tokens))
        if tokens[0] == "add":
            assembly_code.append(get_add_asm())

    assembly_code_as_str = "".join(assembly_code)

    write_to_output(file_name, assembly_code_as_str)
