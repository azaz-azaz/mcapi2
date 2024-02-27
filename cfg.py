from pygame import Vector3


namen: list[Vector3] = [
    Vector3(1, 0, 0),
    Vector3(0, 1, 0),
    Vector3(0, 0, 1),
    Vector3(-1, 0, 0),
    Vector3(0, -1, 0),
    Vector3(0, 0, -1),
    Vector3(1, 1, 0),
    Vector3(-1, 1, 0),
    Vector3(1, -1, 0),
    Vector3(-1, -1, 0),
    Vector3(1, 0, 1),
    Vector3(-1, 0, 1),
    Vector3(1, 0, -1),
    Vector3(-1, 0, -1),
    Vector3(0, 1, 1),
    Vector3(0, -1, 1),
    Vector3(0, 1, -1),
    Vector3(0, -1, -1),
    Vector3(1, 1, 1),
    Vector3(-1, 1, 1),
    Vector3(1, -1, 1),
    Vector3(-1, -1, 1),
    Vector3(1, 1, -1),
    Vector3(-1, 1, -1),
    Vector3(1, -1, -1),
    Vector3(-1, -1, -1),
]

turing: list[Vector3] = [
    Vector3(1, 0, 0),
    Vector3(0, 1, 0),
    Vector3(0, 0, 1),
    Vector3(-1, 0, 0),
    Vector3(0, -1, 0),
    Vector3(0, 0, -1),
]

path: str = "C:/Users/smesh/AppData/Local/Packages/Microsoft.MinecraftUWP_8wekyb3d8bbwe/LocalState/games/com.mojang/development_behavior_packs/functionsPack/functions/"