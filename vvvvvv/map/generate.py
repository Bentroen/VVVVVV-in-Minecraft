from typing import Iterator
from beet import Context, Texture, Model, Structure, Function, TreeNode
from nbtlib import tag
import numpy as np
import time

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

    print("Retrieving map data...")
    start = time.time()
    rooms = map_data.fetch_map_data()
    image = MapAssembler(rooms)
    slices, sliced_rooms = image.slice_rooms_deduplicated(10)
    print(f"Retrieved map data. Operation took {time.time() - start} seconds.")

    print("Generating models...")
    start = time.time()
    modelgen = ModelGenerator()
    for id, model, texture in modelgen.generate(slices, sliced_rooms):
        ctx.assets[f"vvvvvv:rooms/{id + 1}"] = model
        ctx.assets[f"vvvvvv:rooms/{id + 1}"] = texture
    ctx.assets["minecraft:item/diamond_hoe"] = modelgen.get_multipart(
        list(slices.keys())
    )
    print(f"Models generated. Operation took {time.time() - start} seconds.")

    print("Generating collision structure...")
    start = time.time()
    structure = CollisionGenerator().generate(rooms)
    ctx.data["vvvvvv:map_collision"] = structure
    print(
        f"Generated collision structure. Operation took {time.time() - start} seconds."
    )

    print("Generating load functions...")
    start = time.time()
    functiongen = LoadFunctionGenerator()
    for id, func in functiongen.generate_rooms(rooms, sliced_rooms):
        ctx.data[f"vvvvvv:rooms/{id}"] = func

    room_coords = []
    for room in rooms.keys():
        rx, ry = tuple(int(x) for x in room.split(","))
        room_coords.append((rx, ry))
    room_coords.sort(key=map_data.room_coords_to_id)
    # TODO: Consider passing sorted room IDs and converting them back with `room_id_to_coords` in the leaf nodes

    functiongen.generate_tree(room_coords, ctx)
    print(f"Load functions generated. Operation took {time.time() - start} seconds.")


class ModelGenerator:
    def generate(
        self, slices: dict, sliced_rooms: dict
    ) -> Iterator[tuple[str, Model, Texture]]:
        for slice_ids in sliced_rooms.values():

            for id in slice_ids:

                filename = f"vvvvvv:rooms/{id + 1}"
                texture = Texture(slices[id])
                model = Model(self._get_base_model(filename))

                yield id, texture, model

    def get_multipart(self, slices: list) -> Model:
        multipart = self._get_multipart_base()
        for id, _ in enumerate(slices):
            predicate = self._get_multipart_predicate(id + 1, f"vvvvvv:rooms/{id + 1}")
            multipart["overrides"].append(predicate)
        return Model(multipart)

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


class LoadFunctionGenerator:
    def generate_rooms(
        self, rooms: dict, sliced_rooms: dict
    ) -> Iterator[tuple[str, Function]]:

        for room_number, slice_ids in sliced_rooms.items():
            lines = []

            for slice_number, slice_index in enumerate(slice_ids):
                lines.append(
                    (
                        f"data modify entity @e[type=armor_stand,tag=room{slice_number+1},limit=1] "
                        f"HandItems[0].tag.CustomModelData set value {slice_index+1}"
                    )
                )

            id = room_number.replace(",", "_")
            function = Function(lines)

            yield id, function

        # TODO: Add entities, room name, special cases and everything else!

    def generate_tree(self, room_list: list, ctx: Context):
        generate = ctx.generate["map"]
        for node, function in generate.function_tree(
            "load_room", room_list, key=map_data.room_coords_to_id
        ):
            if node.root:
                ctx.generate(Function([f"function {node.parent}"]))
            if node.partition(2):
                function.lines.append(
                    f"execute if score id room matches {node.range} run function {node.children}"
                )
            else:
                room_coords = "_".join(map(str, node.value))
                function.lines.append(
                    f"execute if score id room matches {node.range} run function vvvvvv:rooms/{room_coords}"
                )
