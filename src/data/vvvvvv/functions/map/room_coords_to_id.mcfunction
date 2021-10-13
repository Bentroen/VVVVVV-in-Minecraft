scoreboard players operation rx room = x room
scoreboard players operation ry room = y room

scoreboard players set 20 CONST 20

# World map
execute if score x room matches 100.. run scoreboard players remove rx room 100
execute if score y room matches 100.. run scoreboard players remove ry room 95

# Polar Dimension
execute unless score x room matches 100.. run scoreboard players remove rx room 41
execute unless score y room matches 100.. run scoreboard players remove ry room 50

# ------------------------------

# Intermission 1
execute if score x room matches 56 run scoreboard players remove rx room 6

# Intermission 2
execute if score x room matches 53 if score y room matches ..52 run scoreboard players add rx room 7
execute if score x room matches 53 if score y room matches ..52 run scoreboard players add ry room 2

# VVVV, VVVVV, VVVVVV, Outer Space
execute if score x room matches 54 if score y room matches ..50 run scoreboard players add rx room 1
execute if score x room matches 54 if score y room matches ..50 run scoreboard players add ry room 3

# ------------------------------

# Get room ID
scoreboard players operation id room = ry room
scoreboard players operation id room *= 20 CONST
scoreboard players operation id room += rx room

# Clean up temp room coords
scoreboard players reset rx room
scoreboard players reset ry room
