# Cuenta los vehiculos que inician la ruta en cada carril. Ver ayuda para 
# las opciones de elección de fichero a comprobar

import xml.etree.ElementTree as ET
import glob
import sys


# Contar las apariciones del primer elemento del atributo edges (vehiculo que empieza su ruta en ese carril)
def count_vehicles(file):
    contadores = {}
    contadores["-E0"] = 0
    contadores["-E1"] = 0
    contadores["-E2"] = 0
    contadores["-E3"] = 0

    tree = ET.parse(file)
    root = tree.getroot()

    for vehicle in root.findall('vehicle'):
        route = vehicle.find('route')
        if route is not None:
            edges = route.get('edges')
            if edges:
                first_edge = edges.split()[0]
                if first_edge in contadores:
                    contadores[first_edge] += 1
                else:
                    contadores[first_edge] = 1

    # Obtener los resultados ordenados alfabéticamente
    resultados_ordenados = sorted(contadores.items())
    #Obtiene una lista con los numeros de vehiculos por "edge"
    num_vehiculos = [valor for _, valor in resultados_ordenados]

    return  num_vehiculos
    



###############################
# MAIN
###############################

if len(sys.argv) > 1:
    if ( sys.argv[1] == "-h"):
        print("\t-f nombre_carpeta    : cuenta los vehiculos por carril en la ruta pasada") 
        print("\tnombre_fichero       : cuenta los vehiculos del fichero")
        print("\tsin parametro        : Cuenta los vehiculos del fichero 'ficheroTrafico.xml'")
        exit()
    if ( len(sys.argv) == 2):
        print(f"\nBuscando en el fichero {sys.argv[1]}")
        file = sys.argv[1]
        num_vehiculos = count_vehicles(file)
        print("\n  Número de vehículos por carril : ")
        print("\t", num_vehiculos)
    elif (len(sys.argv) == 3 and (sys.argv[1] == "-f")):
        print(f"\nBuscando en la carpeta {sys.argv[2]}")
        # Usar glob para encontrar todos los archivos que coincidan con el patrón
        file_pattern = sys.argv[2]+'\edgedata_variacion_*'
        files = glob.glob(file_pattern)
        for file in files:
            num_vehiculos = count_vehicles(file)
            print(f"{num_vehiculos} == {file}")
            print(f"{count_vehicles(file)} ===> {file}")
    
else:
    print("\nBuscando en la opcion por defecto (ficheroTrafico.xml)")
    file = "ficheroTrafico.xml"
    num_vehiculos = count_vehicles(file)
    print("\n  Número de vehículos por carril : ")
    print("\t", num_vehiculos)