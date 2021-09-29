from PIL import Image
import zipfile

source_path = "../data.zip"

tilemaps = ["graphics/tiles.png", "graphics/tiles2.png", "graphics/tiles3.png"]


class TileGrabber:
    def __init__(self):
        self._tilemaps = self._init_tilemaps()

    def _init_tilemaps(self):
        assets = AssetLoader(source_path)
        for filename in tilemaps:
            file = assets.load(filename)
            img = Image.open(file)
            self._tilemaps.append(img)

    def get_tile(self, id: int, tileset: int) -> Image:
        img = self._tilemaps[tileset]
        x, y = divmod(id, img.width / 8)
        return img.crop(x, y, x * 8, y * 8)


# TODO: Move this class to a separate module in the future to unify data access
class AssetLoader:
    def __init__(self, path: str):
        self._assets = self._init_assets(path)

    def _init_assets(self, path: str) -> zipfile.ZipFile:
        return zipfile.ZipFile(path, "r")

    def load(self, filename: str):
        return self._assets.read(filename)
