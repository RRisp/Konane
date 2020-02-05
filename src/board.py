"""
use an 18x18 board in this version
rows are 1-18 and columns are a-r
black pieces are X and white pieces are O
"""

from move import Move
import string

class Board:
    def __init__(self):
        self.board = self.createBoard() 
   
    def __getitem__(self, position):
        return self.board[position]
   
    """ 
    override length function to get length of self.board from object
    """
    def __len__(self):
        return len(self.board)
   
    """ initializes full board with X,O pieces """
    def createBoard(self):
        board = [[0 for col in range(18)] for row in range(18)] 
        
        # loop backwards for rows, just how the pdf labels them
        for row in range(len(board) - 1, -1, -1):
            for col in range(18):
                if col % 2 == 0 and row % 2 == 0:
                    board[row][col] = 'O'
                elif col % 2 == 0 and row % 2 != 0:
                    board[row][col] = 'X'
                elif col % 2 != 0 and row % 2 == 0:
                    board[row][col] = 'X'
                else: board[row][col] = 'O'           
        return board
    
    """ override print function to print board object """
    def __str__(self):
        board = ''
        for i in range(len(self.board) - 1, -1, -1):
            board += "%s" % str(i).ljust(2) + ' '
            for j in range(18):
                board += "%s" % (self.board[i][j]) +' '
            board += '\n'


        # print letters for cols
        letters = list(string.ascii_lowercase)[:18]
        board +='   ' + ''
        for i in range(18):
            board +=letters[i] + ' '
        board +='\n'
        return board

    """ populates coordinate with space """
    def removePiece(self, x, y):
        self.board[x][y] = ' '
    
    """
    function that handles the moving of game pieces.
    takes an arg move that contains the starting 
    coordinate to the ending coordinate
    """
    def move(self, move):
        start = move.start
        end = move.end
        moved = self.board[start[0]][start[1]][:]
        self.board[end[0]][end[1]] = moved
        self.board[start[0]][start[1]] = ' '
        startRow = start[0]
        startCol = start[1]
        endRow = end[0]
        endCol = end[1]
        
        if start[0] == end[0]: #horizontal move
            if start[1] < end[1]: #right
                while startCol != endCol:
                    self.board[start[0]][startCol + 1] = ' '
                    startCol += 2
            else:               #left
                while startCol != endCol:
                    self.board[start[0]][startCol - 1] = ' '
                    startCol -= 2

        else:   #veritcal move
            if start[0] < end[0]:#up
                while startRow != endRow:
                    self.board[startRow + 1][start[1]] = ' '
                    startRow += 2
            else:               #down
                while startRow != endRow:
                    self.board[startRow - 1][start[1]] = ' '
                    startRow -= 2
