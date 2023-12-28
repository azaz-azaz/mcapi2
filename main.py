import numpy as np
from pprint import pprint


class Settings:
    start_pos: tuple[int, int, int] = 0, 10, 0
    xsize: int = 100
    ysize: int = 50
    zsize: int = 100


class MinecraftSmth:
    def __init__(self, name: str):
        self.name = name
    
    def __str__(self) -> str:
        return self.name


class MinecraftBlock(MinecraftSmth):
    def __init__(self, name: str, number: int | None):
        super().__init__(name)



def create_array_blocks() -> np.array:
    """Create a 3D array filled with blocks."""
    arr = np.full()
    