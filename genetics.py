"""
# Example usage
from genetic import *
target = 371
p_count = 100
i_length = 6
i_min = 0
i_max = 100
p = population(p_count, i_length, i_min, i_max)
fitness_history = [grade(p, target),]
for i in xrange(100):
    p = evolve(p, target)
    fitness_history.append(grade(p, target))

for datum in fitness_history:
   print datum
"""


'''
didn't work so well
maybe I give the solution I want first and let the gene help me to break through
'''
from random import randint, random
from operator import add
from vs_astar import a_star
from vs_astar import getPath
import copy

class GenePara:
    def __init__(self,mapData,g):
        self.mapData = mapData
        self.g = g
        self.recLi = self.init_recLi(mapData)
        self.gbInd = None
        self.gbScore = -999
        pass
    
    def init_recLi(self,mapData):
        recLi = []
        for i in xrange(mapData.h):
            for j in xrange(mapData.w):
                if mapData.mmap[i][j] == '0':
                    recLi.append((i,j))
        return recLi
                

def individual(length, min, max):
    'Create a member of the population.'
    return [ randint(min,max) for x in xrange(length) ]

def population(count, length, min, max):
    """
    Create a number of individuals (i.e. a population).

    count: the number of individuals in the population
    length: the number of values per individual
    min: the minimum possible value in an individual's list of values
    max: the maximum possible value in an individual's list of values

    """
    return [ individual(length, min, max) for x in xrange(count) ]

def fitness(individual, para):
    """
    Determine the fitness of an individual. Higher is better.

    individual: the individual to evaluate
    """
    
    score = 0
    tempMap = copy.deepcopy(para.mapData)
    #tempMap.mmap = copy.deepcopy(mapData.mmap)
    count = 0
    for i in xrange(len(individual)):
        if individual[i] == 1:
            count+=1
            pos = para.recLi[i]
            tempMap.mmap[pos[0]][pos[1]] = 't'
    for s in tempMap.sli:
        r = a_star(s, para.g, tempMap)
        if r  == -1:
           # print 'No Way',individual
            score += -100
        else:
            score += len(getPath(r))
            score -= count/2.0
        
    if para.gbInd == None or score > para.gbScore:
        para.gbInd = copy.deepcopy(individual)
        para.gbScore = score
    return score

def grade(pop, para):
    'Find average fitness for a population.'
    summed = reduce(add, (fitness(x, para) for x in pop))
    return summed / (len(pop) * 1.0)

def evolve(pop, para, retain=0.2, random_select=0.05, mutate=0.01):
    graded = [ (fitness(x, para), x) for x in pop]
    graded = [ x[1] for x in sorted(graded,None,None,True)]
    retain_length = int(len(graded)*retain)
    parents = graded[:retain_length]

    # print parents
    # randomly add other individuals to
    # promote genetic diversity
    for individual in graded[retain_length:]:
        if random_select > random():
            parents.append(individual)
    # mutate some individuals
    for individual in parents:
        if mutate > random():
            pos_to_mutate = randint(0, len(individual)-1)
            # this mutation is not ideal, because it
            # restricts the range of possible values,
            # but the function is unaware of the min/max
            # values used to create the individuals,
            individual[pos_to_mutate] = randint(
                min(individual), max(individual))
    # crossover parents to create children
    parents_length = len(parents)
    desired_length = len(pop) - parents_length
    children = []
    while len(children) < desired_length:
        male = randint(0, parents_length-1)
        female = randint(0, parents_length-1)
        if male != female:
            male = parents[male]
            female = parents[female]
            half = len(male) / 2
            child = male[:half] + female[half:]
            children.append(child)
    parents.extend(children)
    return parents




def plotMap(para,individual):
    tempMap = copy.deepcopy(para.mapData)
    for i in xrange(len(individual)):
        if individual[i] == 1:
            pos = para.recLi[i]
            tempMap.mmap[pos[0]][pos[1]] = 't'
    print '------------'
    for i in xrange(tempMap.h):
        for j in xrange(tempMap.w):
            print tempMap.mmap[i][j],
        print 
    print '-------------'
def getLayout(mapData,g):
    para = GenePara(mapData,g)
    
    p_count = 100
    gne_max = 10
    i_length = len(para.recLi)
    i_min = 0
    i_max = 1
    
    p = population(p_count, i_length, i_min, i_max)
   # p.append ( [ 1 for x in xrange(i_length) ])
   # p.append ( [ 1 for x in xrange(i_length) ])
   # p.append ( [ 0 for x in xrange(i_length) ])
   # p.append ( [ 0 for x in xrange(i_length) ])
    #print p
 #   print fitness( [ 0 for x in xrange(i_length) ], mapData)
    #fitness_history = [grade(p, mapData),]
    for i in xrange(gne_max):
        p = evolve(p, para,0.2,0.05,0.1)
        #fitness_history.append(grade(p, mapData))
        # print p
        #  print gbesti
        #  print gbestscore
    #for datum in fitness_history:
       # print datum
    #print 'Besti:',para.gbInd
    #print 'Bests:',para.gbScore
    
    #plotMap(para, para.gbInd)
    return para
    
        
if __name__ == "__main__":
    from solve import readMapInput
    bestscore = -999
    besti = None
    s = int(raw_input())
    mapData,l = readMapInput()    
    res = []
    for g in mapData.gli:
        for i in xrange(10):
            para = getLayout(mapData,g)
            if para.gbScore > bestscore:
                bestscore = para.gbScore
                besti = copy.deepcopy(para.gbInd)
                print 'change:'
                print 'Besti:',para.gbInd
                print 'Bests:',para.gbScore
                plotMap(para, besti)
    print 'Last',bestscore
    print besti
    
    plotMap(para, besti)
    '''    
    idv = [0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0]
    print 'WTF:',fitness(idv, para)
    
    idv = [1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0]
    print 'WTF:',fitness(idv, para)
    '''

