$execute store result score .$(x) math run data get storage minecraft:variables $(x)
$execute store result score .$(y) math run data get storage minecraft:variables $(y)
$scoreboard players operation .$(x) math += .$(y) math
$scoreboard players reset .$(x) math
$scoreboard players reset .$(y) math