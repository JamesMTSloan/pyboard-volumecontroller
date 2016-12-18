from os.path import join, split, exists
from glob import glob
from getpass import getuser
from shutil import copyfile


pyboard_mount = join("/media", getuser(), "PYBFLASH")
pyboard_globstr = 'pyboard/*'

if not exists(pyboard_mount):
    print("{} not found. Is Pyboard connected/mounted?".format(pyboard_mount))
    quit()

for file in glob(pyboard_globstr):
    src = file
    dst = join(pyboard_mount, split(src)[1])
    print("Copying:")
    print("\t{} to".format(src))
    print("\t{} ...".format(dst))
    copyfile(src, dst)
    print("Successful!")
