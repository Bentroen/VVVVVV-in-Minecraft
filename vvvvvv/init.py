from beet import Context, FunctionTag
from PIL import Image


def beet_default(ctx: Context):
    # Set up tick and load functions
    ctx.data["minecraft:load"] = FunctionTag({"values": ["vvvvvv:load"]})
    ctx.data["minecraft:tick"] = FunctionTag({"values": ["vvvvvv:tick"]})
