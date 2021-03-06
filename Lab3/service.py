from exceptions import *
from random import *
import copy
import math

class DoubleListGraph():
    def __init__(self,n):
        self._dIn={}
        self._dOut={}
        self._dCosts={}
        for i in range(n):
            self._dIn[i]=[]
            self._dOut[i]=[]

    def appendToFile(self):
        '''
        appends modifications to file
        '''
        f=open("results.txt",'a')
        costs = self.parsedCosts()
        edges = self.parseKeysCosts()
        for ed in edges:
            line=str(ed[0]) + ' ' + str(ed[1]) + ' ' + str(costs[ed])
            f.write(line)
            f.write('\n')
        f.write('\n')
        f.close()

    def saveFile(self,filename):
        '''
        appends modifications to file
        '''
        f=open(filename,'w')
        costs = self.parsedCosts()
        edges = self.parseKeysCosts()
        for ed in edges:
            line=str(ed[0]) + ' ' + str(ed[1]) + ' ' + str(costs[ed])
            f.write(line)
            f.write('\n')
        f.write('\n')
        f.close()

    def parseKeys(self):
        return list(self._dOut.keys())

    def parseKeysCosts(self):
        return list(self._dCosts.keys())

    def parsedCosts(self):
        return self._dCosts

    def parsedIn(self):
        return self._dIn

    def parsedOut(self):
        return self._dOut

    def retdIn(self,v):
        return self._dIn[v]

    def retdOut(self,v):
        return self._dOut[v]

    def retdCosts(self,x,y):
        return self._dCosts[(x,y)]

    def isVertex(self,v):
        vertices=self.parseKeys()
        return v in vertices

    def isEdge(self,x,y):
        return y in self._dOut[x]

    def addEdge(self,x,y,c):
        if not self.isEdge(x,y):
            self._dIn[y].append(x)
            self._dOut[x].append(y)
            self._dCosts[(x,y)]=c
        else:
            raise ExistError()

    def modifEdge(self,x,y,c):
        if self.isEdge(x,y):
            self._dCosts[(x,y)]=c
        else:
            raise ExistError()

    def addVertex(self,v):
        if not self.isVertex(v):
            keys=self.parseKeys()
            last = keys[len(keys) - 1]
            while last!=v:
                self._dIn[last+1] = []
                self._dOut[last+1] = []
                last+=1
        else:
            raise ExistError()

    def removeEdge(self,x,y):
        if self.isEdge(x,y):
            del self._dCosts[(x,y)]
            self._dOut[x].remove(y)
            self._dIn[y].remove(x)
        else:
            raise ExistError()

    def removeVertex(self,v):
        if self.isVertex(v):
            for p in self.retdOut(v):
                del self._dCosts[(v,p)]
                self._dIn[p].remove(v)

            for p in self.retdIn(v):
                del self._dCosts[(p,v)]
                self._dOut[p].remove(v)
            del self._dOut[v]
            del self._dIn[v]
        else:
            raise ExistError()

    def restoreGraph(self,dIn,dOut,dCosts):
        self._dIn=copy.deepcopy(dIn)
        self._dOut=copy.deepcopy(dOut)
        self._dCosts=copy.deepcopy(dCosts)

    def numberOfEdges(self):
        return len(self._dCosts)

    def numberOfVertices(self):
        return len(self._dIn)

    def lowestCostWalk(self,s,t,prev):
        e=self.numberOfEdges()
        v=self.numberOfVertices()
        #d[x][k]=the cost of the lowest cost walk from s to x and of length at most k, where s is the starting vertex
        d=[[math.inf for x in range(e+1)] for y in range(v)]
        d[s][0]=0
        #dynamically modify the matrix
        for k in range(1,e+1):
            for i in range(v):
                #d[i][k]=min(d[i][k],min(d[j][k-1]+cost(j,i)), where j belongs to the set of inbound edges of i
                d[i][k]=d[i][k-1]
                for j in self.retdIn(i):
                    if d[j][k-1]+self.retdCosts(j,i)<d[i][k]:
                        d[i][k]=d[j][k-1]+self.retdCosts(j,i)
                        #i is now the direct predecessor of j
                        prev[i]=j
        #check for negative cost cycles
        for i in range(1,v):
            mincost=d[i][e]
            for j in self.retdIn(i):
                if d[j][e] + self.retdCosts(j, i) < mincost:
                    raise NegativeCycleError
        #the lowest cost found
        return d[t][e]

    def nrOfLowCostWalks(self,s,t):
        v = self.numberOfVertices()
        #we initialise the minimum cost found so far with positive infinity
        dist=[math.inf]*v
        dist[s]=0
        #nrWalks[i]=the number of walks found so far between s and i
        nrWalks=[0]*v
        nrWalks[s]=1
        #prev[i]=the list of predecessors of i
        prev=[[]for i in range(v)]
        #relax edges repeatedly (Bellman-Ford)
        for i in range(v-1):
            changed=False
            for edge in self.parseKeysCosts():
                # check whether we can relax the edge
                if dist[edge[1]]>dist[edge[0]]+self.retdCosts(edge[0], edge[1]):
                    #update minimum length for edge[1]
                    dist[edge[1]] = dist[edge[0]] + self.retdCosts(edge[0], edge[1])
                    #the number of walks for edge[1] becomes the same as for edge[0]
                    nrWalks[edge[1]]=nrWalks[edge[0]]
                    #add edge[0] as a predecessor of edge[1]
                    if edge[0] not in prev[edge[1]]:
                        prev[edge[1]].append(edge[0])
                    changed=True
                #if we find another minimum cost walk
                elif dist[edge[1]]==dist[edge[0]]+self.retdCosts(edge[0], edge[1]) and edge[0] not in prev[edge[1]]:
                    #the number of walks for edge[0] is added to that of edge[1]
                    nrWalks[edge[1]]+=nrWalks[edge[0]]
                    #remove edge[1] as a predecessor for all the vertices, so we can later update the new number of walks of minimum cost
                    prev[edge[1]].append(edge[0])
                    for p in prev:
                        if edge[1] in p:
                            p.remove(edge[1])
                    changed=True
            # if no edge has been relaxed and no number of walks has been modified, we can stop the relaxation
            if not changed:
                break
        #the number of minimum cost walks from s to t
        return nrWalks[t]

class initGraph():
    def __init__(self,n,m,graph,filename):
        self.graph=graph(n)
        self._filename=filename
        self.__loadFile(filename,m)

    def __loadFile(self,filename,m):
        f = open(filename, 'r')
        line = f.readline()
        for i in range(m):
            line=f.readline()
            line=line.strip().split(" ")
            x=int(line[0])
            y=int(line[1])
            c=int(line[2])
            try:
                self.graph.addEdge(x,y,c)
            except:
                continue
        f.close()

class initRandomGraph():
    def __init__(self,n,m,graph,filename):
        self.graph=graph(n)
        self.__newGraph(n,m,filename)

    def __newGraph(self,n,m,filename):
        if m > n * n:
            f=open(filename,'w')
            f.write("Graph cannot be generated.")
            return
        i=0
        while i<m:
            x=randrange(0,n)
            y=randrange(0,n)
            c=randint(0,1000)
            if not self.graph.isEdge(x,y):
                self.graph.addEdge(x,y,c)
                i+=1
            self.graph.saveFile(filename)
