import zipfile
from PIL import Image

source_path = "../data.zip"


class AssetLoader:
    # TODO: Implement context manager to automatically close files
    def __init__(self):
        self._assets = zipfile.ZipFile(source_path)

    def load_img(self, filename: str) -> Image:
        data = self._assets.open(filename)
        return Image.open(data)
