# Lee cada linea del fichero "fichero_datos_simulacion.txt" y selecciona la tupla que tenga un menor tiempo de ejecucion. 
# Finalmente escribe esas tuplas en dos ficheros uno con los valores normalizadas ("datosFiltrados.txt")
# y otro con los valores sin normalizar ("datosFiltrados.SIN_NORMALIZAR.txt") 

def leer_datos(fichero_entrada):
    with open(fichero_entrada, 'r') as f:
        lineas = f.readlines()
    datos = [eval(line.strip()) for line in lineas]
    return datos

def encontrar_lista_minima(datos):
    retLista = []
    for sublista in datos:
        lista_minimo = min(sublista, key=lambda x: x[-1])
        lista_minimo.pop() #Elimina el último valor de la lista
        retLista.append(lista_minimo) 
    return retLista

def escribir_datos_sin_normalizar(fichero_salida, lista):
    with open(fichero_salida, 'w') as f:
        for elemento in lista:
            # Escribe le fichero con los valores sin normalizar (para depuracion)
            f.write(str(elemento) + '\n')

def escribir_datos(fichero_salida, lista):
    with open(fichero_salida, 'w') as f:
        for elemento in lista:
            #Normaliza los datos dividiendo por 200 que es el máximo valor de vehiculos en las simulaciones
            elem_normalizado = [x/200 for x in elemento]
            f.write(str(elem_normalizado) + '\n')



########################################
# MAIN
########################################

fichero_entrada = 'fichero_datos_simulacion.txt'
fichero_salida = 'datosFiltrados.txt'
fichero_salida_sin_normalizar = 'datosFiltrados.SIN_NORMALIZAR.txt'
    
datos = leer_datos(fichero_entrada)
lista_minimos = encontrar_lista_minima(datos)
escribir_datos_sin_normalizar(fichero_salida_sin_normalizar, lista_minimos)
escribir_datos(fichero_salida, lista_minimos)
