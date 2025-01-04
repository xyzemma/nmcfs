$execute store result score .$(x) math run data get storage minecraft:variables $(x)
$scoreboard players add .$(x) math $(y)
$execute store result storage minecraft:variables $(x) 1 run scoreboard players get .$(x) math
$scoreboard players reset .$(x) math