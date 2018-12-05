import literal
import math


def build_constraints(puzzle, solver):
    """ build constraint and pass them to the sat solver from the given puzzle"""
    outer_size = len(puzzle)
    outer_size_squared = outer_size ** 2
    inner_size = int(math.sqrt(outer_size))

    # at least one number in each entry
    for x in range(1, outer_size + 1):
        for y in range(1, outer_size + 1):
            clause = [literal.write(x, y, z, False, outer_size, outer_size_squared) for z in range(1, outer_size + 1)]
            solver.add_clause(clause)

    # each number appears at most once in each row
    for y in range(1, outer_size + 1):
        for z in range(1, outer_size + 1):
            for x in range(1, outer_size):
                for i in range(x + 1, outer_size + 1):
                    solver.add_clause([
                        literal.write(x, y, z, True, outer_size, outer_size_squared),
                        literal.write(i, y, z, True, outer_size, outer_size_squared),
                    ])

    # each number appears at most once in each column
    for x in range(1, outer_size + 1):
        for z in range(1, outer_size + 1):
            for y in range(1, outer_size):
                for i in range(y + 1, outer_size + 1):
                    solver.add_clause([
                        literal.write(x, y, z, True, outer_size, outer_size_squared),
                        literal.write(x, i, z, True, outer_size, outer_size_squared),
                    ])

    # each number appears at most once in each subgrid
    for z in range(1, outer_size + 1):
        for i in range(inner_size):
            for j in range(inner_size):
                for x in range(1, inner_size + 1):
                    for y in range(1, inner_size + 1):
                        for k in range(y + 1, inner_size + 1):
                            solver.add_clause([
                                literal.write(inner_size * i + x, inner_size * j + y, z, True, outer_size, outer_size_squared),
                                literal.write(inner_size * i + x, inner_size * j + k, z, True, outer_size, outer_size_squared),
                            ])

    for z in range(1, outer_size + 1):
        for i in range(inner_size):
            for j in range(inner_size):
                for x in range(1, inner_size + 1):
                    for y in range(1, inner_size + 1):
                        for k in range(x + 1, inner_size + 1):
                            for l in range(1, inner_size + 1):
                                solver.add_clause([
                                    literal.write(inner_size * i + x, inner_size * j + y, z, True, outer_size, outer_size_squared),
                                    literal.write(inner_size * i + k, inner_size * j + l, z, True, outer_size, outer_size_squared),
                                ])

    # baseline 25x25: 0.955s

    # There is at most one number in
    for x in range(1, outer_size + 1):
        for y in range(1, outer_size + 1):
            for z in range(1, outer_size):
                for i in range(z + 1, outer_size + 1):
                    solver.add_clause([
                        literal.write(x, y, z, True, outer_size, outer_size_squared),
                        literal.write(x, y, i, True, outer_size, outer_size_squared)
                    ])
    # new time 25x25: 1.10 s

    # Each number appears at least once in each row
    for y in range(1, outer_size + 1):
        for z in range(1, outer_size + 1):
            clause = [literal.write(x, y, z, False, outer_size, outer_size_squared) for x in range(1, outer_size + 1)]
            solver.add_clause(clause)

    # new time 25x25: 0.1 s
    # → 36x36 : 0.7 s
    # → 49x49 : 3s

    # Each number appears at least once in each column
    for x in range(1, outer_size + 1):
        for z in range(1, outer_size + 1):
            clause = [literal.write(x, y, z, False, outer_size, outer_size_squared) for y in range(1, outer_size + 1)]
            solver.add_clause(clause)

    # 49x49 : 2s, allerdings 100s insgesamt mit parser

    # Each number appears at least once in each 3x3 sub-grid:
    for z in range(1, outer_size + 1):
        for i in range(inner_size):
            for j in range(inner_size):
                clause = list()
                for x in range(1, inner_size + 1):
                    for y in range(1, inner_size + 1):
                        clause.append(literal.write(inner_size * i + x, inner_size * j + y, z, False, outer_size, outer_size_squared))
                solver.add_clause(clause)

    # 49x49:

    # initially set fields
    for x in range(outer_size):
        for y in range(outer_size):
            z = puzzle[x][y]
            if z > 0:
                solver.add_clause([literal.write(x + 1, y + 1, z, False, outer_size, outer_size_squared)])
