import copy

#p is the player going to move
def alphabeta(node, depth, alpha, beta, p):
    if(depth == 0):
	return f(node)
    if(p == 'X'):
	sons = getSons(node,'X')
	for son in sons:
	    alpha = max(alpha, alphabeta(son, depth-1, alpha, beta, 'O'))
	    if beta <= alpha:
   	        break;
        return alpha
    else:
	sons = getSons(node,'O')
	for son in sons:
	    beta = min(beta, alphabeta(son, depth-1, alpha, beta, 'X'))
	    if beta <= alpha:
   	        break;
        return beta

# p is the player who has moved
def getNextChess(chess, p):
    if p == 'X':
	sons = getSons(chess, 'O')
	min_score = 1000
        min_son = None
        for son in sons:
    	    t = alphabeta(son, 3, -1000, 1000, 'X')
	    #drawChess(son) 
            #print 'value is',t
            if t < min_score:
		min_score = t
		min_son = son
        return min_son
    else:
	sons = getSons(chess, 'X')
	max_score = -1000
	max_son = None
	for son in sons:
	    t = alphabeta(son, 3, -1000, 1000, 'O')
            if t > max_score:
		max_score = t
		max_son = son
   	return max_son
        
def getSons(par,p):
    sons=[]
    son=copy.deepcopy(par)
    for i in range(5):
    	for j in range(5):
	    if(par[i][j] == ' '):
	    	son[i][j]=p
		sons.append(son)
		son=copy.deepcopy(par)
    return sons


def drawChess(chess):
    print '--------------------'
    for i in range(5):
        for j in range(5):
       	    print chess[i][j],'|',
	if(i != 4 or j != 4): 
	    print '\n'
    print '\n--------------------'

#evaluate function
def f(chess):
    score = 0
    t = checkDiagnal(chess)
    #print 'diag:',t
    score = score + t
    t = checkVH(chess)
    #print 'vh:',t
    score = score + t
    return score

#check vertical and horizon(?) link
def checkVH(chess):
    score = 0
    count = 0
    oflag = False
    xflag = False
    for i in range(5):
	count = 0
   	oflag = False
   	xflag = False
	for j in range(5):
	    if(chess[i][j] == 'O'):
		oflag = True
	    	count = count + 1
	    if(chess[i][j] == 'X'):
	    	xflag = True
	    	count = count + 1
    	if(oflag or xflag):
	    if(oflag and xflag):
		pass
	    elif(xflag):
	        if(count == 5):
		    score = score + 1000
	        else:
	            score = score + 1
	    elif(oflag):
	        if(count == 5):
		    score = score -1000
	        else:
	            score = score - 1
    for j in range(5):
	count = 0
   	oflag = False
   	xflag = False
	for i in range(5):
	    if(chess[i][j] == 'O'):
		oflag = True
	    	count = count + 1
	    if(chess[i][j] == 'X'):
	    	xflag = True
	    	count = count + 1
    	if(oflag or xflag):
	    if(oflag and xflag):
		pass
	    elif(xflag):
	        if(count == 5):
		    score = score + 1000
	        else:
	            score = score + 1
	    elif(oflag):
	        if(count == 5):
		    score = score -1000
	        else:
	            score = score - 1
    return score

#check diagnal link
def checkDiagnal(chess):
    score = 0
    count = 0
    oflag = False
    xflag = False
    for i in range(5):
	if(chess[i][i] == 'O'):
	    oflag = True
	    count = count + 1
	if(chess[i][i] == 'X'):
	    xflag = True
	    count = count + 1
    if(oflag or xflag):
	if(oflag and xflag):
	    pass
	elif(xflag):
	    if(count == 5):
		score = score + 1000
	    else:
	        score = score + 1
	elif(oflag):
	    if(count == 5):
		score = score - 1000
	    else:
	        score = score - 1
    count = 0
    oflag = False
    xflag = False
    for i in range(5):
	if(chess[4-i][i] == 'O'):
	    oflag = True
	    count = count + 1
	if(chess[4-i][i] == 'X'):
	    xflag = True
	    count = count + 1
    if(oflag or xflag):
	if(oflag and xflag):
	    pass
	elif(xflag):
	    if(count == 5):
		score = score + 1000
	    else:
	        score = score + 1
	elif(oflag):
	    if(count == 5):
		score = score -1000
	    else:
	        score = score - 1
    return score
    

chess = [[' ' for column in range(5)] for row in range(5)]
drawChess(chess)

while(True):
     while True:
     	print 'Please input the coordinates of your input(from 1, e.g. 1,3):'
     	s = raw_input().split(',')
	x = int(s[0])-1
        y = int(s[1])-1
	if chess[x][y] is not ' ':
	    print 'Error move, choose again'
	    continue
        else:
	    break
     # X moves
     chess[x][y] = 'X'
     drawChess(chess)
     if(f(chess) > 500):
	print 'X wins, Congratulations'         
	break
     # O moves
     chess = getNextChess(chess, 'X')
     drawChess(chess)
     print 'f(chess):',f(chess)
     if(f(chess) < -500):
	print 'O wins'         
	break
     
    
