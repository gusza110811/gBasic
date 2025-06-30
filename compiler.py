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
    labelmap = {}

    mainend = 0

    commands = {
        "print": 0x00,
        "dump": 0x01,
        "set": 0x02,
        "input": 0x03,
        "gotoif": 0x04,
        "jump": 0x05,
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
        "read": 0xE0,
        "write": 0xE1,
        "awrite":0xE2,
        "quit": 0xAF,
        "load": 0xA5,
    }

    def add_instruction(opcode: int, value:str=None):
        compiler.bytecode.append(opcode)
        if isinstance(value, int):
            try:
                length = math.ceil((math.floor(math.log2(value))+1)/8)
            except ValueError:
                length = 1
            compiler.bytecode.extend(length.to_bytes(1))
            compiler.bytecode.extend(value.to_bytes(length, byteorder="big"))
        elif isinstance(value, str):
            compiler.bytecode.extend(value.encode("ascii"))
        compiler.bytecode.append(0xFF)

    def compile_expr(expr: list[str]):
        done = False
        chunks = expr
        while not done:
            for idx, token in enumerate(chunks):
                if token in compiler.commands:
                    opcode = compiler.commands[token]
                    lhs = chunks[idx - 1]

                    if lhs.startswith("$"):
                        compiler.add_instruction(0xA5, lhs[1:])
                    else:
                        compiler.add_instruction(0xA0, lhs)
                    
                    try:
                        rhs = chunks[idx + 1]
                        compiler.add_instruction(opcode, rhs[1:] if rhs.startswith("$") else rhs)
                    except IndexError:
                        pass

                    chunks = chunks[idx + 2:]
                    break
            else:
                done = True
        return chunks

    def simulate_length(line: list[str],linen):
        initial_len = len(compiler.bytecode)
        compiler.compilelineparsed(line,linen)
        delta = len(compiler.bytecode) - initial_len
        del compiler.bytecode[initial_len:]
        return delta

    def compilelineparsed(line: list[str],linenumber:int):
        if line[0] == "comment":
            return

        if line[0] == "print":
            args = line[1:]
            for idx,word in enumerate(args):
                if word.startswith("$"):
                    compiler.add_instruction(0xA0,word[1:])
                else:
                    compiler.add_instruction(0xA0,word)
                
                compiler.add_instruction(0x00, "")

                if idx < (len(args)-1):
                    compiler.add_instruction(0xA0," ")
                    compiler.add_instruction(0x00)
            compiler.add_instruction(0xA0,"\n")
            compiler.add_instruction(0x00,"")
        
        elif line[0] == "clean":
            compiler.add_instruction(0xA0,128)
            compiler.add_instruction(0x00)

        elif line[0] == "dump":
            compiler.add_instruction(0x01, "0")

        elif line[0] == "gotoif":
            cond = line[1]
            if cond.startswith("$"):
                compiler.add_instruction(0xA5, cond[1:])
            else:
                compiler.add_instruction(0xA0, cond)
            try:
                label = compiler.labelmap[line[2][1:]]
            except KeyError:
                label = None
            compiler.add_instruction(0x04, label)
        
        elif line[0] == "jump":
            try:
                label = compiler.labelmap[line[1][1:]]
            except KeyError:
                label = None
            compiler.add_instruction(0x05, label)

        elif line[0] == "set":
            compiler.compile_expr(line[2:])
            compiler.add_instruction(0x02, line[1])

        elif line[0] == "input":
            prompt = " ".join(line[2:]) if len(line) > 2 else "Input >"
            compiler.add_instruction(0x03, prompt)
            compiler.add_instruction(0x02, line[1])
        
        elif line[0] == "read":
            compiler.add_instruction(0xE0,line[1])
            compiler.add_instruction(0x02," ".join(line[2:]))
        
        elif line[0] == "write":
            compiler.add_instruction(0xA0," ".join(line[2:]))
            compiler.add_instruction(0xE1,line[1])

        elif line[0] == "awrite":
            compiler.add_instruction(0xA0," ".join(line[2:]))
            compiler.add_instruction(0xE2,line[1])
        
        elif line[0] == "blank":
            length = math.ceil(int(line[1])/2)
            compiler.add_instruction(0xAB,"0"*(length-2))

    def compile(lines: str):
        compiler.bytecode.clear()
        parsed = parser.parse(lines)

        # First pass to get label addresses
        compiler.labelmap = {}
        pc = 0
        for line in parsed:
            if line and line[0] == "comment" and len(line) > 1 and line[1].startswith(":"):
                compiler.labelmap[line[1][1:]] = pc
            else:
                pc += compiler.simulate_length(line,pc)

        # Second pass: real compilation
        for idx, line in enumerate(parsed):
            compiler.compilelineparsed(line,idx)

        compiler.add_instruction(0xAF, '0')

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
        with open(f"{filename}.gb") as f:
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
dump
"""

    except FileNotFoundError:
        print("File not found.")
        quit(1)

    bytecode = compiler.compile(code)
    with open(filename + ".gbc", "wb") as f:
        f.write(bytecode)

    print("Compiled to", filename + ".gbc")
