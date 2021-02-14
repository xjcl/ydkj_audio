import glob
import os
import sys
import aifc

# convert a bunch of mp3 files to ima4 aifc files, including volume bump

if len(sys.argv) < 3:
    print('Usage: If the media files are in the directory `from/` do `python3 all_ffmpeg.py from/ to/`')
    sys.exit()

from_path = sys.argv[1]
to_path = sys.argv[2]
os.makedirs(sys.argv[2], exist_ok=True)

for f in glob.glob(from_path + '/*'):
    extension = f.rsplit('.', 1)[1]
    f_new = f.replace(from_path, to_path).replace('.' + extension, '.aiff')
    print(f, '->', f_new)
    os.system('set -x; ffmpeg -i ' + f + ' -c:a adpcm_ima_qt -filter:a "volume=2.7" -sample_fmt s16 -ar 22500 -ac:a 1 ' + f_new)
    os.rename(f_new, f_new.replace('.aiff', '.aifc'))
