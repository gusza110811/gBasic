#!/bin/python3
import zipfile
import sys
import os

class barrel:
    @staticmethod
    def package(filename,includes):
        with open("meta",'w') as metadata:
            metadata.write(filename)

        with zipfile.ZipFile(f"{filename}.bar","w") as bar:
            bar.write(filename+".gbc")
            bar.write("meta")
            if includes:
                for idx,thing in enumerate(includes):
                    bar.write(thing)
                    if os.path.isfile(thing):
                        bar.write(thing)
                    else:
                        print(f"Warning: {thing} not found, skipping.")

        print(f"Packaged {filename}.gbc as {filename}.bar")


if __name__ == "__main__":
    try:
        filename = sys.argv[1]
        try:
            includes = sys.argv[2:]
        except IndexError:
            includes = None
        
        barrel.package(filename,includes)

    except IndexError:
        print("No File Specified")
        quit(1)

    except FileNotFoundError:
        print(f"File not found: {filename}.gbc")
        quit(1)