#!/bin/python3
import zipfile
import sys
import os
import json

BARRELVERSION = "1"

class barrel:
    @staticmethod
    def package(filename,includes,isolate,packagename):
        metadata = {
            "main":filename,
            "isolate":isolate
        }

        with open("meta.json",'w') as metafile:
            json.dump(metadata,metafile)

        with zipfile.ZipFile(f"{packagename}.bar","w") as bar:
            bar.write(filename+".gbc")
            bar.write("meta.json")
            if includes:
                for idx,thing in enumerate(includes):
                    bar.write(thing)
        
        os.remove("meta.json")

        print(f"Packaged {filename}.gbc as {filename}.bar")


if __name__ == "__main__":
    try:
        filename = sys.argv[1]
        try:
            args = sys.argv[2:]
        except IndexError:
            args = None
        
        packagename = filename
        isolate = False
        includes = []

        # For source existence before proceeding with packing
        with open(filename+".gbc"):pass

        name = False
        including = False
        for idx, arg in enumerate(args):
            if name:
                packagename = arg
                continue
            elif including:
                includes.append(arg)
                continue

            if arg.lower() == "isolate" or (arg.lower() == "-i"):
                isolate = True
            elif (arg.lower() == "include") or (arg.lower() == "-a"):
                including = True
            elif (arg.lower() == "includes") or (arg.lower() == "packswith") or (arg.lower() == "-p"):
                try:
                    includes = args[(idx+1):]
                except IndexError:
                    print("Add directories or files to include in the package")
                    print(f"Or did you add \"{arg}\" by accident?")
                    quit(3)
            elif (arg.lower() == "name") or (arg.lower() == "-n"):
                name = True
            else:
                print(f"Invalid parameter: \"{arg}\"")
                quit(3)

        
        barrel.package(filename,includes,isolate,packagename)

    except IndexError:
        print("No File Specified")
        quit(1)

    except FileNotFoundError:
        print(f"File not found: {filename}.gbc")
        quit(2)