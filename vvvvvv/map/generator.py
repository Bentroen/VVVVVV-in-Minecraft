from map import fetch_map_data
from tiles import TileGrabber

from PIL import Image
import numpy as np


rooms = fetch_map_data()
tile_loader = TileGrabber()


huge_map = Image.new("RGBA", (12800, 9600))

for room_number, room in rooms.items():
    tiles = np.array(room["tiles"])

    map = Image.new("RGBA", (320, 240))
    print(f"Processing room {room_number}")

    for y, x in np.ndindex(tiles.shape):
        id = int(tiles[y, x])
        img = tile_loader.get_tile(id, room["tileset"])

        map.paste(img, (x * 8, y * 8))
    map.save(f".cache/rooms/{room_number}.png")

    xx, yy = (int(x) for x in room_number.split(","))
    map = map.resize((80, 60))
    huge_map.paste(map, ((xx - 40) * 80, (yy - 40) * 60))

huge_map = huge_map.crop(huge_map.getbbox())
huge_map.save(".cache/huge_map.png")
