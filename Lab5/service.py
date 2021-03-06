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
            if v==0:
                self._dIn[0] = []
                self._dOut[0] = []
            else:
                keys=self.parseKeys()
                last = keys[len(keys) - 1]
                while last<v:
                    self._dIn[last+1] = []
                    self._dOut[last+1] = []
                    last+=1
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

    def minTreePrim(self,v):
        tree=DoubleListGraph(0)
        visited=[v]
        tree.addVertex(v)
        for k in range(self.numberOfVertices()-1):
            mincost=math.inf
            for i in visited:
                for j in self.retdOut(i):
                    if j not in visited and self.retdCosts(i,j)<mincost:
                        mincost=self.retdCosts(i,j)
                        x=i
                        y=j
            #print(x)
            print(y)
            visited.append(y)
            try:
                tree.addVertex(y)
            except:
                pass
            tree.addEdge(x,y,self.retdCosts(x,y))
        return tree

    def preorderTree(self,start,tree):
        cycle=[start]
        # add start vertex to stack
        stack = [start]
        while stack:
            # the next vertex we visit will be the top of the stack
            v = stack[-1]
            neigh = tree.retdOut(v)
            done = True
            for p in neigh:
                if p not in cycle:
                    # add to stack and visit neighbour
                    stack.append(p)
                    cycle.append(p)
                    done = False
                    break
            # all neighbours have been visited
            if done:
                del stack[-1]
        cycle.append(start)
        return cycle

    def NNAlgorithm(self,start,visited):
        #the array will not only keep track of the already visited vertices, but also form the cycle needed
        visited.append(start)
        v=start
        mincost=0
        #while there are still vertices left unvisited
        while(len(visited)!=self.numberOfVertices()):
            mini=math.inf
            x=-1
            #we parse through the neighbours of the current vertex
            for i in self.retdOut(v):
                #the vertex has not already been visited and the cost of the edge is minimum
                if i not in visited and self.retdCosts(v,i)<mini:
                    mini=self.retdCosts(v,i)
                    x=i
            #we do this for the last edge only
            if len(visited)==self.numberOfVertices()-1 and self.isEdge(v,start) and self.retdCosts(v,start)<mini:
                mini = self.retdCosts(v, start)
                x = start
            #if we have found the next vertex
            if(x!=-1):
                mincost+=mini
                visited.append(x)
                v=x
            #find another vertex
            else:
                for i in self.parseKeys():
                    if i not in visited:
                        v=i
                        break
        #complete the cycle
        if(v!=start):
            visited.append(start)
            mincost+=self.retdCosts(v,start)
        return mincost

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
                #undirected graph
                self.graph.addEdge(y,x,c)

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
