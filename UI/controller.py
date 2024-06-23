import warnings

import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def fillDD(self):
        listMethod = self._model._listMethod
        listYear = self._model._listYear

        for m in listMethod:
            self._view._ddmethod.options.append(ft.dropdown.Option(m.Order_method_type))

        for y in listYear:
            self._view._ddyear.options.append(ft.dropdown.Option(y))

    def handle_graph(self, e):
        if self._view._ddyear.value is None:
            self._view.create_alert("Inserire un anno")
            return

        try:
            anno = int(self._view._ddyear.value)
        except ValueError:
            self._view.create_alert("Non è stato inserito nessun anno")
            return

        if self._view._ddmethod.value is None:
            self._view.create_alert("Inserire un metodo")
            return

        try:
            soglia = float(self._view._txtIn.value)
        except ValueError:
            self._view.create_alert("Soglia non è un valore float")
            return


        metodo = self._model.reverseIdMapMethod[self._view._ddmethod.value]
        self._model.buildGraph(metodo, anno, soglia)
        self._view.txtOut.clean()
        nN, nE = self._model.getGraphSize()
        self._view.txtOut.controls.append(ft.Text(f"Ci sono {nN} vertici e {nE} archi"))
        self._view.update_page()

    def handle_product(self, e):
        prodotti, eIn = self._model.getProdottiRedditizi()
        self._view.txtOut.controls.append(ft.Text(f""))
        self._view.txtOut.controls.append(ft.Text(f"I prodotti più redditizi sono:"))
        if len(prodotti) >= 5:
            for i in range(5):
                self._view.txtOut.controls.append(ft.Text(f"Prodotto {prodotti[i][0].Product_number}     Archi entranti= {eIn[prodotti[i][0]]}     Ricavo= {self._model.ricavi[prodotti[i][0]]}"))
        else:
            for i in range(len(prodotti)):
                self._view.txtOut.controls.append(ft.Text(f"Prodotto {prodotti[i][0].Product_number} Archi entranti= {eIn[prodotti[i][0]]} Ricavo= {self._model.ricavi[prodotti[i][0]]}"))
        self._view.update_page()

    def handle_search(self, e):
        bestPath = self._model.getBestPath()
        self._view.txtOut2.clean()
        self._view.txtOut2.controls.append(ft.Text(f"Lunghezza percorso migliore: {len(bestPath)}"))
        for n in bestPath:
            self._view.txtOut2.controls.append(ft.Text(f"Prodotto {n.Product_number} Ricavo: {self._model.ricavi[n]}"))

        self._view.update_page()