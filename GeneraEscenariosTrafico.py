# Toma los ficheros de la carpeta "output_probability_files" como entrada para llamar
# al script randomTrips.py perteneciente a SUMO. Con ello genera los ficheros de defición 
# del tráfico. Estos ficheros creados se guardan en la carpeta "output_traffic_file"

import subprocess
import os

# Número de iteraciones por cada fichero de "output_probability_files"
num_iteraciones = 4
carpeta_ficheros_probabilidades = "output_probability_files"
output_dir = 'output_traffic_file'

os.makedirs(output_dir, exist_ok=True)
my_env = os.environ.copy()
script_path = my_env.get("SUMO_HOME", '') + '\\tools\\randomTrips.py'

for nombre_fichero in os.listdir(carpeta_ficheros_probabilidades):

    nombre_fichero_sin_extensiones = carpeta_ficheros_probabilidades + "\\" + nombre_fichero.split('.')[0]
    for i in range(1, num_iteraciones + 1):
        # Construir la lista de argumentos
        args = [
            'python', script_path,
            '-n', 'fichero_generado.net.xml', 
            '-e', '200',    
            '-r', f'{output_dir}\\{nombre_fichero}_ficheroTrafico_{i}.xml', 
            '--fringe-factor', '10', 
            '--seed', str(i*100),
            '--weights-prefix', nombre_fichero_sin_extensiones
        ]

        # Llamar al script "randomTrips.py" con los argumentos
        resultado = subprocess.run(args, capture_output=True, text=True)

        # Imprimir la salida del programa
        print(f"Generando {nombre_fichero}_ficheroTrafico_{i}.xml: {resultado.stdout}")


    