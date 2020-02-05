from game import Game
from board import Board
from connect import Connect
from move import Move
from move import strip

def main():
    #Connection Code
    print("Please enter your username: ")
    uname = str(input())
    print("Please enter your password: ")
    password = str(input())
    cnx = Connect("artemis.engr.uconn.edu", "4705", uname, password)
    color, pnumber, premoved = cnx.authenticate()
    
    black = 'O'
    white = 'X'
    game = Game()
    player = None
    current_player = None
    #Entire removal process
    
    if not color:
        player = game.processMove(x=0,y=0)
        mine, theirs = cnx.remove_piece('[0:0]',pnumber)
        theirs = theirs[8:]
        theirx, theiry = int(strip(theirs,['[',']',':'])[0]), int(strip(theirs,['[',']',':'])[1])
        game.processMove(x = theirx, y = theiry)
    else:
        player = white if color == 'Color:WHITE' else black
        premoved = premoved[8:]
        x,y = int(strip(premoved,['[',']',':'])[0]), int(strip(premoved,['[',']',':'])[1])
        game.processMove(x=x,y=y)
        if game.onBoard(x+1, y):
            x2,y2 = x+1, y
        elif game.onBoard(x,y+1):
            x2,y2 = x,y+1
        elif game.onBoard(x-1, y):
            x2,y2 = x-1,y
        else:
            x2,y2 = x, y-1
        game.processMove(x=x2,y=y2)
        removestr = '['+ str(x2) + ':' + str(y2) + ']'
        mypiece, theirmove = cnx.remove_piece(removestr, pnumber)
        
        game.processMove(move = Move(serverformat=theirmove[4:]))
        
        
    current_player = player 
    game.set_player(player)
    while not game.end:
        if current_player == player:
            move = game.computer_turn()
            if move is None:
                print("You lose")
                cnx.close()
                print(game.comp_move_time)
                print(game.moves)
                return
            else:
                mymove, theirmove = cnx.turn(move.string())
                
            if type(theirmove) == str:
                game.processMove(move = Move(serverformat=theirmove[4:]))
            else:
                msgs = {-1 : 'You lose', 1 : 'You win'}
                print(msgs[theirmove])
                cnx.close()
                print(game.comp_move_time)
                print(game.moves)
                return

if __name__ == "__main__":
    main()
