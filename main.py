from parser import parse
from print_puzzle import print_puzzle


puzzle = parse('examples/bsp-sudoku-input.txt')
print_puzzle(puzzle)
