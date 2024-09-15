# Muestra la cantidad de datos en cada columna por rangos de 10 en 10
# Tiene como entrada la columna que se quiere consultar (la primera columna es 0)


import numpy as np
import sys

def contar_valores_por_rango(data, columna):
    # Inicializamos los contadores para cada rango
    rangos = {
         "0-9": 0,
        "10-19": 0,
        "20-29": 0,
        "30-39": 0,
        "40-49": 0,
        "50-59": 0,
        "60-69": 0, 
        "70-79": 0,
        "80-89": 0,
        "90-99": 0,
        "100-109": 0,             
        "110-119": 0,
        "mayor_que_120": 0
    }
    
    # Iteramos sobre cada fila y contamos los valores según el rango
    for fila in data:
        valor = fila[columna]
        if 0 <= valor <= 9:
            rangos["0-9"] += 1
        elif 10 <= valor <= 19:
            rangos["10-19"] += 1
        elif 20 <= valor <= 29:
            rangos["20-29"] += 1
        elif 30 <= valor <= 39:
            rangos["30-39"] += 1
        elif 40 <= valor <= 49:
            rangos["40-49"] += 1
        elif 50 <= valor <= 59:
            rangos["50-59"] += 1
        elif 60 <= valor <= 69:
            rangos["60-69"] += 1
        elif 70 <= valor <= 79:
            rangos["70-79"] += 1
        elif 80 <= valor <= 89:
            rangos["80-89"] += 1
        elif 90 <= valor <= 99:
            rangos["90-99"] += 1
        elif 100 <= valor <= 109:
            rangos["100-109"] += 1
        elif 110 <= valor <= 119:
            rangos["110-119"] += 1
            rangos["mayor_que_120"] += 1
    
    return rangos



#########################################
# MAIN
#########################################


if (len(sys.argv)==1):
    print("Es necesario argumento con el número de carril (0, 1, 2 ...)")
    exit()
# Leemos el archivo
with open('datosFiltrados.SIN_NORMALIZAR.txt', 'r') as file:
    lines = file.readlines()

# Convertimos las líneas leídas en una lista de listas de enteros
data = [list(map(int, line.strip('[]\n').split(', '))) for line in lines]

argumentos = sys.argv[1:]
print(type(int(argumentos[0])))
# Contamos los valores  de la columna pasado por argumento, en lo rango 0-9, 10-19, etc
resultados = contar_valores_por_rango(data, int(argumentos[0]))

# Imprimimos los resultados
for rango, cuenta in resultados.items():
    print(f"Valores en el rango {rango}: {cuenta}")
