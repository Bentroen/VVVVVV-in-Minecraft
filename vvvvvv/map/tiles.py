from PIL import Image
import zipfile

source_path = "../data.zip"

tilemaps = ["graphics/tiles.png", "graphics/tiles2.png", "graphics/tiles3.png"]


class TileGrabber:
    def __init__(self):
        self._tilemaps = self._init_tilemaps()

    def _init_tilemaps(self):
        tilemaps = []
        loader = AssetLoader(source_path)
        for file in tilemaps:
            img = loader.load_img(file)
            tilemaps.append(img)
        return tilemaps

    def get_tile(self, id: int, tileset: int) -> Image:
        img = self._tilemaps[tileset]
        x, y = divmod(id, img.width / 8)
        return img.crop(x, y, x * 8, y * 8)


# TODO: Move this class to a separate module in the future to unify data access
class AssetLoader:
    def __init__(self, path: str):
        self._assets = zipfile.ZipFile(path)

    def load_img(self, filename: str) -> Image:
        with self._assets.open(filename) as f:
            return Image.open(f)


if __name__ == "__main__":
    TileGrabber()
