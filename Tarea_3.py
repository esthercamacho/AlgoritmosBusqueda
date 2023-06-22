from operator import itemgetter
from datetime import datetime
import hashlib
import bisect

from Tarea_1 import *

profundidadMax = 600

class Problema():
    
    def __init__(self, estadoInicial):
        self.estadoInicial = estadoInicial

    def funcionObjetivo(self, estado):
        if len(estado.idEstado[1]) == 0:
            return True
        return False


class Estado():
    def __init__(self, idEstado):
        self.idEstado = idEstado[:]
        self.idEstadoMd5 = ''

    def md5(self,idNodo,listaNodos):
        nodo=0
        md5 = hashlib.md5()
        md5.update(idNodo.encode())
        for i in listaNodos:
            md5.update(listaNodos[nodo].encode())
            nodo=nodo+1

        self.idEstadoMd5 = md5.hexdigest()
        return self.idEstadoMd5

    def funcionSucesor(self):
        #Consultamos los nodos adyacentes y los ordenamos
        adyacentes = []

        if str(self.idEstado[0]) in diccionario:
            adyacentes = diccionario[str(self.idEstado[0])]
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
            #if self.idEstado[0] == 517 or self.idEstado[0] == 498 or self.idEstado[0] == 54 or self.idEstado[0] == 1201 or self.idEstado[0] == 100:
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
    

class Visitados():
    def __init__(self):
        self.estadosVisitados = []
    
    def insertar(self, estado):
        self.estadosVisitados.append(str(estado.idEstado))
    
    def pertenece(self, estado):
        if (str(estado.idEstado)) in self.estadosVisitados:
            return True
        return False


def busquedas(problema, frontera, estrategia):
    nID = 0
    visitados = Visitados()
    valor_inicio = calcularValor(estrategia, 0, 0)
    nodo = Nodo(nID, None, problema.estadoInicial, valor_inicio, 0, 0, 0, 0)
    frontera.insertar(nodo)

    while len(frontera.nodosFrontera) > 0:
        auxNodo = frontera.obtener()

        if not problema.funcionObjetivo(auxNodo.estado):
            
            if not visitados.pertenece(auxNodo.estado) and auxNodo.profundidad < profundidadMax:

                visitados.insertar(auxNodo.estado)
                listSucesores = auxNodo.estado.funcionSucesor()

                if len(listSucesores) == 0 and frontera.nodosFrontera == []:
                    return None

                else:
                    for x in listSucesores:
                        
                        nuevoId = x[1][0]
                        nuevoEstadosPorVisitar = x[1][1][:]
                        nuevoEstado = (Estado([int(nuevoId), nuevoEstadosPorVisitar]))

                        #if not visitados.pertenece(nuevoEstado):
                        nID += 1

                            #            ID    PADRE   ESTADO        VALOR                                                                         PROFUNDIDAD               COSTO                        HEURISTICA   ACCION
                        nodo = Nodo (nID, auxNodo, nuevoEstado, float(calcularValor(estrategia, auxNodo.profundidad+1, auxNodo.costo + float(x[2]))), int(auxNodo.profundidad + 1), auxNodo.costo + float(x[2]), 0, x[0])
                        frontera.insertar(nodo)
                        #if nodo.id == 1725:
                            #print('odnuocenwone3ou')

        else:
            return auxNodo

    return None


def crearDiccionario(listaNodos):
    diccionario = {}
    for n in listaNodos:
        diccionario[str(n.id)] = n.get_sucesores()
    return diccionario

def calcularValor(estrategia, prof, costo):
    if estrategia=="BREADTH":
        return prof
    elif estrategia=="DEPTH":
        return 1/(prof+1)
    elif estrategia=="UNIFORM":
        return (costo)

def devolverEstrategia(estrategia_input,estrategias):
    estrategia = ""
    if estrategias.get(estrategia_input):
        estrategia = estrategias[estrategia_input]
        return estrategia
    else:
        raise Exception("La extrategia elegida es erronea o no existe")

'''
def fronteraLibre(frontera, estado):
    for i in frontera:
        if i.estado.idEstado == estado.idEstado:
            return False
    return True
'''

def escribirSolucion(nodo):
    solucion = ""

    while nodo.id>0:
        solucion = "[" + str(nodo.id) + "] [" + str(round(nodo.costo, 2)) + ", " + eliminarEspacios(str(nodo.estado.idEstado)) + ", " + str(nodo.padre.id) + ", " + str(nodo.accion) + ", " + str(nodo.profundidad) + ", " + str(nodo.heuristica) + ", " + str(round(float(nodo.valor), 2)) + "]\n" + solucion
        nodo = nodo.padre
    
    solucion = "[" + str(nodo.id) + "] [" + str(round(nodo.costo, 2)) + ", " + eliminarEspacios(str(nodo.estado.idEstado)) + ", None, None, " + str(nodo.profundidad) + ", " + str(nodo.heuristica) + ", " + str(round(float(nodo.valor), 2)) + "]\n" + solucion

    return solucion

def eliminarEspacios(cad): 
    return cad.replace(" ", "") 


estadoInicial = Estado([37,[248,528,896,1097]])
listaNodos = tratamientoGrafo()
diccionario = crearDiccionario(listaNodos)
print(estadoInicial.idEstado[1])

t_inicio = datetime.now()    
print("Estrategias: \n - Anchura\n - Profundidad Acotada\n - Coste uniforme\n")
estrategia_input = input("Seleccione la estrategia deseada: ").lower()
estrategias = {"anchura": "BREADTH", "profundidad acotada": "DEPTH", "coste uniforme": "UNIFORM"}
estrategia = devolverEstrategia(estrategia_input,estrategias)

problema = Problema(estadoInicial)
solucion = busquedas(problema, frontera = Frontera(), estrategia = estrategia)

if solucion:
    print(escribirSolucion(solucion))
    
    print("Tiempo en resolver el problema (en segundos):")
    print(datetime.now()-t_inicio)

else:
    print("NO SE HA ENCONTRADO SOLUCIÓN")




