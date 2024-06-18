

import flet as ft
import networkx as nx

import database.DAO


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self.view = view
        # the model, which implements the logic of the program and holds the data
        self.model = model
        self.grafo = None

    def handleCreaGrafo(self, e):
        durata = self.view._txtInDurata.value
        self.grafo = self.model.buildGraph(durata)
        self.view.txt_result.controls.append(ft.Text(f'Numero nodi: {len(self.grafo.nodes)}\n Numero archi: {len(self.grafo.edges)}'))
        self.view.update_page()
        album = database.DAO.DAO().get_nodi()
        album_ordinato = sorted(album, key=lambda x: x.Title)
        for n in album_ordinato:
            if n.Durata > int(durata):
                self.view._ddAlbum.options.append(ft.dropdown.Option(key=n.AlbumId, text=n.Title))
        self.view.update_page()

    def getSelectedAlbum(self, e):
        print("Funzione chiamata")



    def handleAnalisiComp(self, e):
        self.view.txt_result.clean()
        a1 = self.view._ddAlbum.value
        #print(a1)
        connessi = nx.node_connected_component(self.grafo, int(a1))
        durataTot = 0
        for album in connessi:
            durataTot += self.model.idMap[album].Durata
        self.view.txt_result.controls.append(ft.Text(f'Dimensione componente: {len(connessi)}\nDurata: {durataTot}'))
        self.view.update_page()

    def handleGetSetAlbum(self, e):
        dTot = self.view._txtInSoglia.value
        album = self.view._ddAlbum.value
        soluzione, durata = self.model.setAlbumSet(album, int(dTot))
        for i in soluzione:
            self.view.txt_result.controls.append(ft.Text(f'{self.model.idMap[int(i)].Title}\n{self.model.idMap[int(i)].Durata}'))
        self.view.txt_result.controls.append(ft.Text(f'{durata}'))
        self.view.update_page()


