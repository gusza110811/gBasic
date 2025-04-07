import gbasic
import json
import os

active = True
ram = {
    "mode'":"cmd",
    "line'":0,
    "curdrive'":"A",
    "code'": []
}

drive = {}

# mode,line,curdrive,code variables cannot be modified using gbasic due to intentional design
# modes
"""
gb: Gbasic interface
cmd: Generic terminal interface
edit: Code Editor
"""

HELP = """
<List of commands>
help         : Show this message
clear        : Clear the terminal

gb           : Enter gBasic mode
memory       : See values in ram
clean        : Reset ram

edit         : Enter code editor
run          : Run loaded script
call {name}  : Run {name} without overwriting currently loaded script
start {name} : Run {name} without overwriting currently loaded script in a seperate ram
peek         : See the loaded script

dir          : See the files in the current storage drive
save {name}  : Save the loaded script as {name}
load {name}  : Load {name} as script
del {name}   : Delete {name} from the current storage drive
"""

def run():
    global ram

    ram = gbasic.execute(ram["code'"],ram)

def loaddrive():
    global drive
    with open(ram["curdrive'"]+".json",'r') as fdrive:
        drive = json.load(fdrive)

def syncdrive():
    global drive
    with open(ram["curdrive'"]+".json",'w') as fdrive:
        json.dump(drive,fdrive,indent=4)

print("GDOS Copyright (C) 2025 Sawyer Nelson")
print("Input 'help' to see list of commands.\n")
while active:

    if ram["mode'"] == "gb":
        command = input(ram["curdrive'"]+":gBasic>")
        ram = gbasic.execute(command,ram)

    elif ram["mode'"] == "cmd":
        command = input(ram["curdrive'"]+">")
        com, *arg = command.split()

        try:
            if com == "gb":
                ram["mode'"] = "gb"
            elif com == "edit":
                ram["mode'"] = "edit"
                os.system("cls")
            elif com == "help":
                print(HELP)
            elif com == "run":
                run()
            elif com == "call":
                name = arg[0]
                loaddrive()
                try:
                    script = drive[name]
                except KeyError:
                    print("File doesnt exist!")
                    continue

                ram = gbasic.execute(script,ram)
            elif com == "start":
                name = arg[0]
                loaddrive()
                try:
                    script = drive[name]
                except KeyError:
                    print("File doesnt exist!")
                    continue

                gbasic.execute(script,ram.copy())
                
            elif com == "clear":
                os.system("cls")
            
            elif com == "peek":
                maxnumlen = len(str(len(ram["code'"])))
                print("`")
                for idx, line in enumerate(ram["code'"]):
                    print(f"{str(idx).zfill(maxnumlen)} | {line}")
                print("`")
            
            elif com == "memory":

                fram = dict(list(ram.items())[4:])

                maxnumlen = len(str(len(fram)))
                maxnamelen = max(map(len, fram))
                for idx, value in enumerate(fram):

                    print(str(idx).zfill(maxnumlen) + " | " + value.ljust(maxnamelen," ") + " | " + str(fram[value]))
            elif com == "clean":
                ram = {"mode'":"cmd",
                    "line'":0,
                    "code'": []
                }
            
            elif com == "save":
                name = arg[0]
                loaddrive()
                drive[name] = ram["code'"]
                syncdrive()
            elif com == "load":
                print("This will overwrite your current code! You do wish to proceed?")
                yn = input("(Y/n)>").lower()
                if yn != "y":
                    print("Loading canceled")
                    continue

                name = arg[0]
                loaddrive()
                try:
                    ram["code'"] = drive[name]
                except KeyError:
                    print("File doesnt exist!")
                    continue

            elif com == "dir":
                loaddrive()
                print(f"Files in {ram["curdrive'"]}:{drive["__drivename"]}")
                maxnumlen = len(str(len(drive)))
                print("```")
                for idx, item in enumerate(drive):
                    print(f"{str(idx).zfill(maxnumlen)} | {item}")
                print("```")
            elif com == "del":
                name = arg[0]
                print(f"You do wish to delete {name}?")
                yn = input("(Y/n)>").lower()
                if yn != "y":
                    print("File deletion canceled")
                    continue

                loaddrive()
                
                try:
                    del drive[name]
                except KeyError:
                    print("File doesnt exist!")
                    continue
                syncdrive()
        except IndexError:
            print("Not enough parameters!")

    elif ram["mode'"] == "edit":
        os.system("cls")
        maxnumlen = len(str(len(ram["code'"])))

        print("`")
        for idx, line in enumerate(ram["code'"]):
            print(f"{str(idx).zfill(maxnumlen)} | {line}")
        print("`")

        command = input(ram["curdrive'"]+":codeEditor>")
        index, *com = command.split()

        try:
            int(index)
        except ValueError:
            if index == "cmd":
                ram["mode'"] = "cmd"
                continue
            elif index == "run":
                run()
                input("Enter to continue editing>")
                continue
            elif index == "info":
                print("info                 | Show this message")
                print("{linenumber} {code}  | Change the code at line {linenumber} to {code}")
                print("+{linenumber} {code} | Insert {code} at line {linenumber}")
                print("-{linenumber}        | Remove a line")
                print("cmd                  | Return to commandline mode")
                print("run                  | Run the script")
                continue
            elif index.startswith("+"): pass
            else:
                print("Invalid Command, type info for help.")
                continue

        ram["code'"] += [''] * (int(index) - len(ram["code'"]))

        if index[0] == "+":
            ram["code'"].insert(int(index[1:])," ".join(com))
        
        elif index[0] == "-":
            ram["code'"].pop(int(index[1:]))

        else:
            ram["code'"][int(index)] = " ".join(com)