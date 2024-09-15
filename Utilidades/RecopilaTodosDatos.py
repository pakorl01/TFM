# Llama a RecopilaDatos.py para todos los ficheros "resultado_x_x_x_x.txt"
# Con ello se completa el fichero "TablaDeResultados.xlsx"

import os
import subprocess

path_ficheros="."

archivos = [f for f in os.listdir(path_ficheros) if f.startswith("resultado_")]
for archivo in archivos:
    print(archivo)

    my_env = os.environ.copy()
    path_recopila_datos = my_env.get("SCRIPT_DIR", '') + "\\Utilidades\\RecopilaDatos.py"
    subprocess.run(["python", path_recopila_datos, archivo ])


    