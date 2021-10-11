# execute positioned 16 4 0 align xyz run function vvvvvv:map/init

kill @e[type=armor_stand,tag=room]

execute positioned 0 64 0 align xyz run summon armor_stand ~25 ~0.01 ~5 {Invisible: 1b, NoGravity: 1b, Marker: 1b, Pose: {RightArm: [0f, 0f, 0f], LeftArm: [0f, 0f, 0f]}, Rotation: [90f, 0f], Tags: ["room", "room1"]}
execute positioned 0 64 0 align xyz run summon armor_stand ~25 ~0.01 ~15 {Invisible: 1b, NoGravity: 1b, Marker: 1b, Pose: {RightArm: [0f, 0f, 0f], LeftArm: [0f, 0f, 0f]}, Rotation: [90f, 0f], Tags: ["room", "room2"]}
execute positioned 0 64 0 align xyz run summon armor_stand ~25 ~0.01 ~25 {Invisible: 1b, NoGravity: 1b, Marker: 1b, Pose: {RightArm: [0f, 0f, 0f], LeftArm: [0f, 0f, 0f]}, Rotation: [90f, 0f], Tags: ["room", "room3"]}
execute positioned 0 64 0 align xyz run summon armor_stand ~25 ~0.01 ~35 {Invisible: 1b, NoGravity: 1b, Marker: 1b, Pose: {RightArm: [0f, 0f, 0f], LeftArm: [0f, 0f, 0f]}, Rotation: [90f, 0f], Tags: ["room", "room4"]}
execute positioned 0 64 0 align xyz run summon armor_stand ~15 ~0.01 ~5 {Invisible: 1b, NoGravity: 1b, Marker: 1b, Pose: {RightArm: [0f, 0f, 0f], LeftArm: [0f, 0f, 0f]}, Rotation: [90f, 0f], Tags: ["room", "room5"]}
execute positioned 0 64 0 align xyz run summon armor_stand ~15 ~0.01 ~15 {Invisible: 1b, NoGravity: 1b, Marker: 1b, Pose: {RightArm: [0f, 0f, 0f], LeftArm: [0f, 0f, 0f]}, Rotation: [90f, 0f], Tags: ["room", "room6"]}
execute positioned 0 64 0 align xyz run summon armor_stand ~15 ~0.01 ~25 {Invisible: 1b, NoGravity: 1b, Marker: 1b, Pose: {RightArm: [0f, 0f, 0f], LeftArm: [0f, 0f, 0f]}, Rotation: [90f, 0f], Tags: ["room", "room7"]}
execute positioned 0 64 0 align xyz run summon armor_stand ~15 ~0.01 ~35 {Invisible: 1b, NoGravity: 1b, Marker: 1b, Pose: {RightArm: [0f, 0f, 0f], LeftArm: [0f, 0f, 0f]}, Rotation: [90f, 0f], Tags: ["room", "room8"]}
execute positioned 0 64 0 align xyz run summon armor_stand ~5 ~0.01 ~5 {Invisible: 1b, NoGravity: 1b, Marker: 1b, Pose: {RightArm: [0f, 0f, 0f], LeftArm: [0f, 0f, 0f]}, Rotation: [90f, 0f], Tags: ["room", "room9"]}
execute positioned 0 64 0 align xyz run summon armor_stand ~5 ~0.01 ~15 {Invisible: 1b, NoGravity: 1b, Marker: 1b, Pose: {RightArm: [0f, 0f, 0f], LeftArm: [0f, 0f, 0f]}, Rotation: [90f, 0f], Tags: ["room", "room10"]}
execute positioned 0 64 0 align xyz run summon armor_stand ~5 ~0.01 ~25 {Invisible: 1b, NoGravity: 1b, Marker: 1b, Pose: {RightArm: [0f, 0f, 0f], LeftArm: [0f, 0f, 0f]}, Rotation: [90f, 0f], Tags: ["room", "room11"]}
execute positioned 0 64 0 align xyz run summon armor_stand ~5 ~0.01 ~35 {Invisible: 1b, NoGravity: 1b, Marker: 1b, Pose: {RightArm: [0f, 0f, 0f], LeftArm: [0f, 0f, 0f]}, Rotation: [90f, 0f], Tags: ["room", "room12"]}

execute as @e[type=armor_stand,tag=room] run data merge entity @s {HandItems: [{id: "diamond_hoe", Count: 1b, tag: {CustomModelData: 1}}]}

execute as @e[type=armor_stand,tag=room] at @s run tp @s ~ ~0.01 ~
