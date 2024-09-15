# Script que modifica los ficheros de la carpeta "output_traffic_file" cambiando el valor
# del campo depart a 0. Guarda los ficheros modificados en "output_traffic_file_depart0" 

import xml.etree.ElementTree as ET
import os

# Función para leer, modificar y guardar el archivo XML
def modificar_archivo_xml(ruta_archivo, nombre_archivo):
    # Parsear el archivo XML
    tree = ET.parse(ruta_archivo + '\\'+ nombre_archivo)
    root = tree.getroot()

    # Iterar sobre los vehículos y cambiar el valor de 'depart' a '0'
    for vehicle in root.findall('vehicle'):
        vehicle.set('depart', '0.00')

    # Guardar el archivo XML modificado
    tree.write(carpeta_final+'\\'+ nombre_archivo)



########################################
# MAIN
########################################

carpeta_inicial = 'output_traffic_file'
carpeta_final = 'output_traffic_file_depart0'

# Crear la carpeta para los ficheros finales
try:
    os.makedirs(carpeta_final)
    print(f"Carpeta '{carpeta_final}' creada exitosamente.")
except FileExistsError:
    print(f"La carpeta '{carpeta_final}' ya existe.")

for nombre_fichero in os.listdir(carpeta_inicial):
     modificar_archivo_xml(carpeta_inicial,nombre_fichero)


