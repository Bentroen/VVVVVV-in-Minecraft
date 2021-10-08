from typing import Iterator
from beet import Context, Texture, Model, Structure
from nbtlib import tag
import numpy as np

from .image import MapAssembler
from . import map_data


# TODO: Room placement functions
# TODO: Animated tiles
# TODO: Background separation
# TODO: Remove transparent slices from the pack, and possibly add deduplication
# TODO: Load towers
# TODO: Create alt versions for rooms in final level with tile changes
# TODO: (as well as those that change on time trials etc.)
# TODO: Think about flip mode?


def beet_default(ctx: Context):

    rooms = map_data.fetch_map_data()

    for id, model, texture in ModelGenerator.generate(rooms):
        ctx.assets[f"vvvvvv:rooms/{id}"] = model
        ctx.assets[f"vvvvvv:rooms/{id}"] = texture

    ctx.assets["minecraft:item/diamond_hoe"] = ModelGenerator.get_multipart()

    structure = CollisionGenerator.generate(rooms, ctx)
    ctx.data["vvvvvv:map_collision"] = structure


class ModelGenerator:
    def __init__(self, rooms):
        self._multipart = self._get_multipart_base()

    @classmethod
    def generate(cls, rooms: dict) -> Iterator[tuple[str, Model, Texture]]:
        image = MapAssembler(rooms)
        sliced_rooms = image.slice_rooms(10)

        for room_count, (room_number, slices) in enumerate(sliced_rooms.items()):
            rx, ry = tuple(int(x) for x in room_number.split(","))

            for slice_count, slice in enumerate(slices):
                id = f"{rx}_{ry}_{slice_count}"
                filename = f"vvvvvv:rooms/{id}"
                texture = Texture(slice)
                model = Model(cls._get_base_model(filename))

                yield id, texture, model

                cmd = room_count * 12 + slice_count + 1
                cls._multipart["overrides"].append(
                    cls._get_multipart_predicate(cmd, filename)
                )
    
    @classmethod
    def get_multipart(cls) -> Model:
        return Model(cls._multipart())

    @classmethod
    def _get_base_model(cls, texture: str) -> dict:
        return {"parent": "vvvvvv:base/10x10", "textures": {"texture": texture}}

    @classmethod
    def _get_multipart_base(cls) -> dict:
        return {"parent": "vvvvvv:base/10x10", "overrides": []}

    @classmethod
    def _get_multipart_predicate(cls, cmd: int, model: str) -> dict:
        return {"predicate": {"custom_model_data": cmd}, "model": model}


class CollisionGenerator:
    @classmethod
    def generate(cls, rooms: dict) -> Structure:
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

        return cls._get_structure(blocks)

    @classmethod
    def _get_structure(cls, blocks: np.array) -> Structure:
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
