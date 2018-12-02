from literal import Literal
import numpy as np
import re

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


    return model

# TODO: Belegung überprüfen


def create_separator(inner_dimension):
    """Helper function for write_output"""
    separator = ["+"] * (inner_dimension + 1)
    max_length = inner_dimension ** 2 // 10 + 1
    return ("-" * (inner_dimension * (max_length + 1 ) + 1)).join(separator) + "\n"

def create_line(dimension, row):
    """Helper function for write_output"""
    line = "|"
    for i in range(dimension):
        numbers = [str(number) for number in row[dimension * i: dimension * (i + 1)]]
        max_length = dimension**2 // 10 + 1
        numbers_strings = [" " * (max_length - len(number_string)) + number_string
                           for number_string in numbers]
        line += " {} |".format(" ".join(numbers_strings))

    return line

def parse_model(model, dimension):
    """ parse model into sudoku puzzle matrix """
    sudoku = [[0] * dimension**2 for i in range(dimension**2)]

    # Model in Sudoku Array überführen
    for literal_string in model:
        literal = Literal(literal_string, dimension)
        if literal.negate:
            continue
        sudoku[literal.x - 1][literal.y - 1] = literal.z

    return sudoku

def match_CPU_time(stdout):
    pattern = r"c CPU time\s+: (\d+\.*\d*) s"
    result = re.search(pattern, stdout)
    return result.group(1)

def write_output(model, dimension, stdout):
    """Requires the model as a list of strings and the dimensions and outputs the Sudoku
    to STDOUT"""

    sudoku = parse_model(model, dimension)
    cpu_time = match_CPU_time(stdout)
    for list in sudoku:
        for ele in list:
            assert int(ele) != 0

    # Belegung ins Output Format schreiben
    # neuer Ansatz
    output = ("experiment: generator (Time: {} s) \n".format(cpu_time) +
                "number of tasks: ____\n" +
                "task: ____\n" +
                "puzzle size: {}x{}\n").format(dimension**2, dimension**2)

    for i in range(dimension**2):
        if i % dimension == 0:
            output += create_separator(dimension)
        output += create_line(dimension, sudoku[i]) + "\n"
    else:
        output += create_separator(dimension)

    print(output)

class SolverOutput():
    pass
