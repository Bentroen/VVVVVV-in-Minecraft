from beet import Context, Texture, Model, Structure
from nbtlib import tag
import numpy as np

from .image import MapAssembler
from . import map_data


# TODO: Room placement functions
# TODO: Animated tiles
# TODO: Background separation
# TODO: Remove transparent slices from the pack, and possibly add deduplication

def beet_default(ctx: Context):

    rooms = map_data.fetch_map_data()

    ### MODELS/TEXTURES

    image = MapAssembler(rooms)
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

    ### FUNCTIONS

    # Collision maps

    max_height = max(
        map_data.get_room_stack_position(*tuple(int(x) for x in room.split(",")))[1]
        for room in rooms
    )

    width = 40  # room width
    height = max_height + 1  # height of tallest stack
    length = 30 * 3 + 2  # length of three rooms stacked with a single block gap

    blocks = np.zeros((length, height, width))

    for room_number, room in rooms.items():
        rx, ry = tuple(int(x) for x in room_number.split(","))
        tiles = room["tiles"]
        tileset = room["tileset"]

        stack, index = map_data.get_room_stack_position(rx, ry)

        for i, row in enumerate(tiles):
            for j, tile in enumerate(row):

                tile_type = map_data.tile_type(tileset, tile)

                if tile_type == "wall":
                    block = 1
                elif tile_type == "spike":
                    block = 2
                elif tile_type == "background":
                    block = 3

                x = stack * 31 + (29 - i)
                y = index
                z = j

                blocks[x, y, z] = block

    ctx.data["vvvvvv:map_collision"] = get_collision_structure(blocks)


def get_base_model(texture: str) -> dict:
    return {"parent": "vvvvvv:base/10x10", "textures": {"texture": texture}}


def get_base_multipart() -> dict:
    return {"parent": "vvvvvv:base/10x10", "overrides": []}


def get_predicate(cmd: int, model: str) -> dict:
    return {"predicate": {"custom_model_data": cmd}, "model": model}


def get_collision_structure(blocks: np.array) -> Structure:
    """Return a `Structure` for the blocks in the input array."""

    return Structure(
        {
            "DataVersion": tag.Int(2730),  # 1.17.1
            "size": [tag.Int(x) for x in blocks.shape],
            "palette": [
                {"Name": "minecraft:air"},
                {"Name": "minecraft:black_concrete"},
                {"Name": "minecraft:red_concrete"},
                {"Name": "minecraft:white_concrete"},
            ],
            "blocks": [
                {"pos": coords, "state": tag.Int(block)}
                for coords, block in np.ndenumerate(blocks)
            ],
        }
    )
