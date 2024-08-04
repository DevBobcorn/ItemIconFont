from PIL import Image, ImageOps
import os, glob, json
from json import JSONEncoder

proc_types = [
    'block',
    'item'
]

recolor_dict = {
    'minecraft:block/water_flow': (63, 118, 228),
    'minecraft:block/water_overlay': (63, 118, 228),
    'minecraft:block/water_still': (63, 118, 228),
    
    'minecraft:block/birch_leaves': (128, 167, 55),
    'minecraft:block/spruce_leaves': (97, 153, 97),
    'minecraft:block/lily_pad': (32, 128, 48),
    
    'minecraft:block/grass_block_top': (121, 192, 90),
    'minecraft:block/grass_block_side_overlay': (121, 192, 90),
    'minecraft:block/grass': (121, 192, 90),
    'minecraft:block/fern': (121, 192, 90),
    'minecraft:block/tall_grass_bottom': (121, 192, 90),
    'minecraft:block/tall_grass_top': (121, 192, 90),
    'minecraft:block/large_fern_bottom': (121, 192, 90),
    'minecraft:block/large_fern_top': (121, 192, 90),
    'minecraft:block/sugar_cane': (121, 192, 90),

    'minecraft:block/oak_leaves': (119, 171, 47),
    'minecraft:block/acacia_leaves': (119, 171, 47),
    'minecraft:block/jungle_leaves': (119, 171, 47),
    'minecraft:block/dark_oak_leaves': (119, 171, 47),
    'minecraft:block/vine': (119, 171, 47),
}

skip_list = []

def recolor(srci, col):
    #Preserve the alpha value before converting it..
    r,g,b,alpha = srci.split()
    gray = srci.convert('L')
    rec = ImageOps.colorize(gray, (0,0,0), (255,255,255), col, 0 ,255 ,157).convert('RGBA')
    #Recover its transparency..
    rec.putalpha(alpha)
    #rec.show()
    return rec

size = 1024
rct = 16
lncnt = int(size / rct) # How many textures in a line
print('Textures in a line: ' + str(lncnt))

atlas = Image.new('RGBA', (size, size), (0, 0, 0, 0))

offset = 0
i = 0
j = 0

atlas_dict = { }

root_path = f'{os.getcwd()}/'
res_path = f'{os.getcwd()}/assets'

class TextureInfo:
  def __init__(self, idx, x, y, code, desc):
    self.index = idx
    self.x = x
    self.y = y
    self.code = code
    self.desc = desc

class TextureInfoEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__

namespaces = os.listdir(res_path)
for nspath in namespaces:
    print(f'NameSpace: {nspath}')
    
    for proc_type in proc_types:
        paths = glob.iglob(f'{res_path}/{nspath}/textures/{proc_type}/**/*?.png', recursive=True) # Also search sub-folders...

        pathLen = len(f'{res_path}/{nspath}/textures/')

        for path in paths:
            texname = f'{nspath}:{path[pathLen:-4]}'
            texname = texname.replace('//', '/').replace('\\', '/')

            if texname in skip_list:
                print(f'Skipping {texname}')
                continue
            
            print(f'Processing {texname}')
            #print('\t\t\t[\"' + texname + '\"] = '+ str(offset) + ',')
            
            tex = Image.open(path).convert('RGBA')

            # Rescale if necessary
            if tex.width != rct:
                print(f'Rescaling {texname} to {rct}')
                tex = tex.resize((rct, round(tex.height / tex.width) * rct))

            # Crop if necessary
            if tex.width != tex.height:
                print(f'Cropping {texname}')
                tex = tex.crop((0, 0, tex.width, tex.width))
            
            # Recolor if necessary
            if recolor_dict.__contains__(texname):
                print(f'Recoloring {texname}')
                tex = recolor(tex, recolor_dict[texname])

            index = j * lncnt + i

            # Store its information
            info = TextureInfo(index, i * rct, j * rct, f'e{str(hex(index))[2:].zfill(3)}', path[pathLen:-4])
            atlas_dict[texname] = info

            # Paste it onto the atlas
            atlas.paste(tex, (info.x, info.y))
            
            i += 1
            offset += 1
            if i == lncnt:
                i = 0
                j += 1

with open(f'{root_path}/mc_atlas_dict_v1.json', 'w+') as f:
    data = json.dumps(atlas_dict, indent=4, separators=(',', ': '), cls=TextureInfoEncoder)
    f.write(data)

atlas.save(f'{root_path}/mc_atlas.png')
print('Done.')
