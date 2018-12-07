from argparse import ArgumentParser
from constraint_builder import build_constraints
import cProfile
from input_parser import parse_input
import math
from output_parser import parse_model, write_output
import os
from pathlib import Path
import pstats
from pycryptosat import Solver
from test import test_model
import time


def main(path):
    """ load puzzle from path, build constraints, solve them and print solved puzzle """
    # create out folder if not present
    start_time = time.time()

    if not os.path.exists('out'):
        os.mkdir('out')

    # parse puzzle and print it
    puzzle = parse_input(path)
    inner_size = int(math.sqrt(len(puzzle)))

    # create solver
    solver = Solver()

    # build constraints from parsed puzzle
    build_constraints(puzzle, solver)

    # run sat solver
    solver_start_time = time.time()
    sat, model = solver.solve()
    solver_end_time = time.time()

    # print solver output and stop execution if not satisfiable
    if sat:
        print('SATISFIABLE')
    else:
        print('UNSATISFIABLE')
        return

    # parse dimacs and write output
    solution = parse_model(model, inner_size)
    end_time = time.time()
    write_output(solution, inner_size, end_time - start_time, solver_end_time - solver_start_time)

    # verify model
    test_model(puzzle, model)


if __name__ == '__main__':
    # create argument parser
    parser = ArgumentParser(description='Solve sudoku puzzles.')
    parser.add_argument(
        'path',
        metavar='PATH',
        type=str,
        help='the sudoku puzzle to solve')
    parser.add_argument(
        '--profiler',
        dest='profiler',
        action='store_const',
        const=True,
        default=False,
        help='run the performance profiler (this will slow down the solver significantly)'
    )

    # parse args
    args = parser.parse_args()

    # run main with or without profiler
    print('solving {path} ...'.format(path=args.path))
    if args.profiler:
        save_path = str(Path("out", "performance_profile"))
        cProfile.run("main(args.path)", save_path)
        print("\n\nProfiling result (sorted by time, full report in {}):\n".format(save_path))
        p = pstats.Stats(save_path)
        p.sort_stats(pstats.SortKey.TIME).print_stats(10)
    else:
        main(args.path)
