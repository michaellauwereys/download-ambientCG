###############################################################################
# Created by: PoisonMichael
# Last update: 2021-08-09
# Website: poisonmichael.com
###############################################################################

###############################################################################
# Install module: requests and pillow
###############################################################################

import os
os.system("pip install requests --quiet --disable-pip-version-check")
os.system("pip install pillow --quiet --disable-pip-version-check")

###############################################################################
# Imports
###############################################################################

import requests
import zipfile
import shutil
import glob
from PIL import Image

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

###############################################################################
# Ask user for input
###############################################################################

print('Enter the directory where you want to place the materials (typically in C:\Program Files (x86)\Steam\steamapps\common\sbox\addons):')
dest = input()

print('\nEnter the directory name (eg. custom_materials):')
dirName = input()

print()

root = dest + '\\' + dirName

###############################################################################
# Get the list of assets
###############################################################################

# Human readable file size
def sizeFormat(num, suffix='B'):
    for unit in [' ',' K',' M',' G',' T',' P',' E',' Z']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Y', suffix)

# Check if the material location already exists, and create it if it's doesn't
if not os.path.exists(root):
  os.mkdir(root)

# Check if the tmp location already exists, and create it if it's doesn't. This is used to temporarily store the assets
if not os.path.exists(root + '\\tmp'):
  os.mkdir(root + '\\tmp')

###############################################################################
# Get the total amount of assets
###############################################################################

url = "https://ambientCG.com/api/v2/full_json?limit=1&method&type=PhotoTexturePBR&sort=Latest"
headers = {
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'
}
response = requests.request("GET", url, headers=headers).json()

# Counters
assetCounter = 0
assetOffset = 0
assetTotal = int(response['numberOfResults'])
assetTotalCounter = 0
assetTotalSize = 0

###############################################################################
# Get all of the assets
###############################################################################

while assetCounter <= (assetOffset + 100) and assetCounter < assetTotal:
  if assetCounter == (assetOffset + 100):
    assetOffset += 100

  # API url of ambiantCG
  url = "https://ambientCG.com/api/v2/full_json?limit=100&type=" + str(downloadType) + "&sort=" + str(downloadSort) + "&offset=" + str(assetOffset) + "&include=downloadData&date"

  # We need this header to prevent 403 error
  headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'
  }

  # Do a GET request
  response = requests.request("GET", url, headers=headers).json()

  ###############################################################################
  # Loop over the results to get the info we need
  ###############################################################################

  for asset in response['foundAssets']:
    assetId = asset['assetId'].lower() # Make the name lowercase
    assetDir = root + '\\' + assetId + '_' + downloadResolution.lower()
    assetIdDir = assetDir + '\\' + assetId + '_' + downloadResolution.lower()

    # Zip files
    if 'zip' in asset['downloadFolders']['/']['downloadFiletypeCategories']:
      # Loop over the available zip files
      for assetDownload in asset['downloadFolders']['/']['downloadFiletypeCategories']['zip']['downloads']:
        # Get the assets that match your resolution and format
        if assetDownload['attribute'] == downloadResolution.upper() + '-' + downloadFormat.upper():

          ###############################################################################
          # Download zip file
          ###############################################################################

          download = assetDownload['downloadLink']

          downloadZip = requests.get(download, headers=headers, allow_redirects=True)

          zip = open(root + '\\tmp\\' + assetId + '.zip', 'wb')
          zip.write(downloadZip.content)
          zip.close()

          # Extract zip file
          with zipfile.ZipFile(root + '\\tmp\\' + assetId + '.zip', 'r') as zip_ref:
            zip_ref.extractall(assetDir)

          # Make all the files lowercase
          files = os.listdir(assetDir)
          for file in files:
            os.rename(assetDir + '\\' + file, assetDir + '\\' + file.lower())

          # Check image dimensions (need to be a square, or half size like 1024x512, 1000x300 = not ok)
          image = Image.open(assetDir + '\\' + file)
          width, height = image.size
          image.close()

          if (width == height) or (width - height == 0) or (width - height == height) or (height - width == width):
            # Counter and file size
            assetTotalCounter += 1
            print("{}) {}".format(assetTotalCounter, assetId))
            assetTotalSize = assetTotalSize + int(assetDownload['size'])

            ###############################################################################
            # Create VMAT file
            ###############################################################################

            vmat = open(assetIdDir + '.vmat',"w+")

            # Check for color map
            if os.path.exists(assetIdDir + '_color.' + downloadFormat.lower()):
              color = "  //---- Color ----\n  g_flModelTintAmount \"1.000\"\n  g_vColorTint \"[1.000000 1.000000 1.000000 0.000000]\"\n  TextureColor \"" + assetId + "_" + downloadResolution.lower() + "/" + assetId + "_" + downloadResolution.lower() + "_color." + downloadFormat.lower() + "\"\n\n"
            else:
              color = "  //---- Color ----\n  g_flModelTintAmount \"1.000\"\n  g_vColorTint \"[1.000000 1.000000 1.000000 0.000000]\"\n  TextureColor \"materials/default/default_color.tga\"\n\n"
            
            # Check for normal map
            if os.path.exists(assetIdDir + '_normal.' + downloadFormat.lower()):
              normal = "  //---- Normal ----\n  TextureColor \"" + assetId + "_" + downloadResolution.lower() + "/" + assetId + "_" + downloadResolution.lower() + "_normal." + downloadFormat.lower() + "\"\n\n"
            else:
              normal = "  //---- Normal ----\n  TextureColor \"materials/default/default_normal.tga\"\n\n"

            # Check for roughness map
            if os.path.exists(assetIdDir + '_roughness.' + downloadFormat.lower()):
              roughness = "  //---- Roughness ----\n  TextureColor \"" + assetId + "_" + downloadResolution.lower() + "/" + assetId + "_" + downloadResolution.lower() + "_roughness." + downloadFormat.lower() + "\"\n\n"
            else:
              roughness = "  //---- Roughness ----\n  TextureColor \"materials/default/default_rough.tga\"\n\n"

            # Check for metal map
            if os.path.exists(assetIdDir + '_metalness.' + downloadFormat.lower()):
              metalness = "  //---- PBR ----\n  F_METALNESS_TEXTURE 1\n\n  //---- Metalness ----\n  TextureMetalness \"" + assetId + "_" + downloadResolution.lower() + "/" + assetId + "_" + downloadResolution.lower() + "_metalness." + downloadFormat.lower() + "\"\n\n"
            else:
              metalness = '//---- Metalness ----\n  g_flMetalness \"0.000\"\n\n'

            # Check for ambient occlusion
            if os.path.exists(assetIdDir + '_ambientocclusion.' + downloadFormat.lower()):
              ambientOcclusion = "  //---- PBR ----\n  F_AMBIENT_OCCLUSION_TEXTURE 1\n\n  //---- Ambient Occlusion ----\n  TextureAmbientOcclusion \"" + assetId + "_" + downloadResolution.lower() + "/" + assetId + "_" + downloadResolution.lower() + "_ambientocclusion." + downloadFormat.lower() + "\"\n\n"
            else:
              ambientOcclusion = ''

            # Template to put in the VMAT file
            templateVMAT = [
              "// THIS FILE IS AUTO-GENERATED\n",
              "\n",
              "Layer0\n",
              "{\n",
              "  shader \"" + shader + "\"\n",
              "\n",
              color,
              normal,
              roughness,
              metalness,
              ambientOcclusion,
              "  //---- Fade ----\n",
              "  g_flFadeExponent \"1.000\"\n",
              "\n",
              "  //---- Fog ----\n",
              "  g_bFogEnabled \"1\"\n",
              "\n",
              "  //---- Lighting ----\n",
              "  g_flDirectionalLightmapMinZ \"0.050\"\n",
              "  g_flDirectionalLightmapStrength \"1.000\"\n",
              "\n",
              "  //---- Texture Coordinates ----\n",
              "  g_nScaleTexCoordUByModelScaleAxis \"0\"\n",
              "  g_nScaleTexCoordVByModelScaleAxis \"0\"\n",
              "  g_vTexCoordOffset \"[0.000 0.000]\"\n",
              "  g_vTexCoordScale \"[" + textureCoordScaleX + " " + textureCoordScaleY + "]\"\n",
              "  g_vTexCoordScrollSpeed \"[0.000 0.000]\"\n",
              "}"
            ]
            
            vmat.writelines(templateVMAT)
            vmat.close()

            ###############################################################################
            # Create resolution txt files
            ###############################################################################

            templateResolutionColor = [
              "settings\n",
              "{\n",
              "  \"maxres\" \"" + str(resolutionColor) + "\"\n",
              "}"
            ]

            templateResolutionNormal = [
              "settings\n",
              "{\n",
              "  \"maxres\" \"" + str(resolutionNormal) + "\"\n",
              "}"
            ]

            templateResolutionRoughness = [
              "settings\n",
              "{\n",
              "  \"maxres\" \"" + str(resolutionRoughness) + "\"\n",
              "}"
            ]

            templateResolutionMetalness = [
              "settings\n",
              "{\n",
              "  \"maxres\" \"" + str(resolutionMetallness) + "\"\n",
              "}"
            ]

            templateResolutionAmbientOcclusion = [
              "settings\n",
              "{\n",
              "  \"maxres\" \"" + str(resolutionAmbientOcclusion) + "\"\n",
              "}"
            ]

            # Create resolution txt files if needed
            if os.path.exists(assetIdDir + '_color.' + downloadFormat.lower() + ''):
              makeColorTxt = open(assetIdDir + '_color.txt',"w+")
              makeColorTxt.writelines(templateResolutionColor)
              makeColorTxt.close()
            
            if os.path.exists(assetIdDir + '_normal.' + downloadFormat.lower() + ''):
              makeNormalTxt = open(assetIdDir + '_normal.txt',"w+")
              makeNormalTxt.writelines(templateResolutionNormal)
              makeNormalTxt.close()
            
            if os.path.exists(assetIdDir + '_roughness.' + downloadFormat.lower() + ''):
              makeRoughnessTxt = open(assetIdDir + '_roughness.txt',"w+")
              makeRoughnessTxt.writelines(templateResolutionRoughness)
              makeRoughnessTxt.close()
            
            if os.path.exists(assetIdDir + '_metalness.' + downloadFormat.lower() + ''):
              makeMetalnessTxt = open(assetIdDir + '_metalness.txt',"w+")
              makeMetalnessTxt.writelines(templateResolutionMetalness)
              makeMetalnessTxt.close()
            
            if os.path.exists(assetIdDir + '_ambientocclusion.' + downloadFormat.lower() + ''):
              makeAmbientOcclusionTxt = open(assetIdDir + '_ambientocclusion.txt',"w+")
              makeAmbientOcclusionTxt.writelines(templateResolutionAmbientOcclusion)
              makeAmbientOcclusionTxt.close()
          else:
            # Remove asset directory
            shutil.rmtree(assetDir)

    elif 'sbsar' in asset['downloadFolders']['/']['downloadFiletypeCategories']:
      # Loop over the available sbsar files
      for assetDownload in asset['downloadFolders']['/']['downloadFiletypeCategories']['sbsar']['downloads']:
        # Get the assets that match your quality
        if (assetDownload['attribute'] == downloadSbsarQuality.upper()) or (assetDownload['attribute'] == ''):

          ###############################################################################
          # Download sbsar file
          ###############################################################################

          # Counter and file size
          assetTotalCounter += 1
          print("{}) {}".format(assetTotalCounter, assetId))
          assetTotalSize = assetTotalSize + int(assetDownload['size'])
          
          download = assetDownload['downloadLink']

          downloadSbsar = requests.get(download, headers=headers, allow_redirects=True)

          sbsar = open(root + '\\' + assetId + '.sbsar', 'wb')
          sbsar.write(downloadSbsar.content)
          sbsar.close()

  assetCounter += 100

# Remove temporary directory with all the zip filesos.remove(filePath)
shutil.rmtree(root + '\\tmp')

#  Remove the unused *displacement.jpg files
fileList = glob.glob(root + '\\*\\*displacement.jpg')
for filePath in fileList:
  os.remove(filePath)

# Print
print("\nFinished!\n")
print('Total downloaded assets: ' + str(assetTotalCounter))
print('Total download size: ' + str(sizeFormat(assetTotalSize)) + "\n")
print('Assets stored in: ' + root + "\n")
os.system("pause")
