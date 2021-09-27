import os
import json

maps = [
    "Spacestation2.cpp",
    "Labclass.cpp",
    "Warpclass.cpp",
    "Otherlevel.cpp",
    "Finalclass.cpp"
    #"Tower.cpp" special case - needs different handling
]

source_path = "../VVVVVV-master/desktop_version/src"

class MapParser:
    def __init__(self):
        self.rooms = self.parse_files()

    def parse_files(self):
        areas = {}
        for map in maps:
            path = os.path.join(source_path, map)
            areas[map] = self.parse_file(path)
        return areas

    def parse_file(self, path):
        rooms = {}
        state = None
        with open(path) as f:
            for line in f.readlines():
                line = line.strip()

                # TODO: Make function for split_parenthesis
                # TODO: .cache and fetch_map_data(force_update=False)
                # TODO: Type hinting and private method labeling (_method)

                if not state: # Find start of level data
                    if line == "#if !defined(MAKEANDPLAY)":
                        state = "rooms"

                elif state == "rooms":
                    if line.startswith("case rn"): # case rn(##,##):
                        room_number = line.split("(")[1].split(")")[0]
                    elif line.startswith("static const short contents"): # New room begins
                        state = "tiles"
                        room = {}
                        tiles = []
                        entities = []
                        warpx = False
                        warpy = False
                        roomname = ""
                    elif line == "#endif": # End of rooms
                        break

                elif state == "tiles":
                    if line != "};": # Tile row
                        row = line.strip(",").split(",")
                        tiles.append(row)
                    else: # End of tilemap
                        state = "entities"
                
                elif state == "entities":
                    if line.startswith("obj.createentity"):
                        entity_str = line.split("(")[1].split(")")[0]
                        entity = tuple(int(line) for line in entity_str.split(","))
                        entities.append = []
                    else:
                        state = "metadata"

                elif state == "metadata":
                    if line.startswith("rcol"):
                        color = int(line.split(" ")[1].split(";")[0])
                    if line.startswith("warpx"):
                        warpx = "true" in line
                    elif line.startswith("warpy"):
                        warpy = "true" in line
                    elif line.startswith("roomname"):
                        roomname = line.split('"')[1]
                    elif line.startswith("break"): # End of room
                        room["roomname"] = roomname
                        room["tiles"] = tiles
                        room["entities"] = entities
                        room["color"] = color
                        room["warpx"] = warpx
                        room["warpy"] = warpy
                        rooms[room_number] = room
                        state = "rooms"
        
        return rooms


if __name__ == "__main__":
    rooms = MapParser().rooms
    with open("output.json", "w") as f:
        json.dump(rooms, f)