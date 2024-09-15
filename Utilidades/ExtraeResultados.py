# Genera el fichero "resultado_x_x_x_x.py" con contenido recopilado del fichero "salidaSimulacion_x_x_x_x.txt"
# Agrega también información llamando a "SimulaDatoSimple.py" que llama al simulador SUMO

import ast
import re
import sys
import subprocess
import os

def son_listas_iguales(lista1, lista2):
    # Convertir ambas listas a floats para comparar
    lista1_float = [float(x) for x in lista1]
    lista2_float = [float(x) for x in lista2]

    return lista1_float == lista2_float


# Extrae los datos de la línea del fichero salidaSimulacion_x_x_x_x.txt cuya lista de tiempos coincide con los 
# pasados por argumentos
def buscar_listas_por_argumentos(archivo, tiempo1, tiempo2, tiempo3, tiempo4):
    try:
        with open(archivo, 'r', encoding='latin-1') as f:
            # Iterar sobre las líneas del archivo
            for linea in f:
                # Limpiar la línea de espacios extra
                linea = linea.strip()
                # Dividir la línea en partes usando '==>' como delimitador
                partes = linea.split('==>')

                # Extraer la primera lista (la que aparece antes de '==>')
                primera_lista_str = partes[0].split('\t')[1]  # Extraemos la segunda columna
                primera_lista = ast.literal_eval(primera_lista_str)  # Convertimos la lista de string a lista real

                # Extraer la segunda lista (después de '==>')
                segunda_lista_str = partes[1].split('\t')[0]  # Extraemos la primera lista después del '==>'
                
                # Preprocesar la segunda lista para agregar comas si es necesario
                segunda_lista_str = re.sub(r'(\d+\.\d+)\s+(\d+\.\d+)', r'\1, \2', segunda_lista_str)
                segunda_lista = ast.literal_eval(segunda_lista_str)  # Convertimos la lista de string a lista real

                # Convertir los argumentos a string para comparar con los elementos de la primera lista
                argumentos = [str(tiempo1), str(tiempo2), str(tiempo3), str(tiempo4)]

                # Verificar si la primera lista coincide con los argumentos
                if son_listas_iguales(primera_lista, argumentos):
                    return primera_lista, segunda_lista

        print("No se encontró ninguna fila con la lista proporcionada.")
        return None, None

    except FileNotFoundError:
        print(f"El archivo '{archivo}' no fue encontrado.")
        return None, None
    except Exception as e:
        print(f"Error: {e}")
        return None, None


#Extrae los datos de primera línea del fichero salidaSimulacion_x_x_x_x.txt
def extraer_listas(archivo):
    try:
        # Usar 'latin-1' para manejar caracteres problemáticos
        with open(archivo, 'r', encoding='latin-1') as f:
            # Leer la primera línea
            primera_linea = f.readline().strip()

            # Dividir la línea en partes
            partes = primera_linea.split('==>')

            # Asegurarnos de que el formato de la línea es correcto
            if len(partes) < 2:
                raise ValueError("Formato inesperado en el archivo.")

            # Extraer la primera lista (la que aparece antes del '==>')
            primera_lista = partes[0].split('\t')[1]  # Extrae la segunda columna antes de '==>'

            # Extraer la segunda lista (la que aparece después del '==>')
            segunda_lista = partes[1].split('\t')[0]  # Extrae la parte antes del siguiente conjunto de datos

            # Preprocesar las listas para agregar comas entre los números si es necesario
            segunda_lista = re.sub(r'(\d+\.\d+)\s+(\d+\.\d+)', r'\1, \2', segunda_lista)

            # Convertir las listas de string a listas reales usando ast.literal_eval
            primera_lista = ast.literal_eval(primera_lista)
            segunda_lista = ast.literal_eval(segunda_lista)

            return primera_lista, segunda_lista

    except FileNotFoundError:
        print(f"El archivo '{archivo}' no fue encontrado.")
        return None, None
    except ValueError as ve:
        print(f"Error de valor: {ve}")
        return None, None
    except Exception as e:
        print(f"Error: {e}")
        return None, None


def encontrar_menor_tiempo(cadena):
    # Buscar todas las ocurrencias de "Tiempo de la simulación:" seguido de un número
    tiempos = re.findall(r'Tiempo de la simulación:\s*([\d\.]+)', cadena)
    
    if not tiempos:
        return None
    
    # Convertir los tiempos encontrados a flotantes y encontrar el menor
    tiempos_float = [float(tiempo) for tiempo in tiempos]
    menor_tiempo = min(tiempos_float)
    
    return menor_tiempo


def redondear_lista(lista):
    return [round(valor) for valor in lista]

def agregar_lista_al_fichero(nombre_fichero, linea):
    with open(nombre_fichero, 'a') as fichero:
        fichero.write('\n\n' + linea )



#############################
# MAIN
#############################

if (len(sys.argv)==1):
    print("Es necesario argumentos")
    exit()
argumentos = sys.argv[1:]

archivo = 'salidaSimulacion_'+ str(argumentos[0]) + '_' + str(argumentos[1]) + '_' + str(argumentos[2]) + '_' + str(argumentos[3]) + '.txt'

#Seccion que obtiene los datos de la solucion propuesta a partir del fichero salidaSimulacion_x_x_x_x.txt (usando distancia euclídea)
lista1_solucion_propuesta, lista2_solucion_propuesta = extraer_listas(archivo)
lista2_solucion_propuesta_redondeada = redondear_lista(lista2_solucion_propuesta)
if lista1_solucion_propuesta and lista2_solucion_propuesta:
    print(f"Primera lista: {lista1_solucion_propuesta}")
    print(f"Segunda lista: {lista2_solucion_propuesta} == {lista2_solucion_propuesta_redondeada}")
else:
    print("No se pudieron extraer las listas.")

my_env = os.environ.copy()
path_simulaDatosSimple = my_env.get("SCRIPT_DIR", '') + "\\Utilidades\\SimulaDatoSimple.py"
resultado = subprocess.run(["python", path_simulaDatosSimple,
                             str(argumentos[0]), str(argumentos[1]), str(argumentos[2]), str(argumentos[3]), str(lista2_solucion_propuesta_redondeada[0]), str(lista2_solucion_propuesta_redondeada[1])],
                            capture_output=True,
                            text=True,
                            check=True )

menor_tiempo = encontrar_menor_tiempo(resultado.stdout)
cadena_solucion_propuesta = "Solución propuesta \t" + str(lista1_solucion_propuesta) + "\t ==>\t" + str(lista2_solucion_propuesta) + " == " + str(lista2_solucion_propuesta_redondeada)+ "\t ==>\t" + str(menor_tiempo) + "  (solucion con " + argumentos[0] + ", " + argumentos[1] + ", "+ argumentos[2] + ", " + argumentos[3] + " ) "


#Seccion que obtiene los datos de la solucion propuesta sin usar la distancia euclidea, a partir del fichero salidaSimulacion_x_x_x_x.txt
lista1_solucion_sin_distanciaE, lista2_solucion_sin_distanciaE = buscar_listas_por_argumentos(archivo, argumentos[0], argumentos[1], argumentos[2], argumentos[3])
lista2_solucion_sin_distanciaE_redondeada = redondear_lista(lista2_solucion_sin_distanciaE)

if lista1_solucion_sin_distanciaE and lista2_solucion_sin_distanciaE:
    print(f"Primera lista encontrada: {lista1_solucion_sin_distanciaE}")
    print(f"Segunda lista encontrada: {lista2_solucion_sin_distanciaE} == {lista2_solucion_sin_distanciaE_redondeada}")

resultado = subprocess.run(["python", path_simulaDatosSimple, 
                             str(argumentos[0]), str(argumentos[1]), str(argumentos[2]), str(argumentos[3]), str(lista2_solucion_sin_distanciaE_redondeada[0]), str(lista2_solucion_sin_distanciaE_redondeada[1])],
                            capture_output=True,
                            text=True,
                            check=True )

menor_tiempo = encontrar_menor_tiempo(resultado.stdout)
cadena_solucion_propuesta_sin_distanciaE = "Solución propuesta sin distancia euclidea\t" + str(lista1_solucion_sin_distanciaE) + "\t ==>\t" + str(lista2_solucion_sin_distanciaE) + " == " + str(lista2_solucion_sin_distanciaE_redondeada)+ "\t ==>\t" + str(menor_tiempo) + "  (solucion con " + argumentos[0] + ", " + argumentos[1] + ", "+ argumentos[2] + ", " + argumentos[3] + " ) "


fichero_resultados = 'resultado_'+ str(argumentos[0]) + '_' + str(argumentos[1]) + '_' + str(argumentos[2]) + '_' + str(argumentos[3]) + '.txt'
agregar_lista_al_fichero(fichero_resultados, cadena_solucion_propuesta)
agregar_lista_al_fichero(fichero_resultados, cadena_solucion_propuesta_sin_distanciaE)

















