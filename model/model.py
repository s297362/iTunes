import copy

import networkx as nx

import database.DAO


class Model:
    def __init__(self):
        self.grafo = nx.Graph()
        self.idMap = {}
        self.bestSet = None
        self.bestScore = 0

    def buildGraph(self, durata):
        self.grafo.clear()
        nodi = database.DAO.DAO().get_nodi()
        for n in nodi:
            self.idMap[n.AlbumId] = n
            if n.Durata > int(durata):
                self.grafo.add_node(n.AlbumId)
        archi = database.DAO.DAO().getArchi()
        for a in archi:
            if self.grafo.has_node(a.Nodo1) and self.grafo.has_node(a.Nodo2) and not self.grafo.has_edge(a.Nodo1, a.Nodo2):
                self.grafo.add_edge(a.Nodo1, a.Nodo2, weight = a.Weight)
        return self.grafo

    def setAlbumSet(self, a1, dTot):
        self.bestSet = None
        connessa = nx.node_connected_component(self.grafo, int(a1))
        parziale = set([a1])
        connessa.remove(int(a1))
        self.ricorsione(parziale, connessa, dTot)
        return self.bestSet, self.durataTot(self.bestSet)

    def ricorsione(self, parziale, connessa, dTot):
        # Condizione terminale
        #print(dTot)
        if self.durataTot(parziale) > dTot:
            return
        # Condizione ottimale
        if len(parziale) > self.bestScore:
            self.bestSet = copy.deepcopy(parziale)
            self.bestScore = len(parziale)

        for nodo in connessa:
            if nodo not in parziale:
                parziale.add(nodo)
                #connessa.remove(nodo)
                self.ricorsione(parziale, connessa, dTot)
                parziale.pop()

    def durataTot(self, parziale):
        durata = 0
        for n in parziale:
            durata += self.idMap[int(n)].Durata
            #print(self.idMap[int(n)].Durata)
        return durata



