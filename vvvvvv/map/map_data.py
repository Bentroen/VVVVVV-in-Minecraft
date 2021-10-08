import os
import json


source_path = "../VVVVVV-master/desktop_version/src"


def _get_room_area(rx: int, ry: int) -> int:
    """Return the area (0-11) for a room with coordinates given by `rx`,`ry`."""

    # https://github.com/TerryCavanagh/VVVVVV/blob/2.3.4/desktop_version/src/Map.cpp#L88-L110

    areamap = [
        [1, 2, 2, 2, 2, 2, 2, 2, 0, 3, 0, 0, 0, 4, 4, 4, 4, 4, 4, 4],
        [1, 2, 2, 2, 2, 2, 2, 0, 0, 3, 0, 0, 0, 0, 4, 4, 4, 4, 4, 4],
        [0, 1, 0, 0, 2, 0, 0, 0, 0, 3, 0, 0, 0, 0, 4, 4, 4, 4, 4, 4],
        [0, 0, 0, 0, 2, 0, 0, 0, 0, 3, 0, 0, 5, 5, 5, 5, 4, 4, 4, 4],
        [0, 0, 2, 2, 2, 0, 0, 0, 0, 3, 11, 11, 5, 5, 5, 5, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 5, 5, 5, 5, 5, 5, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 5, 5, 5, 5, 5, 5, 5, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 5, 5, 5, 5, 5, 5, 5, 5, 5, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 5, 5, 5, 5, 5, 5, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 11, 3, 0, 0, 0, 5, 5, 5, 5, 5, 5, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 5, 5, 5, 5, 5, 5, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 5, 5, 5, 5, 5, 5, 5, 5, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 5, 5, 5, 5, 5, 5, 0, 5, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 5, 5, 5, 5, 5, 5, 0, 5, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 5, 5, 0, 0, 0, 0, 0, 5, 0],
        [0, 0, 0, 0, 0, 0, 0, 2, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 2, 2, 2, 2, 2, 2, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 2, 2, 2, 2, 2, 2, 2, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [2, 2, 2, 2, 2, 0, 0, 2, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [2, 2, 2, 2, 2, 0, 0, 2, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    ]

    # https://github.com/TerryCavanagh/VVVVVV/blob/2.3.4/desktop_version/src/Map.cpp#L742-L760
    # https://github.com/TerryCavanagh/VVVVVV/blob/2.3.4/desktop_version/src/Map.cpp#L1382-L1413

    if rx - 100 >= 0 and rx - 100 < 20 and ry - 100 >= 0 and ry - 100 < 20:
        # world map, grab from areamap
        return areamap[ry - 100][rx - 100]
    else:
        if rx == 49 and ry == 52:
            # entered tower 1
            return 7
        elif rx == 49 and ry == 53:
            # re-entered tower 1
            return 8
        elif rx == 51 and ry == 54:
            # entered tower 2
            return 9
        elif rx == 51 and ry == 53:
            # re-entered tower 2
            t = 10
        else:
            return 6


def _get_room_tileset(rx: int, ry: int) -> int:
    """Return the tileset (0-2) for a room with coordinates given by `rx`,`ry`."""

    # https://github.com/TerryCavanagh/VVVVVV/blob/2.3.4/desktop_version/src/Map.cpp#L1484-L1660

    area = _get_room_area(rx, ry)
    if area == 5:  # Space Station
        tileset = 0
    elif area == 11:  # The Tower (entrance and exit)
        tileset = 2
    else:  # 0-4, 6-10 (rest of world map, final level)
        tileset = 1
    return tileset


def tile_is_solid(tileset: int, tile: int) -> bool:
    # https://github.com/TerryCavanagh/VVVVVV/blob/2.3.4/desktop_version/src/Map.cpp#L682-L731

    if (
        tile == 1
        or (tileset == 0 and tile == 59)
        or (tile >= 80 and tile < 680)
        or (tileset == 1 and tile == 740)
    ):
        return True
    else:
        return False


def tile_type(tileset: int, tile: int) -> str:
    # Extends `tile_is_solid` to tell if a non-solid tile is a spike as well.
    # https://github.com/TerryCavanagh/VVVVVV/blob/2.3.4/desktop_version/src/Map.cpp#L682-L731

    if tile_is_solid(tileset, tile):
        return "wall"

    else:
        if tileset == 0:
            if (
                (tile >= 6 and tile <= 9)
                or (tile >= 49 and tile <= 50)
                or (tile >= 1080 and tile <= 1085)
                or (tile >= 1120 and tile <= 1125)
                or (tile >= 1160 and tile <= 1165)
            ):
                return "spike"
            else:
                return "background"

        elif tileset == 1:
            if (tile >= 6 and tile <= 9) or (tile >= 49 and tile <= 80):
                return "spike"
            else:
                return "background"


def get_room_stack_position(rx: int, ry: int) -> tuple[int, int]:
    """Map every room in the world map to a position in one of three stacks.
    "Related" rooms are grouped in the same stack. Useful to store rooms in
    a linear structure without gaps.
    """

    # Custom function. Used to determine the location of collision maps inside the world

    if rx >= 100 and rx < 120:
        if rx <= 108:  # World Map (left of The Tower)
            stack = 0
            index = (ry - 100) * 8 + (rx - 100)

        else:  # World Map (right of The Tower)
            stack = 1
            index = (ry - 100) * 10 + (rx - 110)

    else:
        stack = 2
        if ry == 56 and rx >= 41 and rx <= 54:  # Intermission 1
            index = rx - 41
        elif rx == 53 and ry >= 48 and ry <= 52:  # Intermission 2
            index = 14 + (ry - 48)
        else:  # Final level
            # Order of rooms when you first visit them, without repetition
            order = [
                (46, 54),
                (47, 54),
                (48, 54),
                (49, 54),
                (50, 54),
                (50, 53),
                (50, 52),
                (50, 51),
                (49, 51),
                (48, 51),
                (47, 51),
                (46, 51),
                (45, 51),
                (44, 51),
                (43, 51),
                (42, 51),
                (41, 51),
                (41, 52),
                (42, 52),
                (43, 52),
                (44, 52),
                (45, 52),
                (47, 52),
                (48, 52),
                (52, 53),
                (53, 53),
                (54, 53),
                (54, 52),
                (54, 51),
                (54, 50),
                (54, 49),
                (54, 48),
                (54, 47),
            ]
            index = 19 + order.index((rx, ry))

    return stack, index


class LevelParser:
    """Parse VVVVVV's `.cpp` files to extract level data, such as tiles and entities."""

    levels = [
        "Spacestation2.cpp",
        "Labclass.cpp",
        "WarpClass.cpp",
        "Otherlevel.cpp",
        "Finalclass.cpp"
        # "Tower.cpp" special case - needs different handling
    ]

    # Completely empty rooms (no tiles, entities or name) aren't defined in the game,
    # but tracking them explicitly will make our lives a bit easier.
    empty_rooms = [
        (101, 107),
        (102, 107),
        (104, 106),
        (104, 108),
        (106, 103),
        (107, 112),
        (107, 113),
        (111, 107),  # Super Gravitron
        (111, 115),
        (112, 115),
        (114, 115),
        (115, 115),
        (116, 115),
        (116, 116),
        (116, 118),
        (118, 116),
        (118, 118),
    ]

    def __init__(self):
        self.rooms = self._parse_files()
        self._add_empty_rooms()

    def _parse_files(self) -> dict[str, dict]:
        """
        Parse all files containing levels in the game's source. Returns a `dict`
        containing strings in the form `rx,ry` as keys and a room data `dict` as values.
        """

        areas = {}
        for level in self.levels:
            path = os.path.join(source_path, level)
            areas.update(self._parse_file(path))
        return areas

    def _parse_file(self, path: str) -> dict:
        """Parse an individual file. Returns a `dict` containing the room data."""

        rooms = {}
        state = None
        with open(path) as f:
            for line in f.readlines():
                line = line.strip()

                # TODO: Cache folder creation on __init__.py
                # TODO: Handle special cases (tiles/entities that change on time trial mode etc.)
                # TODO: Do not export unnecessary properties to JSON (i.e. when warpx/y is false)

                if not state:  # Find start of level data
                    if line == "switch(t)":
                        state = "rooms"

                elif state == "rooms":
                    if line.startswith("case rn"):  # case rn(##,##):
                        room_number = self._split_parentheses(line)
                    elif line.startswith(
                        "static const short contents"
                    ):  # New room begins
                        state = "tiles"
                        room = {}
                        tiles = []
                        entities = []
                        color = 0
                        tileset = None
                        warpx = False
                        warpy = False
                        roomname = ""
                    elif line == "#endif":  # End of rooms
                        break

                elif state == "tiles":
                    if line != "};":  # Tile row
                        row = [int(x) for x in line.strip(",").split(",")]
                        tiles.append(row)
                    else:  # End of tilemap
                        state = "entities"

                elif state == "entities":
                    if line.startswith("obj.createentity"):
                        entity = self._split_parentheses(line, convert_numbers=True)
                        entities.append(entity)
                    else:
                        state = "metadata"

                elif state == "metadata":
                    if line.startswith("rcol"):
                        color = int(line.split("=")[1].strip(" ").strip(";"))
                    if line.startswith("warpx"):
                        warpx = "true" in line
                    elif line.startswith("warpy"):
                        warpy = "true" in line
                    elif line.startswith("roomname"):
                        roomname = line.split('"')[1]
                    elif line.startswith("roomtileset"):
                        tileset = int(line.split("=")[1].strip(" ").split(";")[0])
                    elif line.startswith("break"):  # End of room
                        rx, ry = (int(x) for x in room_number.split(","))
                        rx, ry = self._get_area_offset(path, rx, ry)
                        # rn = rx + (ry * 100)

                        room["roomname"] = roomname
                        room["tiles"] = tiles
                        room["entities"] = entities
                        room["color"] = color

                        # For some rooms the tileset is defined on the room
                        # itself, so we only look it up in case it's not
                        room["tileset"] = (
                            tileset if tileset else _get_room_tileset(rx, ry)
                        )

                        room["warpx"] = warpx
                        room["warpy"] = warpy
                        rooms[f"{rx},{ry}"] = room
                        state = "rooms"

        return rooms

    def _add_empty_rooms(self):
        for rx, ry in self.empty_rooms:
            self.rooms[f"{rx},{ry}"] = {
                "tiles": [[0 for i in range(40)] for j in range(30)],
                "tileset": _get_room_tileset(rx, ry),
            }

    def _get_area_offset(self, area: str, rx: int, ry: int) -> tuple[int, int]:
        """Return the room coordinates with that room's offset applied."""

        if "Finalclass.cpp" not in area:
            # https://github.com/TerryCavanagh/VVVVVV/blob/2.3.4/desktop_version/src/Finalclass.cpp#L11-L14
            rx += 100
            ry += 100

        if "Spacestation2.cpp" in area:
            # https://github.com/TerryCavanagh/VVVVVV/blob/2.3.4/desktop_version/src/Spacestation2.cpp#L10-L14
            rx -= 50 - 12
            ry -= 50 - 14

        elif "Labclass.cpp" in area:
            # https://github.com/TerryCavanagh/VVVVVV/blob/2.3.4/desktop_version/src/Labclass.cpp#L13-L22
            if ry - 100 - 48 > 5:
                rx -= 50 - 2
                ry -= 54  # Lab
            else:
                rx -= 50 - 2
                ry -= 50 - 16  # Lab

        elif "WarpClass.cpp" in area:
            # https://github.com/TerryCavanagh/VVVVVV/blob/2.3.4/desktop_version/src/WarpClass.cpp#L13-L14
            rx -= 50 - 14
            ry -= 49  # Warp

        return rx, ry

    def _split_parentheses(self, line: str, convert_numbers: bool = False) -> str:
        """
        Get the contents tuple containing the values inside parenthesis for strings in
        the form `prefix(value1, value2, value3...)`. If `convert_numbers` is `True`,
        return a tuple of the values split by commas (`,`); otherwise, return a string.
        """

        string = line.split("(")[1].split(")")[0]
        if convert_numbers:
            return tuple(int(x) for x in string.split(","))
        else:
            return string


def _generate_map_data(path: str) -> dict[str, dict]:
    """
    Regenerate the map data and save it to the cache. Returns a `dict` with strings in
    the form `rx,ry` for keys and `dict`s containing the room data as values.
    """

    rooms = LevelParser().rooms
    with open(path, "w") as f:
        json.dump(rooms, f)
    return rooms


def fetch_map_data(force_update: bool = False) -> dict[str, dict]:
    """
    Get the map data. If `force_update` is `True` OR the cache is not found, the data is
    regenerated; otherwise, it's retrieved from the cache.
    """

    outpath = os.path.join("vvvvvv", ".cache", "map.json")
    if force_update:
        return _generate_map_data(outpath)
    else:
        try:
            with open(outpath, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return _generate_map_data(outpath)


if __name__ == "__main__":
    fetch_map_data(force_update=True)
