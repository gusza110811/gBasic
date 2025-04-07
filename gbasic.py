import os
import sys
import json

class memory:
    value = {"line'":0}
    drive = {}

def loaddrive():
    global drive
    with open(memory.value["curdrive'"]+".json",'r') as fdrive:
        memory.drive = json.load(fdrive)

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
        for idx, item in enumerate(memory.value):
            if item.endswith("'"): continue
            print(f"{item} : {memory.value[item]}")
    
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
        os.system("cls")
    
    def call(text:list[str]):
        loaddrive()
        name = text[0]
        script = memory.drive[name]
        line = memory.value["line'"]

        execute({script})

        memory.value["line'"] = line

    def cmd(text:list[str]):
        memory.value["mode'"] = "cmd"


def parse(text:str, mem=None):
    if mem:
        memory.value = mem

    lines = text.split("\n")

    chunks:list[str] = []
    # parse each line
    for line in lines:
        if line.startswith("#"):
            chunks.append("comment")
            continue

        lowchunks = line.split()

        chunkmerge = ""
        for chunk in lowchunks:

            if chunk.startswith("#"):
                break
            
            if chunk.startswith('"') or chunk.startswith("'"):
                if chunk.endswith('"') or chunk.endswith("'"):
                    chunks.append(chunk[1:-1])
                else:
                    chunkmerge = chunk[1:]
            
            elif chunk.endswith('"') or chunk.endswith("'"):
                if chunkmerge != "":
                    chunkmerge = chunkmerge + " " + chunk[:-1]
                else:
                    chunkmerge = chunk[:-1]
                chunks.append(chunkmerge)
                chunkmerge = ""
            elif chunkmerge != "":
                chunkmerge = chunkmerge + " " + chunk

            else:
                chunks.append(chunk)
    
    # replace variables with their value
    for index, chunk in enumerate(chunks):
        if chunk.startswith("$"):
            try:
                chunks[index] = memory.value[chunk[1:]]
            except KeyError:
                return f"Variable '{chunk[1:]}' doesn't exist."
    
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
            elif chunk == "-!":
                chunks[idx] = str(not strtobool(chunks[idx+1]))
                chunks.pop(idx+1)
                break
        else:
            done = True
    
    if not chunks:
        chunks.append("comment")

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
    except AttributeError:
        return memory.value, "Unrecognized command: {line[0]}"
    except SyntaxError:
        return memory.value, "Unrecognized command: {line[0]}"

    return memory.value, None

def execute(lines:list[str]|str, mem:list[str]=None):
    if type(lines) is str: lines = lines.split("\n")

    if mem: memory.value = mem

    memory.value["line'"] = 0

    while memory.value["line'"] < len(lines):
        mem, error = executeline(parse(lines[memory.value["line'"]]))
        if error:
            print(f"At line {memory.value["line'"]} `{lines[memory.value["line'"]]}`:")
            print(f"    {error}")
            return memory.value
        memory.value["line'"] += 1
    
    return memory.value

testmode = True
if __name__ == "__main__":
    try:
        filename = sys.argv[1]
    except IndexError:
        filename = "demo.gb"

    file = ""

    with open(filename) as rawfile:
        file = rawfile.read()
    
    execute(file)