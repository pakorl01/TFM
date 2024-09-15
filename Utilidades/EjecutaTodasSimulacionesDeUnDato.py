# Script para obtener todas los valores de simulacion de una entrada de datos.
#
# Recibe por parametro el numero de etiquetas vehicle con <route edges="-E0 E1" />
# Recibe por parametro el numero de etiquetas vehicle con <route edges="-E1 E0" />
# Recibe por parametro el numero de etiquetas vehicle con <route edges="-E2 E3" />
# Recibe por parametro el numero de etiquetas vehicle con <route edges="-E3 E2" />
#
# Crea el fichero en 'route-files' con el número de elementos pasados por parámetros
# Modifica el fichero 'fichero_generado.net.xml' (aunque al final lo deja en el estado original)
# y tambien el fichero de la etiqueta 'route-files' del fichero 'Cruce.sumocfg'
# Modifica las combinaciones de tiempo para las fases de semáforo y cambia el orden
# de las fases para obtener los resultados de las simulaciones.
# Llama al simulador Sumo
#
# Guarda los resultados en el fichero 'salidaSimulacionDeDato.txt'

import xml.etree.ElementTree as ET
import itertools
import subprocess
import re
from itertools import permutations
from xml.dom import minidom
import argparse


def salva_fichero_original(fichero_origen, fichero_destino):
    try:
        # Abre el fichero de origen en modo lectura
        with open(fichero_origen, 'rb') as archivo_origen:
            # Lee el contenido del fichero de origen
            contenido = archivo_origen.read()

        # Abre el fichero de destino en modo escritura
        with open(fichero_destino, 'wb') as archivo_destino:
            # Escribe el contenido en el fichero de destino
            archivo_destino.write(contenido)

        print(f"Fichero copiado exitosamente de {fichero_origen} a {fichero_destino}")

    except FileNotFoundError:
        print(f"Error: El fichero {fichero_origen} no se encontró.")
    except IOError as e:
        print(f"Error de E/S: {e}")


def agregar_lista_al_fichero(nombre_fichero, lista):
    # Abre el fichero en modo 'a' (append) para agregar datos al final
    with open(nombre_fichero, 'a') as fichero:
        linea = '\n# '.join(map(str, lista))
        fichero.write('\n# ' + linea + '\n\n')


def get_value_of_simulation(cadena):
    # Expresión regular para encontrar todas las ocurrencias de "Step #<número>"
    matches = re.findall(r'Step #(\d+\.\d+)', cadena.decode('utf-8'))

    # Verificar si se encontraron coincidencias
    if matches:
        ultimo_numero = float(matches[-1])
        print(f"El número inmediatamente posterior a la última ocurrencia de 'Step' es: {ultimo_numero}")
        return ultimo_numero
    else:
        print("No se encontraron ocurrencias de 'Step' en la cadena.")
        return -1


def obtieneCombinacionesTiempoSemaforo(phases, tree, total_target=90):
    #Obtiene las combinaciones posibles para la duracion de los semaforos
    fixed_durations = [int(phase.get('duration')) for phase in phases if int(phase.get('duration')) == 3]
    variable_phases = [int(phase.get('duration')) for phase in phases if int(phase.get('duration')) != 3]

    total_fixed = sum(fixed_durations)
    remaining_target = total_target - total_fixed

    num_variables = len(variable_phases)
    min_duration = 5

    possible_durations = list(range(min_duration, remaining_target, 5))

    return_list = []
    return_list.append(possible_durations)
    return_list.append(remaining_target)
    return_list.append(num_variables)
    return_list.append(min_duration)
    return return_list


def execute_simulation(combination,num_vehiculos):
    # Ejecuta la simulacion y guarda los datos en una lista,
    p = subprocess.Popen("sumo.exe -c .\\Cruce.sumocfg", shell=True,
             stdout=subprocess.PIPE,
             stderr=subprocess.PIPE
            )
    # Salida y errores
    out, err = p.communicate(timeout=10)

    valueOfSimulation = get_value_of_simulation(out)
    print(f"Tiempos del semaforo {combination} -- Tiempo de la simulación: {valueOfSimulation}")
    datos_simulacion = list(combination)
    datos_simulacion.append(valueOfSimulation)

    return num_vehiculos + datos_simulacion



def get_new_durations(possible_durations, remaining_target, num_variables, min_duration, num_vehiculos):

    #Genera diferentes versiones del fichero *.net.xml con las distintas combinaciones de los tiempos de semaforo
    lista_todas_simulaciones = []
    for combination in itertools.product(possible_durations, repeat=num_variables):
        if (sum(combination) >= remaining_target) and (sum(combination) < remaining_target + min_duration ):
            var_index = 0
            for phase in phases:
                if int(phase.get('duration')) != 3:
                    phase.set('duration', str(combination[var_index]))
                    var_index += 1
            # Guardar los cambios en el archivo XML
            tree.write( "fichero_generado.intermedio.xml", encoding='utf-8', xml_declaration=True)

            # Leer los datos del fichero
            with open('fichero_generado.intermedio.xml', 'r') as file:
                lines = file.readlines()

            # Identificar los índices donde comienza y termina la sección <tlLogic>
            start_idx = next(i for i, line in enumerate(lines) if '<tlLogic' in line)
            end_idx = next(i for i, line in enumerate(lines) if '</tlLogic>' in line)

            # Extraer las líneas dentro de <tlLogic>
            tl_logic_lines = lines[start_idx+1:end_idx]

            # Filtrar solo las líneas <phase>
            phase_lines = [line.strip() for line in tl_logic_lines if '<phase' in line]

            # Crear pares de líneas asociando cada línea con duración distinta de 3 con la siguiente línea con duración 3
            pairs = [(phase_lines[i], phase_lines[i+1]) for i in range(0, len(phase_lines), 2)]

            # Generar todas las permutaciones de los pares
            all_permutations = list(permutations(pairs))

            # Leer la cabecera y la parte final del fichero original
            header = lines[:start_idx+1]
            footer = lines[end_idx:]

            # Escribir cada combinación en un fichero de salida separado
            for idx, perm in enumerate(all_permutations):
                with open(f'fichero_generado.net.xml', 'w') as output_file:
                    # Escribir la cabecera
                    output_file.writelines(header)

                    # Escribir la combinación de pares
                    for pair in perm:
                        output_file.write(pair[0] + "\n")
                        output_file.write(pair[1] + "\n")

                    # Escribir el pie de página
                    output_file.writelines(footer)
                    output_file.close()

                    lista_todas_simulaciones.append (execute_simulation(combination, num_vehiculos))

    # Guarda los datos de las simulaciones en un fichero
    print(f"Se agrega la lista al fichero {nombre_fichero_final_datos}")
    print(lista_todas_simulaciones)
    agregar_lista_al_fichero(nombre_fichero_final_datos, lista_todas_simulaciones)


def read_value_route_files(fichero_xml):
    # Leer y parsear el fichero XML
    tree = ET.parse(fichero_xml)
    root = tree.getroot()
    # Encontrar el nodo route-files y cambiar su valor
    for elem in root.iter('route-files'):
        return elem.get('value')


def change_value_route_files(fichero_xml, nuevo_valor):
    # Leer y parsear el fichero XML
    tree = ET.parse(fichero_xml)
    root = tree.getroot()
    # Encontrar el nodo route-files y cambiar su valor
    for elem in root.iter('route-files'):
        elem.set('value', nuevo_valor)
    # Guardar los cambios en el fichero XML
    tree.write(fichero_xml, encoding='UTF-8', xml_declaration=True)


# Contar las apariciones del primer elemento del atributo edges (vehiculo que empieza su ruta en ese carril)
def count_vehicles(file):
    #contadores = {}
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

    #Resetea la lista de contadores para el siguiente fichero
    for edge in contadores:
        contadores[edge] = 0

    return  num_vehiculos

def crear_fichero_xml(nombre_fichero, num_e0_e1, num_e1_e0, num_e2_e3, num_e3_e2):
    # Crear el elemento raíz
    rutas = ET.Element("routes", {
        "xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance",
        "xsi:noNamespaceSchemaLocation": "http://sumo.dlr.de/xsd/routes_file.xsd"
    })

    # Función auxiliar para añadir vehículos
    def añadir_vehiculos(rutas, num_vehiculos, edges, id_inicio):
        for i in range(num_vehiculos):
            vehiculo = ET.SubElement(rutas, "vehicle", {"id": str(id_inicio + i), "depart": "0.00"})
            ET.SubElement(vehiculo, "route", {"edges": edges})

    # Añadir los vehículos según los números dados
    id_contador = 0
    añadir_vehiculos(rutas, num_e0_e1, "-E0 E1", id_contador)
    id_contador += num_e0_e1
    añadir_vehiculos(rutas, num_e1_e0, "-E1 E0", id_contador)
    id_contador += num_e1_e0
    añadir_vehiculos(rutas, num_e2_e3, "-E2 E3", id_contador)
    id_contador += num_e2_e3
    añadir_vehiculos(rutas, num_e3_e2, "-E3 E2", id_contador)

    # Convertir el árbol a una cadena XML y aplicar formateo
    xml_str = ET.tostring(rutas, encoding='unicode')
    xml_str_pretty = minidom.parseString(xml_str).toprettyxml(indent="    ")

    # Escribir el XML a un fichero, manteniendo los saltos de línea
    with open(nombre_fichero, "w", encoding='utf-8') as f:
        f.write(xml_str_pretty)




#########################################
# MAIN
#########################################

fichero_proyecto = 'Cruce.sumocfg'
fichero_red_calles = 'fichero_generado.net.xml'
fichero_red_calles_copia = fichero_red_calles + '.ORIG'
contadores = {}


parser = argparse.ArgumentParser(description="Genera un archivo XML con rutas de vehículos.")

parser.add_argument("num_e0_e1", type=int, help="Número de vehículos con ruta -E0 E1.")
parser.add_argument("num_e1_e0", type=int, help="Número de vehículos con ruta -E1 E0.")
parser.add_argument("num_e2_e3", type=int, help="Número de vehículos con ruta -E2 E3.")
parser.add_argument("num_e3_e2", type=int, help="Número de vehículos con ruta -E3 E2.")

args = parser.parse_args()

nombre_nuevo_fichero = "ruta_"+ str(args.num_e0_e1) + "_" + str(args.num_e1_e0) + "_" + str(args.num_e2_e3) + "_" + str(args.num_e3_e2) + ".xml"
# Llamar a la función para crear el fichero XML
crear_fichero_xml(nombre_nuevo_fichero, args.num_e0_e1, args.num_e1_e0, args.num_e2_e3, args.num_e3_e2)

change_value_route_files(fichero_proyecto, nombre_nuevo_fichero)


# Crea o vacia el fichero final con los datos de las simulaciones
nombre_fichero_final_datos = 'salidaSimulacion_' + str(args.num_e0_e1) + '_' + str(args.num_e1_e0) + '_' + str(args.num_e2_e3) + '_' + str(args.num_e3_e2) + '.txt'

# Cargar el archivo XML
tree = ET.parse(fichero_red_calles)
root = tree.getroot()

# Encontrar todas las ocurrencias de la etiqueta tlLogic
tlLogics = root.findall(".//tlLogic")

for tlLogic in tlLogics:
    phases = tlLogic.findall('phase')

    # Obtiene las posibles combinaciones de duraciones de los semaforos
    return_list = []
    return_list = obtieneCombinacionesTiempoSemaforo(phases, tree, total_target=90)
    possible_durations = return_list[0]
    remaining_target = return_list[1]
    num_variables = return_list[2]
    min_duration = return_list[3]

print(phases)
route_file = read_value_route_files(fichero_proyecto)
num_vehiculos = count_vehicles(route_file)
print(f"Fichero {route_file} : Num vehiculos: {num_vehiculos}")
get_new_durations(possible_durations, remaining_target, num_variables, min_duration, num_vehiculos )

