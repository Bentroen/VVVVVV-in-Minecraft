from beet import Context, PngFile, FunctionTag, Model
from PIL import Image
from .utils.file import AssetLoader


def beet_default(ctx: Context):
    # Add pack icons
    icon = AssetLoader().load_img("VVVVVV.png")
    ctx.data.icon = PngFile(icon)
    ctx.assets.icon = PngFile(icon)

    # Set up tick and load functions
    ctx.data["minecraft:load"] = FunctionTag({"values": ["vvvvvv:load"]})
    ctx.data["minecraft:tick"] = FunctionTag({"values": ["vvvvvv:tick"]})

    # Clear snow layer model for player platform
    ctx.assets["minecraft:block/snow_height14"] = Model({"elements": []})

