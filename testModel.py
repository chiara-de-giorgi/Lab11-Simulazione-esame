from model.model import Model

myModel=Model()
myModel.buildGraph(7)
nodi, archi=myModel.getGraphDetails()
print("Grafo creato")
print(f"Numero nodi: {nodi}, numero archi: {archi}")
print(myModel.getInfluenzaArtista())
print(myModel.getArchiPesoMaggiore())

