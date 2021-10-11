from PIL import Image
from ..utils.file import AssetLoader


tilemaps = ["graphics/tiles.png", "graphics/tiles2.png", "graphics/tiles3.png"]


class TileGrabber:
    def __init__(self):
        self._tiles = []
        self._init_tiles()

    def _init_tiles(self):
        loader = AssetLoader()
        for file in tilemaps:
            img = loader.load_img(file)
            for y in range(img.height // 8):
                for x in range(img.width // 8):
                    tile = img.crop((x * 8, y * 8, x * 8 + 8, y * 8 + 8))
                    self._tiles.append(tile)

    def get_tile(self, id: int, tileset: int) -> Image:
        return self._tiles[tileset * 1200 + id]


if __name__ == "__main__":
    TileGrabber()
