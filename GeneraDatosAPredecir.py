# Lee los parametros de entrada (número de vehículos por carril) y genera el
# fichero "datosAPredecir.txt" con los argumentos de  entrada multiplicados 
# por una serie de valores

import sys

def procesar_entrada_y_generar_fichero(entrada, multiplicadores, nombre_fichero):
    # Convertir la entrada en una lista de números
    numeros = list(map(int, entrada.split()))
    
    # Abrir el fichero para escribir los resultados
    with open(nombre_fichero, 'w') as fichero:
        for valor in multiplicadores:
            lista = []
            resultadoValido = True
            for numero in numeros:
                resultado = numero * valor
                lista.append(resultado)

            if ( resultadoValido):
                # Escribir el resultado en el fichero
                linea = ""
                for valoresLista in lista:
                    linea += str(valoresLista) + " "
                linea += "\n"
                fichero.write(f'{linea}')


#############################
# MAIN
#############################

# Entrada proporcionada
argumentos = sys.argv[1:]
entrada = ' '.join(argumentos)

# Definir la tabla de multiplicadores
multiplicadores = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# Nombre del fichero de salida
nombre_fichero = 'datosAPredecir.txt'

# Llamar a la función para procesar la entrada y generar el fichero
procesar_entrada_y_generar_fichero(entrada, multiplicadores, nombre_fichero)

print(f'El fichero {nombre_fichero} ha sido generado con los resultados.')
