from map import fetch_map_data
from tiles import TileGrabber

from PIL import Image
import numpy as np


CACHE_ROOMS = True
CACHE_MAP = True

rooms = fetch_map_data()
tile_loader = TileGrabber()


class RoomGenerator:
    pass


class MapAssembler:
    """
    Assembles room images from room tilemaps, tilesets and tile images.
    """

    def create_map_img(self, rooms: dict, rescale_factor: int = 8) -> Image:
        """
        Creates a large image containing all rooms. Only meant
        to preview room placement; not used in asset generation.
        """

        map_width = 320 * 79 // rescale_factor
        map_height = 240 * 72 // rescale_factor

        map_img = Image.new("RGBA", (map_width, map_height))

        for room_number, room_img in self.get_room_imgs(rooms):
            print(f"Processing room {room_number}")

            if CACHE_ROOMS:
                room_img.save(f".cache/rooms/{room_number}.png")

            new_width = room_img.width // rescale_factor
            new_height = room_img.height // rescale_factor

            room_img = room_img.resize((new_width, new_height))
            rx, ry = (int(x) for x in room_number.split(","))
            map_img.paste(room_img, ((rx - 41) * new_width, (ry - 48) * new_height))

        return map_img

    def get_room_imgs(self, rooms: dict) -> Iterator[tuple[str, Image.Image]]:
        for room_number, room in rooms.items():
            tiles = np.array(room["tiles"])
            tileset = room["tileset"]
            yield room_number, self.get_room_img(tiles, tileset)

    def get_room_img(self, tiles: np.array, tileset: int) -> Image:
        room = Image.new("RGBA", (320, 240))

        for y, x in np.ndindex(tiles.shape):
            id = int(tiles[y, x])
            tile = tile_loader.get_tile(id, tileset)
            room.paste(tile, (x * 8, y * 8))

        return room


if __name__ == "__main__":
    map_builder = MapAssembler()
    map = map_builder.create_map_img(rooms)
    map.save(f".cache/map.png")
