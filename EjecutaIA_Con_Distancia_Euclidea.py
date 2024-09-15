# Ejecuta la red neuronal a partir del fichero 'modelo_semaforo.keras' y toma los valores
# a consultar desde el fichero 'datosAPredecir.txt'.
# Utiliza el fichero 'datosFiltrados.SIN_NORMALIZAR.txt' para averiguar los datos de entrenamiento
# más cercanos (distancia euclídea) a los valores pedidos. La predicción del valor que tenga una
# menor distancia será el valor propuesto como solución.
# Devuelve los valores en el fichero "SalidaEjecutaIA.txt"


import numpy as np
import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
from tensorflow.keras.models import Sequential, load_model


# Función para leer el fichero y transformar los datos al formato adecuado
# También normaliza los datos
def transformar_arrays(fichero):
    arrays_2d = []
    lista_original = []
    
    # Leer el fichero
    with open(fichero, 'r') as file:
        for linea in file:
            # Convertir la línea en una lista de enteros
            lista = ([(num) for num in linea.split()])
            lista_original.append(lista)
            # Convertir la línea en una lista de enteros
            array = np.array([float(num)/200 for num in linea.split()])
            # Reorganizar el array en una forma 2D (1 fila, 4 columnas)
            array_2d = array.reshape(1, -1)
            # Añadir el array transformado a la lista
            arrays_2d.append(array_2d)
    
    return lista_original, arrays_2d


# Usar el modelo para predecir
def predecir(modelo_path, nuevos_datos):
    model = load_model(modelo_path)
    predicciones = model.predict(nuevos_datos)
    return predicciones

# Calcula la distancia euclídea entre dos listas
def distancia_euclidiana(lista1, lista2):
    return np.sqrt(np.sum((np.array(lista1) - np.array(lista2)) ** 2))

# Encuentra las 'n' listas en 'data' cuyos primeros cuatro números sean más parecidos a 'target'.
# Retorna las 'n' listas de 'data' cuyos primeros cuatro números sean más parecidos a 'target'
def encontrar_listas_mas_parecidas(data, target, n=5):
    distancias = []
    
    for lista in data:
        distancia = distancia_euclidiana(lista[:4], target)
        distancias.append((distancia, lista))
    
    # Ordenamos las listas por distancia y tomamos las 'n' primeras
    distancias.sort(key=lambda x: x[0])
    listas_mas_parecidas = distancias[:n]
    
    return listas_mas_parecidas



###############################
# MAIN
###############################

if __name__ == '__main__':
    fichero_red_entrenada = 'modelo_semaforo.keras' 
    fichero_datos_a_predecir = 'datosAPredecir.txt'
    fichero_datos_filtrados_sin_normalizar = 'datosFiltrados.SIN_NORMALIZAR.txt'
    lista_total = []

    # Leemos el archivo para calcular las distancias euclideas
    with open(fichero_datos_filtrados_sin_normalizar, 'r') as file:
        lines = file.readlines()
    # Convertimos las líneas leídas en una lista de listas de enteros
    data = [list(map(int, line.strip('[]\n').split(', '))) for line in lines]

    # Transforma el formato de los datos y normaliza.
    lista_original, arrays_transformados = transformar_arrays(fichero_datos_a_predecir)

    model = load_model(fichero_red_entrenada)

    for i in range(0,len(arrays_transformados)):
        predicciones = model.predict(arrays_transformados[i])
        pred_final = [x*200 for x in predicciones]

        target = [int(float(lista_original[i][0])), int(float(lista_original[i][1])), int(float(lista_original[i][2])), int(float(lista_original[i][3]))]
        # Encuentra las listas más parecidas
        listas_mas_parecidas = encontrar_listas_mas_parecidas(data, target, 1)
        lista_total.append((listas_mas_parecidas[0][0], lista_original[i], pred_final[0], listas_mas_parecidas[0][1]))
            
    # Imprime los valores de distancia euclidea, valores buscados, tiempos propuestos, y datos más parecido en los ejemplos
    lista_total.sort(key=lambda x: x[0])
    for valor in lista_total:
        print(valor)
    print(f"\nResultado propuesto: {lista_total[0][2]}")  

    nombre_fichero = 'SalidaEjecutaIA.txt'
    with open(nombre_fichero, 'w') as fichero:
        for lista in lista_total:
            linea = str(lista[0]) + "\t" + str(lista[1]) + "\t ==> " + str(lista[2]) + "\t" + str(lista[3]) + "\n"
        
            fichero.write(linea)
