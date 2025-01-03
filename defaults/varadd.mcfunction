$execute store result score .$(x) math run data get storage minecraft:variables $(x)
$execute store result score .$(y) math run data get storage minecraft:variables $(y)
$scoreboard players operation .$(x) math += .$(y) math
$execute store result storage minecraft:variables $(x) 1 run scoreboard players get .$(x) math
$scoreboard players reset .$(x) math
$scoreboard players reset .$(y) math