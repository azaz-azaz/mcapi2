import os
import sys
import numpy as np
from numpy import sin
from math import gamma
from pprint import pprint
from typing import Callable, Literal
from cfg import *


def fact(n: int | float) -> float:
	try:
		return gamma(n + 1)
	except OverflowError:
		return 99999999999
	except ValueError:
		return 99999999999


class Settings:
	start_pos: tuple[int, int, int] = 0, -60, 0
	xsize: int = 300
	ysize: int = 380
	zsize: int = 300
	size: tuple[int, int, int] = xsize, ysize, zsize

	xscope: int = 0.03  # сколько в 1 блоке
	yscope: int = 0.1  # сколько в 1 блоке
	zscope: int = 0.03  # сколько в 1 блоке
	# n2 xscope: int = 0.1  # сколько в 1 блоке
	# n2 yscope: int = 0.1  # сколько в 1 блоке
	# n2 zscope: int = 0.1  # сколько в 1 блоке
	scope: Vector3 = Vector3(xscope, yscope, zscope)
	xoffset: int = int(-xsize * 0.5)
	yoffset: int = 0
	zoffset: int = int(-zsize * 0.8)
	# n2 xoffset: int = int(-xsize * 0.5)
	# n2 yoffset: int = int(-ysize * 0.5)
	# n2 zoffset: int = int(-zsize * 0.8)
	offset: Vector3 = Vector3(xoffset, yoffset, zoffset)

format_pos: Callable[[Vector3], Vector3]
check_function: Callable[[Vector3], bool]
check_1: Callable[[Vector3], bool]
check_2: Callable[[Vector3], bool]
format_pos = lambda pos: Vector3(
	(pos.x + Settings.xoffset) * Settings.xscope,
	(pos.y + Settings.yoffset) * Settings.yscope,
	(pos.z + Settings.zoffset) * Settings.zscope,
)
# n2 check_function = lambda pos: 4 - pos.y >= pow(pos.x - pos.y * np.cos(pos.z), 2) + pow(pos.z - pos.y * np.cos(pos.x), 2)

def check_1(pos: Vector3) -> bool:
	pos.rotate_ip(22.5, Vector3(0, 1, 0))
	return fact(abs(pos.x) - 2) + fact(abs(pos.z) - 2) < sin(pos.y)
def check_2(pos: Vector3) -> bool:
	pos.rotate_ip(-22.5, Vector3(0, 1, 0))
	return fact(abs(pos.x) - 2) + fact(abs(pos.z) - 2) < sin(pos.y)

check_function = lambda pos: check_1(pos=pos) and check_2(pos=pos) or abs(pos.x) + abs(pos.y) < 5

class MinecraftSmth:
	def __init__(self, name: str):
		self.name = name
	
	def __str__(self) -> str:
		return self.name


class MinecraftBlock(MinecraftSmth):
	def __init__(self, name: str, *, pos: Vector3, number: int | None=None):
		self.id_number: int = number if number is not None else 0
		self.pos: Vector3 = pos
		super().__init__(name)
	
	def __str__(self) -> str:
		return f"setblock {int(self.pos.x)} {int(self.pos.y)} {int(self.pos.z)} {super().__str__()}{(' ' + str(self.id_number)) if self.id_number else str()}"


class BlockMash:
	def __init__(self, block_check_f: Callable[[Vector3], bool]) -> None:
		self.arr: np.ndarray[MinecraftBlock] = np.full(Settings.size, MinecraftBlock("none", pos=Vector3(0, 0, 0)))
		self.f: Callable[[Vector3], bool] = block_check_f
		self.generate()

	def _progress_bar(self, progress):
		bar_length = 100
		filled_length = int(round(bar_length * progress))
		bar = '#' * filled_length + '-' * (bar_length - filled_length)
		sys.stdout.write('\r' + '[{}] {:.0%}'.format(bar, progress))
		sys.stdout.flush()
	
	def generate(self) -> None:
		n: int = 0
		print("GENERATION")
		for x_ind in range(Settings.xsize):
			progress = x_ind / Settings.xsize
			self._progress_bar(progress)
			for y_ind in range(Settings.ysize):
				for z_ind in range(Settings.zsize):
					to_create: int = int(self.f(Vector3(x_ind, y_ind, z_ind)))
					n += to_create
					self.arr[x_ind][y_ind][z_ind] = MinecraftBlock("stone", pos=Vector3(x_ind, y_ind, z_ind)) if to_create else MinecraftBlock("air", pos=Vector3(x_ind, y_ind, z_ind))

		sys.stdout.write('\n')
		print(F"RESULT: CREATED {n} BLOCKS")

		assert n != Settings.xsize * Settings.ysize * Settings.zsize
		assert not not n

	def clear(self, *, neighborhood_mode: Literal["turing", "fonnamen"]="fonnamen") -> None:
		"""Removes blocks inside figure"""
		n = 0
		print("FORMATING")

		ready_mash = self.arr.copy()
		neighborhood_marix = namen if neighborhood_mode == "fonnamen" else turing if neighborhood_mode == "turing" else quit(2)  # соседство тьюринга/фоннеймана

		for x_ind in range(Settings.xsize):
			progress = x_ind / Settings.xsize
			self._progress_bar(progress)
			for y_ind in range(Settings.ysize):
				for z_ind in range(Settings.zsize):
					current_block: MinecraftBlock = self.arr[x_ind][y_ind][z_ind]
					offs: Vector3
					for offs in neighborhood_marix:
						offsed_pos = current_block.pos + offs
						try:
							if offsed_pos.x < 0 or offsed_pos.y < 0 or offsed_pos.z < 0:
								raise IndexError
							if self.arr[int(offsed_pos.x)][int(offsed_pos.y)][int(offsed_pos.z)].name == 'air':
								# нужен так как с воздухом
								break
						except IndexError as e:
							# нужен так как скраю
							break # оставляет блок
					else:
						# не нужен
						n += 1
						ready_mash[x_ind][y_ind][z_ind] = MinecraftBlock("air", pos=Vector3(x_ind, y_ind, z_ind))

		self.arr = ready_mash
		sys.stdout.write('\n')
		
		print(F"RESULT: REMOVED {n} BLOCKS")

	def to_minecraft_syntax(self) -> np.ndarray:
		ar = self.arr.ravel()
		for i in range(len(ar)):
			ar[i].pos += Settings.start_pos
		indices_to_delete = [i for i, block in enumerate(ar) if block.name == "air"]  # удаляем воздух
		ar = np.delete(ar, indices_to_delete)
		return np.array([str(block) for block in ar], dtype=str)

	def print_for_slices(self) -> None:
		print('\n\n'.join(['\n'.join(l) for l in [[''.join([str(int(self.arr[x][y][z].name != 'air')) for z in range(self.arr.shape[2])]) for y in range(self.arr.shape[1])] for x in range(self.arr.shape[0])]]))

	def get_in_file_blocks(self) -> np.ndarray:
		max_len: int = 10_000  # максимум с одного mcfunction
		minecraft_syntax = self.to_minecraft_syntax()
		return np.array_split(minecraft_syntax, len(minecraft_syntax) // max_len + 1)

	def get_str_file_contain(self) -> np.ndarray:
		return np.array(['\n'.join(x) for x in self.get_in_file_blocks()])

	def write_to_files(self, *, remove_old=True) -> None:
		"""Removes old files if need and then creates new files with content"""
		# удаляем старые
		if remove_old:
			print("REMOVING OLD FILES")
			n = 0
			while True:
				file = path + f'autofunction_{n}.mcfunction'
				try:
					os.remove(file)
				except FileNotFoundError:
					print(f"DELETED {n} FILES")
					break
				n += 1
		# создаем новые
		n = 0
		for text in self.get_str_file_contain():
			with open(path + f"autofunction_{n}.mcfunction", "w") as f:
				f.write(text)
				print(f'writing {len(text)} symbols to {f.name}')
				
			n += 1
			
		else:
			print(f"created {n} files")	
			

def main():
	mash = BlockMash(block_check_f=lambda pos: check_function(format_pos(pos)))
	mash.clear(neighborhood_mode="turing")
	mash.write_to_files()

if __name__ == '__main__':
	main()
