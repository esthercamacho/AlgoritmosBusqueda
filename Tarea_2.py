import hashlib

from Tarea_1 import tratamientoGrafo

# Estado debe imprimirse: "(2,[11,40,50,300])"
# ID de estado:  MD5("(2,[11,40,50,300])")="6e4848518f13077b7410a5adf8565d10"

class Problema():
    
    def __init__(self, listaNodos):
        self.estadoInicial = ''
        self.listaNodos = listaNodos

    def setEstadoInicial(self):
        nodosPorVisitar = []
        for i in listaNodos:
            nodosPorVisitar.append(i.id)
        self.estadoInicial = Estado(0, [1,2])
        return self.estadoInicial

    def funcionObjetivo(estado):
        if len(estado.getListaNodosPorVisitar) == 0:
            return True


class Estado():
    def __init__(self, idNodoActual, nodosPorVisitar):
        self.idNodoActual = idNodoActual #Nodo donde esta
        self.nodosPorVisitar = nodosPorVisitar
        self.nodosAdyacentes = []
        self.idEstado = '' #Cadena de caracteres como MD5

    def getNodoActual(self):
        return self.idNodoActual

    def getListaNodosPorVisitar(self):
        return self.nodosPorVisitar

    # ToString Estado
    def __str__(self):
        return "("+self.idNodoActual+","+"str(self.nodosPorVisitar)"+")"    

    def md5(self,idNodo,listaNodos):
        nodo=0
        md5 = hashlib.md5()
        md5.update(idNodo.encode())
        for i in listaNodos:
            md5.update(listaNodos[nodo].encode())
            nodo=nodo+1

        self.idEstado = md5.hexdigest()
        return self.idEstado

    def funcionSucesor(self):
        #Consultamos los nodos adyacentes y los ordenamos
        if self.idNodoActual in diccionario:
            self.nodosAdyacentes = diccionario[self.idNodoActual]
        self.nodosAdyacentes.sort()

        #Comprobamos si el nuevo estado esta visitado y en ese caso borramos su id de los estados por visitar
        #idNuevoEstado = int(self.nodosAdyacentes.pop(0))
        #self.nodosPorVisitar
        #if idNuevoEstado in self.nodosPorVisitar:
            #self.nodosPorVisitar.remove(self.nodosPorVisitar.index(idNuevoEstado))

        #Creamos el nuevo estado
        #nuevoEstado = Estado(str(idNuevoEstado), self.nodosPorVisitar)
        #return nuevoEstado

        return self.nodosAdyacentes


def crearDiccionario(listaNodos):
    diccionario = {}
    for n in listaNodos:
        diccionario[str(n.id)] = n.get_sucesores()
    return diccionario


listaNodos = tratamientoGrafo()

diccionario = crearDiccionario(listaNodos)
problema = Problema(crearDiccionario)
print(problema.setEstadoInicial().funcionSucesor())
print(diccionario["0"])



