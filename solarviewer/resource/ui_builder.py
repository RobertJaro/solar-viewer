import glob
import subprocess

from os.path import basename
from qtpy.uic import compileUi

if __name__ == '__main__':
    for file in glob.glob("**/*.ui", recursive=True):
        compileUi(open(file, "r"), open("../ui/" + basename(file).replace(".ui", ".py"), "w"))
    for file in glob.glob("**/*.qrc", recursive=True):
        subprocess.call(["pyrcc5", '-o', "../ui/" + basename(file).replace(".qrc", "_rc.py"), file])
