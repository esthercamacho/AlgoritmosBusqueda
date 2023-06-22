
from hashlib import new
import xml.sax

listaNodos = []

class bcolors:
    nodo = '\033[92m' #GREEN
    arista = '\033[93m' #YELLOW
    RESET = '\033[0m' #RESET COLOR

class Nodo():
    def __init__(self):
        self.id = ''
        self.id_osm = []
        self.lon = ''
        self.lat = ''
        self.aristas = []
    
    def get_sucesores(self):
        targets = []
        for n in self.aristas:
            accion = n.source+" -> "+n.target
            targets.append([str(accion), [n.target, []], n.longitud])
        return targets
    
    def get_nodoLonLat(self):
        if self.lon != '' and self.lat != '':
            return [float(self.lon), float(self.lat)][:]

    def set_id(self, x):
        self.id = x
    def set_id_osm(self, x):
        self.id_osm = x
    def set_lon(self, x):
        self.lon = x
    def set_lat(self, x):
        self.lat = x
    def add_arista(self, x):
        self.aristas.append(x)
    
    def get_info(self):
        strAristas = ''
        for n in self.aristas:
            strAristas += n.get_info()
        return bcolors.nodo+'ID: '+self.id+'. ID_OSM: '+self.id_osm+'. LON: '+self.lon+'. LAT: '+self.lat+'.\n\nARISTAS: \n'+strAristas+' \n\n'

class Arista():
    def __init__(self):
        self.longitud= ''
        self.source = ''
        self.target = ''

    def set_longitud(self, x):
        self.longitud = x
    def set_source(self, x):
        self.source = x
    def set_target(self, x):
        self.target = x
    def get_info(self):
        return (bcolors.arista+
        'ORIGEN: '+self.source+
        '. DESTINO: '+self.target+bcolors.RESET+
        '. LONGITUD: '+self.longitud+'\n\n')

class MapHandler( xml.sax.ContentHandler ):
    def __init__(self):
        self.nodoID = -1
        self.aristaID = -1
        self.nodoTargetId = -1
        self.currentData = ''
        self.key = ''
        self.content = ''
        self.arista = Arista()
        self.minimoArco = 100000000

    def startElement(self, tag, attributes):
        self.CurrentData = tag
        if tag == 'node':
            #print ('*****node*****')
            id = attributes['id']
            #print ('ID:', id)
            self.nodoID = id
            nodo = Nodo()
            nodo.set_id(id)
            listaNodos.append(nodo)
            
        if tag == 'edge':
            #print ('*****edge*****')
            source = attributes['source']
            target = attributes['target']
            id = attributes['id']
            self.aristaID = id
            self.arista = Arista()
            self.arista.set_source(source)
            self.arista.set_target(target)
                        
            #print ('source:', source)
            #print ('target:', target)

        if tag == 'data':
            self.key = attributes['key']

    def endElement(self, tag):
        if self.CurrentData == 'data':
            if int(self.nodoID) > -1:
                if self.key == 'd4':
                    #print (self.content)
                    listaNodos[int(self.nodoID)].set_id_osm(self.content)
                if self.key == 'd5':
                    #print (self.content)
                    listaNodos[int(self.nodoID)].set_lon(self.content)
                if self.key == 'd6':
                    #print (self.content)
                    listaNodos[int(self.nodoID)].set_lat(self.content)
                if self.key == 'd17':
                    self.arista.set_longitud(self.content)
                    if self.aristaID == "0":
                        adyacentes(listaNodos, self.arista)
                        self.arista = None
        self.CurrentData = ""

    def characters(self, content):
        if self.CurrentData == "data":
            if self.key == 'd4' or self.key == 'd5' or self.key == 'd6' or self.key == 'd17':
                self.content = content
                


def printearListaNodos(listaNodos):
    for n in listaNodos:
        print(n.get_info())
    
def adyacentes(listaNodos, arista):
    listaNodos[int(arista.source)].add_arista(arista)

def tratamientoGrafo():    

    parser = xml.sax.make_parser()
    parser.setFeature(xml.sax.handler.feature_namespaces, 0)

    Handler = MapHandler()
    parser.setContentHandler( Handler )
    parser.parse('Grafos/CR_Capital.graphXML')

    #printearListaNodos(listaNodos)

    #print(len(listaNodos))
    
    return(listaNodos)


#tratamientoGrafo()




 
