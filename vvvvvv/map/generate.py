from beet import Context, Texture, Model

from .image import MapAssembler
from . import map_data


# TODO: Room placement functions
# TODO: Animated tiles
# TODO: Background separation
# TODO: Remove transparent slices from the pack, and possibly add deduplication
# TODO: Map each room's coordinates to a position in a stack (for placing collision maps)
# TODO: Add collision maps (map spikes, backgrounds and solid blocks)

def beet_default(ctx: Context):

    image = MapAssembler(fetch_map_data())
    multipart = get_base_multipart()

    sliced_rooms = image.slice_rooms(10)

    for room_count, (room_number, slices) in enumerate(sliced_rooms.items()):
        rx, ry = tuple(int(x) for x in room_number.split(","))

        for slice_count, slice in enumerate(slices):
            id = f"{rx}_{ry}_{slice_count}"
            filename = f"vvvvvv:rooms/{id}"
            ctx.assets[filename] = Texture(slice)
            ctx.assets[filename] = Model(get_base_model(filename))

            cmd = room_count * 12 + slice_count + 1
            multipart["overrides"].append(get_predicate(cmd, filename))

            # ctx.data[filename + ".mcfunction"] = Function([lines], tags=["minecraft:load"])

    ctx.assets["minecraft:item/diamond_hoe"] = Model(multipart)


def get_base_model(texture: str) -> dict:
    return {"parent": "vvvvvv:base/10x10", "textures": {"texture": texture}}


def get_base_multipart() -> dict:
    return {"parent": "vvvvvv:base/10x10", "overrides": []}


def get_predicate(cmd: int, model: str) -> dict:
    return {"predicate": {"custom_model_data": cmd}, "model": model}
