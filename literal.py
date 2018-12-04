def read(literal_string, inner_size):
    """ return x, y, z, neg tuple from literal string """
    literal = int(literal_string) - 1

    # extract negation
    if literal < 0:
        neg = True
        literal = -literal
    else:
        neg = False

    # convert 1d literal to 3d coords
    z = literal // (inner_size ** 4) + 1
    literal -= (z - 1) * (inner_size ** 4)
    y = literal // (inner_size ** 2) + 1
    x = literal % (inner_size ** 2) + 1

    return x, y, z, neg


def write(x, y, z, neg, inner_size):
    """ return literal string from x, y, z literal coords """
    # convert 3d coords to 1d literal
    literal = (z - 1) * (inner_size ** 4) + (y - 1) * (inner_size ** 2) + (x - 1) + 1
    sign = '-' if neg else ''

    return '{sign}{literal}'.format(sign=sign, literal=literal)
