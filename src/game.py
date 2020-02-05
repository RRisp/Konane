from copy import deepcopy
import random
import board
import move
import connect
import time
from move import Move
from minimax import minimax

class Game:
    #Initializer with several optional arguments that we use in various parts of our program.
    def __init__(self,player = None, _board = None, moves= 0, last_move = None):
        if not _board:
            self.board = board.Board()
        else:
            self.board = _board
        self.player = player
        self.end = 0
        self.moves = moves
        self.result = None
        self.last_move = last_move
        self.comp_move_time = 0

    def set_player(self, player):
        #Method used to set the player at the beginning of the game.
        self.player = player
    
    # check if adjacent is on board
    def onBoard(self, x, y):
        #Try catch to check if any given x,y is on the board
        if x < 0 or y < 0:
            return False

        try:
            return self.board.board[x][y]
        except:
            return False

    def processMove(self,move : Move = None, x = None, y = None):
        self.moves+=1
        if move:
            self.board.move(move)
            print(self.board)
        else:
            val = self.board[x][y]
            self.board.removePiece(x,y)
            print(self.board)
            return val
        

    # legal moves
    def get_moves(self, current_turn):
        legal_moves = []
        b = self.board

        # determine oppenent piece from arg
        opp = 'X' if current_turn == 'O' else 'O'

        for i in range(len(b) - 1, -1, -1):
            for j in range(18):

                """
                find valid jumps and store starting, ending
                positions as object, return collection of objects
                """
                if b[i][j] == current_turn:
                    #Goes through all options, up , right, down, left and
                    #then uses a while loop to generate multi-jump moves.
                    #we use functions below named with their respective move
                    #type in order to validate if the moves are correct
                    #without if statements in our loops.
                    start = (i,j)
                    i_hold = i
                    up = self.moveUp(i_hold, j,opp)
                    while up:
                        up.start = start
                        legal_moves.append(up)
                        i_hold += 2
                        up = self.moveUp(i_hold, j, opp)

                    start = (i,j)
                    i_hold = i
                    down = self.moveDown(i,j,opp)
                    while down:
                        down.start = start
                        legal_moves.append(down)
                        i_hold -= 2
                        down = self.moveDown(i_hold, j, opp)

                    start = (i,j)
                    j_hold = j
                    left = self.moveLeft(i,j,opp)
                    while left:
                        left.start = start
                        legal_moves.append(left)
                        j_hold -= 2
                        left = self.moveLeft(i,j_hold, opp)

                    start = (i,j)
                    j_hold = j
                    right = self.moveRight(i,j,opp)
                    while right:
                        right.start = start
                        legal_moves.append(right)
                        j_hold += 2
                        right = self.moveRight(i,j_hold,opp)

        #Returns an empty list if we have no moves to return
        return legal_moves if legal_moves else list()

    """ The aformentioned move functions that generates and tests
    whether certain moves are valid or not. Returns none otherwise, and 
    none ends the loop."""
    def moveUp(self, i , j, opp):
        up = self.onBoard(i+1, j)
        if up == opp:
            if self.isValid((i, j), (i+2, j)):
                m = move.Move((i,j), (i+2, j))
                return m
        return False

    def moveDown(self, i, j, opp):
        down = self.onBoard(i-1,j)
        if down == opp:
            if self.isValid((i,j), (i-2, j)):
                m = move.Move((i,j), (i-2, j))
                return m
        return False

    def moveLeft(self, i, j, opp):
        left = self.onBoard(i,j-1)
        if left == opp:
            if self.isValid((i,j), (i, j-2)):
                m = move.Move((i,j), (i, j-2))
                return m
        return False

    def moveRight(self, i, j, opp):
        right = self.onBoard(i,j+1)
        if right == opp:
            if self.isValid((i,j), (i, j+2)):
                m = move.Move((i,j), (i, j+2))
                return m
        return False
    
    
    """Function that takes a start and and end point, and figures out whether or not a move is valid or not.
    Returns True if valid, false otherwise."""
    def isValid(self, start, end):
        if end[0] < 0 or end[0] > 17 or end[1] < 0 or end[1] > 17:
            return False
        if end[0] > start[0]:#vertical move upwards
            if self.board.board[start[0]+1][start[1]] == ' ':
                return False
            if self.board.board[end[0]][start[1]] != ' ':
                return False
        if end[0] < start[0]:#vertical move downwards
            if self.board.board[start[0]-1][start[1]] == ' ':
                return False
            if self.board.board[end[0]][start[1]] != ' ':
                return False
        if end[1] > start[1]: #horizontal move to the right
            if self.board.board[start[0]][start[1]+1] == ' ':
                return False
            if self.board.board[start[0]][end[1]] != ' ':
                return False
        if end[1] < start[1]: #horizontal move to the left
            if self.board.board[start[0]][start[1]-1] == ' ':
                return False
            if self.board.board[start[0]][end[1]] != ' ':
                return False
        return True

    """Method that uses get moves to generate successor games states. This is then passed back to our minimax
    which evaluates each game state in order to figure out what successor is the best option for us
    and or the worst for our opponent."""
    def gen_successors(self):
        possible_boards = list()
        for possible_move in self.get_moves(self.player):
            new_board = deepcopy(self.board)
            new_board.move(possible_move)
            g = Game(self.player, _board= new_board,moves = self.moves, last_move=possible_move)
            g.player = 'X' if self.player == 'O' else 'X'
            possible_boards.append(g)
        return possible_boards


    """ Function that returns a random move."""
    def random_comp_turn(self):
        moves = self.get_moves(self.player)
        if len(moves) == 0:
            self.end = 1
            self.result = 'X'
        else:
            move = random.choice(moves)
            self.board.move(move)
            return move
            

    def computer_turn(self):
        """ The driver of generating a computer turn. Calls minimax, which returns our best move."""
        self.moves += 1
        if len(self.get_moves(self.player)) == 0:
            self.end = 1
            self.result = 'X'
        else:
            start = int(round(time.time() * 1000))
            if self.moves > 100:
                depth = 4
            elif self.moves < 20:
                depth = 2
            else:
                depth = 3
            print("Depth: ", depth, "Moves: ", self.moves)
            moves = minimax(self, float('-inf'), float('inf'), 0, max_depth=depth)
            move = moves[1]
            if move is None:
                move = random.choice(self.get_moves(self.player))
            
            self.board.move(move)
            self.last_move = move
            end = int(round(time.time() * 1000))
            self.comp_move_time += (end - start)
            return move
        
    """Static evaluation function that is used to evaluate the value of each game state.
    This uses a heuristic of minimizing the number of opponent moves."""
    def static_eval(self):
        comp_moves = self.get_moves('X')
        opp_moves = self.get_moves('X')
        if comp_moves == 0:
            return float('inf')
        elif opp_moves == 0:
            return float('-inf')
        else:

            #FINAL CHOICE:
            
            return -1 * len(opp_moves)

            #return len(comp_moves) - len(opp_moves) - x + o
            #OPTION 1:
            #return len(comp_moves) - len(opp_moves) - x + o**2
            #OPTION 2: 25/50 Wins
            #return len(comp_moves) - len(opp_moves) - o**2
            #OPTION 3: 27/50 Wins
            #return len(comp_moves) - len(opp_moves) + x
            #OPTION 4: 30/50 Wins
            #return len(comp_moves) - len(opp_moves) + x**2
            #OPTION 5: 22/50 Wins
            #return len(comp_moves) - len(opp_moves) + (x/self.moves)
            #OPTION 6: 24/50 Wins
            #return len(comp_moves) - len(opp_moves) + (x*self.moves)
            #OPTION 7: 29/50 Wins
            #return len(comp_moves) - len(opp_moves) + (x*self.moves)  + (o/self.moves)
            #OPTION 8: 28/50 Wins
            #return len(comp_moves) - len(opp_moves) + (x*self.moves)  - (o*self.moves)
            #OPTION 9: 26/50 Wins


"""
results = list()
for i in range(50):
    bd = board.Board()
    g = Game(bd, 'X')
    g.play()
    results.append(g.result)
    print("Game terminated")

num_wins = 0
for i in results:
    if i == 'O':
        num_wins+=1

print("O won :", num_wins)
"""
""""
test connecting to konane server via telnet
read/write responses
"""

# server, port, username, pw
#cnx = connect.Connect("artemis.engr.uconn.edu", "4705", '1', 'password')
#game_info = cnx.authenticate()
#print("game info\n")
#print(game_info)
#print()
#print("\n\n")
#
#if game_info[1] == "Player:1":
#    h = cnx.remove_piece("[0:0]", game_info[1])
#    print(h)
#    print("turn return value")
#    print(cnx.turn("[2:0]:[0:0]"))
#
#if game_info[1] == "Player:2":
#    print("here")
#    h = cnx.remove_piece("[0:1]", game_info[1])
#    print(h)
#    print("turn return value")
#    cnx.turn("[2:1]:[0:1]")
