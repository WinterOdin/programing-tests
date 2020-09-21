SPACE = " "
NEWLINE = "\n"
BORDERS = "*"

def pileUp(generator):
    return ''.join(list(generator))

def transpose(matrix):
    return [list(row) for row in zip(*matrix)]
    #or import numpy and go for the .transpose()

def reversedRows(matrix):
    return [list(reversed(row)) for row in matrix]


def clockwise(matrix):
    return reversedRows(transpose(matrix))


def counterClockwise(matrix):
    return transpose(reversedRows(matrix))


def draw(x):
    return BORDERS if x == 1 else SPACE
