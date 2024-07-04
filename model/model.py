import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._grafo = nx.DiGraph()
        self.prezziMap={}
        self.nodiRed=[]
        self.bestSol=[]
        self.maxDistanza = 0


    def getPrezzo(self, nodo):
        return self.prezziMap[nodo]


    def searchPath(self):

        for n in self._grafo.nodes:
            if not self._grafo.in_edges(n):
                parziale=[n]
                archi_visitati=[]
                self.ricorsione(parziale,archi_visitati)



    def ricorsione(self, parziale,archi_visitati):
        last=parziale[-1]
        vicini = self._grafo[last]

        vicini_utilizzabili=[]
        for v in vicini:
            if (last,v) not in archi_visitati:
                vicini_utilizzabili.append(v)


        if len(vicini_utilizzabili)==0 and not self._grafo.out_edges(parziale[-1]):
            distanza=len(parziale)
            if distanza>self.maxDistanza:
                self.maxDistanza= len(parziale)
                self.bestSol = copy.deepcopy(parziale)
            return

        for v in vicini_utilizzabili :
            archi_visitati.append((last,v))
            parziale.append(v)

            self.ricorsione(parziale, archi_visitati)

            archi_visitati.pop()
            parziale.pop()




    def getNodiRedditizzi(self):
        prezzo=0
        #print(self.prezziMap)

        for n in self._grafo.nodes:
            if not self._grafo[n]:
                #print(n)
                prezzo=self.prezziMap[n]
                self.nodiRed.append((n,prezzo,len(self._grafo.in_edges(n))))
        prodotti=sorted(self.nodiRed, key=lambda x:x[2], reverse=True)

        return prodotti




    def getmetodo(self):
        return DAO.getMetodo()

    def getAnni(self):
        return DAO.getAnno()

    def creaGrafo(self, metodo, anno, soglia):
        self._grafo.clear()
        nodi = DAO.getProdotti(metodo, anno)

        self._grafo.add_nodes_from(nodi)

        archi = DAO.getEdges(metodo,anno,soglia)
        for e in archi:
            self._grafo.add_edge(e[0],e[1])
        self.calcolaPrezzo(metodo, anno)


    def calcolaPrezzo(self, metodo, anno):
        for p in DAO.getPrezzi(metodo, anno):
            self.prezziMap[p[0]]=float(p[1])
        return self.prezziMap

    def getNumNodi(self):
        return len(self._grafo.nodes)

    def getNumArchi(self):
        return len(self._grafo.edges)

