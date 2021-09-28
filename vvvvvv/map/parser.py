import os
import json

maps = [
    "Spacestation2.cpp",
    "Labclass.cpp",
    "Warpclass.cpp",
    "Otherlevel.cpp",
    "Finalclass.cpp"
    # "Tower.cpp" special case - needs different handling
]

source_path = "../VVVVVV-master/desktop_version/src"


def split_parentheses(line: str, convert_numbers: bool = False) -> str:
    string = line.split("(")[1].split(")")[0]
    if convert_numbers:
        return tuple(int(x) for x in string.split(","))
    else:
        return string


class MapParser:
    def __init__(self):
        self.rooms = self._parse_files()

    def _parse_files(self) -> dict:
        areas = {}
        for map in maps:
            path = os.path.join(source_path, map)
            areas[map] = self._parse_file(path)
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
                        room_number = split_parentheses(line)
                    elif line.startswith(
                        "static const short contents"
                    ):  # New room begins
                        state = "tiles"
                        room = {}
                        tiles = []
                        entities = []
                        color = 0
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
                        entity = split_parentheses(line, convert_numbers=True)
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
                    elif line.startswith("break"):  # End of room
                        room["roomname"] = roomname
                        room["tiles"] = tiles
                        room["entities"] = entities
                        room["color"] = color
                        room["warpx"] = warpx
                        room["warpy"] = warpy
                        rooms[room_number] = room
                        state = "rooms"

        return rooms


def _generate_map_data(path: str) -> dict:
    rooms = MapParser().rooms
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