import copy

import networkx as nx
from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph=nx.DiGraph()
        self._idMapA={}

    def getAllGenres(self):
        return DAO.getAllGenres()

    def buildGraph(self, genreId):
        self._graph.clear()
        nodes=DAO.getAllNodes(genreId)
        for n in nodes:
            self._idMapA[n.ArtistId]=n

        self._graph.add_nodes_from(nodes)
        self.getEdgesPesati(genreId)

    def getEdgesPesati(self, genreId):
        popArtista=DAO.getPopArtista(genreId)  #Lista di tuple con idA --> popolarità
        coppieArtisti=DAO.getCoppieArtisti(genreId) #Lista di tuple con a1, a2

        popMap={}
        for idA, pop in popArtista:
            popMap[idA]=pop

        for idA1, idA2 in coppieArtisti:
            pop1= popMap[idA1]
            pop2= popMap[idA2]

            a1=self._idMapA[idA1]
            a2=self._idMapA[idA2]

            peso=pop1+pop2

            if pop1> pop2:
                self._graph.add_edge(a1, a2, weight=peso)
            elif pop2 > pop1:
                self._graph.add_edge(a2, a1, weight=peso)
            else:
                self._graph.add_edge(a1, a2, weight=peso)
                self._graph.add_edge(a2, a1, weight=peso)

    def getInfluenzaArtista(self):
        bestInfluenza=0
        bestArtist=0

        for n in self._graph.nodes():
            peso_entranti =0
            for u, v, data in self._graph.in_edges(n, data=True):
                peso_entranti += data["weight"]
            peso_uscenti=0
            for u, v, data in self._graph.out_edges(n, data=True):
                peso_uscenti += data["weight"]

            score = peso_uscenti - peso_entranti

            if score > bestInfluenza:
                bestInfluenza=score
                bestArtist= n

        return bestArtist, bestInfluenza



    def getArchiPesoMaggiore(self):
        archi = []
        for u, v, peso in self._graph.edges(data=True):
            archi.append((u, v, peso["weight"]))
        archi.sort(key=lambda x: x[2], reverse=True)
        return archi[:5]

    def getAllArtists(self):
        return self._graph.nodes()


    def getGraphDetails(self):
        return len(self._graph.nodes), len(self._graph.edges)


    def getBestPath(self, artistName):
        self._bestPath=[]
        artist=self._idMapA[artistName]
        parziale=[artist]
        self._ricorsione(parziale)
        return self._bestPath

    def _ricorsione(self, parziale):
        #1) Condizione ottimale
        if len(parziale)> len(self._bestPath):
            self._bestPath= copy.deepcopy(parziale)


        if len(parziale)>1:
            for n in self._graph.neighbors(parziale[-1]):
                if self._graph[parziale[-2]][parziale[-1]]["weight"] > self._graph[parziale[-1]][n]["weight"]:
                    parziale.append(n)
                    self._ricorsione(parziale)
                    parziale.pop()




