# -*- coding: utf-8 -*
#file:solve.py  

''' DON'T THINK ABOUT TIME !!!'''
''' I JUST NEED IT TO BE CORRECT !!!'''
''' main battle field'''
''' Implement First, Improve Latter'''

#@Idea: use the information of enemies to improve heuristics 

import copy
from vs_astar import a_star 
from vs_astar import getPath

life = 0
money = 0
class MapData:
    def __init__(self,mmap,w,h):
        self.mmap = mmap
        self.w = w
        self.h = h
class CVSMap:
    def __init__(self,mmap,w,h,sli,gli):
    # mapLayout
        self.mmap = mmap
        self.w = w
        self.h = h
        self.sli = sli
        self.gli = gli
        self.tdict = {}
        self.tli = []
        self.eli = []
    def getMapData(self):
        m = copy.deepcopy(self.mmap)
        return MapData(m,self.w,self.h)
    def clearTower(self):
        self.tdict.clear()
        for i in xrange(self.h):
            for j in xrange(self.w):
                if self.mmap[i][j] == 't':
                    self.mmap[i][j] = '0'
    def addTower(self,t): # TODO: can be changed a lot
        #assert self.mmap[t.x][t.y] == '0'
        self.mmap[t.x][t.y] = 't'  # TODO: may be not good what if we destroy the tower?
        self.tdict[(t.x,t.y)] = t
    def delTower(self,i,j):
        assert self.mmap[i][j] == 't'
        self.mmap[i][j] = '0'
        if self.tdict.pop((i,j),-1) == -1:
            print 'ERROR: NO Target Tower'
    def clearEnemy(self):
        self.eli.clear()
    def addEnemy(self,e):
        self.eli.append(e)
    def getMaxG(self):
        ''' get the goal '''
        ''' can be improved '''
        maxDistG = None
        maxDist = -999
        for g in self.gli:
            minDist = 999
            for s in self.sli:
                dist = CVSMap.getDist(g, s)
                if dist < minDist:
                    minDist = dist
            if minDist > maxDist:
                maxDistG = g
                maxDist = minDist
        return maxDistG
    
    def getStrategy(self,actionCode = 0,mapNr = 0, levelNr = 0):
        if actionCode == 0:
            return self.SimpleSetUp()
        if actionCode == 1:
            return self.CloseAndTrap()
    def __SimpleSetUp__(self):
        # close
        g = self.getMaxG()
        gliTemp = copy.deepcopy(self.gli)
        gliTemp.remove(g)
        pathli = []
        for gt in gliTemp:
            self.closeG(gt)
        # getLayout
        
        # getPath
        for s in self.sli:    
            r = a_star(s, g, self)
            if r == -1:
                print "ERROR: NO TO GET G!!!"
                exit(-1)
            path = getPath(r)
            pathli.add(path)
        
        # getTower
        countMap = [[0 for column in range(self.w)] for row in range(self.h)]
        for path in pathli:
            for pos in path:
                countMap[pos[0],pos[1]] = 'X'
        att_range = 2
        #@attention: heavy code, try to improve, maybe use algorithms from comp graphics
        for path in pathli:
            for pos in path:
                for i in xrange(self.h):
                    for j in xrange(self.w):
                        if self.mmap[i][j] == '0' and countMap[i,j] != 'X':
                            if self.__getDist__([i,j], pos) <= 2: 
                                countMap[i][j] += 10
                            if self.__getDist__([i,j], pos) <= 3:
                                countMap[i][j] += 7
                            if self.__getDist__([i,j], pos) <= 4:
                                countMap[i][j] += 5
                            if self.__getDist__([i,j], pos) <= 5:
                                countMap[i][j] += 2
                            if self.__getDist__([i,j], pos) <= 6:
                                countMap[i][j] += 1
        
    def inBound(self,x,y):
        if 0 <= x < self.h and \
           0 <= y < self.w:
            return True
        else:
            return False
    # f for meta-heuristics
    def __f__(self,g = None):
        if g != None:
            score = 0
            for s in self.sli:    
                r = a_star(s, g, self)
                if r == -1:
                    return -9999
                score += len(getPath(r))
            return score
        else:
            raise Exception("NO Implemented Yet!")
        
    def __inRange__(self):
        pass
    def __checkCovered__(self):
        pass
    def __isValid__(self,g = None):
        if g != None:
            for s in self.sli:    
                r = a_star(s, g, self)
                if r == -1:
                    return False
        else:
            for g in self.gli:
                for s in self.sli:
                    r = a_star(s, g, self)
                    if r == -1:
                        return False
        return True
    def __CloseAndTrap__(self):
        g = self.getMaxG()
        gliTemp = copy.deepcopy(self.gli)
        gliTemp.remove(g)
        for gt in gliTemp:
            self.closeG(gt)         
    #build tower around the last g 
        self.LineTrap(g)
    def __LineTrap__(self,g):
        pass
    def __CurlTrap__(self,g):
        pass
    def __closeG__(self,g):
        assert self.mmap[g[0]][g[1]] == 'g'
        dirctions = [[0,1],[-1,0],[0,-1],[1,0]]
        for direc in dirctions: 
            if(not self.isBlocked(g[0]+direc[0],g[1]+direc[1])):
                self.addTower(Tower.getTower(g[0]+direc[0],g[1]+direc[1], 0, 0)) # use a cheap tower
    def __isBlocked__(self,x,y):
        try:
            if x < 0 or y < 0: # Fix: is this good?
                return True
            if self.mmap[x][y] == '0':
                return False
            else:
                return True
        except IndexError:
            return True
    @staticmethod
    def __getDist__(x,y):
        return ((y[0]-x[0])**2 + (y[1]-x[1])**2)**0.5

class Tower:
    def __init__(self,x,y,n,t):
        self.x = x
        self.y = y
        self.stren = n # strength
        self.t = t # type
        if t == 0: #rapid tower
            self.cost = 10 * (3**n) 
            self.power = 10
            self.range = 3 + n
            self.charge = 10 - 2*n
        elif t == 1: #attack tower
            self.cost = 15 * (4**n)
            self.power = 20 * (5**n)
            self.range = 2
            self.charge = 100
        elif t == 2: #freezing tower
            self.cost = 20 * (1+n)
            self.power = 3 * (1+n)
            self.range = 2 + n
            self.charge = 20
            self.freez = 0.1 * self.charge
    def __str__(self):
        return ''+self.x+' '+self.y+' '+self.stren+' '+self.t
    @staticmethod
    def getTower(x,y,n,t):
        return Tower(x,y,n,t)
    @staticmethod
    def getk(chess):
        pass

class Enemy:
    def __init__(self,x,y,appr_t,life,m_t):
        self.x = x
        self.y = y
        self.appr_t = appr_t
        self.life = life
        self.m_t = m_t

def readMapInput():
    # wide height
    wh = raw_input().split()
    w = int(wh[0])
    h = int(wh[1])
    # map arrange
    mmap = [[' ' for column in range(w)] for row in range(h)]
    sli = []
    gli = []
    for i in range(h):
        line = raw_input()
        for j in range(w):
            mmap[i][j] = line[j]
            if(line[j] == 's'):
                sli.append([i,j])
            elif(line[j] == 'g'):
                gli.append([i,j])
    # level
    l = int(raw_input()) 
    # check end 
    temp=str(raw_input())
    temp = temp[0:3]
    if temp != str('END'):
        print temp.__len__()
        print temp
        print "ERROR: 1"
    cvsMap = CVSMap(mmap,w,h,sli,gli)
    return cvsMap,l
    
def readLevelInput(cvsMap):
    global life,money
    line = raw_input().split()
    # life
    life = int(line[0])
    # money
    money = int(line[1])
    # nr of tower
    t_nr = int(line[2])
    # nr of enemy
    e_nr = int(line[3])
    # read towers
    cvsMap.clearTower()
    for i in range(t_nr):
        line = raw_input().split()
        cvsMap.addTower(Tower(int(line[0]),
                              int(line[1]),
                              int(line[2]),
                              int(line[3])))
    # read enemy
    cvsMap.clearEnemy()
    for i in range(e_nr):
        line = raw_input().split();
        cvsMap.addEnemy(Enemy(int(line[0]),
                              int(line[1]),
                              int(line[2]),
                              int(line[3]),
                              int(line[4])))
    # check end 
    temp = raw_input()
    if temp[0,3] != 'END':
        print temp
        print "ERROR: 2"

def levelLoop(cvsMap):
    if not isinstance(cvsMap, CVSMap):
        print 'ERROR: Type, cvsMap is not CVSMap'
        return -1
    #read level info
    readLevelInput(cvsMap)

def mapLoop(map_nr):
    cvsMap,l = readMapInput()
    for i in range(l):
        levelLoop(cvsMap)
        #setTower
        #outputSolution

def main():
    # map nr
    s = int(raw_input())
    for i in range(s):
        mapLoop(i);

if __name__ == "__main__":  
    main()  


'''
    x = (sli[0][0] + sli[1][0])/2
    y = (sli[0][1] + sli[1][1])/2
    print 4
    while(True):
        for i in range(4):
            pass
            #print x,y-3+i,3,0
'''
    
    
    