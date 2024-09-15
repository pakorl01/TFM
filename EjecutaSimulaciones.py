# Ejecuta las simulaciones con SUMO. Toma los ficheros de configuracion desde la carpeta
# "output_traffic_file_depart0" (ficheros de tráfico) y el fichero "fichero_generado.net.xml",
# (fichero del trazado de calles) al que va cambiando los valores de duracion del semaforo.
# Se usa el mismo fichero de "output_traffic_file_depart0" tantas veces como 
# variaciones se hace del fichero "fichero_generado.net.xml"

import xml.etree.ElementTree as ET
import itertools
import subprocess
import re
import glob
from itertools import permutations

def crear_o_vaciar_fichero(nombre_fichero):
    # Abre el fichero en modo 'w' (write) para vaciar su contenido o crearlo si no existe
    with open(nombre_fichero, 'w') as fichero:
        pass  # No hace nada, solo abre y cierra el fichero


def agregar_lista_al_fichero(nombre_fichero, lista):
    # Abre el fichero en modo 'a' (append) para agregar datos al final
    with open(nombre_fichero, 'a') as fichero:
        linea = ', '.join(map(str, lista))
        fichero.write(linea + '\n')


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
    #Obtiene las combinaciones posibles para la duracion de los semaforos entre 5 y 90 seg, en saltos de 5 seg
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
    # Ejecuta la simulacion y guarda los datos en una lista
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
    agregar_lista_al_fichero(nombre_fichero_final_datos, lista_todas_simulaciones)
                       


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



########################################
# MAIN
########################################

fichero_proyecto = 'Cruce.sumocfg'
fichero_red_calles = 'fichero_generado.net.xml'
nombre_fichero_final_datos = 'fichero_datos_simulacion.txt'

# Crea o vacia el fichero final con los datos de las simulaciones
crear_o_vaciar_fichero(nombre_fichero_final_datos)

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
    
contadores = {}
file_pattern = 'output_traffic_file_depart0\\edgedata_variacion_*'
files = glob.glob(file_pattern)
for file in files:
    print(file)
    #Cambia el valor de route-files en *.sumocfg
    change_value_route_files(fichero_proyecto, file)
    #Cuenta el numero de vehiculos del fichero
    num_vehiculos = count_vehicles(file)
    
    get_new_durations(possible_durations, remaining_target, num_variables, min_duration, num_vehiculos )