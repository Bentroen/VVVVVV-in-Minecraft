from PIL import Image
import zipfile


source_path = "../data.zip"

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


# TODO: Move this class to a separate module in the future to unify data access
# TODO: Implement context manager to automatically close files
class AssetLoader:
    def __init__(self):
        self._assets = zipfile.ZipFile(source_path)

    def load_img(self, filename: str) -> Image:
        data = self._assets.open(filename)
        return Image.open(data)


if __name__ == "__main__":
    TileGrabber()
