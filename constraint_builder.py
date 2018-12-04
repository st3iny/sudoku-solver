import literal
import math


def build_constraints(puzzle):
    """ build constraint list for the sat solver from the given puzzle """
    outer_size = len(puzzle)
    inner_size = int(math.sqrt(outer_size))
    constraints = list()

    # at least one number in each entry
    for x in range(1, outer_size + 1):
        for y in range(1, outer_size + 1):
            constraints.append(list())
            for z in range(1, outer_size + 1):
                constraints[-1].append(literal.write(x, y, z, False, inner_size))

    # each number appears at most once in each row
    for y in range(1, outer_size + 1):
        for z in range(1, outer_size + 1):
            for x in range(1, outer_size):
                for i in range(x + 1, outer_size + 1):
                    constraints.append([
                        literal.write(x, y, z, True, inner_size),
                        literal.write(i, y, z, True, inner_size),
                    ])

    # each number appears at most once in each column
    for x in range(1, outer_size + 1):
        for z in range(1, outer_size + 1):
            for y in range(1, outer_size):
                for i in range(y + 1, outer_size + 1):
                    constraints.append([
                        literal.write(x, y, z, True, inner_size),
                        literal.write(x, i, z, True, inner_size),
                    ])

    # each number appears at most once in each subgrid
    for z in range(1, outer_size + 1):
        for i in range(inner_size):
            for j in range(inner_size):
                for x in range(1, inner_size + 1):
                    for y in range(1, inner_size + 1):
                        for k in range(y + 1, inner_size + 1):
                            constraints.append([
                                literal.write(inner_size * i + x, inner_size * j + y, z, True, inner_size),
                                literal.write(inner_size * i + x, inner_size * j + k, z, True, inner_size),
                            ])

    for z in range(1, outer_size + 1):
        for i in range(inner_size):
            for j in range(inner_size):
                for x in range(1, inner_size + 1):
                    for y in range(1, inner_size + 1):
                        for k in range(x + 1, inner_size + 1):
                            for l in range(1, inner_size + 1):
                                constraints.append([
                                    literal.write(inner_size * i + x, inner_size * j + y, z, True, inner_size),
                                    literal.write(inner_size * i + k, inner_size * j + l, z, True, inner_size),
                                ])

    # baseline 25x25: 0.955s

    # There is at most one number in
    for x in range(1, outer_size + 1):
        for y in range(1, outer_size + 1):
            for z in range(1, outer_size):
                for i in range(z + 1, outer_size + 1):
                    constraints.append([
                        literal.write(x, y, z, True, inner_size),
                        literal.write(x, y, i, True, inner_size)
                    ])
    # new time 25x25: 1.10 s

    # Each number appears at least once in each row
    for y in range(1, outer_size + 1):
        for z in range(1, outer_size + 1):
            constraints.append(list())
            for x in range(1, outer_size + 1):
                constraints[-1].append(literal.write(x, y, z, False, inner_size))

    # new time 25x25: 0.1 s
    # → 36x36 : 0.7 s
    # → 49x49 : 3s

    # Each number appears at least once in each column
    for x in range(1, outer_size + 1):
        for z in range(1, outer_size + 1):
            constraints.append(list())
            for y in range(1, outer_size + 1):
                constraints[-1].append(literal.write(x, y, z, False, inner_size))

    # 49x49 : 2s, allerdings 100s insgesamt mit parser

    # Each number appears at least once in each 3x3 sub-grid:
    for z in range(1, outer_size + 1):
        for i in range(inner_size):
            for j in range(inner_size):
                constraints.append(list())
                for x in range(1, inner_size + 1):
                    for y in range(1, inner_size + 1):
                        constraints[-1].append(literal.write(inner_size * i + x, inner_size * j + y, z, False, inner_size))

    # 49x49:

    # initially set fields
    for x in range(outer_size):
        for y in range(outer_size):
            z = puzzle[x][y]
            if z > 0:
                constraints.append([literal.write(x + 1, y + 1, z, False, inner_size)])

    return constraints
