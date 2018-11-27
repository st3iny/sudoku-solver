class Literal:
    """ represents a sudoku field as a cnf literal """
    def __init__(self, *args):
        """ set coordinates as x, y and z or from a literal string """
        if len(args) == 2:
            # get lit string and outer puzzle size
            index = int(args[0])
            self.size = args[1] ** 2

            # copy negation
            if index < 0:
                self.negate = True
                index = -index
            else:
                self.negate = False

            # save index
            self.index = index

            # convert index to 3d coords
            self.z = index // (self.size * self.size)
            index -= self.z * self.size * self.size
            self.y = index // self.size
            self.x = index % self.size
        else:
            # apply coords and size from positional args
            self.x = args[0]
            self.y = args[1]
            self.z = args[2]
            self.negate = False
            self.size = args[3] ** 2

    def __neg__(self):
        """ unary negation operator """
        literal = Literal(self.x, self.y, self.z)
        literal.negate = not self.negate
        return literal

    def __str__(self):
        """ format as cnf literal """
        neg = '-' if self.negate else ''
        index = self.z * self.size * self.size + self.y * self.size + self.x
        return '{neg}{index}'.format(neg=neg, index=index)
