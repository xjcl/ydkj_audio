import os
import sys
import glob

# **** EXTRACTION OF SRF ARCHIVE FILE (YOU DON'T KNOW JACK GAMES) INTO INDIVIDUAL MEDIA ****

print('Usage:  `python3 srf_unbuilder.py ARCHIVE.SRF destination_media_folder/`')

if len(sys.argv) == 1:
    print('Drag&Drop the following file paths from Windows Explorer and press <Enter>')
    sys.argv.append( input('Which .SRF archive file do you want to extract? ') )
    sys.argv.append( input('Which folder do you want to extract it into? ') )
assert len(sys.argv) == 3

os.makedirs(sys.argv[2], exist_ok=True)


by = lambda x: int.from_bytes(x, byteorder='big', signed=True)


with open(sys.argv[1], 'rb') as f:
    assert f.read(4) == b'srf1'
    f.read(4)
    f.read(4)

    assert f.read(4) == b'off4'
    total_off4 = by(f.read(4))  # number of graphics
    for i in range(total_off4):
        with open(sys.argv[2] + '/' + str(by(f.read(4))) + '.pre_graphic', 'wb') as media_out:
            offset = by(f.read(4))
            size = by(f.read(4))
            offset_backup = f.tell()
            f.seek(offset)
            media_out.write(f.read(size))
            f.seek(offset_backup)

    assert f.read(4) == b'snd '
    total_snd = by(f.read(4))  # number of audio files
    for i in range(total_snd):
        with open(sys.argv[2] + '/' + str(by(f.read(4))) + '.pre_aifc', 'wb') as media_out:
            offset = by(f.read(4))
            size = by(f.read(4))
            offset_backup = f.tell()
            f.seek(offset)
            media_out.write(f.read(size))
            f.seek(offset_backup)


print('Extracted ' + sys.argv[1] + ' into raw .pre_graphic and .pre_aifc files')
print('However, .pre_aifc files are not yet playable by an audio player')
print('This is why we will now replace their headers to make them playable (.aifc files)')


# for more on this, see 'aifc_audio_fixer.py'
for fn in glob.glob(sys.argv[2] + '/*.pre_aifc'):
    with open(fn, 'rb') as old, open(fn[:-9] + '.aifc', 'wb') as new:
        a = old.read()

        HEADERSIZE  = 72
        remain_size = ( len(a) -               8 - 12).to_bytes(4, byteorder='big')
        size_div_34 = ((len(a) - HEADERSIZE)//34     ).to_bytes(4, byteorder='big')
        weird_size  = ((len(a) - HEADERSIZE) + 8 - 12).to_bytes(4, byteorder='big')

        new.write(bytes((
            0x46, 0x4f, 0x52, 0x4d)) + remain_size + bytes((0x41, 0x49, 0x46, 0x43, 0x46, 0x56, 0x45, 0x52,
            0x00, 0x00, 0x00, 0x04, 0xa2, 0x80, 0x51, 0x40, 0x43, 0x4f, 0x4d, 0x4d, 0x00, 0x00, 0x00, 0x18,
            0x00, 0x01)) + size_div_34 + bytes((0x00, 0x04, 0x40, 0x0d, 0xaf, 0xc8, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x69, 0x6d, 0x61, 0x34, 0x00, 0x00, 0x53, 0x53, 0x4e, 0x44)) + weird_size + bytes((
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00
        )))

        new.write(a[84:])


print('Construction of .aifc files complete')
print('AUDIO NOTES: They are in mono with left-ear audio only')
print('MODDING NOTES: Just replace the .aifc files in this folder with your custom ones')
print('               and run `srf_builder.py` (will take care of the header change)')
print('AIFC NOTES: You can obtain the ima4-encoded 22.5kHz files required for modding')
print('            in multiple ways, this is an example using the program `ffmpeg`:')
print('                ffmpeg -i in.mp3 -c:a adpcm_ima_qt -ar 22500 out.aiff')
print('            Make sure your volume is at the same level as the original files!')

if __name__ == '__main__':
    input()
