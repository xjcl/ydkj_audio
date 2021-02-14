import os
import sys
import glob

print('Usage:  `python3 srf_builder.py ARCHIVE.SRF source_media_folder/`')

if len(sys.argv) == 1:
    print('Drag&Drop the following file paths from Windows Explorer and press <Enter>')
    sys.argv.append( input('Which .SRF archive file do you want to build? ') )
    sys.argv.append( input('Which folder do you want to use as media source? ') )

assert len(sys.argv) == 3

os.makedirs(os.path.dirname(sys.argv[1]), exist_ok=True)

print('First, we will convert all (incl. custom) .aifc files to .pre_aifc files')


# **** 'CONVERSION' OF AUDIO (ADD MYSTERIOUS HEADER)  .aifc -> .pre_aifc ****

lng = lambda x: int(x).to_bytes(4, byteorder='big', signed=True)

aifc_header_84 = bytes((
    0x00, 0x01, 0x00, 0x01, 0x00, 0x05, 0x00, 0x00, 0x00, 0x80, 0x00, 0x01, 0x80, 0x51, 0x00, 0x00, 0x00, 0x00, 0x00, 0x14, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x01, 0x56, 0x22, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xfe, 0x3c,    0,    0,    0,    0, 0x40, 0x0d,
    0xac, 0x44, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x69, 0x6d, 0x61, 0x34, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0xff, 0xff, 0x00, 0x00, 0x00, 0x00, 0x00, 0x10,
))

for fn in glob.glob(sys.argv[2] + '/*.aifc'):
    with open(fn, 'rb') as old, open(fn[:-5] + '.pre_aifc', 'wb') as new:
        a = old.read()
        # print(fn, len(a[72:]), len(a[72:])//34, hex(len(a[72:])//34))
        aifc_header_84 = aifc_header_84[:42] + lng(len(a[72:])//34) + aifc_header_84[42+4:]   # 70 vs 72
        new.write(aifc_header_84)
        new.write(a[72:])  # 70 vs 72
        print('CUSTOM audio track added! ' + fn)



# **** ASSEMBLY OF SRF FILE (see ./SRF_file_format.md) ****

print('Conversion successful! Assembling SRF file now...')

total_bytes = 7 * 4
total_off4  = 0
total_snd   = 0

# XXX i changed these 2 (pre_graphic vs pre_aifc)
for fn in glob.glob(sys.argv[2] + '/*.pre_graphic'):
    with open(fn, 'rb') as f:
        a = f.read()
        total_bytes += len(a) + 3 * 4
        total_off4 += 1

for fn in glob.glob(sys.argv[2] + '/*.pre_aifc'):
    with open(fn, 'rb') as f:
        a = f.read()
        total_bytes += len(a) + 3 * 4
        total_snd += 1

print(total_bytes)



header_bytes = 7*4 + 3*4*(total_off4 + total_snd)
offset = header_bytes

with open(sys.argv[1], 'wb') as out:

    graphic_list = glob.glob(sys.argv[2] + '/*.pre_graphic')
    aifc_list = glob.glob(sys.argv[2] + '/*.pre_aifc')

    out.write(b'srf1')
    out.write(lng(total_bytes))
    out.write( lng(header_bytes - 3*4) )

    out.write(b'off4')
    out.write(lng(total_off4))
    for fn in graphic_list:
        out.write(lng(fn[fn.rfind('/')+1:-12]))
        out.write(lng(offset))
        b = open(fn, 'rb').read()
        out.write(lng(len(b)))
        print(fn, offset, len(b))
        offset += len(b)

    out.write(b'snd ')
    out.write(lng(total_snd))
    for fn in aifc_list:
        out.write(lng(fn[fn.rfind('/')+1:-9]))
        out.write(lng(offset))
        b = open(fn, 'rb').read()
        out.write(lng(len(b)))
        print(fn, offset, len(b))
        offset += len(b)

    for fn in graphic_list:
        b = open(fn, 'rb').read()
        out.write(b)

    for fn in aifc_list:
        b = open(fn, 'rb').read()
        out.write(b)


print('**** Built SRF successfully! =)  ' + sys.argv[1])
print('Graphics files: ' + str(total_off4) + '  Audio files: ' + str(total_snd))
print('If custom audio is corrupted, look at the aifc notes in `srf_unbuilder.py`')

if __name__ == '__main__':
    input()
