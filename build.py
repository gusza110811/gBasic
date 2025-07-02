import sys
import os
try:
    import PyInstaller.__main__
except ImportError:
    print("Missing required library for installation: Pyinstaller.")
    if os.name == "nt":
        yes = input("Do you want to try installing it now? (Y/n)").lower() == "y"
        if yes:
            exitcode = os.system("pip install pyinstaller")
            if exitcode == 0:
                print("\nSuccessful, proceeding to installation")
                import PyInstaller.__main__
            else:
                print("Failed to install PyInstaller.")
                sys.exit(2)
        else:
            sys.exit()
    elif os.name == "posix":
        print("Library 'Pyinstaller' is included in the local environment '.env', did you try to run this script in global environment?\n")
        print("If you want to run this in the local environment,")
        print("run this to use the virtual environment: `source .env/bin/activate`")
        print("Or you can use `pip install pyinstaller` to install it in the global environment but it depends on your configuration and OS")
        sys.exit(2)

def confirm(include_compiler, include_virtual_machine, include_barrel):
    if include_compiler and (not include_virtual_machine):
        abort = input("Compiler is selected, but VM is not, You will not be able to run compiled gBasic. \nAre you sure you want to proceed? (Y/n)").lower() == "n"
        if abort:
            sys.exit("Build aborted")

        print("\n")

    if include_barrel and (not include_virtual_machine):
        abort = input("Packager is selected, but VM is not, You will not be able to run packaged gBasic. \nAre you sure you want to proceed? (Y/n)").lower() == "n"
        if abort:
            sys.exit("Build aborted")

        print("\n")

    if include_barrel and (not include_compiler):
        abort = input("Packager is selected, but the compiler is not. You can only package Bytecodes from the compiler. \nAre you sure you want to proceed? (Y/n)").lower() == "n"
        if abort:
            sys.exit("Build aborted")

        print("\n")

helpmsg = """(python )build(.py) [options]
Options
    -c : Include Compiler
    -m : Include VM (gBvm)
    -b : Include Packager (Barrel)
    -d : Include Demos in _internal
    -a : Include everything above

    -y : Skip all confirmation
    -h : Show this message
"""
def help():
    global helpmsg
    print(helpmsg)
    sys.exit()

params = sys.argv

include_compiler = False
include_virtual_machine = False
include_barrel = False

include_demo = False

skip_confirm = False
send_help = False

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
    elif param == "all" or param == "-a":
        include_compiler = True
        include_virtual_machine = True
        include_barrel = True
        include_demo = True

    elif param == "help" or param == "-h":
        send_help = True

if send_help:
    help()

if not skip_confirm:
    confirm(include_compiler, include_virtual_machine, include_barrel)
else:
    print("Skipping all confirmations\n")

print("\nBuilding Interpreter\n")
installargs = [
    "gbasic.py"
]
if skip_confirm: installargs.append("--noconfirm")

if include_demo:
    installargs.append(f"--add-data")
    installargs.append(f"demos{os.pathsep}demos")

PyInstaller.__main__.run(installargs)

if include_compiler:
    print("\n\nBuilding Compiler\n")
    installargs = [
        "compiler.py"
    ]
    if skip_confirm: installargs.append("--noconfirm")

    if include_demo:
        installargs.append(f"--add-data")
        installargs.append(f"compiled-demos{os.pathsep}compiled-demos")

    PyInstaller.__main__.run(installargs)

if include_barrel:
    print("\n\nBuilding Packager (Barrel)\n")
    installargs = [
        "barrel.py"
    ]
    if skip_confirm: installargs.append("--noconfirm")

    if include_demo:
        installargs.append(f"--add-data")
        installargs.append(f"compiled-demos{os.pathsep}compiled-demos")

    PyInstaller.__main__.run(installargs)

if include_virtual_machine:
    print("\n\nBuilding Virtual Machine (gBvm)\n")
    installargs = [
        "gbvm.py"
    ]
    if skip_confirm: installargs.append("--noconfirm")

    if include_demo:
        installargs.append(f"--add-data")
        installargs.append(f"compiled-demos{os.pathsep}compiled-demos")

    PyInstaller.__main__.run(installargs)

print("\n\ngBasic and related programs have been built, they are available at dist/")