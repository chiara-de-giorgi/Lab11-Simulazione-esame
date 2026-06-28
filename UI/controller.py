import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._genreValue= None
        self._artistValue = None

    def fillDDGenre(self):
        genre=self._model.getAllGenres()
        genreDDOption = list(map(lambda x: ft.dropdown.Option(data=x, key=x[1], on_click=self._choiceDDgenre), genre))
        self._view._ddGenre.options = genreDDOption
        self._view.update_page()

    def _choiceDDgenre(self, e):
        self._genreValue = e.control.data


    def handleCreaGrafo(self,e):
        genre = self._genreValue
        if genre is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Selezionare un genere musicale per procedere!", color="red"))
            self._view.update_page()
            return

        self._view.txt_result.controls.clear()
        self._model.buildGraph(genre[0])
        self._view.txt_result.controls.append(ft.Text("Grafo correttamente creato"))
        n, a =self._model.getGraphDetails()
        self._view.txt_result.controls.append(ft.Text(f"Numero di nodi: {n}"))
        self._view.txt_result.controls.append(ft.Text(f"Numero di archi: {a}"))

        art, influenza = self._model.getInfluenzaArtista()
        self._view.txt_result.controls.append(ft.Text(f"Artista più influente: {art}, con influenza {influenza}"))
        top5Archi=self._model.getArchiPesoMaggiore()
        self._view.txt_result.controls.append(ft.Text(f"Top 5 archi:"))
        for u, v, peso in top5Archi:
            self._view.txt_result.controls.append(ft.Text(f"{u} -> {v} : {peso}"))


        self._view._ddArtist.disabled = False
        self.fillDDArtist()
        self._view.update_page()

    def handleCammino(self,e):
        artista=self._artistValue
        if artista is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Selezionare un artista dall'apposito dropdown !", color="red"))
            self._view.update_page()
            return

        self._view.txt_result.controls.clear()
        bestPath= self._model.getBestPath(artista.ArtistId)
        self._view.txt_result.controls.append(ft.Text(f"Ho trovato un cammino ottimo di lunghezza {len(bestPath)}."))
        self._view.txt_result.controls.append(ft.Text(f"Di seguito di nodi che compongono il cammino:"))
        for n in bestPath:
            self._view.txt_result.controls.append(ft.Text(f"{n}"))
        self._view.update_page()


    def fillDDArtist(self):
        artisti=self._model.getAllArtists()
        artistDDOption = list(map(lambda x: ft.dropdown.Option(data=x, key=x, on_click=self._choiceDDartist), artisti))
        self._view._ddArtist.options = artistDDOption
        self._view.update_page()

    def _choiceDDartist(self, e):
        self._artistValue = e.control.data