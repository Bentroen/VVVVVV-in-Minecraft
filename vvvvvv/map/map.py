import os
import json


source_path = "../../VVVVVV-master/desktop_version/src"


# https://github.com/TerryCavanagh/VVVVVV/blob/3decf54dbc9e7898a980086dc34a1bfbb52b16ac/desktop_version/src/Map.cpp#L88-L110
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


def _get_room_tileset(rx: int, ry: int) -> int:
    # https://github.com/TerryCavanagh/VVVVVV/blob/3decf54dbc9e7898a980086dc34a1bfbb52b16ac/desktop_version/src/Map.cpp#L1484
    area = _get_room_area(rx, ry)
    if area == 0 or area == 1:  # World Map (defined per room)
        tileset = None
    elif area == 5:  # Space Station
        tileset = 0
    else:
        tileset = 1
    return tileset


def _get_room_area(rx: int, ry: int) -> int:
    # https://github.com/TerryCavanagh/VVVVVV/blob/3decf54dbc9e7898a980086dc34a1bfbb52b16ac/desktop_version/src/Map.cpp#L742-L760
    # https://github.com/TerryCavanagh/VVVVVV/blob/3decf54dbc9e7898a980086dc34a1bfbb52b16ac/desktop_version/src/Map.cpp#L1382-L1413
    if rx - 100 >= 0 and rx - 100 < 20 and ry - 100 >= 0 and ry - 100 < 20:
        return areamap[rx - 100][ry - 100]
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


class LevelParser:

    levels = [
        "Spacestation2.cpp",
        "Labclass.cpp",
        "WarpClass.cpp",
        "Otherlevel.cpp",
        "Finalclass.cpp"
        # "Tower.cpp" special case - needs different handling
    ]

    def __init__(self):
        self.rooms = self._parse_files()

    def _parse_files(self) -> dict:
        areas = {}
        for level in self.levels:
            path = os.path.join(source_path, level)
            areas.update(self._parse_file(path))
        return areas

    def _parse_file(self, path: str) -> dict:
        rooms = {}
        state = None
        with open(path) as f:
            for line in f.readlines():
                line = line.strip()

                # TODO: Cache folder creation on __init__.py
                # TODO: Handle special cases (tiles/entities that change on time trial mode etc.)
                # TODO: Do not export unnecessary properties to JSON (i.e. when warpx/y is false)

                if not state:  # Find start of level data
                    if line == "#if !defined(MAKEANDPLAY)":
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
                        row = line.strip(",").split(",")
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
                        x, y = (int(x) for x in room_number.split(","))
                        room["roomname"] = roomname
                        room["tiles"] = tiles
                        room["entities"] = entities
                        room["color"] = color
                        room["tileset"] = (
                            tileset if tileset else _get_room_tileset(x, y)
                        )
                        room["warpx"] = warpx
                        room["warpy"] = warpy
                        rooms[room_number] = room
                        state = "rooms"

        return rooms

    def _split_parentheses(self, line: str, convert_numbers: bool = False) -> str:
        string = line.split("(")[1].split(")")[0]
        if convert_numbers:
            return tuple(int(x) for x in string.split(","))
        else:
            return string


def _generate_map_data(path: str) -> dict:
    rooms = LevelParser().rooms
    with open(path, "w") as f:
        json.dump(rooms, f)
    return rooms


def fetch_map_data(force_update: bool = False) -> dict:
    outpath = os.path.join(".cache", "map.json")
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
