from PIL import Image
import os
import shutil

side = 16  # int(input())
path = './tiles/'
input_path = path + "input_tileset.png"


def parse_tiles(file_name: str = input_path,
                tile_size: int = side,
                output_path: str = path + 'parsed/'):

    if not output_path.endswith('/'):
        output_path += '/'

    number = 0
    spritesheet = Image.open(file_name)
    if len(os.listdir()) >= 1:
        shutil.rmtree(output_path)
    os.makedirs(output_path, exist_ok=True)
    for i in range(0, int(spritesheet.size[0] / tile_size)):
        for j in range(0, int(spritesheet.size[0] / tile_size)):
            number += 1
            box = (tile_size * i, tile_size * j, tile_size * (i + 1), tile_size * (j + 1))
            tile = spritesheet.crop(box)

            if not len(tile.convert("1").getcolors()) == 1 and tile.getbbox() is not None:
                print(f'Tile "tile{number}.png" is saved.')
                tile.save(path + f'parsed/tile{number}.png')
            else:
                print(f'Tile "tile{number}.png" is fully opacity. Skipping.')


def parse_tileset(folder_path: str = f'{path}parsed',
                  tile_size: int = side,
                  output_file: str = f'{path}output_tileset.png'):
    if not folder_path.endswith('/'):
        folder_path += '/'

    os.makedirs(folder_path, exist_ok=True)
    files = os.listdir(folder_path)
    image_size = calculate_size(folder_path, tile_size)
    print(calculate_size(folder_path, tile_size))
    output_tileset = Image.new('RGBA', image_size)
    ignored_files = []
    x = 0
    y = 0

    for i in range(0, len(files) - 1):
        image = Image.open(f'{folder_path}{files[i]}')
        #print([files[i], len(image.convert("1").getcolors()), image.getbbox()])
        if len(image.convert("1").getcolors()) == 1 and image.getbbox() is None:
            ignored_files.append(files[i])

    for j in files:
        if j not in ignored_files:
            tile_to_add = Image.open(f'{folder_path}{j}')
            box = (tile_size * x, tile_size * y, tile_size * (x + 1), tile_size * (y + 1))
            print([j, box, [x, y]])
            output_tileset.paste(tile_to_add, box)
            y += 1
            if y == image_size[0] // tile_size:
                y = 0
                x += 1
        else:
            print(f'Ignoring {j}')

    output_tileset.save(output_file)


def calculate_size(folder_path: str = f'{path}parsed',
                   tile_size: int = side):
    os.makedirs(folder_path, exist_ok=True)
    files = os.listdir(folder_path)
    image_side = round(len(files) ** 0.5 * tile_size)

    if image_side <= 64:
        image_size = (64, 64)
        return image_size
    elif 64 < image_side <= 256:
        image_size = (256, 256)
        return image_size
    elif 256 < image_side <= 512:
        image_size = (512, 512)
        return image_size
    elif 512 < image_side <= 1024:
        image_size = (1024, 1024)
        return image_size
    elif 1024 < image_side <= 2048:
        image_size = (2048, 2048)
        return image_size
    elif 2048 < image_side <= 4096:
        image_size = (4096, 4096)
        return image_size


parse_tiles('./tiles/celeste_tileset.png', side)
print(calculate_size(tile_size=side))
parse_tileset(tile_size=side)
