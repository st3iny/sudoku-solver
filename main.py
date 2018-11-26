from constraint_builder import build_constraints
from parser import parse_cnf, parse_puzzle
from print_puzzle import print_puzzle
import subprocess
import sys


def main(path):
    """ load puzzle from path, build constraints, solve them and print solved puzzle """
    # parse puzzle and print it
    puzzle = parse_puzzle(path)
    print_puzzle(puzzle)

    # build constraints from parsed puzzle
    constraints = build_constraints(puzzle)

    # write cnf output file
    size = len(puzzle)
    with open('out/sat.in.cnf', 'w') as file:
        # write problem meta
        file.write('p cnf {literal_count} {clause_count}\n'.format(
            literal_count=size * size * size, clause_count=len(constraints)))

        # write constraints
        for row in constraints:
            literals = [str(literal) for literal in row]
            file.write('{literals} 0\n'.format(literals=' '.join(literals)))

    # run sat solver (glucose)
    process = subprocess.run(['glucose', 'out/sat.in.cnf', 'out/sat.out.cnf'], capture_output=True)
    with open('out/glucose.stdout', 'w') as file:
        file.write(str(process.stdout))

    # convert result into sudoku and print it
    solved_puzzle = parse_cnf('out/sat.out.cnf', size)
    print('---')
    print_puzzle(solved_puzzle)


if __name__ == '__main__':
    main(sys.argv[1])
