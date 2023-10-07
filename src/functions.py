import sys
import os

from init import Files, Procedure

def delete_last_line():
    cursorUp = "\x1b[1A"
    eraseLine = "\x1b[2K"
    sys.stdout.write(cursorUp)
    sys.stdout.write(eraseLine)

def lock(type: Procedure = Procedure.Unknown):
    with open(Files.lockfile, "w") as lockfile:
        lockfile.write(type)