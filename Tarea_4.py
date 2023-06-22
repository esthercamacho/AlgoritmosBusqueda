from math import sqrt
from operator import itemgetter
from datetime import datetime
import hashlib
import bisect
import random
from Tarea_1 import *

profundidadMax = 600
c = 0

class Problema():
    
    def __init__(self, estadoInicial):
        self.estadoInicial = estadoInicial

    def funcionObjetivo(self, estado):
        if len(estado.idEstado[1]) == 0:
            return True
        return False


class Estado():
    def __init__(self, idEstado):
        self.idEstado = idEstado
        self.idEstadoMd5 = self.md5()

    def md5(self):
        md5 = hashlib.md5()
        idStr = eliminarEspacios("("+str(self.idEstado[0])+","+ str(self.idEstado[1])+")")
        md5.update(idStr.encode())

        self.idEstadoMd5 = md5.hexdigest()
        return self.idEstadoMd5

    def funcionSucesor(self):
        #Consultamos los nodos adyacentes y los ordenamos
        adyacentes = []

        if str(self.idEstado[0]) in diccionarioAristas:
            adyacentes = diccionarioAristas[str(self.idEstado[0])]
            #print(adyacentes)

            for x in adyacentes:
                listaEstadosPorVisitar = self.idEstado[1][:]
                idX = x[1]

                if int(idX[0]) in listaEstadosPorVisitar:
                    listaEstadosPorVisitar.remove(int(idX[0]))

                idX[1] = listaEstadosPorVisitar[:]

                #Pasamos id a int para que al ordenarlo ahora no se raye
                idX[0] = int(idX[0])

            adyacentes = sorted(adyacentes, key=(itemgetter(1)))
            #print(adyacentes)
            #if self.idEstado[0] == 1196:
               #print(adyacentes)


        return adyacentes[:]



#---------------------------------------------------------------------------------------------------------------TAREA 3
class Frontera():
    def __init__(self):
        self.nodosFrontera = []
    
    def insertar(self, nodo):
        bisect.insort(self.nodosFrontera, nodo)

    def obtener(self):
        return self.nodosFrontera.pop(0)


class Nodo():
    def __init__(self, id, padre, estado, valor, profundidad, costo, heuristica, accion):
        self.id = id
        self.padre = padre
        self.estado = estado
        self.valor = valor
        self.profundidad = profundidad
        self.costo = costo
        self.heuristica = heuristica
        self.accion = accion

    def __lt__(self, other):
        return self.valor < other.valor or (self.valor == other.valor and self.id < other.id)

    def toString(self):
        return(''+str(self.id)+','+str(self.estado.idEstado)+','+str(self.valor)+','+str(self.profundidad))
    

class Visitados():
    def __init__(self):
        self.estadosVisitados = []
    
    def insertar(self, estado):
        self.estadosVisitados.append(str(estado.idEstadoMd5))
    
    def pertenece(self, estado):
        if (str(estado.idEstadoMd5)) in self.estadosVisitados:
            return True
        return False

def busquedas(problema, frontera, estrategia):
    visitados = Visitados()
    nID = 0
    if h == 'euclidia':
        h_inicio = heuristicaEuclidiaFuncion(estadoInicial, 1, d1)
    if h == 'arco':
        h_inicio = heuristicaArcoMinimoFuncion(estadoInicial)
    valor_inicio = calcularValor(estrategia, 0, 0, h_inicio)
    nodo = Nodo(nID, None, problema.estadoInicial, valor_inicio, 0, 0, h_inicio, None)
    frontera.insertar(nodo)

    while len(frontera.nodosFrontera) > 0:
        auxNodo = frontera.obtener()

        if not problema.funcionObjetivo(auxNodo.estado):
            
            if not visitados.pertenece(auxNodo.estado) and auxNodo.profundidad < profundidadMax:

                visitados.insertar(auxNodo.estado)
                listSucesores = auxNodo.estado.funcionSucesor()[:]

                if len(listSucesores) == 0 and frontera.nodosFrontera == []:
                    return None

                else:
                    for x in listSucesores:

                        nuevoId = x[1][0]
                        nuevoEstadosPorVisitar = x[1][1][:]
                        nuevoEstado = (Estado([int(nuevoId), nuevoEstadosPorVisitar]))

                        nID += 1
                        if h == 'euclidia':
                            heuristica = heuristicaEuclidiaFuncion(nuevoEstado, 1, d1)
                        if h == 'arco':
                            heuristica = heuristicaArcoMinimoFuncion(nuevoEstado)
                        valor = calcularValor(estrategia, auxNodo.profundidad+1, auxNodo.costo + float(x[2]), heuristica)

                        #            ID      PADRE  ESTADO     VALOR    PROFUNDIDAD               COSTO                     HEURISTICA  ACCION
                        nodo = Nodo (nID, auxNodo, nuevoEstado, valor, auxNodo.profundidad + 1, auxNodo.costo + float(x[2]), heuristica, x[0])
                        frontera.insertar(nodo)

        
        else:
            return auxNodo

    return None



def creardiccionarioAristas(listaNodos):
    diccionarioAristas = {}
    for n in listaNodos:
        diccionarioAristas[str(n.id)] = n.get_sucesores()
        
    return diccionarioAristas

def creardiccionarioNodos(listaNodos):
    diccionarioNodos = {}
    for n in listaNodos:
        diccionarioNodos[str(n.id)] = n.get_nodoLonLat()
    return diccionarioNodos

def calcularValor(estrategia, prof, costo, heuristica):
    if estrategia=="BREADTH":
        return prof
    elif estrategia=="DEPTH":
        return 1/(prof+1)
    elif estrategia=="UNIFORM":
        return costo
    elif estrategia=="GREEDY":
        return heuristica
    elif estrategia=="A":
        return heuristica+costo

def arcoMinimo(diccionarioAristas):
    arcoMinimo = 1000000
    for i in diccionarioAristas:
        for r in diccionarioAristas[i]:
            arcoMinimo = min(arcoMinimo, float(r[2]))

    return arcoMinimo

def heuristicaArcoMinimoFuncion(estado):
    return len(estado.idEstado[1]) * arcoM

def heuristicaEuclidiaFuncion(estado, m, d1):
    #H( (n,[v1, ..., vr]) ) = min(d(n,vi),min(d(vj,vk)) Para todo  i,j,k  en [1, .., r]
    #d(n,m)=sqrt((n.x-m.x)^2+(n.y-my)^2)

    if m == 0:

        dMin = 1000000000
        listaLonLat = []

        for i in estado.idEstado[1]:
            if diccionarioNodos[str(i)] != None:
                iLonLat = diccionarioNodos[str(i)]
                listaLonLat.append(iLonLat)

        for i in listaLonLat:
            for r in listaLonLat:
                if i != r:
                    d = sqrt(((float(i[0])-float(r[0]))**2) + ((float(i[1])-float(r[1]))**2))

                    dMin = min(d, dMin)

        return(dMin)

    if m == 1:

        dMin = 1000000000
        estadoLonLat = 0
        listaLonLat = []

        if diccionarioNodos[str(estado.idEstado[0])] != None:
            estadoLonLat = diccionarioNodos[str(estado.idEstado[0])]

            for i in estado.idEstado[1]:
                if diccionarioNodos[str(i)] != None:
                    iLonLat = diccionarioNodos[str(i)]
                    listaLonLat.append(iLonLat)
            
            for i in listaLonLat:
                if estadoLonLat != i:
                    d = sqrt(((float(estadoLonLat[0])-float(i[0]))**2) + ((float(estadoLonLat[1])-float(i[1]))**2))

                    dMin = min(d, dMin)

        return min(d1, dMin)*len(estado.idEstado[1])


def devolverEstrategia(estrategia_input,estrategias):
    estrategia = ""
    if estrategias.get(estrategia_input):
        estrategia = estrategias[estrategia_input]
        return estrategia
    else:
        raise Exception("La extrategia elegida es erronea o no existe")

def escribirSolucion(nodo):
    solucion = ""

    # Imprimir MD5 entero: 
    # + "["+ nodo.estado.idEstadoMd5 +"]" +
    # Imprimir ultimos 6 caracteres:
    # + "|"+ nodo.estado.idEstadoMd5[-6:] +"]" +


    while nodo.id>0:
        solucion = "[" + str(nodo.id) + "] [" + str(round(nodo.costo, 2)) + ", " + eliminarEspacios(str(nodo.estado.idEstado)) + ", " + "|"+ nodo.estado.idEstadoMd5[-6:] +"]" + ", " + str(nodo.padre.id) + ", " + str(nodo.accion) + ", " + str(nodo.profundidad) + ", " + str(round(float(nodo.heuristica), 2)) + ", " + str(round(float(nodo.valor), 2)) + "]\n" + solucion
        nodo = nodo.padre
    
    solucion = "[" + str(nodo.id) + "] [" + str(round(nodo.costo, 2)) + ", " + eliminarEspacios(str(nodo.estado.idEstado)) +  ", " + "|"+ nodo.estado.idEstadoMd5[-6:] +"]" + ", None, None, " + str(nodo.profundidad) + ", " + str(round(float(nodo.heuristica), 2)) + ", " + str(round(float(nodo.valor), 2)) + "]\n" + solucion

    f = open("SOLUCIONES/_solucion.txt", "w")
    f.write(solucion)
    f.close()
    return solucion

def eliminarEspacios(cad): 
    return cad.replace(" ", "")


estadoInicial = Estado([1163, [242, 817, 915, 1202]])
#Heuristica ('euclidia' o 'arco')
h = 'euclidia'

listaNodos = tratamientoGrafo()
diccionarioAristas = creardiccionarioAristas(listaNodos)
diccionarioNodos = creardiccionarioNodos(listaNodos)

arcoM = arcoMinimo(diccionarioAristas)
d1 = heuristicaEuclidiaFuncion(estadoInicial, 0, 0)

#print(diccionarioNodos)


t_inicio = datetime.now()
print("Estrategias: \n - Anchura\n - Profundidad Acotada\n - Coste uniforme\n - Greedy\n - A*\n")
estrategia_input = input("Seleccione la estrategia deseada: ").lower()
estrategias = {"anchura": "BREADTH", "profundidad acotada": "DEPTH", "coste uniforme": "UNIFORM", "greedy": "GREEDY", "a": "A"}
estrategia = devolverEstrategia(estrategia_input,estrategias)

problema = Problema(estadoInicial)
solucion = busquedas(problema, frontera = Frontera(), estrategia = estrategia)

if solucion:
    print(escribirSolucion(solucion))
    
    print("Tiempo en resolver el problema (en segundos):")
    print(datetime.now()-t_inicio)


else:
    print("NO SE HA ENCONTRADO SOLUCIÓN")


