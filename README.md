# Download from ambientCG

## What is this?

I discovered [ambientCG.com](http://ambientcg.com) by watching [Gvarados' video](https://www.youtube.com/watch?v=Kpp4uC-W6Ss) about custom materials. They have over a thousand assets that are [completely free to use](https://help.ambientcg.com/01-General/Licensing.html). Getting them manually is a lot of work. Therefor I made this script that gets all of them, and adds a VMAT file for them.

**Note:** these are custom textures so the scaling might not be perfect. When generating the .vmat I set the scaling to `3.000`. This can be changed in the code (mentioned below).

## How does it work?

- Installs pip module:
    - Requests
    - Pillow
- Prompt for the location where you want to place the assets
    - I recommend using `C:\Program Files (x86)\Steam\steamapps\common\sbox\addons`
- Prompt for the directory name (this name will be in the asset browser filters)
    - Eg. `custom_materials`
- Create a `tmp` directory in the directory you provided, and put the downloads in there (this will be removed later)
- Download the assets, and put them in the tmp directory
- Change the filenames to lowercase (for the directories)
- Unpack the zip files in the parent directory
- Change the filenames to lowercase
- Check if the file dimensions are correct (eg. 1024x1024 = ok, 1024x512 = ok. 1024x300 = not ok)
- Create a VMAT file in every directory, and include if available:
    - Color map
    - Normal map
    - Metal map
    - Roughness map
    - Ambient Occlusion map
- Create resolution txt files
- Remove the downloaded zip files in the tmp directory
- Remove the unused displacement images

After the script is done, open your asset browser, and filter on the newly added mod. You will notice a lot of yellow icons with a grey ball in it. Also your asset browser will hang. This is because it's now generating a .vmat_c and .vtex_c files. Every time you scroll and you see those icons it will generate those files. So this might take a while. After a few seconds/minutes the materials will show up.

## Using the Script

### Prerequisites

You need to have Python 3 installed.

[Get Python 3.9 - Microsoft Store](https://www.microsoft.com/en-us/p/python-39/9p7qfqmjrfp7)

### Code

In the code there are some variables you can change to customize the download and generated files.

```python
###############################################################################
# Vars
###############################################################################

# Download options
downloadType = 'PhotoTexturePBR' # Options: PhotoTexturePBR, DecalPBR, AtlasPBR, PhotoTexturePlain, SBSAR, 3DModel, Terrain
downloadSort = 'Alphabet' # Options: Latest, Popular, Alphabet, Downloads
downloadResolution = '1K' # Options: 1K, 2K, 4k, 8K, 16K
downloadFormat = 'JPG' # Options: JPG, PNG (stats same texture: JPG = 262 KB vs. PNG = 1.833 KB)

downloadSbsarQuality = 'HQ' # Options: LQ, HQ

# Material settings
shader = 'simple.vfx'
textureCoordScaleX = '3.000'
textureCoordScaleY = '3.000'

# Resolution options: 
resolutionColor = '1024'
resolutionNormal = '1024'
resolutionRoughness = '1024'
resolutionMetallness = '1024'
resolutionAmbientOcclusion = '1024'
```

## Direct Download

If you don't want to download the latest assets with the Python script you can download this zip from my Google Drive.

As of Aug. 9th, 2021

- Assets: 1075
- Resolution: 1024
- Total size: 4 GB
- Includes:
    - .vmat
    - .vmat_c
    - .vtex_c
    - .txt

[custom_materials.zip](https://poisonmichael.com/hammer/download-from-ambientcg#66013be9fd194cf48d6ae7ae302cdcec)

Extract in `C:\Program Files (x86)\Steam\steamapps\common\sbox\addons`

> Contains assets from [ambientCG.com](http://ambientcg.com/), licensed under CC0 1.0 Universal.
