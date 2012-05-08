# -*- coding: utf-8 -*


class Node:
    def __init__(self,pos,dest,g,par=None):
        self.pos = pos
        self.g = g
        self.h = Node.geth(pos,dest)
        self.f = g+self.h
        self.par = par
    @staticmethod
    def geth(source,dest):
        xDistance = abs(source[0]-dest[0])
        yDistance = abs(source[1]-dest[1])
        if xDistance > yDistance:
            h = 14*yDistance + 10*(xDistance-yDistance)
        else:
            h = 14*xDistance + 10*(yDistance-xDistance)
        return h

def addNode(p,son,openli,dest):
    inOpenli = False
    for node in openli:
        if son[0:2] == node.pos:
            inOpenli = True
            if p.g + son[2] < node.g: 
                # @note: 
                # not changed when equal,
                # maybe need to think about direction
                node.g = p.g + son[2]
                node.f = node.g +  node.h
                node.par = p
            break # only one
    if inOpenli == False:
        #  print 'ADD OPENLI'
        #  print 'son:',son[0],son[1]
        n = Node(son[0:2],dest,p.g + son[2],p)
        openli.append(n)
    

def getSons(p,closedli,cvsMap):
    sons = []
    direct = [[0,1,10],[-1,1,14],[-1,0,10],[-1,-1,14],
              [0,-1,10],[1,-1,14],[1,0,10],[1,1,14]]
    assert len(direct) == 8 
    for i in xrange(len(direct)):
        x_tar = p.pos[0]+direct[i][0]
        y_tar = p.pos[1]+direct[i][1]
        inClosed = False
        for e in closedli:
            if e.pos == [x_tar,y_tar]:
                #   print 'FIND IN CLOSEDLI'
                #   print 'Targ:',x_tar,y_tar
                inClosed = True
                break
        isPassable = True
        try:
            if x_tar < 0 or y_tar < 0 or \
               x_tar >= cvsMap.h or y_tar >= cvsMap.w or \
               cvsMap.mmap[x_tar][y_tar] == 't' or \
               cvsMap.mmap[x_tar][y_tar] == '1':
                isPassable = False
            if isPassable and direct[i][2] == 14:
                # now, target exist, check diag rule
                x = p.pos[0]
                y = p.pos[1]
                if cvsMap.mmap[x][y_tar] == 't' or \
                   cvsMap.mmap[x][y_tar] == '1' or \
                   cvsMap.mmap[x_tar][y] == 't' or \
                   cvsMap.mmap[x_tar][y] == '1':
                    isPassable = False
        except IndexError:
            print 'ERROR: INDEX ERROR @','Func getSons'   
        if not inClosed and isPassable:
            sons.append([x_tar,y_tar,direct[i][2]])
    return sons

def a_star(source,dest,cvsMap):
    openli = []
    closedli = []
    g = 0 
    s0 = Node(source,dest,g)
    openli.append(s0)
    while(True):
        if(openli == []):
            #raise Exception('No Path')
            return -1
        closedli.append(openli.pop(0))
        #print closedli[-1].pos,'#'
        if(closedli[-1].h == 0):
            return closedli[-1]
        sons = getSons(closedli[-1],closedli,cvsMap)
        #print sons,"$"
        if(sons == []):
            #print 'no son'
            continue
        else:
            for son in sons:
                addNode(closedli[-1],son,openli,dest)
            openli.sort(lambda x,y: cmp(x.f,y.f)) # "IN PLACE" Stable

def getPath(r):
    pli = []
    while(r is not None):
        pli.append(r.pos)
        r = r.par
    pli.reverse()
    #print pli
    return pli

if __name__ == "__main__":
    from solve import readMapInput
    s = int(raw_input())
    cvsMap,l = readMapInput()    
    for s in cvsMap.sli:
        for g in cvsMap.gli:
            r = a_star(s, g, cvsMap)
            if r == -1:
                print 'ERROR!'
            else:
                getPath(r)
                print '--------------------'
    

