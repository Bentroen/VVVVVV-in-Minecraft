from typing import Iterator
from PIL import Image
import numpy as np

from .map import fetch_map_data
from .tiles import TileGrabber


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

    def __init__(self, rooms: dict):
        self._rooms = rooms

    def get_map_preview(self, rescale_factor: int = 8) -> Image:
        """
        Creates a large image containing all rooms. Only meant
        to preview room placement; not used in asset generation.
        """

        room_numbers = [tuple(room.split(",")) for room in self._rooms.keys()]

        minx = min((int(rn[0]) for rn in room_numbers))
        maxx = max((int(rn[0]) for rn in room_numbers))
        miny = min((int(rn[1]) for rn in room_numbers))
        maxy = max((int(rn[1]) for rn in room_numbers))

        width = maxx - minx + 1
        height = maxy - miny + 1

        map_width = 320 * width // rescale_factor
        map_height = 240 * height // rescale_factor

        map_img = Image.new("RGBA", (map_width, map_height))

        for room_number, room_img in self.get_room_imgs():
            print(f"Processing room {room_number}")

            if CACHE_ROOMS:
                room_img.save(f".cache/rooms/{room_number}.png")

            new_width = room_img.width // rescale_factor
            new_height = room_img.height // rescale_factor

            room_img = room_img.resize((new_width, new_height))
            rx, ry = (int(x) for x in room_number.split(","))
            map_img.paste(room_img, ((rx - minx) * new_width, (ry - miny) * new_height))

        return map_img

    def slice_rooms(self, cell_size: int) -> dict[str, Image.Image]:
        """Return a `dict` containing room numbers as keys and sliced room images as values."""

        return {
            rn: self.slice_room(rimg, cell_size) for rn, rimg in self.get_room_imgs()
        }

    def slice_room(self, room_img: Image.Image, cell_size: int) -> list[Image.Image]:
        """Slice a room into a square panel with sides of `cell_size` tiles."""

        if 30 % cell_size > 0 or 40 % cell_size > 0:
            raise ValueError("Cell size must be a factor of 30 and 40 (1, 2, 5, 10)")

        slices = []
        panel_size = cell_size * 8
        for y in range(30 // cell_size):
            for x in range(40 // cell_size):
                slice = room_img.crop(
                    (
                        x * panel_size,
                        y * panel_size,
                        x * panel_size + panel_size,
                        y * panel_size + panel_size,
                    )
                )
                slices.append(slice)
        return slices

    def get_room_imgs(self) -> Iterator[tuple[str, Image.Image]]:
        """
        Generator that yields `tuple`s containing the room number, and images for
        all rooms in this map.
        """

        for room_number in self._rooms:
            yield room_number, self.get_room_img(*room_number.split(","))

    def get_room_img(self, rx: int, ry: int) -> Image:
        """Get the room image for a room with coordinates given by `rx`,`ry`."""

        room = self.get_room(rx, ry)
        tiles = np.array(room["tiles"])
        tileset = room["tileset"]

        room_img = Image.new("RGBA", (320, 240))

        for y, x in np.ndindex(tiles.shape):
            id = int(tiles[y, x])
            tile = tile_loader.get_tile(id, tileset)
            room_img.paste(tile, (x * 8, y * 8))

        return room_img

    def get_room(self, rx: int, ry: int) -> dict:
        """Get the room data for a room with coordinates given by `rx`,`ry`."""

        return self._rooms[f"{rx},{ry}"]


if __name__ == "__main__":
    map_builder = MapAssembler(rooms)

    map = map_builder.get_map_preview()
    map.save(f".cache/map.png")

    slices = map_builder.slice_rooms(10)
    for rn, slices in slices.items():
        for i, slice in enumerate(slices):
            slice.save(f".cache/slices/{rn.replace(',', '_')}_{i+1}.png")
