import os
import sys
import glob
import shutil

assert len(sys.argv) == 4

os.makedirs(sys.argv[3], exist_ok=True)

# take files from [1] if they exist in [1] else take them from [2]
for f in glob.glob(sys.argv[2] + '/*'):
    f_replacement = f.replace(sys.argv[2], sys.argv[1])
    if os.path.exists(f_replacement):
        shutil.copyfile(f.replace(sys.argv[2], sys.argv[1]), f.replace(sys.argv[2], sys.argv[3]))
    else:
        shutil.copyfile(f.replace(sys.argv[2], sys.argv[2]), f.replace(sys.argv[2], sys.argv[3]))
