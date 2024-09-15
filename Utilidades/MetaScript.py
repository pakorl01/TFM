# Genera peticiones segun la entrada por argumentos (script GeneraDatosAPredecir.py) 
# Consulta a la red neuronal por las peticiones generadas (script EjecutaIA_Con_Distancia_Euclidea.py).
# Ejecuta las simulaciones de la salida del paso anterior (script EjecutaTodasSimulacionesDeUnDato.py)
# Llama a ExtraeResultados.py para presentar los resultados (genera el fichero "resultado_x_x_x_x.txt")
# Se muestran los resultados en el fichero "resultado_x_x_x_x.txt"

import subprocess
import sys
import shutil
import os

# Busca la línea con meno tiempo de ejecución en la seccion que empieza por "#" del fichero.
def leer_y_encontrar_minimo(archivo):
    # Leer los datos del archivo y almacenarlos en una lista
    with open(archivo, 'r') as f:
        datos = []
        for linea in f:
            if linea.strip().startswith('#'):
                # Limpiar la línea, eliminar corchetes y verificar que no esté vacía
                linea = linea.strip('#').strip().strip('[]')
                if linea:  # Solo procesar si la línea no está vacía
                    # Convertir la línea en una lista de números flotantes
                    try:
                        fila = list(map(float, linea.split(',')))
                        datos.append(fila)
                    except ValueError as e:
                        print(f"Error al procesar la línea: {linea}, error: {e}")

    # Asegurarse de que hay datos para procesar
    if datos:
        # Encontrar la línea con el menor valor en la última columna
        linea_menor_valor = min(datos, key=lambda x: x[-1])

        # Imprimir la línea con el menor valor en la última columna
        return "Línea con el menor valor en la última columna:" + str(linea_menor_valor)
    else:
        return "No se encontraron datos válidos en el archivo."


def agregar_lista_al_fichero(nombre_fichero, linea):
    with open(nombre_fichero, 'w') as fichero:
        fichero.write('\n\n' + linea )



#########################################
# MAIN
#########################################


if (len(sys.argv)==1):
    print("Es necesario argumentos")
    exit()
argumentos = sys.argv[1:]

print(f"{argumentos[0]} {argumentos[1]} {argumentos[2]} {argumentos[3]}")
fichero_salida_simulacion = 'salidaSimulacion_' + str(argumentos[0]) + '_' + str(argumentos[1]) + '_' + str(argumentos[2]) + '_' + str(argumentos[3]) + '.txt'
fichero_resultados = 'resultado_'+ str(argumentos[0]) + '_' + str(argumentos[1]) + '_' + str(argumentos[2]) + '_' + str(argumentos[3]) + '.txt'

my_env = os.environ.copy()
path_genera_datos = my_env.get("SCRIPT_DIR", '') + "\\GeneraDatosAPredecir.py"
path_ejecutaIA = my_env.get("SCRIPT_DIR", '') + "\\EjecutaIA_Con_Distancia_Euclidea.py"
path_ejecutaTodasSimulaciones = my_env.get("SCRIPT_DIR", '') + "\\Utilidades\\EjecutaTodasSimulacionesDeUnDato.py"
path_extraeResultados = my_env.get("SCRIPT_DIR", '') + "\\Utilidades\\ExtraeResultados.py"
 

subprocess.run(["python", path_genera_datos, argumentos[0], argumentos[1], argumentos[2], argumentos[3] ])

subprocess.run(["python", path_ejecutaIA ])
shutil.copy('SalidaEjecutaIA.txt', fichero_salida_simulacion)

subprocess.run(["python", path_ejecutaTodasSimulaciones, argumentos[0], argumentos[1], argumentos[2], argumentos[3] ])

# Llama a la función pasando el nombre del fichero
linea_menor = leer_y_encontrar_minimo(fichero_salida_simulacion)
agregar_lista_al_fichero(fichero_resultados, linea_menor)

subprocess.run(["python", path_extraeResultados, argumentos[0], argumentos[1], argumentos[2], argumentos[3] ])


