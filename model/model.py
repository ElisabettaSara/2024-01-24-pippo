import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._listMethod = []
        self.reverseIdMapMethod = {}
        self._listYear = []
        self._listProduct = []
        self.idMapProduct = {}

        self.nodes = []
        self.edges = []
        self.grafo = nx.DiGraph()
        self.ricavi = {}
        self.redditoNodi = []
        self.nodiIniziali = []

        self._bestPath = []

        self.loadMethod()
        self.loadYears()
        self.loadProduct()

    def getBestPath(self):
        self._bestPath = []

        for n in self.nodiIniziali:
            parziale = [n]
            archi_visitati = []
            self._ricorsione(parziale, archi_visitati)

        return self._bestPath

    def _ricorsione(self, parziale, archi_visitati):
        if len(parziale) > len(self._bestPath):
            self._bestPath = copy.deepcopy(parziale)

        for n in self.grafo[parziale[-1]]:
            if (parziale[-1], n) not in archi_visitati:
                archi_visitati.append((parziale[-1], n))
                parziale.append(n)
                self._ricorsione(parziale, archi_visitati)
                archi_visitati.pop()
                parziale.pop()

    def getProdottiRedditizi(self):
        tmp_prodotti = []
        tmp_entranti = {}
        self.nodiIniziali = []
        for n in self.grafo.nodes:
            eIn = len(self.grafo.in_edges(n))
            eOut = len(self.grafo.out_edges(n))
            if eOut == 0 and eIn > 0:
                tmp_prodotti.append((n, self.ricavi[n]))
                tmp_entranti[n] = eIn

            if eIn == 0:
                self.nodiIniziali.append(n)
        tmp_prodotti = sorted(tmp_prodotti, key=lambda x: x[1], reverse=True)
        return tmp_prodotti, tmp_entranti

    def loadMethod(self):
        self._listMethod = DAO.getMethods()
        for m in self._listMethod:
            self.reverseIdMapMethod[m.Order_method_type] = m

    def loadYears(self):
        self._listYear = DAO.getYears()

    def loadProduct(self):
        self._listProduct = DAO.getProduct()
        for p in self._listProduct:
            self.idMapProduct[p.Product_number] = p

    def buildGraph(self, metodo, anno, soglia):
        self.grafo.clear()
        tmp_nodi = DAO.getNodes(self.idMapProduct, metodo.Order_method_code, anno)
        for n in tmp_nodi:
            self.nodes.append(n)
        self.grafo.add_nodes_from(self.nodes)

        tmp_edge = DAO.getEdge(metodo.Order_method_code, anno)
        for c in tmp_edge:
            if float(c[3]) > (1 + soglia) * float(c[2]) and self.idMapProduct[c[0]] in self.nodes and self.idMapProduct[
                c[1]] in self.nodes:
                self.edges.append((self.idMapProduct[c[0]], self.idMapProduct[c[1]]))
                self.grafo.add_edge(self.idMapProduct[c[0]], self.idMapProduct[c[1]])
                self.ricavi[self.idMapProduct[c[0]]] = float(c[2])
                self.ricavi[self.idMapProduct[c[1]]] = float(c[3])

        """for a in self.edges:
            self.grafo.add_edge(a[0], a[1])"""

        """tmp_ric = DAO.getRicavo(metodo.Order_method_code, anno)
        for r in tmp_ric:
            if self.idMapProduct[r[0]] in self.nodes:
                self.ricavi[self.idMapProduct[r[0]]] = float(r[1])"""

    def getGraphSize(self):
        return len(self.nodes), len(self.edges)
