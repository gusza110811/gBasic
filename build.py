import sys
import os
try:
    import PyInstaller.__main__
except ImportError:
    print("Missing require library for installation: Pyinstaller.")
    print("Library 'Pyinstaller' is included in the local environment '.env', did you try to run this script in global environment?\n")
    print("If you prefer to install gbasic in global enviroment, please install PyInstaller there")
    if os.name == "nt":
        print("You can run `pip install pyinstaller` to install it")
    elif os.name == "posix":
        print("You can use `pip install pyinstaller` but it depends on your configuration and OS")
    quit(2)

params = sys.argv

include_compiler = False
include_virtual_machine = False
include_barrel = False

include_demo = False

skip_confirm = False
help = False

for param in params:
    param = param.lower()
    if param == "compiler" or param == "-c":
        include_compiler = True
    elif param == "vm" or param == "-m":
        include_virtual_machine = True
    elif param == "barrel" or param == "bar" or param == "-b":
        include_barrel = True
    elif param == "demos" or param == "demo" or param == "-d":
        include_demo = True
    elif param == "skip" or param == "-y":
        skip_confirm = True
    elif param == "help" or param == "-h":
        help = True

def confirm(include_compiler, include_virtual_machine, include_barrel):
    if include_compiler and (not include_virtual_machine):
        abort = input("Compiler is selected, but VM is not, You will not be able to run compiled gBasic. \nAre you sure you want to proceed? (Y/n)").lower() == "n"
        if abort:
            quit("Build aborted")

        print("\n")\

    if include_barrel and (not include_virtual_machine):
        abort = input("Packager is selected, but VM is not, You will not be able to run packaged gBasic. \nAre you sure you want to proceed? (Y/n)").lower() == "n"
        if abort:
            quit("Build aborted")

        print("\n")

    if include_barrel and (not include_compiler):
        abort = input("Packager is selected, but the compiler is not. You can only package Bytecodes from the compiler. \nAre you sure you want to proceed? (Y/n)").lower() == "n"
        if abort:
            quit("Build aborted")

        print("\n")

if not skip_confirm:
    confirm(include_compiler, include_virtual_machine, include_barrel)
else:
    print("Skipping all confirmations\n")

print("Building Interpreter")
installargs = [
    "gbasic.py"
]

if include_demo:
    installargs.append(f"--add-data")
    installargs.append(f"demos{os.pathsep}demos")

PyInstaller.__main__.run(installargs)

if include_compiler:
    print("Building Compiler")
    installargs = [
        "compiler.py"
    ]

    if include_demo:
        installargs.append(f"--add-data")
        installargs.append(f"compiled-demos{os.pathsep}compiled-demos")

    PyInstaller.__main__.run(installargs)

if include_barrel:
    print("Building Packager (Barrel)")
    installargs = [
        "barrel.py"
    ]

    if include_demo:
        installargs.append(f"--add-data")
        installargs.append(f"compiled-demos{os.pathsep}compiled-demos")

    PyInstaller.__main__.run(installargs)

if include_virtual_machine:
    print("Building Virtual Machine (gBvm)")
    installargs = [
        "gbvm.py"
    ]

    if include_demo:
        installargs.append(f"--add-data")
        installargs.append(f"compiled-demos{os.pathsep}compiled-demos")

    PyInstaller.__main__.run(installargs)