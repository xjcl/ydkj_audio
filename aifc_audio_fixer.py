import sys

for fn in sys.argv[1:]:
    with open(fn, 'rb') as old, open(fn + 'new', 'wb') as new:
        a = old.read()

        # *** OPTION 1 ***

        HEADERSIZE  = 70
        remain_size = ( len(a) -               8).to_bytes(4, byteorder='big')
        size_div_34 = ((len(a) - HEADERSIZE)//34).to_bytes(4, byteorder='big')
        weird_size  = ((len(a) - HEADERSIZE) + 8).to_bytes(4, byteorder='big')
        print(remain_size, size_div_34, weird_size)

        # 4 * 16 + 6  = 70
        # new.write(bytes((
        #     0x46, 0x4f, 0x52, 0x4d)) + remain_size + bytes((0x41, 0x49, 0x46, 0x43, 0x46, 0x56, 0x45, 0x52,
        #     0x00, 0x00, 0x00, 0x04, 0xa2, 0x80, 0x51, 0x40, 0x43, 0x4f, 0x4d, 0x4d, 0x00, 0x00, 0x00, 0x16,
        #     0x00, 0x01)) + size_div_34 + bytes((0x00, 0x10, 0x40, 0x0d, 0xaf, 0xc8, 0x00, 0x00, 0x00, 0x00,
        #     0x00, 0x00, 0x69, 0x6d, 0x61, 0x34, 0x53, 0x53, 0x4e, 0x44)) +  weird_size + bytes((0x00, 0x00,
        #     0x00, 0x00, 0x00, 0x00, 0x00, 0x00
        # )))

        # *** OPTION 2 ***

        # idk why '-12' here. i'm just imitating the (hopefully correct) output ima4 aifc that ffmpeg produced =)
        HEADERSIZE  = 72
        remain_size = ( len(a) -               8 - 12).to_bytes(4, byteorder='big')
        size_div_34 = ((len(a) - HEADERSIZE)//34     ).to_bytes(4, byteorder='big')
        weird_size  = ((len(a) - HEADERSIZE) + 8 - 12).to_bytes(4, byteorder='big')
        print(remain_size, size_div_34, weird_size)

        # 4 * 16 + 6 + 2  = 72
        new.write(bytes((
            0x46, 0x4f, 0x52, 0x4d)) + remain_size + bytes((0x41, 0x49, 0x46, 0x43, 0x46, 0x56, 0x45, 0x52,
            0x00, 0x00, 0x00, 0x04, 0xa2, 0x80, 0x51, 0x40, 0x43, 0x4f, 0x4d, 0x4d, 0x00, 0x00, 0x00, 0x18,
            0x00, 0x01)) + size_div_34 + bytes((0x00, 0x04, 0x40, 0x0d, 0xaf, 0xc8, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x69, 0x6d, 0x61, 0x34, 0x00, 0x00, 0x53, 0x53, 0x4e, 0x44)) + weird_size + bytes((0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00
        )))

        new.write(a[84:])
        # new.write(a)
        # new.write(a[:84])  # needed!  # bug: only plays on left ear in linux-vlc!!

        print('wrote vlc-playable audio file to ' + fn + 'new')


        # for i in range(16):
        #     new.write(bytes((0x00,)))
        #
        # new.write(a[100:])
        # new.write(a[:100])

        # TODO: read 100 bytes further down instead xD
        # TODO: test without 84 at the end

