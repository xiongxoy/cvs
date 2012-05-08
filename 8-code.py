# -*- coding: utf-8 -*

import copy
import sys

class Node:
    def __init__(self,chess,g,par=None):
        self.chess = chess
        self.g = g
        self.k = Node.getk(chess)
        self.f = g+self.k
        self.par = par

    @staticmethod
    def getk(chess):
    	val = 0
    	li = [None,[0,0],[0,1],[0,2],[1,2],[2,2],[2,1],[2,0],[1,0]]
    	for i in range(3):
            for j in range(3):
                if(chess[i][j] != ' '):
                    val += (abs(li[int(chess[i][j])][0] - i) + 
                            abs(li[int(chess[i][j])][1] - j))
        return val

def addSon(p,i0,j0,i1,j1,sons,openli,closedli):
    try:
        schess = copy.deepcopy(p.chess)
	if(i1 < 0 or j1 < 0):
            return
        schess[i0][j0],schess[i1][j1] = schess[i1][j1],schess[i0][j0]
	for node in closedli:
            if schess == node.chess:
		#print 'a'
                return
        for node in openli:
            if schess == node.chess:
                #print 'b'
                return
        if(p.par == None or schess != p.par.chess):
            sons.append(Node(schess,p.g+1,p))
    except IndexError:
        pass

def getSons(p,openli,closedli):
    sons = []
    for i in range(3):
        for j in range(3):
	    if p.chess[i][j] == ' ':
                addSon(p,i,j,i-1,j,sons,openli,closedli)
                addSon(p,i,j,i,j-1,sons,openli,closedli)
                addSon(p,i,j,i+1,j,sons,openli,closedli)
                addSon(p,i,j,i,j+1,sons,openli,closedli)
    return sons

def a_star(chess):
    openli = []
    closedli = []
    g = 0 
    s0 = Node(chess,g)
    openli.append(s0)
    while(True):
        if(openli == []):
	    return -1
        closedli.append(openli[0])
        del openli[0]
        if(closedli[-1].k == 0):
	    return closedli[-1]
        sons = getSons(closedli[-1],openli,closedli)
        if(sons == []):
            #print 'no son'
	    continue
	else:
            #print 'have son'
	    for son in sons:
                openli.append(son)
            openli.sort(lambda x,y: cmp(x.f,y.f)) #check
    
def readChess():
    board_in = open("board_in.txt")
    str = board_in.read()
    chess = [[' ' for column in range(3)] for row in range(3)]
    i=0
    j=0
    str = str.split('\n')
    del str[-1]

    for line in str:
        j=0
        for num in line.split(','):
            chess[i][j] = num
            j+=1
        i+=1
    return chess

def drawChess(chess):
    print '-----------'
    for i in range(3):
        for j in range(3):
       	    print chess[i][j],'|',
	if(~(i == 2 and j == 2)): 
	    print ''
    print '-----------'

def drawSolution(n):
    if n.par != None:
        drawSolution(n.par)
        print '\nmoves to:'
        drawChess(n.chess)
    else:
        drawChess(n.chess)

chess = readChess()
r = a_star(chess)
if(r == -1):
    print 'No Way!'
else:
    drawSolution(r)

