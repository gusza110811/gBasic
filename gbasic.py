import os
import sys

class memory:
    value = {"line":0,"n":"\n"}

def strtobool(string:str):
    return not (string.lower()=="false")

class commands:

    def comment(text):return

    def print(text:list[str]=[""]):
        for _, word in enumerate(text):
            print(word, end="")
            
            if _ != len(text)-1:
                print(end=" ")
        print()

        return
    
    def dump(text):
        length = max(map(len, memory.value))
        for idx, item in enumerate(memory.value):
            print(f"{item.ljust(length," ")} : {memory.value[item]}")
    
    def set(text:list[str]):
        key = text[0]
        value = " ".join(text[1:])

        memory.value[key] = value

        return
    
    def input(text:list[str]):
        key = text[0]
        message = " ".join(text[1:])
        if message == "":
            message = "Input >"

        memory.value[key] = input(message)

        return
    
    def clean(text:list[str]):
        if os.name == "nt":
            os.system("cls")
        else:
            os.system("clear")
    
    def gotoif(text:list[str]):
        condition = text[0]
        line = text[1]

        if strtobool(condition): memory.value["line"] = int(line)

        return
    
    def jump(text:list[str]):
        line = text[0]
        memory.value["line"] = int(line)
        return
    
    def read(text:list[str]):
        filename = text[0]
        key = text[1]
        try:
            with open(filename,"r") as file:
                memory.value[key] = file.read()
        except FileNotFoundError:
            return
    
    def write(text:list[str]):
        filename = text[0]
        value = " ".join(text[1:])
        with open(filename,"w") as file:
            file.write(value)

    def awrite(text:list[str]):
        filename = text[0]
        value = " ".join(text[1:])
        with open(filename,"a") as file:
            file.write(value)

class parser:
    def parse(text:str, mem=None):
        if mem:
            memory.value = mem

        lines = text.split("\n")

        chunks:list[list[str]] = []
        # parse each line
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
                    if chunk.startswith(":"):
                        memory.value[chunk[1:]] = linenum
                        linechunks.append("comment")
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
            chunks.append(linechunks)

        return chunks

    def variableparser(linechunks:list):
        if not linechunks: return linechunks

        if linechunks[0] == "comment": return linechunks

        linechunks = linechunks.copy()

        # replace variables with their value
        for index, chunk in enumerate(linechunks):
            if chunk.startswith("$"):
                linechunks[index] = memory.value[linechunks[index][1:]]
        return linechunks

    def calculationparser(chunks:list):
        if not chunks: return chunks

        if chunks[0] == "comment": return chunks

        chunks = chunks.copy()

        # do calculations (no specific orders)
        done = False
        while not done:
            for idx, chunk in enumerate(chunks):
                # algebra
                try:
                    if chunk == "+":
                        chunks[idx] = str(float(chunks[idx-1]) + float(chunks[idx+1]))
                        chunks.pop(idx-1)
                        chunks.pop(idx)
                        break
                    elif chunk == "-":
                        chunks[idx] = str(float(chunks[idx-1]) - float(chunks[idx+1]))
                        chunks.pop(idx-1)
                        chunks.pop(idx)
                        break
                    elif chunk == "*":
                        chunks[idx] = str(float(chunks[idx-1]) * float(chunks[idx+1]))
                        chunks.pop(idx-1)
                        chunks.pop(idx)
                        break
                    elif chunk == "**":
                        chunks[idx] = str(float(chunks[idx-1]) ** float(chunks[idx+1]))
                        chunks.pop(idx-1)
                        chunks.pop(idx)
                        break
                    elif chunk == "/":
                        chunks[idx] = str(float(chunks[idx-1]) / float(chunks[idx+1]))
                        chunks.pop(idx-1)
                        chunks.pop(idx)
                        break
                    elif chunk == "//":
                        chunks[idx] = str(float(chunks[idx-1]) // float(chunks[idx+1]))
                        chunks.pop(idx-1)
                        chunks.pop(idx)
                        break
                    elif chunk == "%":
                        chunks[idx] = str(float(chunks[idx-1]) % float(chunks[idx+1]))
                        chunks.pop(idx-1)
                        chunks.pop(idx)
                        break
                except ValueError:
                    return "Type error: You must use Number"
                
                # conditional
                if chunk == "==":
                    try:
                        chunks[idx] = str(float(chunks[idx-1]) == float(chunks[idx+1]))
                    except ValueError:
                        chunks[idx] = str(chunks[idx-1] == chunks[idx+1])
                    chunks.pop(idx-1)
                    chunks.pop(idx)
                    break
                try:
                    if chunk == "<":
                        chunks[idx] = str(float(chunks[idx-1]) < float(chunks[idx+1]))
                        chunks.pop(idx-1)
                        chunks.pop(idx)
                        break
                    elif chunk == ">":
                        chunks[idx] = str(float(chunks[idx-1]) > float(chunks[idx+1]))
                        chunks.pop(idx-1)
                        chunks.pop(idx)
                        break
                except ValueError:
                    return "Type error: You must use Number"
                
                # boolean algebra
                if chunk == "||":
                    chunks[idx] = str(strtobool(chunks[idx-1]) | strtobool(chunks[idx+1]))
                    chunks.pop(idx-1)
                    chunks.pop(idx)
                    break
                elif chunk == "&&":
                    chunks[idx] = str(strtobool(chunks[idx-1]) & strtobool(chunks[idx+1]))
                    chunks.pop(idx-1)
                    chunks.pop(idx)
                    break
                elif chunk == "~~":
                    chunks[idx] = str(not strtobool(chunks[idx+1]))
                    chunks.pop(idx+1)
                    break
            else:
                done = True
        return chunks

def executeline(line:list[str], mem:list[str]=None):

    if type(line) is str:
        return mem, line

    if mem:
        memory.value = mem
    try:
        command = eval("commands."+line[0])
        try:
            command(line[1:])
        except IndexError:
            return memory.value, "Not enough parameters!"
    except IndexError:
        return memory.value, None
    except AttributeError:
        return memory.value, f"Unrecognized command: {line[0]}"
    except SyntaxError:
        return memory.value, f"Unrecognized command: {line[0]}"
    except FileNotFoundError:
        return memory.value, "File not Found"
    except KeyboardInterrupt:
        return memory.value, "Keyboard Interrupt"

    return memory.value, None

def execute(lines:str, mem:list[str]=None):

    if mem: memory.value = mem

    memory.value["line"] = 0
    parsed = parser.parse(lines)

    while memory.value["line"] < len(lines.split("\n")):
        mem, error = executeline(parser.calculationparser(parser.variableparser(parsed[memory.value["line"]])))
        if error:
            print(f"At line {memory.value["line"]+1} `{lines.split("\n")[memory.value["line"]]}`:")
            print(f"    {error}")
            quit(1)
        memory.value["line"] += 1
    
    return

if __name__ == "__main__":
    try:
        filename = sys.argv[1]
        file = ""

        try:
            with open(filename) as rawfile:
                file = rawfile.read()
        except FileNotFoundError:
            print("That Program doesn't exist")
            sys.exit()
    except IndexError:
        DEMO = """:loop
input user truth>
set isone $user == 1
?$isone $end
print Go
?True $loop
:end
print End
dump
"""
        file = DEMO


    
    execute(file)
    sys.exit()