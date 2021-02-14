# Modding Classic You Don't Know Jack Games!

Mod the You Don't Know Jack games from the late 90s with your own audio files, as described in my Medium article.

https://medium.com/@KonopkaKodes/modding-classic-you-dont-know-jack-games-2b64c9ec7dae

## Usage

1. Ensure Python and ffmpeg are installed -- I will add a Dockerfile to facilitate this.
2. Copy the desired SRF to replace from `C:\Program Files (x86)\Steam\steamapps\common\YDKJ_VOL3` (e.g. `QNUMBERS.SRF` for question number segues)
3. Place your custom audio files in `input_custom_mp3s/`. If you do not know the filenames needed, run step 4 first to see which files can be replaced and then come back to this step.
4. Run `python main.py`
5. Copy result in `output_single_SRF/` back into the game files (see step 2).

## Demo video

[![Demo video](https://img.youtube.com/vi/dMVHbfKfRP4/0.jpg)](https://youtu.be/dMVHbfKfRP4 "Demo video")
