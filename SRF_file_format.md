
```
# file format

#  LONG magicno srf1    -- it's an ".SRF" file
#  LONG filelen         -- INCLUDING header, in bytes
#  LONG headerlen       -- of REMAINING header EXCLUDING the 3 already-seen longs

#  LONG 'off4'          -- constant indicating graphics section begins
#  LONG numgraphics     -- after that an array of graphics
#  [LONG name  LONG offset  LONG size]   -- pointers into the RAW data below

#  LONG 'snd '          -- constant indicating audio section begins
#  LONG numsounds       -- after that an array of audio clips
#  [LONG name  LONG offset  LONG size]   -- pointers into the RAW data below

#  RAW data
```

```
# 46 4F 52 4D XX XX XX XX 41 49 46 43 46 56 45 52
# 00 00 00 04 A2 80 51 40 43 4F 4D 4D 00 00 00 16
# 00 01 YY YY YY YY 00 10 40 0D AF C8 00 00 00 00
# 00 00 69 6D 61 34 53 53 4E 44 ZZ ZZ ZZ ZZ 00 00
# 00 00 00 00 00 00
# You have to calculate the values for X, Y and Z in big endian.
# X = the total filesize (data+header) - 8 Bytes
# Y = size of data / 34 Bytes
# Z = size of data + 8 Bytes
```
