from exceptions import *
from random import *
import copy

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
            self._dIn[v] = []
            self._dOut[v] = []
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

def stronglyConnected(graph):
    allComps = []
    visV=[]
    bigStacc=[]
    for p in graph.parseKeys():
        if p not in visV:
            visV.append(p)
            compF=dfsF(graph, p,bigStacc)
            for i in compF:
                visV.append(i)
    visV=[]
    while bigStacc:
        p=bigStacc.pop()
        if p not in visV:
            compB = dfsB(graph, p, visV)
            allComps.append(compB)
            for q in compB.parseKeys():
                visV.append(q)
                for v in compB.parseKeys():
                    if graph.isEdge(q,v):
                        compB.addEdge(q,v,graph.retdCosts(q, v))
    return allComps

def dfsF(graph,start,bigStacc):
    comp=[]
    stack=[start]
    vis=[start]
    while stack:
        v=stack[-1]
        neigh=graph.retdOut(v)
        done=True
        for p in neigh:
            if p not in vis:
                stack.append(p)
                vis.append(p)
                done=False
                break
        if done:
            if v not in bigStacc:
                bigStacc.append(v)
            del stack[-1]
    return vis

def dfsB(graph,start,visV):
    comp=DoubleListGraph(0)
    stack=[start]
    while stack:
        v=stack[-1]
        visV.append(v)
        neigh=graph.retdIn(v)
        done=True
        for p in neigh:
            if p not in visV:
                stack.append(p)
                done=False
                break
        if done:
            try:
                comp.addVertex(v)
            except:
                pass
            del stack[-1]
    return comp

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
            self.graph.addEdge(x,y,c)
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
