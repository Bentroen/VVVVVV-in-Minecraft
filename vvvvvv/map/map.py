from room_parser import fetch_map_data

map = fetch_map_data()


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


# https://github.com/TerryCavanagh/VVVVVV/blob/3decf54dbc9e7898a980086dc34a1bfbb52b16ac/desktop_version/src/Map.cpp#L1484


def get_tileset(rx: int, ry: int) -> int:
    area = get_area(rx, ry)
    if area == 0 or area == 1:  # World Map (defined per room)
        room = map[f"{rx},{ry}"]
        tileset = room.get("tileset", 1)
    if area == 5:  # Space Station
        tileset = 0
    else:
        tileset = 1


# https://github.com/TerryCavanagh/VVVVVV/blob/3decf54dbc9e7898a980086dc34a1bfbb52b16ac/desktop_version/src/Map.cpp#L742-L760
# https://github.com/TerryCavanagh/VVVVVV/blob/3decf54dbc9e7898a980086dc34a1bfbb52b16ac/desktop_version/src/Map.cpp#L1382-L1413


def get_area(rx: int, ry: int) -> int:
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
