class Literal:
    """ represents a sudoku field as a cnf literal """
    def __init__(self, *args):
        """ set coordinates as x, y and z or from a literal string """
        if len(args) == 2:
            # get lit string and outer puzzle inner size
            index = int(args[0]) - 1
            self.inner_size = args[1]

            # copy negation
            if index < 0:
                self.negate = True
                index = -index
            else:
                self.negate = False

            # save index
            self.index = index

            # convert index to 3d coords
            self.z = index // (self.inner_size ** 4) + 1
            index -= self.z * (self.inner_size ** 4)
            self.y = index // (self.inner_size ** 2) + 1
            self.x = index % (self.inner_size ** 2) + 1
        else:
            # apply coords and inner size from positional args
            self.x = args[0]
            self.y = args[1]
            self.z = args[2]
            self.negate = False
            self.inner_size = args[3]

    def __neg__(self):
        """ unary negation operator """
        literal = Literal(self.x, self.y, self.z, self.inner_size)
        literal.negate = not self.negate
        return literal

    def __str__(self):
        """ format as cnf literal """
        neg = '-' if self.negate else ''
        index = (self.z - 1) * (self.inner_size ** 4) + (self.y - 1) * (self.inner_size ** 2) + (self.x - 1) + 1
        return '{neg}{index}'.format(neg=neg, index=index)
