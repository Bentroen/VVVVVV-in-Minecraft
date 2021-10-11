# Gamerules
gamerule commandBlockOutput false
gamerule logAdminCommands false
# gamerule sendCommandFeedback false
# gamerule reducedDebugInfo false
gamerule doDaylightCycle false
gamerule doWeatherCycle false
gamerule randomTickSpeed 0
gamerule fallDamage false
gamerule doImmediateRespawn true
gamerule showDeathMessages false
gamerule keepInventory true
gamerule spawnRadius 0
gamerule doFireTick false
gamerule doTileDrops false
gamerule doEntityDrops false
gamerule doMobLoot false
gamerule mobGriefing false
gamerule doMobSpawning false
gamerule doPatrolSpawning false
gamerule doTraderSpawning false

# World
time set 1000t
weather clear
defaultgamemode adventure
difficulty peaceful
setworldspawn 14 109 19

# Remove The Void platform
fill -8 3 -8 24 3 24 air

# Map collision
setblock 0 0 50 minecraft:structure_block{mode: "LOAD", name: "vvvvvv:map_collision"}
setblock 1 0 50 redstone_block
setblock 1 0 50 air

# Level platform
fill 0 63 0 29 63 39 black_concrete

# Player platform
fill 14 108 19 15 108 20 barrier
fill 14 109 19 15 109 20 snow[layers=7]

# Room armor stands
execute positioned 0 64 0 run function vvvvvv:map/init
