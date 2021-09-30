from PIL import Image
import zipfile
import io

source_path = "../data.zip"

tilemaps = ["graphics/tiles.png", "graphics/tiles2.png", "graphics/tiles3.png"]


class TileGrabber:
    def __init__(self):
        self._tilemaps = []
        self._init_tilemaps()

    def _init_tilemaps(self):
        loader = AssetLoader()
        for file in tilemaps:
            img = loader.load_img(file)
            self._tilemaps.append(img)

    def get_tile(self, id: int, tileset: int) -> Image:
        img = self._tilemaps[tileset]
        y, x = divmod(id, img.width / 8)
        print(x * 8, y * 8)
        return img.crop((x * 8, y * 8, 8, 8))


# TODO: Move this class to a separate module in the future to unify data access
class AssetLoader:
    def __init__(self):
        self._assets = zipfile.ZipFile(source_path)

    def load_img(self, filename: str) -> Image:
        data = self._assets.open(filename)
        return Image.open(data)


if __name__ == "__main__":
    TileGrabber()
