import telnetlib
from time import sleep

class Connect:

    def __init__(self, server, port, username, pw):
        self.host = server
        self.port = port
        self.username = username
        self.pw = pw

        # connection telnet object
        TIMEOUT = 5
        try:
            self.cnx = telnetlib.Telnet(self.host, self.port, TIMEOUT)
        except:
            print("\nConnection to %s failed...\nTerminating\n" % (self.host))
        print("\nSuccessfully connected to Konane server at %s..." % (self.host))


    """ 
    function that authenticates with server and begins a game
    returns player number and color
    """
    def authenticate(self):
        self.cnx.read_until(b"?Username:", 10)
        self.cnx.write((self.username + "\r\n").encode('utf-8'))
        print("Username: %s" % (self.username))

        self.cnx.read_until(b"?Password:", 10)
        self.cnx.write((self.pw + "\r\n").encode('utf-8'))
        print("Password: %s" % (self.pw))

        self.cnx.read_until(b"?Opponent:", 60)

        try:
            opp = int(input("Enter an opponent number: "))
        except ValueError as e:
            print(e)
            print("You entered an invalid opponent number")
            self.close()

        self.cnx.write((str(opp) + "\r\n").encode('utf-8'))
        
        # get game number and player number
        sleep(1)
        game_regex = bytes(r"Game:*", encoding='utf-8') 
         
        val = self.cnx.expect([game_regex], 30)[1].string.decode('utf-8')
        val = val.split()
        sleep(1)

        # if only one value is returned then we are player 2, else player 1
        if (len(val) < 2):
            game_no = val[0]
            print(val[0])
            # now wait and check for color after player 1 moves      
            remove_regex = bytes(r"Removed:*", encoding='utf-8')
            remove = self.cnx.expect([remove_regex], 30)[1].string.decode('utf-8')
            remove = remove.split()
            
            print(remove[2])
            print()
            # return color, player, removed piece
            return (remove[1], remove[2], remove[3])

        # player 1
        else:
            game_no = val[0]
            player = val[1]
            print(game_no)
            print(player)
            return (None, player, None)            
            
    """
    remove initial piece for player 2 and return next move made by opponent
    takes player no. as an argument because player 1 and player 2 removals
    recieve different feedback from the server, which is stupid.
    """
    def remove_piece(self, xy, player):
        if player == "Player:1":    
            self.cnx.write((xy + "\r\n").encode('utf-8'))
             
            info = self.cnx.read_until(b"?Move", 180).decode('utf-8')
            info = info.split()
            color = info[0]
            my_move = info[4]
            opp_move = info[5]
            
            return (my_move, opp_move)

        elif player == "Player:2":
            self.cnx.write((xy + "\r\n").encode('utf-8'))
         
            info = self.cnx.read_until(b"?Move", 180).decode('utf-8')
            info = info.split()
            my_move = info[2]
            opp_move = info[3]
            
            return (my_move, opp_move)
    
    """
    function submits a move to server and returns your move (to validate) and
    opponents move
    """
    def turn(self, move):
        self.cnx.write((move + "\r\n").encode('utf-8'))
        info = self.cnx.read_until(b"?Move", 180).decode('utf-8').split("\n")
        print()
        print(info[1])
        print(info[2])
        print() 
         
        if "You win!" in info[2]: 
            return (info[1], 1)
        
        if "Opponent wins!" in info[1]:
            return (info[1], -1)

        return (info[1], info[2])
   
    """ close telent connection """
    def close(self):
        print("Closing connection...\n")
        self.cnx.close()
