from literal import Literal
import numpy as np

def parse_dimacs(dimacs_string):
    # Belegung parsen
    for line in dimacs_string:
        if line.startswith("c"):
            continue
        elif line.startswith("s") and line.split(" ")[1] == "UNSATISFIABLE":
            print("Es gibt keine Lösung für das Sudoku.")
            break
        elif line.startswith("s") and line.split(" ")[1] == "SATISFIABLE":
            print("Es existiert eine Lösung für das Sudoku.")
        elif line.startswith("v"):
            model = [variable for variable in line.split(" ") if variable != "v" and int(variable) != 0]
            break
        else:
            raise ValueError("Fehlerhafte Input Datei\nFolgende Zeile kann nicht gelesen werden: {}".format(line))
    else:
        raise AttributeError("Das Parsen der Lösung ist fehlgeschlagen")

    # Throw away negative variables
    # model = [var for var in model if var > 0]

    return model

# TODO: Belegung überprüfen


def create_separator(inner_dimension):
    """Helper function for write_output"""
    separator = ["+"] * (inner_dimension + 1)
    return ("-" * (2*inner_dimension + 1)).join(separator) + "\n"

def create_line(dimension, row):
    """Helper function for write_output"""
    line = "|"
    for i in range(dimension):
        numbers = [str(number) for number in row[dimension * i: dimension * (i + 1)]]
        numbers_strings = [" " * (dimension**2 - len(number_string)) + number_string
                           for number_string in numbers]
        line += " {} |".format(" ".join(numbers))

    return line

def write_output(model, dimension):
    """Requires the model as a list of strings and the dimensions and outputs the Sudoku
    to STDOUT"""
    outer_dimension = dimension ** 2
    sudoku = np.zeros((outer_dimension, outer_dimension))

    # Model in Sudoku Array überführen
    for literal_string in model:
        literal = Literal(literal_string, dimension)
        sudoku[literal.x, literal.y] = literal.z


    # Belegung ins Output Format schreiben
    # neuer Ansatz
    output = """experiment: generator (Time: _____ s)
    number of tasks: ____
    task: ____
    puzzle size: {}x{}\n""".format(outer_dimension, outer_dimension)

    for i in range(outer_dimension):
        if i % dimension == 0:
            output += create_separator(dimension)
        output += create_line(dimension, sudoku[i]) + "\n"
    else:
        output += create_separator(dimension)

    print(output)
