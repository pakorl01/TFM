import itertools
import subprocess
import os

# Valores posibles para cada elemento en la lista
valores = [1, 20, 40, 60, 80]
#valores = [1, 40, 80]

# Tamaño de la lista
tamano_lista = 4

# Generar todas las combinaciones posibles
permutaciones = itertools.product(valores, repeat=tamano_lista)

# Imprimir cada permutación
for perm in permutaciones:
    print(perm)
    my_env = os.environ.copy()
    script_path = my_env.get("SCRIPT_DIR", '') + "\\Utilidades\\MetaScript.py"
    subprocess.run(["python", script_path, str(perm[0]), str(perm[1]), str(perm[2]), str(perm[3]) ])
