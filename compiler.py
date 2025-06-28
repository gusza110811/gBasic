import os
import sys
import math

class memory:
    value = {"line": 0}

def strtobool(string: str):
    return not (string.lower() == "false")

class compiler:
    ending = []
    script = []
    compilingline = 0
    variables = {}
    bytecode = []

    mainend = 0

    commands = {
        "print": 0x00,
        "dump": 0x01,
        "set": 0x02,
        "input": 0x03,
        "gotoif": 0x04,
        "load": 0x05,
        "+": 0xB0,
        "-": 0xB1,
        "*": 0xB2,
        "**": 0xB3,
        "/": 0xB4,
        "//": 0xB5,
        "%": 0xB6,
        "==": 0xC0,
        "<": 0xC1,
        ">": 0xC2,
        "||": 0xD0,
        "&&": 0xD1,
        "~~": 0xD2,
        "quit": 0xAF
    }

    def add_instruction(opcode: int, value):
        compiler.bytecode.append(opcode)
        if isinstance(value, int):
            length = math.ceil(value/((2**8)-1))
            compiler.bytecode.extend(value.to_bytes(length, byteorder="little"))
        elif isinstance(value, str):
            compiler.bytecode.extend(value.encode("ascii"))
        compiler.bytecode.append(0xFF)

    def compile_expr(expr: list[str]):
        done = False
        chunks = expr[:]
        while not done:
            for idx, token in enumerate(chunks):
                if token in compiler.commands:
                    opcode = compiler.commands[token]
                    lhs = chunks[idx - 1]
                    rhs = chunks[idx + 1]

                    if lhs.startswith("$"):
                        compiler.add_instruction(0x05, lhs[1:])
                    else:
                        compiler.add_instruction(0xA0, lhs)

                    compiler.add_instruction(opcode, rhs[1:] if rhs.startswith("$") else rhs)

                    chunks = ["$"] + chunks[idx + 2:]
                    break
            else:
                done = True
        return chunks

    def simulate_length(line: list[str]):
        initial_len = len(compiler.bytecode)
        compiler.compilelineparsed(line)
        delta = len(compiler.bytecode) - initial_len
        del compiler.bytecode[initial_len:]
        return delta

    def compilelineparsed(line: list[str]):
        if line[0] == "comment":
            compiler.bytecode.append(0xAB)
            return

        if line[0] == "print":
            args = line[1:]
            if len(args) == 1:
                chunks = compiler.compile_expr(args)
                compiler.add_instruction(0x00, chunks[0] if chunks[0] != "$" else "_")
            else:
                for word in args:
                    compiler.add_instruction(0x00, word)

        elif line[0] == "dump":
            compiler.add_instruction(0x01, "")

        elif line[0] == "gotoif":
            cond = line[1]
            if cond.startswith("$"):
                compiler.add_instruction(0x05, cond[1:])
            else:
                compiler.add_instruction(0xA0, cond)
            compiler.add_instruction(0x04, line[2])

        elif line[0] == "set":
            chunks = compiler.compile_expr(line[2:])
            compiler.add_instruction(0x02, line[1])

        elif line[0] == "input":
            prompt = " ".join(line[2:]) if len(line) > 2 else "Input >"
            compiler.add_instruction(0x03, prompt)
            compiler.add_instruction(0x02, line[1])

    def compile(lines: str):
        compiler.bytecode.clear()
        parsed = parser.parse(lines)

        # First pass to get label addresses
        labelmap = {}
        pc = 0
        for line in parsed:
            if line and line[0] == "comment" and len(line) > 1 and line[1].startswith(":"):
                labelmap[line[1][1:]] = pc
            pc += compiler.simulate_length(line)
        compiler.add_instruction(0x05, "True")
        compiler.add_instruction(0xA0, pc+10)

        # Second pass: real compilation
        for line in parsed:
            compiler.compilelineparsed(line)
        
        compiler.add_instruction(0xAF, 0)

        # Emit label header
        for label, addr in labelmap.items():
            compiler.add_instruction(0xA0, addr+10)
            compiler.add_instruction(0x02, label)

        compiler.add_instruction(0x05, "True")
        compiler.add_instruction(0xA0, 1)

        return bytes(compiler.bytecode)

class parser:
    def parse(text: str, mem=None):
        lines = text.split("\n")
        chunks: list[list[str]] = []
        for linenum, line in enumerate(lines):
            line = line.strip()
            linechunks = []
            if line == "":
                chunks.append(["comment"])
                continue

            lowchunks = line.split()
            chunkmerge = ""
            for idx, chunk in enumerate(lowchunks):
                if chunk.startswith("#"):
                    chunks.append(["comment"])
                    break

                if idx == 0:
                    if chunk.startswith("?"):
                        linechunks.append("gotoif")
                        chunk = chunk[1:]
                    elif chunk == "if":
                        linechunks.append("gotoif")
                        continue
                    if chunk.startswith(":" ):
                        linechunks.append("comment")
                        linechunks.append(chunk)
                        continue

                if chunk.startswith('"') or chunk.startswith("'"):
                    if chunk.endswith('"') or chunk.endswith("'"):
                        linechunks.append(chunk[1:-1])
                    else:
                        chunkmerge = chunk[1:]

                elif chunk.endswith('"') or chunk.endswith("'"):
                    if chunkmerge != "":
                        chunkmerge = chunkmerge + " " + chunk[:-1]
                    else:
                        chunkmerge = chunk[:-1]
                    linechunks.append(chunkmerge)
                    chunkmerge = ""
                elif chunkmerge != "":
                    chunkmerge = chunkmerge + " " + chunk
                else:
                    linechunks.append(chunk)
            if linechunks:
                chunks.append(linechunks)
        return chunks

if __name__ == "__main__":
    try:
        filename = sys.argv[1]
        with open(filename) as f:
            code = f.read()

    except IndexError:
        filename = "demo"
        code = """:loop
input user truth>
set isone $user == 1
?$isone $end
print Go
?True $loop
:end
print End
"""

    except FileNotFoundError:
        print("File not found.")
        quit(1)

    bytecode = compiler.compile(code)
    with open(filename + ".gbo", "wb") as f:
        f.write(bytecode)

    print("Compiled to", filename + ".gbo")
