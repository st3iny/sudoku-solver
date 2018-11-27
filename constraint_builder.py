from literal import Literal
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
                constraints[-1].append(Literal(x, y, z, inner_size))

    # each number appears at most once in each row
    for y in range(1, outer_size + 1):
        for z in range(1, outer_size + 1):
            for x in range(1, outer_size):
                for i in range(x + 1, outer_size + 1):
                    constraints.append([
                        -Literal(x, y, z, inner_size),
                        -Literal(i, y, z, inner_size),
                    ])

    # each number appears at most once in each column
    for x in range(1, outer_size + 1):
        for z in range(1, outer_size + 1):
            for y in range(1, outer_size):
                for i in range(y + 1, outer_size + 1):
                    constraints.append([
                        -Literal(x, y, z, inner_size),
                        -Literal(x, i, z, inner_size),
                    ])

    # each number appears at most once in each subgrid
    for z in range(1, outer_size + 1):
        for i in range(inner_size):
            for j in range(inner_size):
                for x in range(1, inner_size + 1):
                    for y in range(1, inner_size + 1):
                        for k in range(y + 1, inner_size + 1):
                            constraints.append([
                                -Literal(inner_size * i + x, inner_size * j + y, z, inner_size),
                                -Literal(inner_size * i + x, inner_size * j + k, z, inner_size),
                            ])

    for z in range(1, outer_size + 1):
        for i in range(inner_size):
            for j in range(inner_size):
                for x in range(1, inner_size + 1):
                    for y in range(1, inner_size + 1):
                        for k in range(x + 1, inner_size + 1):
                            for l in range(1, inner_size + 1):
                                constraints.append([
                                    -Literal(inner_size * i + x, inner_size * j + y, z, inner_size),
                                    -Literal(inner_size * i + k, inner_size * j + l, z, inner_size),
                                ])

    # initially set fields
    for x in range(outer_size):
        for y in range(outer_size):
            z = puzzle[x][y]
            if z > 0:
                constraints.append([Literal(x + 1, y + 1, z, inner_size)])

    return constraints
