from literal import Literal
import math


def build_constraints(puzzle):
    """ build constraint list for the sat solver from the given puzzle """
    size = len(puzzle)
    size_squared = int(math.sqrt(size))
    constraints = list()

    # at least one number in each entry
    for x in range(1, size + 1):
        for y in range(1, size + 1):
            constraints.append(list())
            for z in range(1, size + 1):
                constraints[-1].append(Literal(x, y, z))

    # each number appears at most once in each row
    for y in range(1, size + 1):
        for z in range(1, size + 1):
            for x in range(1, size):
                for i in range(x + 1, size + 1):
                    constraints.append([-Literal(x, y, z), -Literal(i, y, z)])

    # each number appears at most once in each column
    for x in range(1, size + 1):
        for z in range(1, size + 1):
            for y in range(1, size):
                for i in range(y + 1, size + 1):
                    constraints.append([-Literal(x, y, z), -Literal(x, i, z)])

    # each number appears at most once in each subgrid
    for z in range(1, size + 1):
        for i in range(size_squared):
            for j in range(size_squared):
                for x in range(1, size_squared + 1):
                    for y in range(1, size_squared + 1):
                        for k in range(y + 1, size_squared + 1):
                            constraints.append([
                                -Literal(3 * i + x, 3 * j + y, z),
                                -Literal(3 * i + x, 3 * j + k, z),
                            ])

    for z in range(1, size + 1):
        for i in range(size_squared):
            for j in range(size_squared):
                for x in range(1, size_squared + 1):
                    for y in range(1, size_squared + 1):
                        for k in range(x + 1, size_squared + 1):
                            for l in range(1, size_squared + 1):
                                constraints.append([
                                    -Literal(3 * i + x, 3 * j + y, z),
                                    -Literal(3 * i + k, 3 * j + l, z),
                                ])

    # initially set fields
    for x in range(size):
        for y in range(size):
            z = puzzle[x][y]
            if z > 0:
                constraints.append([Literal(x + 1, y + 1, z)])

    return constraints
