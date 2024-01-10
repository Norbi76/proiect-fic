from typing import Dict, List
from pprint import pprint

class Assembler:
    MACHINE_CODE_LINE_LEN: int = 16
    REGISTERS: Dict[str, str] = {
        "X": "000",
        "Y": "001",
        "ACC": "010"
    }
    INSTRUCTION_OPCODES: Dict[str, str] = {
        # R-format
        "ADD": "000",
        # I-format
        "LW": "100",
        "SW": "101",
        "BEQ": "110",
        "ADDI": "111",
        "SLI": "001",
        # J-format
        "J": "010",
        "JAL": "011"
    }
    INSTRUCTION_FORMATS: Dict[str, str] = {
        # R-format
        "ADD": "R",
        # I-format
        "LW": "I",
        "SW": "I",
        "BEQ": "I",
        "ADDI": "I",
        "SLI": "I",
        # J-format
        "J": "J",
        "JAL": "J"
    }

    def remove_comments_and_extra_whitespace(self, asm_lines: List[str]) -> List[str]:
        for line_idx, line in enumerate(asm_lines):
            # Clear comments
            comment_start: int = line.find("#")
            if comment_start != -1:
                line = line[:comment_start]
            # Clear extra whitespace
            asm_lines[line_idx] = line.strip()
        return asm_lines

    def remove_empty_lines(self, asm_lines: List[str]) -> List[str]:
        return [line for line in asm_lines if line]

    def get_label_positions(self, asm_lines: List[str]) -> Dict[str, int]:
        """
        Call this after clearing extra whitespace (or at least run an lstrip on the line)
        Also removes labels form lines (they get put in the returned dict)
        """
        labels_and_positions: Dict[str, int] = {}
        for line_idx, line in enumerate(asm_lines):
            colon_position: int = line.find(":")
            if colon_position == -1:
                continue
            # Make sure colon is not first char of the line
            if colon_position == 0:
                raise ValueError("Colon found at index 0. Invalid ASM code.")
            # Nor the last one
            if colon_position == len(line) - 1:
                raise ValueError("Colon found at end of line. Invalid ASM code.")
            # Get label
            label: str = line[:colon_position]
            # Check if label with same name already exists
            if labels_and_positions.get(label):
                raise ValueError(f"Found already defined label {label}. Invalid ASM code.")
            # Place label in dict
            labels_and_positions[label] = line_idx
            # Remove label from ASM line
            asm_lines[line_idx] = line[colon_position + 1:].lstrip()
            #pprint(f"Found label \"{label}\" at line {line_idx + 1}.")
        #pprint("Found labels (with line indexes):")
        #pprint(labels_and_positions)
        return labels_and_positions

    def get_words_from_line(self, line: str) -> List[str]:
        return [word.strip() for word in line.replace(",", " ").split()]

    def assemble(self, asm_code: str) -> List[str]:
        # Get a list of every asm code line
        asm_lines: List[str] = asm_code.split("\n")
        asm_lines = self.remove_comments_and_extra_whitespace(asm_lines)
        # Clear all empty lines
        asm_lines = self.remove_empty_lines(asm_lines)
        # Get labels and their positions
        labels_and_positions: Dict[str, int] = self.get_label_positions(asm_lines)
        machine_code_lines: List[str] = []
        # Do the actual assembling, by instruction format
        for line in asm_lines:
            line_content: List[str] = self.get_words_from_line(line)
            op: str = line_content[0]
            machine_code_line: str = Assembler.INSTRUCTION_OPCODES[op]
            #pprint(f"Found {op}.")
            if Assembler.INSTRUCTION_FORMATS[op] == "R":
                if len(line_content) != 4:
                    raise ValueError("R instruction does not have 3 arguments. Invalid ASM code.")
                machine_code_line += Assembler.REGISTERS[line_content[1]] # RS
                machine_code_line += Assembler.REGISTERS[line_content[2]] # RT
                machine_code_line += Assembler.REGISTERS[line_content[3]] # RD
                machine_code_line += "0000" # FUNCT
            elif Assembler.INSTRUCTION_FORMATS[op] == "I":
                # This does not respect the spec sheet because it's stupid
                if len(line_content) != 3:
                    raise ValueError("I instruction does not have 2 arguments. Invalid ASM code.")
                machine_code_line += Assembler.REGISTERS[line_content[1]] # RS
                try: # Try to add an
                    machine_code_line += bin(int(line_content[2]))[2:] # Immediate value
                except ValueError: # And if that does not work, add the
                    machine_code_line += Assembler.REGISTERS[line_content[2]] # Address
            else: # J
                if len(line_content) != 2:
                    raise ValueError("J instruction does not have 1 argument. Invalid ASM code.")
                machine_code_line += bin(labels_and_positions[line_content[1]])[2:]
            # Add 0 bits filler bits where necessary
            machine_code_line = machine_code_line.ljust(Assembler.MACHINE_CODE_LINE_LEN, "0")
            # Append the new macine code line to the machine code lines list
            machine_code_lines.append(machine_code_line)
        return machine_code_lines

def main() -> None:
    assembler: Assembler = Assembler()
    asm_code = """
        # START: ACC=0, X=0, Y=0, data memory is empty
        ADDI X, 1		# X val to store
        SW X, ACC		# store X at Mem[0]

        ADDI Y, 2		# Y val to store
        ADDI ACC, 2		# ACC=2
        SW Y, ACC		# store Y at Mem[2]

        ADD X, Y, X		# X = X + Y, set FLAGS
        J L1			# any other comment?

        ADDI ACC, 4		# ACC=4
        SW Y, ACC		# store Y at Mem[4]
        J L2			# goto L2

        L1:	ADD ACC, ACC, ACC	# ACC * 2
        LW X, ACC		# load Mem[0] in X (restore old)
        ADDI ACC, 4		# ACC=4
        SW X, ACC		# store X at Mem[4]

        L2:	JAL L2			# goto L2 (infinite loop)
        """
    machine_code: List[str] = assembler.assemble(asm_code)
    pprint(machine_code)
    return

if __name__ == "__main__":
    main()