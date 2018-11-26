def parse_puzzle(path):
    """ parse a sudoku text file into a matrix and return it """
    # store sudoku as a matrix
    puzzle = list()

    with open(path, 'r') as file:
        for n, line in enumerate(file):
            # skip first 4 lines
            if n < 4:
                continue

            # extract literals and blank entries, ignore the rest
            row = list()
            cols = line.split(' ')
            for col in cols:
                if col.isalnum():
                    row.append(int(col))
                elif col == '_':
                    row.append(0)

            if len(row) > 0:
                puzzle.append(row)

    # assert quadratic puzzle matrix
    for row in puzzle:
        if len(puzzle) != len(row):
            raise SyntaxError('malformed puzzle')

    return puzzle


def parse_cnf(path, size):
    """ parse sat solver result cnf file into puzzle matrix with given size """
    # read sat solver result
    with open(path, 'r') as file:
        result = file.readline()

    # extract literals and truncate trailing zero
    literals = [int(literal) for literal in result.split(' ')[:-1]]

    # create puzzle matrix
    puzzle = [[0] * size for i in range(size)]

    for literal in literals:
        # skip negated and unused literals
        if literal <= 0 or abs(literal) < 111:
            continue

        # extract literal coords
        x = literal // 100
        y = (literal % 100) // 10
        z = literal % 10

        # set puzzle entry
        puzzle[x - 1][y - 1] = z

    return puzzle
