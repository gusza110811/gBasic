import sys
import os
import zipfile
import json

class virtual:
    memory = {"n":"\n"}
    acc = ""
    code = []
    pc = 0

    removeonquit = False

    @staticmethod
    def read_ascii():
        result = b""
        while virtual.pc < len(virtual.code) and virtual.code[virtual.pc] != 0xFF:
            result += bytes([virtual.code[virtual.pc]])
            virtual.pc += 1
        virtual.pc += 1  # skip 0xFF
        result = result.decode("ascii")
        if result.startswith("$"):
            result = virtual.memory[result[1:]]
        return result

    @staticmethod
    def read_int():
        if virtual.pc + 1 >= len(virtual.code): return 0

        length = virtual.code[virtual.pc]
        val = 0
        for i in range(length):
            virtual.pc +=1
            val = virtual.code[virtual.pc] + (val << 8)

        return val

    @staticmethod
    def executeline():
        if virtual.pc >= len(virtual.code):
            return False

        opcode = virtual.code[virtual.pc]
        virtual.pc += 1

        if opcode == 0x00:  # print
            val = virtual.read_ascii()
            val = virtual.memory.get(val, val) if val != "_" else virtual.acc
            try:
                if bytes(val,'utf-8') == bytes(128):
                    if os.name == "nt":
                        os.system("cls")
                    else:
                        os.system("clear")
            except UnicodeDecodeError:
                pass
            else:
                print(val, end="")

        elif opcode == 0x01:  # dump
            for k, v in virtual.memory.items():
                print(f"{k} : {v}")

        elif opcode == 0x02:  # set
            varname = virtual.read_ascii()
            virtual.memory[varname] = virtual.acc

        elif opcode == 0x03:  # input
            prompt = virtual.read_ascii()
            virtual.acc = input(prompt)

        elif opcode == 0x04:  # gotoif
            target = virtual.read_int()
            if virtual.acc.lower() != "false":
                virtual.pc = target+1
        
        elif opcode == 0x05:  # gotoif
            target = virtual.read_int()
            virtual.pc = target+1

        elif opcode == 0xA5:  # load
            varname = virtual.read_ascii()
            virtual.acc = virtual.memory.get(varname, "")

        elif opcode == 0xA0:  # special set
            virtual.acc = virtual.read_ascii()

        elif opcode == 0xAB:  # noop
            _ = virtual.read_ascii()

        elif opcode == 0xAF:  # quit
            code = virtual.read_ascii()
            quit(int(code))

        # arithmetic ops
        elif opcode in range(0xB0, 0xB7):
            val = virtual.read_ascii()
            lhs = float(virtual.acc)
            rhs = float(virtual.memory.get(val, val))
            if opcode == 0xB0:
                virtual.acc = str(lhs + rhs)
            elif opcode == 0xB1:
                virtual.acc = str(lhs - rhs)
            elif opcode == 0xB2:
                virtual.acc = str(lhs * rhs)
            elif opcode == 0xB3:
                virtual.acc = str(lhs ** rhs)
            elif opcode == 0xB4:
                virtual.acc = str(lhs / rhs)
            elif opcode == 0xB5:
                virtual.acc = str(lhs // rhs)
            elif opcode == 0xB6:
                virtual.acc = str(lhs % rhs)

        # comparison
        elif opcode in range(0xC0, 0xC3):
            val = virtual.read_ascii()
            lhs = virtual.acc
            rhs = virtual.memory.get(val, val)
            try:
                lhsf = float(lhs)
                rhsf = float(rhs)
                if opcode == 0xC0:
                    virtual.acc = str(lhsf == rhsf)
                elif opcode == 0xC1:
                    virtual.acc = str(lhsf < rhsf)
                elif opcode == 0xC2:
                    virtual.acc = str(lhsf > rhsf)
            except:
                if opcode == 0xC0:
                    virtual.acc = str(lhs == rhs)
                else:
                    virtual.acc = "False"

        # logic
        elif opcode == 0xD0:  # or
            val = virtual.read_ascii()
            virtual.acc = str((virtual.acc.lower() != "false") or (val.lower() != "false"))

        elif opcode == 0xD1:  # and
            val = virtual.read_ascii()
            virtual.acc = str((virtual.acc.lower() != "false") and (val.lower() != "false"))

        elif opcode == 0xD2:  # not
            _ = virtual.read_ascii()
            virtual.acc = str(virtual.acc.lower() == "false")
        
        # file i/o
        elif opcode == 0xE0: # read
            try:
                with open(virtual.read_ascii(),'r') as file:
                    virtual.acc = file.read()
            except FileNotFoundError:
                pass
        elif opcode == 0xE1: # write
            with open(virtual.read_ascii(),'w') as file:
                file.write(virtual.acc)

        return True

    @staticmethod
    def execute():
        running = True
        while running:
            running = virtual.executeline()
            continue

class package:
    @staticmethod
    def unpack(file:str):
        with zipfile.ZipFile(file,'r') as zipped:
            zipped.extractall(f".{file.replace("/",".")}")
        os.chdir(f".{file.replace("/",".")}")
        
        metadata = {}
        try:
            with open("meta.json",'r') as metafile:
                metadata = json.load(metafile)
            mainscript = metadata["main"] + ".gbc"
        # Legacy metafile
        except FileNotFoundError:
            with open("meta",'r') as metafile:
                mainscript = metafile.read() + ".gbc"
        
        with open(mainscript, 'rb') as code:
            virtual.code = code.read()

        if metadata["isolate"]:
            virtual.removeonquit = True

if __name__ == "__main__":
    try:
        filename = sys.argv[1]
        with open(filename, "rb") as f:
            virtual.code = list(f.read())

    except IndexError:
        filename = "demo.gbc"
        with open(filename, "rb") as f:
            virtual.code = list(f.read())

    except FileNotFoundError:
        print("File not found.")
        quit(1)

    if filename[-3:] == "bar":
        package.unpack(filename)
        quit(0)

    try:
        virtual.execute()
    except KeyboardInterrupt:
        print("\nProgram has been aborted due to Keyboard Interrupt")
    except Exception as error:
        print("Program has been aborted due to an Error")
        print("     "+str(error))
        quit(255)

    if virtual.removeonquit:
        os.remove(f".{filename.replace("/",".")}")