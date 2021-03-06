from service import *
from random import *
import copy
import os

class UI():
    def __init__(self):
        f = open("graph.txt", 'r')
        line = f.readline()
        line = line.strip().split(" ")
        n = int(line[0])
        m = int(line[1])
        self._serv=initGraph(n,m,DoubleListGraph,"graph.txt")


    def printMenu(self):
        print("1.In degree of a given vertex\n"
              "2.Out degree of a given vertex\n"
              "3.Modify cost\n"
              "4.Add edge\n"
              "5.Remove edge\n"
              "6.Add vertex\n"
              "7.Remove vertex\n"
              "8.Print graph\n"
              "9.Copy graph\n"
              "10.Restore graph to last copy\n"
              "11.Number of vertices\n"
              "12.Number of edges\n"
              "13.Inbound edges of a vertex\n"
              "14.Outbound edges of a vertex\n"
              "15.Iterate the set of vertices\n"
              "16.Check if edge exists\n"
              "17.Find the biconnected components of the graph\n"
              "0.Exit\n")

    def printGetGraphMenu(self):
        print("1.Get graph from file.\n"
              "2.Generate random graph\n")

    def start(self):
        copied=False
        validOption=False
        while not validOption:
            self.printGetGraphMenu()
            graphOpt=input("Your option:")
            if graphOpt=='1':
                validOption=True
            if graphOpt=='2':
                valid = False
                while not valid:
                    n = randint(1, 1000)
                    m = randint(1, 4000)
                    if m <= n * (n - 1):
                        valid = True
                self._serv=initRandomGraph(n,m,DoubleListGraph,"results.txt")
                validOption = True
            elif graphOpt!='1':
                print("Invalid option")
                continue
            while validOption:
                self.printMenu()
                opt=input("Your option:")
                if opt=='0':
                    print("Program ended")
                    return
                elif opt=='1':
                    v=int(input("Vertex:"))
                    indeg = len(self._serv.graph.retdIn(v))
                    print(indeg)
                elif opt=='2':
                    v = int(input("Vertex:"))
                    outdeg = len(self._serv.graph.retdOut(v))
                    print(outdeg)
                elif opt=='3':
                    try:
                        x=int(input("Startpoint of edge:"))
                        y=int(input("Endpoint of edge:"))
                        c=int(input("New cost of edge:"))
                        self._serv.graph.modifEdge(x,y,c)
                        self._serv.graph.saveFile("graph1k_modif.txt")
                        self._serv.graph.appendToFile()
                        print("Edge was modified.")
                    except ExistError:
                        print("You cannot modify an edge that doesn't already exist.")
                    except ValueError:
                        print("Invalid command")
                elif opt=='4':
                    try:
                        x = int(input("Startpoint of edge:"))
                        y = int(input("Endpoint of edge:"))
                        c = int(input("Cost of edge:"))
                        self._serv.graph.addEdge(x,y,c)
                        self._serv.graph.saveFile("graph1k_modif.txt")
                        self._serv.graph.appendToFile()
                        print("Edge was added.")
                    except ExistError:
                        print("This edge already exists")
                    except ValueError:
                        print("Invalid command")
                elif opt=='5':
                    try:
                        x = int(input("Startpoint of edge:"))
                        y = int(input("Endpoint of edge:"))
                        self._serv.graph.removeEdge(x,y)
                        self._serv.graph.saveFile("graph1k_modif.txt")
                        self._serv.graph.appendToFile()
                        print("Edge was removed.")
                    except ExistError:
                        print("This edge doesn't exist and cannot be removed")
                    except ValueError:
                        print("Invalid command")
                elif opt=='6':
                    try:
                        v = int(input("New vertex:"))
                        self._serv.graph.addVertex(v)
                        print("Vertex added.")
                    except ExistError:
                        print("This vertex already exists")
                    except ValueError:
                        print("Invalid command")
                elif opt=='7':
                    try:
                        v = int(input("Vertex to be removed:"))
                        self._serv.graph.removeVertex(v)
                        self._serv.graph.saveFile("graph1k_modif.txt")
                        self._serv.graph.appendToFile()
                        print("Vertex was removed")
                    except ExistError:
                        print("This vertex doesn't exist and cannot be removed")
                    except ValueError:
                        print("Invalid command")
                elif opt=='8':
                    costs=self._serv.graph.parsedCosts()
                    edges=self._serv.graph.parseKeysCosts()
                    for ed in edges:
                        print(str(ed[0])+' '+str(ed[1])+' '+str(costs[ed]))
                elif opt=='9':
                    copyDictIn=copy.deepcopy(self._serv.graph.parsedIn())
                    copyDictOut=copy.deepcopy(self._serv.graph.parsedOut())
                    copyDictCosts=copy.deepcopy(self._serv.graph.parsedCosts())
                    copied=True
                    print("Graph copied")
                elif opt=='10':
                    if not copied:
                        print("There is no copy to restore")
                    else:
                        self._serv.graph.restoreGraph(copyDictIn,copyDictOut,copyDictCosts)
                        self._serv.graph.saveFile("graph1k_modif.txt")
                        self._serv.graph.appendToFile()
                        print("Graph was restored")
                elif opt=='11':
                    print(self._serv.graph.numberOfVertices())
                elif opt=='12':
                    print(self._serv.graph.numberOfEdges())
                elif opt=='13':
                    x=int(input("Vertex:"))
                    inEdges=self._serv.graph.retdIn(x)
                    if len(inEdges) == 0:
                        print("No inbound edges")
                    else:
                        for p in inEdges:
                            print(p)
                elif opt=='14':
                    x=int(input("Vertex:"))
                    outEdges = self._serv.graph.retdOut(x)
                    if len(outEdges)==0:
                        print("No outbound edges")
                    else:
                        for p in outEdges:
                            print(p)
                elif opt=='15':
                    vertices=self._serv.graph.parseKeys()
                    for p in vertices:
                        print(p)
                elif opt=='16':
                    x = int(input("Startpoint of edge:"))
                    y = int(input("Endpoint of edge:"))
                    if self._serv.graph.isEdge(x,y):
                        print("Edge exists")
                    else:
                        print("Edge does not exist")
                elif opt=='17':
                    allComps = biconnectedComponents(self._serv.graph)
                    for comp in range(len(allComps)):
                        print("Component number " + str(comp + 1) + ":")
                        print("Vertices:")
                        for q in allComps[comp].parseKeys():
                            print(q)
                        print("Edges:")
                        for q in allComps[comp].parseKeys():
                            for i in allComps[comp].retdOut(q):
                                print(str(q) + ' ' + str(i) + ' ' + str(allComps[comp].retdCosts(q, i)))
                    print("There are "+str(len(allComps))+" components")
                else:
                    print("Not a valid option")
                    continue
                os.system("pause")


#initRandomGraph(7,20,DoubleListGraph,"random_graph1.txt")
#initRandomGraph(6,40,DoubleListGraph,"random_graph2.txt")
UI().start()