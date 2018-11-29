from constraint_builder import build_constraints
from input_parser import parse_input
import math
from output_parser import parse_dimacs, write_output
import os
import subprocess
import sys
from test import test_model


def main(path):
    """ load puzzle from path, build constraints, solve them and print solved puzzle """
    # create out folder if not present
    if not os.path.exists('out'):
        os.mkdir('out')

    # parse puzzle and print it
    puzzle = parse_input(path)

    # build constraints from parsed puzzle
    constraints = build_constraints(puzzle)

    # write cnf output file
    size = int(math.sqrt(len(puzzle)))
    with open('out/sat.in.cnf', 'w') as file:
        # write problem meta
        file.write('p cnf {literal_count} {clause_count}\n'.format(
            literal_count=size ** 6, clause_count=len(constraints)))

        # write constraints
        for row in constraints:
            literals = [str(literal) for literal in row]
            file.write('{literals} 0\n'.format(literals=' '.join(literals)))

    # run sat solver
    process = subprocess.run(['riss/bin/riss', 'out/sat.in.cnf'], capture_output=True)
    stdout = process.stdout.decode('UTF-8')

    # write stdout for debug
    with open('out/riss.stdout', 'w') as file:
        file.write(stdout)

    # parse dimacs and write output
    model = parse_dimacs(stdout.splitlines())
    write_output(model, size)

    # verify model
    test_model(puzzle, model)


if __name__ == '__main__':
    # run main for every given path
    for path in sys.argv[1:]:
        print('Solving {path} ...'.format(path=path))
        main(path)
        print('\n')
