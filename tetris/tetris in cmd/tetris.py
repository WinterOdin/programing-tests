import sys
import select
import math
from random import randint
import fun #don't name your files "function" because ram doesn't like it










'''
Hi to the person who is checking this pile of garbage for the good sake im webdev not gamedev
btw i wrote tetris with pygame in late 2019 so i will include it into github repo


here is the tutorial i used making this 
https://www.youtube.com/watch?v=dQw4w9WgXcQ

'''


#######################################################################################################


class ShapeOfBlock(object):
   #define those damn blocks here 
    def __init__(self, top=None, left=None):
      
        line            = [[[1,1,1,1]],4,1]  
        lGuy            = [[[0,1],[0,1],[1,1]],2,3]
        lGuyButFlipped  = [[[1,0],[1,0],[1,1]],2,3]
        z               = [[[0,1],[1,1],[1,0]],2,3]
        square          = [[[1,1],[1,1]],2,2]
        
        tupleOfShapes=(line,lGuy,lGuyButFlipped,z,square)
       
        #this can't be a global variable because it need to be random every time we have new shape 
        #learned painfull way 
        randomNumber = randint(0,4)
        
        shape = tupleOfShapes[randomNumber]
        self.height     = shape[2]
        self.matrix     = shape[0]
        self.width      = shape[1]
        self.left       = left
        self.top        = top
  
    def turnClockwise(self):
        self.matrix = fun.clockwise(self.matrix)

    def turnCounterClockwise(self):
        self.matrix = fun.counterClockwise(self.matrix)


#####################################################################################################


class Board(object):
    def __init__(self, height=20, width=20):
        self.height     = height
        self.width      = width
        #I needed tutorial on list comprehensions with this one to make it pythonic 
        self.matrix     = [[1]+[0 for _ in range(width)]+[1] for __ in range(height)]+[[1 for _ in range(width+2)]]

    def __str__(self):

        #fun fact I've wanted to draw it this way 
        #board = ["//////////"] + ["*                 *"] * 20 + ["********************"]
        #yikes
        
        series = fun.pileUp(fun.draw(x) for x in self.matrix[0])
        for row in self.matrix[1:-1]:
            series += fun.NEWLINE
            series += fun.pileUp(fun.draw(x) for x in row)
        series     += fun.NEWLINE
        series     += fun.pileUp(fun.draw(x) for x in self.matrix[-1])
        return series

    def willItFit(self, shape, row, col):  
        try:
            return all(q + self.matrix[row+qw][col + qwe] in (0, 1)
                    for qw, qwer in enumerate(shape.matrix)
                    for qwe, q in enumerate(qwer))
        except IndexError:
            return False

    def put(self, shape, y, x):
        for qw, qwer in enumerate(shape.matrix):
            for qwe, q in enumerate(qwer):
                self.matrix[y + qw][x + qwe] += q
        shape.top  = y
        shape.left = x

    def remove(self, shape, y, x):
        for qw, qwer in enumerate(shape.matrix):
            for qwe, q in enumerate(qwer):
                self.matrix[y + qw][x + qwe] -= q
        shape.top  = y
        shape.left = x

##################################################################################################################


def pivotClockwise(board, shape):
    board.remove(shape, shape.top, shape.left)
    shape.turnClockwise()
    if board.willItFit(shape, shape.top, shape.left):
        board.put(shape, shape.top, shape.left)
    else:
        shape.turnCounterClockwise()
        board.put(shape, shape.top, shape.left)
        print("invalid move")


def pivotCounterClockwise(board, shape):
    board.remove(shape, shape.top, shape.left)
    shape.turnCounterClockwise()
    if board.willItFit(shape, shape.top, shape.left):
        board.put(shape, shape.top, shape.left)
    else:
        shape.turnClockwise()
        board.put(shape, shape.top, shape.left)
        print("invalid move")


def down(board, shape):
    board.remove(shape, shape.top, shape.left)
    if board.willItFit(shape, shape.top+1, shape.left):
        board.put(shape, shape.top+1, shape.left)
    else:
        board.put(shape, shape.top, shape.left)
        raise Exception


def top(board, shape):
    top = 0
    left = randint(1, board.width-shape.width)
    if board.willItFit(shape, top, left):
        board.put(shape, top, left)
    else:
        raise Exception


def right(board, shape):
    board.remove(shape, shape.top, shape.left)
    if board.willItFit(shape, shape.top, shape.left+1):
        board.put(shape, shape.top, shape.left+1)
    else:
        board.put(shape, shape.top, shape.left)
        print("invalid move")


def left(board, shape):
    board.remove(shape, shape.top, shape.left)
    if board.willItFit(shape, shape.top, shape.left-1):
        board.put(shape, shape.top, shape.left-1)
    else:
        board.put(shape, shape.top, shape.left)
        print("invalid move")


if 1 == 1:
    h = 20
    w = 20
    board = Board(h, w)
    shape = ShapeOfBlock()
    top(board, shape)
    print(board)
    x        = input('use a d w s and for moving without changing anything press enter or just random: ')
    while x != 'EOF':
        try:
            down(board, shape)
        except:
            shape = ShapeOfBlock()
            try:
                top(board, shape)
            except:
                print ("it's over for you")
                break
        if x is not None:
            if   x == 'a':
                left(board, shape)
            elif x == 'd':
                right(board, shape)
            elif x == 'w':
                pivotCounterClockwise(board, shape)
            elif x == 's':
                pivotClockwise(board, shape)
        print(board)
        x = input('use a d w s and for moving without changing anything press enter or just random: ')