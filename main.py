"""
Usage:
    Place necessary files into subfolders
    - input_single_SRF/
        SRF from the actual game files, e.g. QNUMBERS.SRF for question segues
        Game file location (Steam):
            C:\Program Files (x86)\Steam\steamapps\common\YDKJ_VOL3\J3Items
    - input_custom_mp3s/
        mp3s you recorded to serve as custom audio segues, e.g. for the question segues:
        1002.mp3  Question 1 Version AK
        1003.mp3  Question 1 Version B
        2002.mp3  Question 2 Version A
        3003.mp3  Question 2 Version B
        ...and so on
        If you don't know the filenames, run this script to extract the SRF and check that

    Then just run python main.py (no Python libraries needed) (ffmpeg installaton needed)
    Output will be in output_single_SRF/

    The code quality is kind of terrible because the project is several years old
    (back when I used text editors instead of IDEs/PyCharm) so I apologize.

TODO: Dockerfile
TODO: refactor

TODO: Kidz Bop demo
"""

import os
import sys
import glob

fn = os.path.basename(glob.glob('input_single_SRF/*.SRF')[0])

sys.argv = ['', 'input_single_SRF/' + fn, 'tmp_SRF_extract/']
import srf_unbuilder

sys.argv = ['', 'input_custom_mp3s/', 'tmp_custom_aifc/']
import all_ffmpeg

sys.argv = ['', 'tmp_custom_aifc/', 'tmp_SRF_extract/', 'tmp_custom_aifc_all/']
import combine_media

sys.argv = ['', 'output_single_SRF/' + fn, 'tmp_custom_aifc_all/']
import srf_builder
