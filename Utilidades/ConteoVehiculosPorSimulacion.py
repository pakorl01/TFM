# Programa que cuenta el número de ocurrencias de todos los valores en el fichero 
# datosFiltrados.SIN_NORMALIZAR.txt en la columna pasada por parámetro.
# Genera una gráfica con los resultados.

from collections import defaultdict
import matplotlib.pyplot as plt
import sys

# Función para leer el archivo y contar los valores de la primera columna
def contar_valores_primera_columna(filename, columna):
    contador = defaultdict(int)
    
    # Leer el archivo
    with open(filename, 'r') as file:
        print(type(file))
        for line in file:
            # Convertir la línea en una lista
            lista = eval(line.strip())
            # Incrementar el contador para el valor de la primera columna
            contador[lista[columna]] += 1
  
    contador_ordenado = dict(sorted(contador.items()))
    print(contador)
    print(contador_ordenado)
    return contador

# Función para dibujar la gráfica
def dibujar_grafica(conteo, carril):
    valores = list(conteo.keys())
    cantidades = list(conteo.values())
    
    plt.bar(valores, cantidades)
    plt.xlabel('Num de vehículos en el carril '+ carril)
    plt.ylabel('Número de simulaciones')
    plt.show()  





###############################
# MAIN
###############################

if len(sys.argv) == 2:
    # Archivo de entrada
    archivo = 'datosFiltrados.SIN_NORMALIZAR.txt'
    carril = sys.argv[1]

    # Obtener el conteo de valores en la primera columna
    conteo = contar_valores_primera_columna(archivo, int(carril)-1)

    # Imprimir el resultado
    for valor, cantidad in conteo.items():
        print(f"Valor: {valor}, Número de listas: {cantidad}")

    # Dibujar la gráfica
    dibujar_grafica(conteo, carril)
else:
    print(f"Uso : {sys.argv[0]} num_carril  ")
