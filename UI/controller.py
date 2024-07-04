import warnings

import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def fillDD(self):

        metodi = self._model.getmetodo()
        for m in metodi:
            self._view._ddmethod.options.append(ft.dropdown.Option(m))

        anni= self._model.getAnni()
        for a in anni:
            self._view._ddyear.options.append(ft.dropdown.Option(a))

    def handle_graph(self, e):
        s = self._view._txtIn.value
        try:
            sFloat= float(s)
        except ValueError:
            self._view.txtOut.controls.append(ft.Text("Il valore inserito non è un numero"))
            return
        if sFloat<0:
            self._view.txtOut.controls.append(ft.Text("Il valore inserito deve essere maggiore di zero"))
            return

        self._model.creaGrafo(self._view._ddmethod.value, self._view._ddyear.value, self._view._txtIn.value)

        self._view.txtOut.controls.append(ft.Text(f"Numero di nodi:{self._model.getNumNodi()} e numero archi:{self._model.getNumArchi()}"))
        self._view.update_page()

    def handle_product(self, e):
        nodiRed= self._model.getNodiRedditizzi()
        if len(nodiRed)<5:
            for n in range(0,len(nodiRed)):
                self._view.txtOut.controls.append(ft.Text(f"Prodotto {nodiRed[n][0]}    Archi entranti= {nodiRed[n][2]}    Ricavo={nodiRed[n][1]}"))
                self._view.update_page()
        else:
            for n in range(0,5):
                self._view.txtOut.controls.append(ft.Text(f"Prodotto {nodiRed[n][0]}    Archi entranti= {nodiRed[n][2]}    Ricavo={nodiRed[n][1]}"))
                self._view.update_page()





    def handle_search(self, e):
        self._model.searchPath()
        for nodo in self._model.bestSol:
            self._view.txtOut2.controls.append(ft.Text(f"nodo {nodo}, ricavo={self._model.getPrezzo(nodo)}"))
            self._view.update_page()
