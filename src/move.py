"""
this class holds the positions of a valid move from start piece to goal state
"""


def strip(string, delims):
    newstring = ''
    for i in range(len(string)):
        if string[i] not in delims:
            newstring+= string[i]
            
    return newstring

def parse(encoded):
    print(encoded)
    retlist = list()
    currstring = ''
    for i in encoded:
        if i == ':':
            retlist.append(int(currstring))
            currstring = ''
        else:
            currstring+=i
            
    if currstring:
        retlist.append(int(currstring))
        
    return (retlist[0], retlist[1]), (retlist[2], retlist[3])
    

class Move:
    
    def __init__(self, start = None, end = None, serverformat = None):
        
        if serverformat is None:
            self.start = start
            self.end = end 
        else:
            self.start, self.end = parse(strip(serverformat, ['[',']']))
            

        
    
    def __str__(self):
        return self.string()
    
    def string(self):
        return '[%(s1)s:%(s2)s]:[%(e1)s:%(e2)s]' % {'s1' : self.start[0], 's2' : self.start[1], 'e1' : self.end[0], 'e2' : self.end[1]}