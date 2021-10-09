from typing import Iterator
from beet import Context, Texture, Model, Structure
from nbtlib import tag
import numpy as np

from .image import MapAssembler
from . import map_data


# TODO: Room placement functions
# TODO: Animated tiles
# TODO: Background separation
# TODO: Load towers
# TODO: Create alt versions for rooms in final level with tile changes
# TODO: (as well as those that change on time trials etc.)
# TODO: Think about flip mode?


def beet_default(ctx: Context):

    rooms = map_data.fetch_map_data()

    modelgen = ModelGenerator()
    for id, model, texture in modelgen.generate(rooms):
        ctx.assets[f"vvvvvv:rooms/{id}"] = model
        ctx.assets[f"vvvvvv:rooms/{id}"] = texture
    ctx.assets["minecraft:item/diamond_hoe"] = modelgen.get_multipart()

    structure = CollisionGenerator().generate(rooms)
    ctx.data["vvvvvv:map_collision"] = structure


class ModelGenerator:
    def __init__(self):
        self._multipart = self._get_multipart_base()

    def generate(self, rooms: dict) -> Iterator[tuple[str, Model, Texture]]:
        image = MapAssembler(rooms)
        slices, sliced_rooms = image.slice_rooms_deduplicated(10)

        for room_count, (room_number, slice_hashes) in enumerate(sliced_rooms.items()):
            rx, ry = tuple(int(x) for x in room_number.split(","))

            print(f"Processing room {room_count+1}")

            for slice_count, hash in enumerate(slice_hashes):

                id = f"{rx}_{ry}_{slice_count}"
                filename = f"vvvvvv:rooms/{hash}"
                texture = Texture(slices[hash])
                model = Model(self._get_base_model(filename))

                yield hash, texture, model

                cmd = room_count * 12 + slice_count + 1
                self._multipart["overrides"].append(
                    self._get_multipart_predicate(cmd, filename)
                )

    def get_multipart(self) -> Model:
        return Model(self._multipart)

    def _get_base_model(self, texture: str) -> dict:
        return {"parent": "vvvvvv:base/10x10", "textures": {"texture": texture}}

    def _get_multipart_base(self) -> dict:
        return {"parent": "vvvvvv:base/10x10", "overrides": []}

    def _get_multipart_predicate(self, cmd: int, model: str) -> dict:
        return {"predicate": {"custom_model_data": cmd}, "model": model}


class CollisionGenerator:
    def generate(self, rooms: dict) -> Structure:
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

        return self._get_structure(blocks)

    def _get_structure(self, blocks: np.array) -> Structure:
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


# class LoadFunctionGenerator:

#    yield Function()
