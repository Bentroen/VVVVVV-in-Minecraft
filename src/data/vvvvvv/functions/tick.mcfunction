# Play mode
execute as @a[tag=play] at @s run function vvvvvv:player_effects

# Return to creative mode when leaving play mode
gamemode creative @a[tag=!play,gamemode=adventure]

# Reset room armor stands if one is missing
execute store result score count test if entity @e[tag=room]
execute unless score count test matches 12 positioned 0 64 0 run function vvvvvv:map/init
